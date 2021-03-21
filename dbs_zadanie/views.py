from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dbs_zadanie.delete_request import delete_request
from dbs_zadanie.get_request import *
from dbs_zadanie.post_request import *


def index(request):
    return HttpResponse("Hello, world.")


def uptime(request):
    cursor = connection.cursor()
    cursor.execute("SELECT date_trunc('second', current_timestamp -pg_postmaster_start_time()) as uptime")
    uptime_db = cursor.fetchone()
    output = {'pgsql': {'uptime': str(uptime_db[0]).replace(',', '')}}
    return JsonResponse(output, safe=False)


@csrf_exempt
def submissions(request):
    if request.method == 'GET':
        post = get_request(request)
        return JsonResponse(post)
    if request.method == 'POST':
        validated, post = post_request(request)
        if validated:
            return JsonResponse({"response": post}, status=201)
        else:
            return JsonResponse(post, status=422)


@csrf_exempt
def delete(request, sub_id):
    if request.method == 'DELETE':
        success, error = delete_request(request, sub_id)
        if success:
            return JsonResponse({}, status=204)
        else:
            return JsonResponse(error, status=404)


