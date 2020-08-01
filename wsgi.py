from server import create_app
from dotenv import load_dotenv

load_dotenv()

application = app = create_app()
