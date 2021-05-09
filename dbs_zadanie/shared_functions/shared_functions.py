import math
from datetime import datetime


def parse_url_get(request):
    information = {'page': request.GET.get('page', '1'),
                   'per_page': request.GET.get('per_page', '10'),
                   'registration_date_gte': request.GET.get('registration_date_gte', '0001-01-01'),
                   'registration_date_lte': request.GET.get('registration_date_lte', '9999-12-12'),
                   'order_by': request.GET.get('order_by', 'id'),
                   'order_type': request.GET.get('order_type', 'desc'),
                   'query': request.GET.get('query', '')}

    validate_params_get(information)

    return information


def validate_params_get(information):
    order_by = {'id': 1,
                'br_court_name': 2,
                'kind_name': 3,
                'cin': 4,
                'registration_date': 5,
                'corporate_body_name': 6,
                'br_section': 7,
                'br_insertion': 8,
                'text': 9,
                'street': 10,
                'postal_code': 11,
                'city': 12}

    if information['order_by'] in order_by.keys():
        information['order_by'] = order_by[information['order_by']]
    else:
        information['order_by'] = 1

    if information['order_type'].lower() != 'asc' and information['order_type'].lower() != 'desc':
        information['order_type'] = 'desc'

    if information['registration_date_gte'] != '0001-01-01':
        if not validate_date(information['registration_date_gte']):
            information['registration_date_gte'] = '0001-01-01'

    if information['registration_date_lte'] != '9999-12-12':
        if not validate_date(information['registration_date_lte']):
            information['registration_date_lte'] = '9999-12-12'

    if information['page'].isnumeric():
        information['page'] = int(information['page'])
        if information['page'] > 0:
            information['page'] = information['page'] - 1
    else:
        information['page'] = 0
    if information['per_page'].isnumeric():
        information['per_page'] = int(information['per_page'])
    else:
        information['per_page'] = 10

    information['offset'] = information['per_page'] * information['page']


def validate_date(date_time):
    try:
        datetime.fromisoformat(date_time)
    except ValueError:
        return False
    return True


def format_output_get(information, total, posts_json):
    per_page = information['per_page']
    pages = math.ceil(total / per_page)

    metadata = {"page": information['page'] + 1, "per_page": information['per_page'], "pages": pages, "total": total}
    output = {"items": posts_json, "metadata": metadata}

    return output


def validate_params_post(post):
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


def create_response_get(post):
    response = {"id": post['id'], "br_court_name": post['br_court_name'], "kind_name": post["kind_name"],
                "cin": post["cin"], "registration_date": post["registration_date"],
                "corporate_body_name": post["corporate_body_name"], "br_section": post["br_section"],
                "br_insertion": post["br_insertion"], "text": post["text"], "street": post["street"],
                "postal_code": post["postal_code"], "city": post["city"]}
    return response
