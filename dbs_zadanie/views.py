from django.db import connection
from django.http import HttpResponse

from django.views import View


def index(request):
    return HttpResponse("Hello, world.")


def uptime(request):
    cursor = connection.cursor()
    cursor.execute("SELECT date_trunc('second', current_timestamp -pg_postmaster_start_time()) as uptime")
    string = cursor.fetchone()
    return HttpResponse(string)
