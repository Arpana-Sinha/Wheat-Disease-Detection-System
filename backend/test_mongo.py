from db import users_collection, history_collection

def test_connection():
    users_collection.insert_one({
        "username": "atlas_test_user",
        "password": "atlas_test_pass"
    })

    history_collection.insert_one({
        "user_id": "atlas_test_user_id",
        "disease": "Atlas Test Disease",
        "confidence": 88.8
    })

    print("✅ MongoDB Atlas connection successful")
    print("✅ Test documents inserted into Atlas")

if __name__ == "__main__":
    test_connection()
