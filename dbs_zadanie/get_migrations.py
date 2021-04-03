from django.db import connection
from datetime import datetime
import math


def get_request_migrations(request):
    information = parse_url(request)
    cursor = connection.cursor()

    where = ''
    if information['query'] != '':
        where = ' WHERE (name ~* %(query)s OR address_line ~* %(query)s)'
    where_date = ''
    if information['last_update_gte'] != '0001-01-01' or information['last_update_lte'] != '9999-12-12':
        if where == '':
            where_date = ' WHERE last_update BETWEEN %(last_update_gte)s::date AND %(last_update_lte)s::date'
        else:
            where_date = ' AND last_update BETWEEN %(last_update_gte)s::date AND %(last_update_lte)s::date'

    posts_json = []
    cursor.execute('''with likvidator_count AS (
                            SELECT companies.cin,
                               count(companies.cin) as likvidator_issues_count
                            FROM ov.companies
                            INNER JOIN ov.likvidator_issues ON (likvidator_issues.company_id = companies.cin)
                            WHERE likvidator_issues.cin = companies.cin
                            group by companies.cin
                        ),
                        or_podanie_count AS (
                            SELECT companies.cin,
                               count(companies.cin) as or_podanie_issues_count
                            FROM ov.companies
                            INNER JOIN ov.or_podanie_issues ON (or_podanie_issues.company_id = companies.cin)
                            WHERE or_podanie_issues.cin = companies.cin
                            group by companies.cin
                        ),
                        znizenie_count AS (
                        SELECT companies.cin,
                               count(companies.cin) as znizenie_imania_issues_count
                            FROM ov.companies
                            INNER JOIN ov.znizenie_imania_issues ON (znizenie_imania_issues.company_id = companies.cin)
                            WHERE znizenie_imania_issues.cin = companies.cin
                            group by companies.cin
                        ),
                        konkurz_vyrovanania_count AS (
                        SELECT companies.cin,
                               count(companies.cin) as konkurz_vyrovnanie_issues_count
                            FROM ov.companies
                            INNER JOIN ov.konkurz_vyrovnanie_issues ON (konkurz_vyrovnanie_issues.company_id = companies.cin)
                            WHERE konkurz_vyrovnanie_issues.cin = companies.cin
                            group by companies.cin
                        ),
                        konkurz_actors_count AS (
                        SELECT companies.cin,
                               count(companies.cin) as konkurz_restrukturalizacia_actors_count
                            FROM ov.companies
                            INNER JOIN ov.konkurz_restrukturalizacia_actors ON (konkurz_restrukturalizacia_actors.company_id = companies.cin)
                            WHERE konkurz_restrukturalizacia_actors.cin = companies.cin
                            group by companies.cin
                        )
                        
                        SELECT companies.cin,
                            name,
                            br_section,
                            address_line,
                            last_update,
                            or_podanie_count.or_podanie_issues_count,
                            znizenie_count.znizenie_imania_issues_count,
                            likvidator_count.likvidator_issues_count,
                            konkurz_vyrovanania_count.konkurz_vyrovnanie_issues_count,
                            konkurz_actors_count.konkurz_restrukturalizacia_actors_count
                        FROM ov.companies
                        FULL JOIN or_podanie_count on or_podanie_count.cin = companies.cin
                        FULL JOIN znizenie_count on znizenie_count.cin = companies.cin
                        FULL JOIN likvidator_count on likvidator_count.cin = companies.cin
                        FULL JOIN konkurz_vyrovanania_count on konkurz_vyrovanania_count.cin = companies.cin
                        FULL JOIN konkurz_actors_count on konkurz_actors_count.cin = companies.cin'''
                    + where + where_date +
                   ''' ORDER BY %(order_by)s ''' + information['order_type'] +
                   ''' LIMIT %(per_page)s OFFSET %(offset)s''', information)

    print(cursor.query)
    posts = cursor.fetchall()

    cursor.execute('''SELECT count(*) 
                      FROM ov.companies'''
                   + where + where_date, information)
    print(cursor.query)
    total, = cursor.fetchone()

    if posts:
        for post in posts:
            post_json = {"cin": post[0], "name": post[1], "br_section": post[2], "address_line": post[3],
                         "last_update": str(post[4]), "or_podanie_issues_count": post[5], "znizenie_imania_issues_count": post[6],
                         "likvidator_issues_count": post[7], "konkurz_vyrovnanie_issues_count": post[8], "konkurz_restrukturalizacia_actors_count": post[9]}
            posts_json.append(post_json)

    per_page = information['per_page']
    pages = math.ceil(total / per_page)

    metadata = {"page": information['page'] + 1, "per_page": information['per_page'], "pages": pages, "total": total}
    output = {"items": posts_json, "metadata": metadata}

    return output


def parse_url(request):
    information = {'page': request.GET.get('page', '1'),
                   'per_page': request.GET.get('per_page', '10'),
                   'last_update_gte': request.GET.get('last_update_gte', '0001-01-01'),
                   'last_update_lte': request.GET.get('last_update_lte', '9999-12-12'),
                   'order_by': request.GET.get('order_by', 'cin'),
                   'order_type': request.GET.get('order_type', 'desc'),
                   'query': request.GET.get('query', '')}

    validate_params(information)

    return information


def validate_params(information):
    order_by = {'cin': 1,
                'name': 2,
                'br_section': 3,
                'address_line': 4,
                'last_update': 5,
                'or_podanie_issues_count': 6,
                'znizenie_imania_issues_count': 7,
                'likvidator_issues_count': 8,
                'konkurz_vyrovnanie_issues_count': 9,
                'konkurz_restrukturalizacia_actors_count': 10,
                }

    if information['order_by'] in order_by.keys():
        information['order_by'] = order_by[information['order_by']]
    else:
        information['order_by'] = 1

    if information['order_type'].lower() != 'asc' and information['order_type'].lower() != 'desc':
        information['order_type'] = 'desc'

    if information['last_update_gte'] != '0001-01-01':
        if not validate_date(information['last_update_gte']):
            information['last_update_gte'] = '0001-01-01'

    if information['last_update_lte'] != '9999-12-12':
        if not validate_date(information['last_update_lte']):
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
