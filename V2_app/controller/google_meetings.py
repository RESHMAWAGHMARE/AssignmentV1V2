from flask import Blueprint, request, jsonify

from app.service.google_service import google_service, meeting_fetch
from extension import logging

google_meetings = Blueprint('upcomings-meetings', 'upcomings-meetings', url_prefix='/api/v1')


@google_meetings.route('/upcomings-meetings', methods=['GET'])
def fetch():
    max_result = request.args['limit'] if 'limit' in request.args else 10
    logging.info(f'Fetching Upcoming Meetings For User ID %s', request.args["user_id"])
    creds = google_service(request.args['user_id'])
    events_result = {"data": meeting_fetch(creds,max_result)}
    logging.info(events_result)
    return jsonify(events_result)
