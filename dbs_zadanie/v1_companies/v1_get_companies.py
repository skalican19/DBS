from django.db import connection
from datetime import datetime
from dbs_zadanie.shared_functions.shared_functions import format_output_get, parse_url_companies


def get_request_migrations(request):
    information = parse_url_companies(request)
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
                        LEFT JOIN or_podanie_count on or_podanie_count.cin = companies.cin
                        LEFT JOIN znizenie_count on znizenie_count.cin = companies.cin
                        LEFT JOIN likvidator_count on likvidator_count.cin = companies.cin
                        LEFT JOIN konkurz_vyrovanania_count on konkurz_vyrovanania_count.cin = companies.cin
                        LEFT JOIN konkurz_actors_count on konkurz_actors_count.cin = companies.cin'''
                    + where + where_date +
                   ''' ORDER BY %(order_by)s ''' + information['order_type'] +
                   ''' LIMIT %(per_page)s OFFSET %(offset)s''', information)

    posts = cursor.fetchall()

    cursor.execute('''SELECT count(*) 
                      FROM ov.companies'''
                   + where + where_date, information)

    total, = cursor.fetchone()

    if posts:
        for post in posts:
            post_json = {"cin": post[0], "name": post[1], "br_section": post[2], "address_line": post[3],
                         "last_update": str(post[4]), "or_podanie_issues_count": post[5], "znizenie_imania_issues_count": post[6],
                         "likvidator_issues_count": post[7], "konkurz_vyrovnanie_issues_count": post[8], "konkurz_restrukturalizacia_actors_count": post[9]}
            posts_json.append(post_json)

    return format_output_get(information, total, posts_json)




