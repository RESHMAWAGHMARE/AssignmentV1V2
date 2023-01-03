from flask import jsonify
import uuid
import os
from app.models.rapid_query import get_meet_detail, meeting_detail, transcript_get
from app.service.message_trance import meeting_details
from celery import Celery
from config import app
from extension import logging

simple_app = Celery(app.config['CELERY_WORKER'],
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_BACKEND_URL'])


def meeting_link_gen(request):
    uid = str(uuid.uuid1())
    meet_id = request.form['meet_id']
    meet_data = meeting_detail(meet_id)
    meet_data = meet_data[0]
    upload_folder = None
    filename = None
    title_with_underscore = meet_data['title'].strip().replace(" ", "_")

    time_with_date = f"{meet_data['start_time'].hour}:{meet_data['start_time'].minute}_{meet_data['start_time'].year}-{meet_data['start_time'].month}-{meet_data['start_time'].day}"
    filename = f"{title_with_underscore.lower()}_{time_with_date}"
    upload_folder = os.path.join(os.getcwd(), f'transcripts/{filename}.csv')

    resp = meeting_details( meet_id, meet_data['meet_link'], meet_data['title'], meet_data['notes'], upload_folder)

    # call celery worker
    task_result = simple_app.send_task('tasks.google_meet',
                                       kwargs={'meet_link': meet_data['meet_link'], 'filename': filename,
                                               'title': meet_data['title'],
                                               'start_time': time_with_date, 'transcript_id': resp})

    transcripts_url = os.path.join(os.getcwd(), f'transcripts/{filename}.csv')

    result = {}
    result['meet_id'] = meet_data['meet_id']
    result['transcript_url'] = transcripts_url
    return jsonify({"status_code": 200, "message": "meeting initiated successfully ended.", "data": result})