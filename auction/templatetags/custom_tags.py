from django import template

register = template.Library()

@register.filter()
def to_milliseconds(timedelta):
    td_ms = timedelta.total_seconds()*1000
    return td_ms

@register.filter()
def live_count(qset, count=0):
    for item in qset:
        if  item.is_active:
            count+=1
    return count