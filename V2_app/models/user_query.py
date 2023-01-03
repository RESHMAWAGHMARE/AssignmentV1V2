from extension import app, db, collection

user_collection = db['users']


def insert_user(request_data):
    app.logger.info(f"RapidTrance: new user added")
    user_collection.insert_one(
        request_data
    )


def exist_user(user_id):
    app.logger.info(f"RapidTrance: check user exists or not")
    return user_collection.find_one(
        {
            'user_id': user_id
        }
    )