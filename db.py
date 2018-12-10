from pymongo import MongoClient
client = MongoClient('localhost', 27017)

def connect():
    return client.food
