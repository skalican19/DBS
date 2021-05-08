import json
from datetime import date

from dbs_zadanie.models import OrPodanieIssues
from dbs_zadanie.shared_functions.shared_functions import validate_params_post, create_response_get


def post_request(request):
    post = json.loads(request.body.decode('utf-8'))

    validated, errors = validate_params_post(post)
    if validated:
        insert(post)
        response = create_response_get(post)
        return validated, response
    else:
        error_message = {"errors": errors}
        return validated, error_message


def insert(post):
    today = date.today()
    address_line = post['postal_code'] + ", " + post['postal_code']+ " " + post['city']

    db_entry = OrPodanieIssues(br_court_name=post['br_court_name'], kind_name=post['kind_name'], cin=post['cin'],
                               registration_date=post['registration_date'],
                               corporate_body_name=['corporate_body_name'],
                               br_section=post['br_section'], br_insertion=['br_insertion'], text=post['text'],
                               street=post['street'], postal_code=post['postal_code'], city=post['city'],
                               created_at=today, updated_at=today, br_mark='-', br_court_code='-',
                               kind_code='-', address_line=address_line, )






