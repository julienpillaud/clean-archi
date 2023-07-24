from pymongo import MongoClient
from pymongo.database import Database

from app.config import settings
from app.repository.mongodb.items import ItemSchema

client: MongoClient[ItemSchema] = MongoClient(settings.MONGODB_URI)
database: Database[ItemSchema] = client[settings.MONGODB_DATABASE]
