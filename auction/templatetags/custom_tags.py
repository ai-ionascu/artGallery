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

@register.filter()
def live_filter(qset):
    output=[]
    for item in qset:
        if  item.is_active:
            output.append(item)
    return output

@register.filter()
def get_remainder(count,val):
    return count % val

@register.filter()
def is_odd_row(count,val):
    floor = count // val
    return floor % 2 == 0

@register.filter()
def is_last_row(count,length):
        return count == length - 4
