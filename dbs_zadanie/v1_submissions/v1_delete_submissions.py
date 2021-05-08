from django.db import connection


def delete_request(request, sub_id):

    cursor = connection.cursor()
    cursor.execute('''SELECT bulletin_issue_id, raw_issue_id FROM ov.or_podanie_issues WHERE id = %s''', [sub_id])

    if cursor.rowcount == 0:
        return False, {"error": {"message": "Záznam neexistuje"}}

    bulletin_id, raw_id, = cursor.fetchone()
    cursor.execute('''SELECT COUNT(raw_issue_id) FROM ov.or_podanie_issues WHERE raw_issue_id = %s''', [raw_id])
    count_raw, = cursor.fetchone()

    cursor.execute('''SELECT COUNT(bulletin_issue_id) FROM ov.or_podanie_issues where bulletin_issue_id = %s''',
                   [bulletin_id])

    count_bulletin, = cursor.fetchone()
    cursor.execute('''SELECT COUNT(bulletin_issue_id) FROM ov.raw_issues where bulletin_issue_id = %s''',
                   [bulletin_id])
    count_bulletin_2, = cursor.fetchone()

    if count_bulletin == 1 and count_bulletin_2 == 1:
        cursor.execute('''DELETE FROM ov.bulletin_issues WHERE id = %s''', [bulletin_id])

    if count_raw == 1:
        cursor.execute('''DELETE FROM ov.raw_issues WHERE id = %s''', [raw_id])

    cursor.execute('''DELETE FROM ov.or_podanie_issues WHERE id = %s''', [sub_id])

    return True, {}







