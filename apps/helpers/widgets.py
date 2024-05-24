from django_select2.forms import ModelSelect2Widget
from django import forms


class CustomSelect2Mixin(ModelSelect2Widget):
    @property
    def media(self):
        return forms.Media([])

