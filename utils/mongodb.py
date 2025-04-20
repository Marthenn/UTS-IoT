import threading
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoDBHandler:
    def __init__(self, uri, database_name, collection_name):
        self.uri = uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_data(self, query=None):
        try:
            if query is None:
                query = {}
            return list(self.collection.find(query))
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []

    def push_data(self, data):
        try:
            if isinstance(data, dict):
                result = self.collection.insert_one(data)
                print(f"Inserted document with ID: {result.inserted_id}")
            elif isinstance(data, list):
                result = self.collection.insert_many(data)
                print(f"Inserted {len(result.inserted_ids)} documents")
            else:
                print("Data must be a dictionary or a list of dictionaries")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def observe_changes(self, callback):
        def watch_changes():
            try:
                with self.collection.watch() as stream:
                    for change in stream:
                        if change['operationType'] == 'insert':
                            callback(change['fullDocument'])
            except Exception as e:
                print(f"Error observing changes: {e}")
        observer_thread = threading.Thread(target=watch_changes)
        observer_thread.start()
