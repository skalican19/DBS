import json
from datetime import datetime

from django.db import connection


def post_request(request):
    post = json.loads(request.body.decode('utf-8'))

    validated, errors = validate_params(post)

    if validated:
        insert(post)
        response = create_response(post)
        return validated, response
    else:
        error_message = {"errors": errors}
        return validated, error_message


def validate_params(post):
    validation = True
    keys = ['br_court_name', 'kind_name', 'cin', 'registration_date', 'corporate_body_name',
            'br_section', 'br_insertion', 'text', 'street', 'postal_code', 'city']
    error = []

    for key in keys:
        if key not in post.keys():
            error.append({"field": key, "reasons": ['required']})
            validation = False
            continue

        if key == 'cin':
            if not isinstance(post['cin'], int):
                error.append({"field": key, "reasons": ['required', 'not_number']})
                validation = False

        elif key == 'registration_date':
            if validate_date(post['registration_date']):
                date = datetime.fromisoformat(post['registration_date'])
                if date.year != datetime.today().year:
                    error.append({"field": key, "reasons": ['required', 'invalid_range']})
                    validation = False
            else:
                error.append({"field": key, "reasons": ['required', 'invalid_range']})
                validation = False

        elif not isinstance(post[key], str) or post[key] == '':
            error.append({"field": key, "reasons": ['required']})
            validation = False

    return validation, error


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


def create_response(post):
    response = {"id": post['id'], "br_court_name": post['br_court_name'], "kind_name": post["kind_name"],
                "cin": post["cin"], "registration_date": post["registration_date"],
                "corporate_body_name": post["corporate_body_name"], "br_section": post["br_section"],
                "br_insertion": post["br_insertion"], "text": post["text"], "street": post["street"],
                "postal_code": post["postal_code"], "city": post["city"]}
    return response

