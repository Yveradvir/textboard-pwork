from os import getenv, getcwd, path
from dotenv import load_dotenv

load_dotenv(
    path.join(
        getcwd(), 
        "..", ".env"
    )
)

_genv = lambda key: getenv(key.upper())