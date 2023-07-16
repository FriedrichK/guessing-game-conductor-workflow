import os
from typing import Optional

from dotenv import load_dotenv


BASE_PATH: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")

load_dotenv(os.environ.get(BASE_PATH, ".env"))


CONDUCTOR_API_URL: str = os.environ.get("CONDUCTOR_API_URL")

version_file_path: str = os.path.join(BASE_PATH, "VERSION")
if not os.path.isfile(version_file_path):
    raise AssertionError(f"version file could not be found at {version_file_path}")
with open(version_file_path, "r") as f:
    content: str = f.read()
    if not content.isnumeric():
        raise AssertionError(f"version information is not a number: {content}")
    VERSION: int = int(content)
