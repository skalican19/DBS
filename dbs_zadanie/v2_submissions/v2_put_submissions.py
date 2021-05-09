import json
from datetime import datetime

from dbs_zadanie.models import OrPodanieIssues
from dbs_zadanie.shared_functions import shared_functions


def put_from_id(request, sub_id):
    post_to_edit = OrPodanieIssues.objects.get(id=sub_id)
    params_for_edit = json.loads(request.body.decode('utf-8'))

    if post_to_edit is None:
        return False, {"error": {"message": "Záznam neexistuje"}}

    validation, error = validate_params(params_for_edit)

    if validation:
        OrPodanieIssues.objects.filter(id=sub_id).update(**params_for_edit)
        return True, {'response': OrPodanieIssues.objects.get(id=sub_id).as_dict()}
    else:
        return False, {'errors': error}


def validate_params(params):
    keys = ['br_court_name', 'kind_name', 'cin', 'registration_date', 'corporate_body_name',
            'br_section', 'br_insertion', 'text', 'street', 'postal_code', 'city']
    error = []
    validation = True

    for key in keys:

        if key in params:

            if key == 'cin':
                if not isinstance(params['cin'], int):
                    error.append({"field": key, "reasons": ['not_number']})
                    validation = False

            elif key == 'registration_date':
                if shared_functions.validate_date(params['registration_date']):
                    date = datetime.fromisoformat(params['registration_date'])
                    if date.year != datetime.today().year:
                        error.append({"field": key, "reasons": ['invalid_range']})
                        validation = False
                else:
                    error.append({"field": key, "reasons": ['invalid_range']})
                    validation = False

            elif not isinstance(params[key], str):
                error.append({"field": key, "reasons": ['not_string']})
                validation = False

    for key in params:
        if key not in keys:
            del params[keys]

    return validation, error

