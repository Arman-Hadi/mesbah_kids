import hashlib

from django.db.models import Count, Max


def normalize_etag(value):
    if not value:
        return ''
    value = value.strip()
    if value.startswith('W/'):
        value = value[2:].strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        value = value[1:-1]
    return value


def compute_kids_etag(queryset):
    agg = queryset.aggregate(
        count=Count('pk'),
        max_last_change=Max('last_change'),
    )
    max_last_change = agg['max_last_change']
    token = f"{agg['count']}:{max_last_change.isoformat() if max_last_change else ''}"
    return hashlib.md5(token.encode()).hexdigest()
