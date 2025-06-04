import os
from dotenv import load_dotenv

# pour récupérer les constantes depuis .env
load_dotenv()
PROJECT_ROOT = os.environ.get('ROOT')

LOCAL_DATA_PATH = os.path.join(PROJECT_ROOT, 'data')
