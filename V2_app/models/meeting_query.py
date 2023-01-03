import logging

import pymongo

from extension import app, db, collection
import bson
from flask import jsonify
import json

meeting_collection = db['meeting']


def insert_meeting(request_data):
    app.logger.info(f"RapidTrance: new meeting added")
    return meeting_collection.insert_one(
        request_data
    )


def meeting_get_by_id(identifier):
    identifier = bson.ObjectId(oid=str(identifier))
    app.logger.info(f"RapidTrance: meetings_get route got called with input: {identifier}")
    if meeting_collection.find({'_id': identifier}):
        document = meeting_collection.find({'_id': identifier})

        data = []
        for i, obj in enumerate(document):
            obj["_id"] = str(obj["_id"])
            data.append(obj)

        return data
    return 404


def meeting_get_all(filter_params, sort_field, skips, length):
    app.logger.info(f"RapidTrance: meetings_get route got called")
    document = meeting_collection.find(dict(filter_params)).sort(sort_field).skip(skips).limit(length)
    total_count = meeting_collection.find()

    data = []
    for i, obj in enumerate(document):
        obj["_id"] = str(obj["_id"])
        data.append(obj)

    data2 = []
    for i, obj in enumerate(total_count):
        obj["_id"] = str(obj["_id"])
        data2.append(obj)
    total_length = len(data2)
    total_page = total_length / length

    return jsonify({
        'status_code': 200,
        'message': 'Successfully fetched',
        'list': data,
        'meta': {
            'total_pages': int(total_page),
            'count': len(data),
            'total_count': total_length
        }
    })

def update_meeting(id, data):
    app.logger.info(f"RapidTrance: update_meeting query function got called with input: {id}")
    meeting_collection.update_one(
        {
            '_id': bson.ObjectId(id)
        },
        {
            '$set': data
        }
    )

def update_meeting_by_event_id(event_id, data):
    app.logger.info(f"RapidTrance: update_meeting_by_event_id query function got called with input: {event_id}")
    if meeting_collection.find({'event_id': event_id}):
        meeting_collection.update_one(
            {
                'event_id': event_id
            },
            {
                '$set': data
            }
        )
        return True

    return False


def meeting_get_by_event_id(event_id):
    app.logger.info(f"RapidTrance: meeting_get_by_event_id route got called with eventId: {event_id}")

    result = meeting_collection.find_one({"event_id":event_id})
    if isinstance(result, dict):

        result['_id'] = str(result['_id'])
        return result
    return False


def event_ownered_by_user(user_id, event_id):
    app.logger.info(f"RapidTrance: check_with_multiple_cond route got called with userId and eventId: {user_id}, {event_id}")

    result = meeting_collection.find_one({"event_id":event_id})
    if result:
        if result['organiser_id'] == user_id:
            return True
        return False
    return False