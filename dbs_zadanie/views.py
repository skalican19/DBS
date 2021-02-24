from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse

from django.views import View


def index(request):
    return HttpResponse("Hello, world.")


def uptime(request):
    cursor = connection.cursor()
    cursor.execute("SELECT date_trunc('second', current_timestamp -pg_postmaster_start_time()) as uptime")
    uptime_db = cursor.fetchone()
    output = {'pgsql': {'uptime': str(uptime_db[0]).replace(',', '')}}
    return JsonResponse(output, safe=False)
