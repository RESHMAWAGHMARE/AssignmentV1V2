import json
from flask import Blueprint, request, jsonify
from app.service import get_all_meet
from app.service.meeting_service import meeting_create, meeting_update
from extension import logging
from app.models.meeting_query import meeting_get_by_id


meeting = Blueprint('meeting', 'meeting', url_prefix='/api/v1')


@meeting.route('/meeting', methods=['POST'])
def post_meet():
    logging.info(f"Check user id {request.form.get('user_id')}")
    return meeting_create(request)


@meeting.route('/meeting/<identifier>', methods=['GET'])
def get_by_id(identifier):
    logging.info(f"meetings_create:meetings called with:{identifier}")
    result = meeting_get_by_id(identifier)
    if result == 404 or len(result) == 0:
        return jsonify({"status_code": 404, "message": "something went wrong."})
    return jsonify({"status_code": 200, "message": "meeting details.", "transcript": result})


@meeting.route('/meeting', methods=['GET'])
def get():
    logging.info(f"meetings called")
    inputs = {
        'page': request.args['page'] if 'page' in request.args else 0,
        'length': request.args['length'] if 'length' in request.args else 0,
        'filter': json.loads(request.args['filter']) if 'filter' in request.args else {},
        'sort': json.loads(request.args['sort']) if 'sort' in request.args else {}
    }
    all_list = get_all_meet.get(inputs)
    return all_list


@meeting.route('/meeting/<string:event_id>', methods=['PUT'])
def edit(event_id):
    logging.info(f"meetings_update:meetings called with")

    return meeting_update(event_id, request)
