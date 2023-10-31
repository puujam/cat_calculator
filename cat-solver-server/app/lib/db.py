from pymongo import MongoClient

def get_db_handle():
    return MongoClient( "127.0.0.1:27017" )