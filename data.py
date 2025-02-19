import pymongo
import streamlit as st

# Function to connect to MongoDB and return the collection
def get_collection():
    try:
        client = pymongo.MongoClient("mongouri")
        db = client["Login"]
        collection = db["Signup"]
        st.success("MongoDB connected successfully!")
        return collection
    except pymongo.errors.ConnectionError as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to insert data into MongoDB
def insert_data(collection, data):
    try:
        collection.insert_one(data)
        st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to retrieve data from MongoDB
def get_data(collection):
    try:
        data = list(collection.find({}, {"_id": 0}))  # Excluding the MongoDB ID field for cleaner output
        return data
    except Exception as e:
        st.error(f"An error occurred while retrieving data: {e}")
        return []
