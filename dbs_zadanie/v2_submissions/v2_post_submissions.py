import json

from django.db.models import Max
from django.utils import timezone

from dbs_zadanie.models import OrPodanieIssues, BulletinIssues, RawIssues
from dbs_zadanie.shared_functions.shared_functions import validate_params_post, create_response_get


def post_request(request):
    post = json.loads(request.body.decode('utf-8'))

    validated, errors = validate_params_post(post)
    if validated:
        insert(post)
        response = create_response_get(post)
        return validated, response
    else:
        error_message = {"errors": errors}
        return validated, error_message


def insert(post):
    today = timezone.now()
    year = today.year

    address_line = post['street'] + ", " + post['postal_code'] + " " + post['city']

    max_number = BulletinIssues.objects.aggregate(Max('number'))
    bulletin_entry = BulletinIssues(year=year, number=max_number['number__max'] + 1, published_at=today, created_at=today,
                                    updated_at=today)
    bulletin_entry.save()

    raw_entry = RawIssues(bulletin_issue=bulletin_entry, file_name='-', content='-', created_at=today, updated_at=today)
    raw_entry.save()

    or_podanie_entry = OrPodanieIssues(br_court_name=post['br_court_name'], kind_name=post['kind_name'],
                                       cin=post['cin'],
                                       registration_date=post['registration_date'],
                                       corporate_body_name=['corporate_body_name'],
                                       br_section=post['br_section'],
                                       br_insertion=post['br_insertion'],
                                       text=post['text'],
                                       street=post['street'],
                                       postal_code=post['postal_code'],
                                       city=post['city'],
                                       created_at=today,
                                       updated_at=today,
                                       address_line=address_line,
                                       bulletin_issue=bulletin_entry,
                                       raw_issue=raw_entry,
                                       br_mark='-', br_court_code='-', kind_code='-')
    or_podanie_entry.save()
    post['id'] = or_podanie_entry.id
