from django import forms
from .models import Auction, Bid
from paintings.models import Painting
import datetime
from django.forms import widgets
from django.forms import SplitDateTimeWidget
from django.utils.safestring import mark_safe



class DurationSelectWidget(forms.widgets.MultiWidget):

    template_name = 'select.html'

    def __init__(self, attrs=None):
        days = ((day, day) for day in (1,3,7,14,21,30))
        hours = ((hour, hour) for hour in range(6,24+1,6))
        minutes = ((minute, minute) for minute in range(10,50+1,10))
        _widgets = (
            widgets.Select(attrs={'time':'days'}, choices=days),
            widgets.Select(attrs={'time':'hours'}, choices=hours),
            widgets.Select(attrs={'time':'minutes'}, choices=minutes),
        )
        
        
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value, value, value]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = datetime.timedelta(
                days=int(datelist[0]),
                hours=int(datelist[1]),
                minutes=int(datelist[2]),
            )
        except ValueError:
            return ''
        else:
            return str(D)


class AuctionForm(forms.ModelForm):

    # DAYS_CHOICES = [(i, i) for i in range(1, 10+1)]
    # HOURS_CHOICES = [(i, i) for i in range(1, 24)]
    # MINUTES_CHOICES = [(i, i) for i in range(1, 60)]

    # days = forms.ChoiceField(label='Days', choices=DAYS_CHOICES, required=False)
    # hours = forms.ChoiceField(label='Hours', choices=HOURS_CHOICES, required=False)
    # minutes = forms.ChoiceField(label='Minutes', choices=MINUTES_CHOICES, required=False)

    class Meta:
        model = Auction
        fields = ('painting', 'start_price', 'increment', 'duration',  'is_active')

    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['painting'] = forms.ModelChoiceField(queryset=(Painting.objects.filter(owner=self.request.user)))
        self.fields['duration'].widget = DurationSelectWidget()

    