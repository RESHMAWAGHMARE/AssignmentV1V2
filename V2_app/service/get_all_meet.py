from app.models.meeting_query import meeting_get_all
from extension import app


def get(args):
    app.logger.info(f"RapidTrance: get arguments")
    if int(args['page']) == 0:
        args['page'] = 1
    if int(args['length']) == 0:
        args['length'] = 10
    skips = 10 * (int(args['page']) - 1)
    filter_params = args['filter']

    sort_field = args['sort'] if 'sort' in args else {}
    if not len(sort_field.keys()):
        sort_field = {'created_at': -1}

    sort_field = [(k, v) for k, v in sort_field.items()]

    return meeting_get_all(filter_params, sort_field, skips, int(args['length']))
