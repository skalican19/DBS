from django.db.models import Q, Count, F

from dbs_zadanie.models import Companies
from dbs_zadanie.shared_functions.shared_functions import parse_url_companies, format_output_get


def get_request(request):
    information = parse_url_companies(request)
    convert_order_by = ['cin', 'name', 'br_section', 'address_line', 'last_update', 'or_podanie_issues_count',
                        'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count',
                        'konkurz_restrukturalizacia_actors_count']

    order_by = convert_order_by[information['order_by'] - 1]
    filter_with = create_filter(information)

    query = Companies.objects.filter(filter_with).annotate(or_podanie_issues_count=Count('orpodanieissues'),
                                                           znizenie_imania_issues_count=Count('znizenieimaniaissues'),
                                                           likvidator_issues_count=Count('likvidatorissues'),
                                                           konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues'),
                                                           konkurz_restrukturalizacia_actors_count=Count(
                                                               'konkurzrestrukturalizaciaactors'))

    if information['order_type'] == 'asc':
        query = query.order_by(F(order_by).asc(nulls_last=True))
    else:
        query = query.order_by(F(order_by).desc(nulls_last=True))

    total = query.count()
    query = query[information['page']:information['page'] + information['per_page']]

    index = 0
    posts_json = []
    for post in query:
        posts_json.append(post.as_dict())
        posts_json[index]['or_podanie_issues_count'] = post.or_podanie_issues_count
        posts_json[index]['znizenie_imania_issues_count'] = post.znizenie_imania_issues_count
        posts_json[index]['likvidator_issues_count'] = post.likvidator_issues_count
        posts_json[index]['konkurz_vyrovnanie_issues_count'] = post.konkurz_vyrovnanie_issues_count
        posts_json[index]['konkurz_restrukturalizacia_actors_count'] = post.konkurz_restrukturalizacia_actors_count

    output = format_output_get(information, total, posts_json)

    return output


def create_filter(information):
    new_filter = Q()

    if information['query'] != '':
        new_filter |= (Q(name__contains=information['query']) | Q(address_line__contains=information['query']))
    if information['last_update_gte'] != '1000-01-01' or information['last_update_lte'] != '3000-12-12':
        new_filter &= Q(last_update__range=
                        [information['last_update_gte'][:10], information['last_update_lte'][:10]])

    return new_filter
