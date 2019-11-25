
from django_mvc import forms

from ..models import (Bushfire,)

class BushfireCleanMixin(object):
    pass


class BushfireConfigMixin(object):
    class Meta:
        field_classes_config = {
            "__default__":forms.fields.CharField,
            "q":forms.fields.CharField
        }
        labels_config = {
            "q":"Search",
        }
        widgets_config = {
            "__default__.view":forms.widgets.TextDisplay(),
            "__default__.edit":forms.widgets.TextInput(),
            "__default__.filter":forms.widgets.TextInput()
        }

class BushfireBaseForm(BushfireCleanMixin,BushfireConfigMixin,forms.ModelForm):
    class Meta:
        model = Bushfire


class BushfireBaseListForm(BushfireConfigMixin,forms.ListForm):
    class Meta:
        purpose = (None,('list','view'))
        model = Bushfire

class BushfireListForm(BushfireBaseListForm):
    class Meta:
        all_fields = ('fire_number','name')
