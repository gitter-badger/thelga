#!/usr/bin/python
import datetime
import os
import sys
import mimetypes

import subprocess
from io import BytesIO

from helga import Helga, SendMessage
from helga.config import load_config, config
import asyncio
import shelve
import glob
import configparser

from helga.log import init_logging
from helga.telegram.api.commands import SendVoice, SendAudio

ASTERISK_SPOOLPATH = '/tmp/'
ASTERISK_VM_CONTEXT = 'default'
ASTERISK_EXTENSION = '1000'


def get_voicemail():
    spool_path = os.path.join(ASTERISK_SPOOLPATH, 'voicemail', ASTERISK_VM_CONTEXT, ASTERISK_EXTENSION, 'INBOX')
    messages = []
    for mail in glob.glob(os.path.join(spool_path, '*.txt')):
        config = configparser.ConfigParser()
        config.read(mail)
        wav_file = '.'.join((os.path.basename(mail).split('.')[0], 'wav'))
        messages.append({'duration': config.getint('message', 'duration'),
                         'from': config.get('message', 'callerid'),
                         'date': datetime.datetime.fromtimestamp(config.getint('message', 'origtime')),
                         'file': os.path.join(spool_path, wav_file)})
    return messages

def encode_opus(filename):
    args = ['opusenc', '--quiet', filename, '-']
    with open(filename, 'rb') as ih:
        proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = proc.communicate()
        if err or len(out) == 0:
            print('error', err)
        opus_data = BytesIO(out)
        # convice aiohttp to set the correct header
        opus_data.name = 'voicemail.opus'
        return opus_data

if __name__ == '__main__':
    load_config()
    init_logging()
    loop = asyncio.get_event_loop()
    helga = Helga(loop=loop)
    messages = []
    with shelve.open(os.path.join(config.workdir, 'chat.shelve')) as s:
        for mail in get_voicemail():
            cmd = SendMessage(chat_id=s['teddydestodes'], text='New Voicemail from {caller} at {date}'.format(caller=mail['from'],
                                                                                                              date=str(mail['date'])))
            messages.append(helga._execute_command(cmd))
            cmd = SendVoice(chat_id=s['teddydestodes'], voice=encode_opus(mail['file']))
            messages.append(helga._execute_command(cmd, headers={'content-type': 'audio/opus'}))
    loop.run_until_complete(asyncio.gather(*messages))
