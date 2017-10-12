import os
from dotenv import Dotenv

dotenv = Dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
os.environ.update(dotenv)

# mLab_URI = os.environ.get("mlab_URI")
