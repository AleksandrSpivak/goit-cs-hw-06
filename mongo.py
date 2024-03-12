import logging

from pymongo.mongo_client import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime as dt


def add_message(username, message):
    """
    A function to add a message to the user_message collection in MongoDB.
    Params:
    - username: string, the username of the user
    - message: string, the message content
    Returns: None
    """

    uri = "mongodb://mongo:27017/"
    client = MongoClient(uri)
    db = client.cs_final_work

    try:

        db.user_message.insert_one(
            {
                "date": dt.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                "username": username,
                "message": message,
            }
        )

        logging.info("MongoDB: Message added")
    except ServerSelectionTimeoutError:
        logging.info("MongoDB: Unable to connect to the server.")
    finally:
        client.close()
        logging.info("MongoDB: Connection closed")

    return
