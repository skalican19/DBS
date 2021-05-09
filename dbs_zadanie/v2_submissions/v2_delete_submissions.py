from dbs_zadanie.models import OrPodanieIssues, BulletinIssues, RawIssues


def delete_from_id(sub_id):
    post_to_delete = OrPodanieIssues.objects.get(id=sub_id)

    if post_to_delete is None:
        return False, {"error": {"message": "Záznam neexistuje"}}

    bulletin_count_1 = OrPodanieIssues.objects.filter(bulletin_issue=post_to_delete.bulletin_issue).count()
    bulletin_count_2 = RawIssues.objects.filter(bulletin_issue=post_to_delete.bulletin_issue).count()
    raw_count = OrPodanieIssues.objects.filter(raw_issue=post_to_delete.raw_issue).count()

    if bulletin_count_1 == 1 and bulletin_count_2 == 1:
        BulletinIssues.objects.get(id=post_to_delete.bulletin_issue.id).delete()

    if raw_count == 1:
        RawIssues.objects.get(id=post_to_delete.raw_issue.id).delete()

    post_to_delete.delete()

    return True, {}


