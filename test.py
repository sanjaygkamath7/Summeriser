import pymongo

# Replace with your actual MongoDB connection string
mongo_uri = "mongodb+srv://sanjaykamath6969:wBgUzSlKebdHlsXJ@cluster0.wlatvo2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = pymongo.MongoClient(mongo_uri)
    db = client.test_database
    collection = db.test_collection
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Error connecting to MongoDB:", e)