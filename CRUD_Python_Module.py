# CRUD_Python_Module.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

class AnimalShelter:
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username: str, password: str):
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'
        try:
            self.client = MongoClient(
                f'mongodb://{username}:{password}@{HOST}:{PORT}/?authSource=admin',
                serverSelectionTimeoutMS=5000
            )
            self.client.server_info()
            self.database = self.client[DB]
            self.collection = self.database[COL]
            print("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            print(f"Connection failed: {e}")
            raise
        except Exception as e:
            print(f"Error during initialization: {e}")
            raise

    def create(self, data: dict):
        if not data or not isinstance(data, dict):
            return False
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    def read(self, query: dict):
        if query is None or not isinstance(query, dict):
            return []
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as e:
            print(f"Query failed: {e}")
            return []

    def update(self, query: dict, update_data: dict):
        if not query or not update_data:
            return 0
        try:
            result = self.collection.update_many(query, {"$set": update_data})
            return result.modified_count
        except Exception as e:
            print(f"Update failed: {e}")
            return 0

    def delete(self, query: dict):
        if not query:
            return 0
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Delete failed: {e}")
            return 0