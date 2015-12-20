from helga.telegram.api.types import Structure
import helga.telegram.api.commands

Structure.finalize()

API_URL = "https://api.telegram.org/bot{token}/{method}"
FILE_URL = "https://api.telegram.org/file/bot{token}/{method}"
