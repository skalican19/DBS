from django.db import connection
from dbs_zadanie.shared_functions.shared_functions import parse_url_get, format_output_get


def get_request(request):
    information = parse_url_get(request)
    cursor = connection.cursor()

    where_date = ''
    if information['registration_date_gte'] != '0001-01-01' or information['registration_date_lte'] != '9999-12-12':
        where_date = 'AND registration_date BETWEEN %(registration_date_gte)s::date AND %(' \
                     'registration_date_lte)s::date '

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
                        city,  count(*) OVER() AS full_count                           
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

    return format_output_get(information, total, posts_json)
