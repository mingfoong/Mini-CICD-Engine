import os
from dotenv import load_dotenv

load_dotenv()

WORKDIR = os.getenv("WORKDIR", "/tmp/mini-PaaS-jobs")
DEPLOY_HOST = os.getenv("DEPLOY_HOST", "localhost")
PORT_RANGE_START = int(os.getenv("PORT_RANGE_START", "9000"))
PORT_RANGE_END = int(os.getenv("PORT_RANGE_END", "9100"))