from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dbs_zadanie.v1_companies.v1_get_companies import get_request_migrations
from dbs_zadanie.v1_submissions import v1_delete_submissions
from dbs_zadanie.v1_submissions import v1_get_submissions
from dbs_zadanie.v1_submissions import v1_post_submissions
from dbs_zadanie.v2_submissions import v2_get_submissions, v2_delete_submissions, v2_post_submissions


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
        post = v1_get_submissions.get_request(request)
        return JsonResponse(post)
    if request.method == 'POST':
        validated, post = v1_post_submissions.post_request(request)
        if validated:
            return JsonResponse({"response": post}, status=201)
        else:
            return JsonResponse(post, status=422)


@csrf_exempt
def companies(request):
    post = get_request_migrations(request)
    return JsonResponse(post)


@csrf_exempt
def delete(request, sub_id):
    if request.method == 'DELETE':
        success, error = v1_delete_submissions.delete_request(request, sub_id)
        if success:
            return JsonResponse({}, status=204)
        else:
            return JsonResponse(error, status=404)


@csrf_exempt
def v2_submissions(request):
    if request.method == 'GET':
        post = v2_get_submissions.get_request(request)
        return JsonResponse(post)
    if request.method == 'POST':
        validated, post = v2_post_submissions.post_request(request)
        if validated:
            return JsonResponse({"response": post}, status=201)
        else:
            return JsonResponse(post, status=422)


@csrf_exempt
def v2_submissions_url_with_id(request, sub_id):
    if request.method == 'DELETE':
        success, error = v2_delete_submissions.delete_request(sub_id)
        if success:
            return JsonResponse({}, status=204)
        else:
            return JsonResponse(error, status=404)
    if request.method == 'GET':
        post = v2_get_submissions.get_from_id(sub_id)
        return JsonResponse(post)
