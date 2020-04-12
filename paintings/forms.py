from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from .models import Painting, Subject, Trend, Media, Like
from generic_models.models import Comment
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
    trend = forms.CharField(required=True)
    media = forms.CharField(required=True)
    subject = SubjectDataField(required=False)

    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['artist'].widget = SelectInputWidget(data_list=Artist.objects.all(), name='artist')
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

        owner = User.objects.get(username=self.request.user.username) if self.request is not None else None

        for f in self.instance._meta.fields:
            if f.related_model and f.related_model not in [User, Subject]:
                try:
                    item = f.related_model.objects.get(**{f.name:self.cleaned_data['{}'.format(f.name)]})
                except f.related_model.DoesNotExist:
                    item = f.related_model(**{f.name:self.cleaned_data['{}'.format(f.name)]}, owner=owner)
                    item.save()
                
                self.instance.__setattr__('{}'.format(f.name), item)

        self.instance.owner = owner

        super().save(commit)
        
        subject_list = self.cleaned_data['subject'].split(",")

        for i in subject_list:
            try:
                subject = Subject.objects.get(subject=i.strip())
            except Subject.DoesNotExist:
                subject = Subject(subject=i.strip(), owner=owner)
                subject.save()
            self.instance.subject.add(subject)
        return self

    class Meta:
        model = Painting
        fields = ('name', 'image', 'description',
                 'year', 'size', 'price', 'availability')

class EditPainting(forms.ModelForm):

    artist = forms.CharField(required=True)
    trend = forms.CharField(required=True)
    media = forms.CharField(required=True)
    new_subject = forms.CharField(required=False)

    class Meta:
        model = Painting
        fields = ('name', 'image', 'description', 'year',
                'subject', 'size', 'price', 'availability')

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        for f in instance._meta.fields:
            if f.related_model and f.related_model not in [User, Subject]:
                self.fields[f.name].initial = f.related_model.objects.get(painting__id=instance.id)
                self.fields[f.name].widget = SelectInputWidget(data_list=f.related_model.objects.all(), name=f.name)
            elif f.related_model is Subject:
                self.fields[f.name].initial = f.related_model.objects.filter(painting__id=instance.id) 

    def save(self, commit=True):

        for f in self.instance._meta.fields:
            if f.related_model and f.related_model not in [User, Subject]:
                try:
                    item = f.related_model.objects.get(**{f.name:self.cleaned_data['{}'.format(f.name)]})
                except f.related_model.DoesNotExist:
                    item = f.related_model(**{f.name:self.cleaned_data['{}'.format(f.name)]}, owner=owner)
                    item.save()
                
                self.instance.__setattr__('{}'.format(f.name), item)

        super().save(commit)
        
        if self.cleaned_data['new_subject']:
            subject_list = self.cleaned_data['new_subject'].split(",")

            for i in subject_list:
                try:
                    subject = Subject.objects.get(subject=i.strip())
                except Subject.DoesNotExist:
                    subject = Subject(subject=i.strip(), owner=owner)
                    subject.save()
                self.instance.subject.add(subject)
        return self

class DeletePainting(forms.ModelForm):

    class Meta:
        model = Painting
        fields = ('name',) 
        widgets = {'name': forms.HiddenInput()}

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',) 
        widgets = {'comment': forms.Textarea(attrs={'rows':5, 'cols':50})}