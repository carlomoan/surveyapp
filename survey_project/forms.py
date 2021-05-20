from django import forms
from django.contrib.auth import authenticate
from .models import *


class Add_ProjectForm(forms.ModelForm):
    author = forms.CharField(widget = forms.HiddenInput(), required = False)
    class Meta:
        model = SurveyProject
        fields = ['site_No', 'Region', 'District', 'Ward', 'Location', 'Current_source', 'Distance_source',
                  'Affected_people', 'Picture', 'Video', 'Attachment']
        labels = {
            'Current_source': 'Current Source of water',
            'Distance_source': 'Distance from source of Water(in Kilometers)',
            'Affected_people': 'Number of Beneficiary',
            'Picture': 'Current source Picture(jpeg)',
            'Video': 'Current source Video',
            'Attachment': 'Application Letter'
        }
        


class WellInfoForm(forms.ModelForm):
    class Meta:
        model = WellInfo
        fields = ['site', 'contact1', 'contact2',
                  'depth', 'picture', 'Video', 'equipment']
        labels = {
            'site': 'Site Number',
            'contact1': 'Contact 1',
            'contact2': 'Contact 2',
            'depth': 'Well Depth',
            'picture': 'Well Picture',
            'Video': 'Well Video',
            'equipment': 'Equipment'
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'size', 'unit_of_size', 'material',
                  'manufacturer', 'price', 'description', 'photo']


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['item', 'amount', 'buy_time',
                  'uploader']
        labels = {
            'item': 'Stored Item',
            'amount': 'Number of units',
            'buy_time': 'Time',
            'uploader': 'Issuer'
        }
