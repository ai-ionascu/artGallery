from django import forms
from .models import Auction, Bid
from paintings.models import Painting
import datetime
from django.forms import widgets
from django.forms import SplitDateTimeWidget
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError



class DurationSelectWidget(forms.widgets.MultiWidget):

    template_name = 'select.html'

    def __init__(self, attrs=None):
        days = ((day, day) for day in (0,1,3,7,14,21,30))
        hours = ((hour, hour) for hour in range(0,24+1,6))
        minutes = ((minute, minute) for minute in range(1,50+1,10))
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

    class Meta:
        model = Auction
        fields = ('painting', 'start_price', 'increment', 'duration')

    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['painting'] = forms.ModelChoiceField(queryset=(Painting.objects.filter(owner=self.request.user)))
        self.fields['duration'].widget = DurationSelectWidget()      

class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Bid
        fields=('bid',)
        widgets = {'bid': forms.NumberInput(attrs={'step':'100'})}

    def clean(self):

        new_bid = self.cleaned_data.get('bid')
        bid_minimum = self.auction.current_price + self.auction.increment
        print(bid_minimum)
        if new_bid:
            if new_bid < bid_minimum:
                raise ValidationError('You cannot bid less than %d' % bid_minimum)