from config import Config
from mockfirestore import MockFirestore
from firebase_admin import firestore


def init_db(client, config: Config):
    if config.ENV == "test":
        return MockFirestore()
    else:
        return firestore.client(client)
