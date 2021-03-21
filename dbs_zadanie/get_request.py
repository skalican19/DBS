from django.db import connection
from datetime import datetime
import math


def get_request(request):
    information = parse_url(request)
    cursor = connection.cursor()

    where_date = ''
    if information['registration_date_gte'] != '0001-01-01' or information['registration_date_lte'] != '9999-12-12':
        where_date = ' AND registration_date BETWEEN %(registration_date_gte)s::date AND %(registration_date_lte)s::date'

    posts_json = []
    cursor.execute('''SELECT id,
                        br_court_name,
                        kind_name,cin,
                        registration_date,
                        corporate_body_name,
                        br_section,
                        br_insertion,
                        text,
                        street,
                        postal_code,
                        city, count(*) OVER() AS full_count                             
                        FROM ov.or_podanie_issues   
                        WHERE (cin::text ~* %(query)s OR city ~* %(query)s OR corporate_body_name ~* %(query)s)'''
                   + where_date +
                   ''' ORDER BY %(order_by)s ''' + information['order_type'] +
                   ''' LIMIT %(per_page)s OFFSET %(offset)s''', information)
    posts = cursor.fetchall()
    total = 0
    if posts:
        for post in posts:
            post_json = {"id": post[0], "br_court_name": post[1], "kind_name": post[2],
                         "cin": post[3], "registration_date": str(post[4]), "corporate_body_name": post[5],
                         "br_section": post[6], "br_insertion": post[7], "text": post[8], "street": post[9],
                         "postal_code": post[10], "city": post[11]}
            posts_json.append(post_json)
        total = posts[0][12]

    per_page = information['per_page']
    pages = math.ceil(total / per_page)

    metadata = {"page": information['page'] + 1, "per_page": information['per_page'], "pages": pages, "total": total}
    output = {"items": posts_json, "metadata": metadata}

    return output


def parse_url(request):
    information = {'page': request.GET.get('page', '1'),
                   'per_page': request.GET.get('per_page', '10'),
                   'registration_date_gte': request.GET.get('registration_date_gte', '0001-01-01'),
                   'registration_date_lte': request.GET.get('registration_date_lte', '9999-12-12'),
                   'order_by': request.GET.get('order_by', 'id'),
                   'order_type': request.GET.get('order_type', 'desc'),
                   'query': request.GET.get('query', '')}

    validate_params(information)

    return information


def validate_params(information):
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
