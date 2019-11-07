from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from paintings.models import Painting, Subject, Trend, Media
from artists.models import Artist
from django.core.validators import ValidationError
from django.utils.safestring import mark_safe

class SelectInputWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super().render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class SelectMultipleInputWidget(forms.widgets.MultiWidget):

    def __init__(self, data_list, name, attrs=None, *args, **kwargs):
        _widgets = (forms.TextInput(attrs=attrs), forms.SelectMultiple(attrs=attrs, choices=data_list),)
        super().__init__(_widgets, attrs, *args, **kwargs)

    def decompress(self, value):
        if value:
            return [value, value]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        result = [widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)] 
        if not result[0] and not result[1]:
            output=None
        output=[result[0],] if result[0] else []
        for k in result[1]:
            output.append(k)
        return ','.join(output)
    
class SubjectDataField(forms.CharField):
    def formfield(self, **kwargs):
        return super().formfield(form_class=forms.MultiValueField)

class NewPainting(forms.ModelForm):

    artist = forms.CharField(required=True)
    artist_image = forms.ImageField(required=False)
    artist_user = forms.CharField(widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
    trend = forms.CharField(required=True)
    media = forms.CharField(required=True)
    subject = SubjectDataField(required=False)

    def __init__(self, *args, **kwargs):
        _items_list = kwargs.pop('data_list', None)
        super().__init__(*args, **kwargs)
        self.fields['trend'].widget = SelectInputWidget(data_list=Trend.objects.all(), name='trend')
        self.fields['media'].widget = SelectInputWidget(data_list=Media.objects.all(), name='media')
        self.fields['subject'].widget = SelectMultipleInputWidget(
                                        data_list=[(q['subject'],q['subject']) for q in Subject.objects.values('subject')],
                                        name='subject'
                                        )

    def clean_subject(self):
        if self.cleaned_data['subject'].strip() is '':
            raise ValidationError(
                ('Please add or select at least a Subject.')
            )
        return self.cleaned_data['subject']

    def save(self, commit=True):

        artist_img = self.cleaned_data['artist_image'] if self.cleaned_data['artist_image'] else '/static/img/default_img.jpg'
        artist = Artist.objects.get_or_create(name=self.cleaned_data['artist'])[0]
        # artist.objects.add(image=self.cleaned_data['artist_image'])
        artist_user = User.objects.get(username=self.cleaned_data['artist_user'])
        trend = Trend.objects.get_or_create(trend=self.cleaned_data['trend'])[0]
        media = Media.objects.get_or_create(media=self.cleaned_data['media'])[0]
        
        self.instance.artist = artist
        self.instance.artist_user = artist_user
        self.instance.trend = trend
        self.instance.media = media
        super().save(commit)

        subject_list = self.cleaned_data['subject'].split(",")

        for i in subject_list:
            subject = (Subject.objects.get_or_create(subject=i.strip())[0])
            self.instance.subject.add(subject)
        return self

    class Meta:
        model = Painting
        fields = ('name',  'image', 'description',
                 'year', 'size', 'price', 'availability')

class EditPainting(forms.ModelForm):

    artist = forms.CharField(required=True)
    trend = forms.CharField(required=True)
    media = forms.CharField(required=True)
    new_subject = forms.CharField(required=False)

    class Meta:
        model = Painting
        fields = ('name', 'image', 'description', 'year',
                'subject', 'size', 'availability')

    def __init__(self, *args, **kwargs):
        _items_list = kwargs.pop('data_list', None)
        super().__init__(*args, **kwargs)

        self.fields['artist'].widget = SelectInputWidget(data_list=Artist.objects.all(), name='artist')
        self.fields['trend'].widget = SelectInputWidget(data_list=Trend.objects.all(), name='trend')
        self.fields['media'].widget = SelectInputWidget(data_list=Media.objects.all(), name='media')
        print(self.fields['image'].initial)
        print(self.fields['image'])
    def save(self, commit=True):

        artist = Artist.objects.get_or_create(name=self.cleaned_data['artist'])[0]
        trend = Trend.objects.get_or_create(trend=self.cleaned_data['trend'])[0]
        media = Media.objects.get_or_create(media=self.cleaned_data['media'])[0]
        
        self.instance.artist = artist
        self.instance.trend = trend
        self.instance.media = media
        super().save(commit)
        
        if self.cleaned_data['new_subject']:
            subject_list = self.cleaned_data['new_subject'].split(",")

            for i in subject_list:
                subject = (Subject.objects.get_or_create(subject=i.strip())[0])
                self.instance.subject.add(subject)
        return self

class DeletePainting(forms.ModelForm):

    class Meta:
        model = Painting
        fields = ('name',) 
        widgets = {'name': forms.HiddenInput()}