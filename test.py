import pymongo

# Replace with your actual MongoDB connection string
mongo_uri = "mongouri"

try:
    client = pymongo.MongoClient(mongo_uri)
    db = client.test_database
    collection = db.test_collection
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Error connecting to MongoDB:", e)
