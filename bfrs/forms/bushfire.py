from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.html import mark_safe

from django_mvc import forms

from ..models import (Bushfire,BushfireSnapshot)

class BushfireCleanMixin(object):
    pass


def notification_url(value,form,instance):
    if value == Bushfire.STATUS_INITIAL:
        return reverse("bfrs:initial_bushfire_update",kwargs={"pk":instance.id})
    elif value > Bushfire.STATUS_REVIEWED:
        return reverse("bfrs:invalid_bushfire_update",kwargs={"pk":instance.id})
    else:
        return reverse("bfrs:initial_bushfire_snapshot",kwargs={"pk":instance.id})

def report_url(value,form,instance):
    if value == Bushfire.STATUS_INITIAL:
        return ""
    elif value == Bushfire.STATUS_INITIAL_AUTHORISED:
        return reverse("bfrs:submitted_bushfire_update",kwargs={"pk":instance.id})
    elif value > Bushfire.STATUS_REVIEWED:
        return ""
    else:
        return reverse("bfrs:final_bushfire_snapshot",kwargs={"pk":instance.id})

def notification_template(value):
    if value == Bushfire.STATUS_INITIAL:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="Edit the initial fire report" style="color:red"><span style="display:none">100</span><i class="icon-edit icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_INITIAL_AUTHORISED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="View the submitted fire report" style="color:green"><span style="display:none">100</span><i class="icon-ok icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_FINAL_AUTHORISED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="View the authorised fire report" style="color:green"><span style="display:none">100</span><i class="icon-ok icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_REVIEWED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="View the reviewed fire report" style="color:green"><span style="display:none">100</span><i class="icon-ok icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_MERGED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="Edit the merged fire report"><span style="display:none">100</span><i class="icon-ban-circle icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_DUPLICATED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="Edit the duplicated fire report"><span style="display:none">101</span><i class="icon-ban-circle icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_INVALIDATED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="Edit the invalidated fire report"><span style="display:none">5</span><i class="icon-ban-circle icon-white"></i></a>
        """
    else:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="Edit the invalidated fire report"><span style="display:none">6</span><i class="icon-ban-circle icon-white"></i></a>
        """

