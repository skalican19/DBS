import json
from datetime import datetime

from django.db import connection

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
    cursor = connection.cursor()
    date = datetime.fromisoformat(post['registration_date'])
    year = date.year

    cursor.execute('''INSERT INTO ov.bulletin_issues(year, number, published_at, created_at, updated_at) 
                            VALUES (%s, (SELECT MAX(number) + 1 from ov.bulletin_issues), %s, %s, %s)
                            RETURNING  id;''',
                   [year, date, date, date])

    post['bulletin_id'], = cursor.fetchone()

    cursor.execute('''INSERT INTO ov.raw_issues(bulletin_issue_id, file_name, content, created_at, updated_at)
                            VALUES (%s, '-', '-', %s, %s) 
                            RETURNING id;''',
                   [post['bulletin_id'], date, date])

    post['raw_id'], = cursor.fetchone()

    post['address_line'] = post['street'] + ',' + post['postal_code'] + post['city']
    cursor.execute('''INSERT INTO ov.or_podanie_issues(bulletin_issue_id, raw_issue_id, br_mark, 
                             br_court_code, br_court_name, kind_code, kind_name, cin, 
                             registration_date, corporate_body_name, br_section, br_insertion, text,
                             created_at, updated_at, address_line, street, postal_code, city)
                             VALUES  (%(bulletin_id)s, %(raw_id)s, '-', '-', %(br_court_name)s, '-', %(kind_name)s, %(cin)s, 
                             %(registration_date)s, %(corporate_body_name)s, %(br_section)s, 
                             %(br_insertion)s, %(text)s, %(registration_date)s, %(registration_date)s,
                             %(address_line)s, %(street)s, %(postal_code)s, %(city)s)
                             RETURNING id;'''
                   , post)
    post['id'] = cursor.fetchone()[0]


def validate_date(date_time):
    try:
        datetime.fromisoformat(date_time)
    except ValueError:
        return False
    return True



