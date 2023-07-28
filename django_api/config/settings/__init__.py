import os
from dotenv import load_dotenv

load_dotenv()


if os.environ.get('DEBUG') == 'True':
    from .dev import *
else:
    from .prod import *