def report_template(value):
    if value == Bushfire.STATUS_INITIAL:
        return ""
    elif value == Bushfire.STATUS_INITIAL_AUTHORISED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="Edit the submitted fire report" style="color:red"><span style="display:none">100</span><i class="icon-edit icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_FINAL_AUTHORISED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="View the authorised fire report" style="color:green"><span style="display:none">100</span><i class="icon-ok icon-white"></i></a>
        """
    elif value == Bushfire.STATUS_REVIEWED:
        return """
            <a href="{url}" onclick="event.stopPropagation();" title="View the reviewed fire report" style="color:green"><span style="display:none">100</span><i class="icon-ok icon-white"></i></a>
        """
    else:
        return ""

class BushfireConfigMixin(object):
    class Meta:
        field_classes_config = {
            "__default__":forms.fields.CharField,
            "q":forms.fields.CharField,
            "notifications":forms.fields.HyperlinkFieldFactory(Bushfire,'report_status',notification_url),
            "report":forms.fields.HyperlinkFieldFactory(Bushfire,'report_status',report_url),
            "report_status":forms.fields.ChoiceFieldFactory(Bushfire.REPORT_STATUS_CHOICES,field_params={"coerce":forms.fields.coerce_int,"empty_value":None}),
            "field_officer":forms.fields.OtherOptionFieldFactory(Bushfire,"field_officer",("other_field_officer","other_field_officer_agency","other_field_officer_phone"),
                other_option=lambda:User.OTHER,
                policy=forms.fields.ALWAYS,
                other_layout=u"{}<br> Name: {}<br> Agency: {}<br> Phone: {}",
                edit_layout=u"""
                {0}<div id='id_{4}_body'>
                <table>
                <tr><td style="padding:5px">Name *</td><td style="padding:5px">{1}</td></tr>
                <tr><td style="padding:5px">Agency *</td><td style="padding:5px">{2}</td></tr>
                <tr><td style="padding:5px">Phone</td><td style="padding:5px">{3}</td></tr>
                </table>
                </div>
                """
                ),
            "field_officer.list":forms.fields.OtherOptionFieldFactory(Bushfire,"field_officer",("other_field_officer","other_field_officer_agency","other_field_officer_phone"),
                other_option=lambda:User.OTHER,
                policy=forms.fields.ALWAYS,
                other_layout=u"{} (Name: {}  <span style='padding-left:20px'>Agency:</span> {}  <span style='padding-left:20px'>Phone:</span> {})"
                ),
            'linked_bushfires':forms.fields.ListFormFieldFactory("bfrs.forms.bushfire.LinkedBushfireListForm",null_value="No Linked Bushfires")
        }
        labels_config = {
            "q":"Search",
            'dfes_incident_no':'DFES',
            'name':'Name',
            'notifications':"Notifications",
            'report':"report"
        }
        widgets_config = {
            "__default__.view":forms.widgets.TextDisplay(),
            "__default__.edit":forms.widgets.TextInput(),
            "__default__.filter":forms.widgets.TextInput(),
            "notifications.view":forms.widgets.HyperlinkWidget(widget=None,template=notification_template),
            "report.view":forms.widgets.HyperlinkWidget(widget=None,template=report_template),
            "report_status.view":forms.widgets.ChoiceWidgetFactory("reportstatus",Bushfire.REPORT_STATUS_CHOICES)(),
            "created.view": forms.widgets.DatetimeDisplay("%Y-%m-%d %H:%M:%S"),
            "modified.view": forms.widgets.DatetimeDisplay("%Y-%m-%d %H:%M:%S"),
        }

class BushfireBaseForm(BushfireCleanMixin,BushfireConfigMixin,forms.ModelForm):
    class Meta:
        model = Bushfire
        purpose = ('edit','view')

class BushfireSnapshotForm(BushfireBaseForm):
    class Meta:
        purpose = (None,'view')
        model = BushfireSnapshot
        all_fields = ('fire_number','dfes_incident_no','name','job_code',"report_status","district","creator","created","field_officer","duty_officer","other_field_officer","other_field_officer_agency","other_field_officer_phone","linked_bushfires")
        ordered_fields = ('fire_number','dfes_incident_no','name','job_code')

class InitialBushfireEditForm(BushfireBaseForm):
    class Meta:
        all_fields = ('fire_number','dfes_incident_no','name','job_code',"report_status","district","creator","created","field_officer","duty_officer","other_field_officer","other_field_officer_agency","other_field_officer_phone","linked_bushfires")
        ordered_fields = (
                (mark_safe('BUSHFIRE NOTIFICATION <span style="color:red;padding-left:20px">(submit within 30 mins of detection)</span>'),False,False,(
                    ('fire_number','dfes_incident_no'),
                    ('name','job_code')
                )),
        )
        editable_fields = ('name','job_code')

class SubmittedBushfireEditForm(BushfireBaseForm):
    class Meta:
        all_fields = ('fire_number','dfes_incident_no','name','job_code',"report_status","district","creator","created","field_officer","duty_officer","other_field_officer","other_field_officer_agency","other_field_officer_phone","linked_bushfires")
        ordered_fields = ('fire_number','dfes_incident_no','name','job_code')
        editable_fields = ('name','job_code')

class AuthorisedBushfireEditForm(BushfireBaseForm):
    class Meta:
        all_fields = ('fire_number','dfes_incident_no','name','job_code',"report_status","district","creator","created","field_officer","duty_officer","other_field_officer","other_field_officer_agency","other_field_officer_phone","linked_bushfires")
        ordered_fields = ('fire_number','dfes_incident_no','name','job_code')
        editable_fields = ('name','job_code')

class InvalidBushfireEditForm(BushfireBaseForm):
    class Meta:
        all_fields = ('fire_number','dfes_incident_no','name','job_code',"report_status","district","creator","created","field_officer","duty_officer","other_field_officer","other_field_officer_agency","other_field_officer_phone","linked_bushfires")
        ordered_fields = ('fire_number','dfes_incident_no','name','job_code')
        editable_fields = ('name','job_code')



class BushfireBaseListForm(BushfireConfigMixin,forms.ListForm):
    class Meta:
        purpose = (None,('list','view'))
        model = Bushfire
        columns_attrs = {
            "job_code":({"style":"width:80px"},None),
            "notifications":({"style":"width:110px"},None),
            "report":({"style":"width:60px"},None),
            "dfes_incident_no":({"style":"width:70px"},None),
            "fire_number":({"style":"width:130px"},None),
            "modified":({"style":"width:150px"},None),
            "report_status":({"style":"width:150px"},None),
        }

class BushfireListForm(BushfireBaseListForm):
    class Meta:
        all_fields = ('fire_number','dfes_incident_no','name','job_code','notifications',"report","report_status","district","creator","created","field_officer","duty_officer","other_field_officer","other_field_officer_agency","other_field_officer_phone","linked_bushfires")
        ordered_fields = ('fire_number','dfes_incident_no','name','job_code','notifications',"report")
        sortable_fields = ('fire_number','name','job_code','notifications',"report")
        detail_fields = (
            ('report_status','district'),
            ('creator','created'),
            ('field_officer','duty_officer'),
            ('linked_bushfires',),
        )
        columns_attrs = {
                "linked_bushfires":(None,{"colspan":3})
        }

class LinkedBushfireListForm(forms.InnerListFormTableTemplateMixin,BushfireBaseListForm):
    class Meta:
        all_fields = ('fire_number','modified','modifier','report_status','invalid_details')
        table_header = True
        table_classes = {
            "table": "table table-striped table-bordered table-condensed table-hober table-fixed-header innertable"
        }


