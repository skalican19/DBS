from django.db.models import Q, F

from dbs_zadanie.models import OrPodanieIssues
from dbs_zadanie.shared_functions.shared_functions import parse_url_submissions, format_output_get


def get_from_id(sub_id):
    post = OrPodanieIssues.objects.get(id=sub_id)
    if post is not None:
        return {'response': post.as_dict()}
    return {'response': ''}


def get_request(request):
    information = parse_url_submissions(request)

    convert_order_by = ['id', 'br_court_name', 'kind_name', 'cin', 'registration_date', 'corporate_body_name',
                        'br_section', 'br_insertion', 'text', 'street', 'postal_code', 'city']

    order_by = convert_order_by[information['order_by'] - 1]
    filter_with = create_filter(information)

    if information['order_type'] == 'desc':
        query = OrPodanieIssues.objects.filter(filter_with).order_by(F(order_by).desc(nulls_last=True))
    else:
        query = OrPodanieIssues.objects.filter(filter_with).order_by(F(order_by).asc(nulls_last=True))

    total = query.count()
    query = query[information['page']:information['page'] + information['per_page']]

    posts_json = [post.as_dict() for post in query]
    output = format_output_get(information, total, posts_json)

    return output


def create_filter(information):
    new_filter = Q()

    if information['query'] != '':
        new_filter |= Q(cin__contains=information['query']) | \
                      Q(corporate_body_name__contains=information['query']) | \
                      Q(city__contains=information['query'])
    if information['registration_date_gte'] != '0001-01-01' or information['registration_date_lte'] != '9999-12-12':
        new_filter &= Q(registration_date__range=
                        [information['registration_date_gte'][:10], information['registration_date_lte'][:10]])

    return new_filter

