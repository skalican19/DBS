from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import math


def index(request):
    return HttpResponse("Hello, world.")


def uptime(request):
    cursor = connection.cursor()
    cursor.execute("SELECT date_trunc('second', current_timestamp -pg_postmaster_start_time()) as uptime")
    uptime_db = cursor.fetchone()
    output = {'pgsql': {'uptime': str(uptime_db[0]).replace(',', '')}}
    return JsonResponse(output, safe=False)


@csrf_exempt
def show_pages(request):
    if request.method == 'GET':
        post = get_method(request)
        return JsonResponse(post)
    if request.method == 'POST':
        return HttpResponse("post")
    if request.method == 'DELETE':
        return HttpResponse("del")


def get_method(request):
    information = parse_url(request)
    cursor = connection.cursor()

    where_date = ''
    if information['registration_date_gte'] != '0001-01-01' or information['registration_date_lte'] != '9999-12-12':
        where_date = ' AND registration_date BETWEEN %(registration_date_gte)s AND %(registration_date_lte)s '

    cursor.execute('''SELECT id,
                        br_court_code,
                        kind_name,cin,
                        registration_date,
                        corporate_body_name,
                        br_section,
                        br_insertion,
                        text,
                        street,
                        postal_code,
                        city, 
                        (SELECT COUNT(*) 
                        FROM ov.or_podanie_issues 
                        WHERE (cin::text ~* %(query)s OR city ~* %(query)s OR corporate_body_name ~* %(query)s)'''
                   + where_date + ''') AS TotalRows
                            
                        FROM ov.or_podanie_issues   
                        WHERE (cin::text ~* %(query)s OR city ~* %(query)s OR corporate_body_name ~* %(query)s) '''
                   + where_date +
                   '''ORDER BY %(order_by)s ''' + information['order_type'] +
                   ''' LIMIT %(per_page)s OFFSET %(offset)s''', information)

    posts = cursor.fetchall()
    posts_json = []

    for post in posts:
        post_json = {"id": post[0], "br_court_code": post[1], "kind_name": post[2],
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

    information = {'page': request.GET.get('page', ''),
                   'per_page': request.GET.get('per_page', ''),
                   'registration_date_gte': request.GET.get('registration_date_gte', '0001-01-01'),
                   'registration_date_lte': request.GET.get('registration_date_lte', '9999-12-12'),
                   'order_by': order_by[request.GET.get('order_by', 'id')],
                   'order_type': request.GET.get('order_type', 'desc'),
                   'query': request.GET.get('query', '')}

    if information['per_page'] == '':
        information['per_page'] = 10
    else:
        information['per_page'] = int(information['per_page'])
    if information['page'] == '':
        information['page'] = 0
    else:
        information['page'] = int(information['page']) - 1
    information['offset'] = information['per_page'] * information['page']

    return information
