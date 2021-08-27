'''Data Base Connection'''

from config import MONGODB_URL


client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)  # Set with export in .env
db = client.stuff  # Set client to the Stuff Collection
