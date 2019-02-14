import pymongo


class Mongodb:
    mongo_client = None
    collection = None

    def __init__(self):
        self.mongo_client= pymongo.MongoClient("mongodb://localhost:27017/")
        database = self.mongo_client["FundData"]
        self.collection = database["HistoryData"]

    def __del__(self):
        self.mongo_client.close()


    def append_one(self, data):
        query = self.collection.find_one({"_id": data['_id']})
        if query is None:
            return self.collection.insert_one(data)
        return query