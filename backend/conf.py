from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# DATABASE_NAME=os.getenv('DATABASE_NAME')
# DATABASE_PORT=os.getenv('DATABASE_PORT')
# DATABASE_HOST=os.getenv('DATABASE_HOST')
# DATABASE_USER=os.getenv('DATABASE_USER')
# DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')