from django.http import (HttpResponseRedirect,)
from django.urls import (reverse,)

from django_mvc import views

from ..models import (Bushfire,BushfireSnapshot)
from ..forms import (BushfireListForm,InitialBushfireEditForm,BushfireSnapshotForm,SubmittedBushfireEditForm,AuthorisedBushfireEditForm,InvalidBushfireEditForm)

class BushfireListView(views.ListView):
    title = "Regional Overview"
    listform_class = BushfireListForm
    #filterform_class = PrescriptionFilterForm
    #filter_class = PrescriptionFilter
    model = Bushfire
    paginate_by=50
    default_order = ("modified","name","fire_number")
    order_mapping = {
        "modified":("modified","name","fire_number"),
        "-modified":("-modified","-name","-fire_number"),
        "name":("name","fire_number"),
        "-name":("-name","-fire_number"),
        "notifications":("report_status","modified","name","fire_number"),
        "-notifications":("-report_status","-modified","-name","-fire_number"),
        "report":("report_status","modified","name","fire_number"),
        "-report":("-report_status","-modified","-name","-fire_number"),
        "region":("region","district","fire_number"),
        "-region":("-region","-district","-fire_number"),
        "district":("district","fire_number"),
        "-district":("-district","-fire_number"),
        "year":("financial_year","fire_number"),
        "-year":("-financial_year","-fire_number"),
    }

    @classmethod
    def _get_extra_urlpatterns(cls):
        return [
        ]

    """
    def update_context_data(self,context):
        super().update_context_data(context)
    """

class InitialBushfireSnapshotView(views.DetailView):
    title = "Initial Bushfire Report Snapshot"
    model = Bushfire
    form_class = BushfireSnapshotForm
    urlpattern = 'bushfire/<int:pk>/snapshot/initial/'
    urlname = "initial_bushfire_snapshot"

    def get_object(self,*args,**kwargs):
        bushfire = super().get_object(*args,**kwargs)
        if bushfire.report_status == Bushfire.STATUS_INITIAL:
            raise views.HttpResponseRedirectException(HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":bushfire.id})))
        elif bushfire.report_status > Bushfire.STATUS_REVIEWED:
            raise views.HttpResponseRedirectException(HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":bushfire.id})))
        else:
            snapshot = bushfire.initial_snapshot
            if not snapshot:
                raise Exception("The initial snapshot of the bushfire Report({}) is missing.".format(bushfire.fire_number))

            return snapshot
                
class InitialBushfireEditView(views.EditView):
    title = "Edit Initial Bushfire Report"
    model = Bushfire
    form_class = InitialBushfireEditForm
    urlpattern = 'bushfire/<int:pk>/initial/'
    urlname = "initial_bushfire_update"

    def get(self,*args,**kwargs):
        resp = super().get(*args,**kwargs)
        if self.object.report_status != Bushfire.STATUS_INITIAL and self.object.report_status <= Bushfire.STATUS_REVIEWED:
            return HttpResponseRedirect(reverse("bfrs:initial_bushfire_snapshot",kwargs={"pk":self.object.id}))
        elif self.object.report_status > Bushfire.STATUS_REVIEWED:
            return resp
        else:
            return resp
            
class FinalBushfireSnapshotView(views.DetailView):
    model = Bushfire
    form_class = BushfireSnapshotForm
    urlpattern = 'bushfire/<int:pk>/snapshot/final/'
    urlname = "final_bushfire_snapshot"

    @property
    def title(self):
        if self.object.report_status == Bushfire.STATUS_FINAL_AUTHORISED:
            return "Authorised Bushfire Report Snapshot"
        elif self.object.report_status == Bushfire.STATUS_REVIEWED:
            return "Reviewed Bushfire Report Snapshot"
        else:
            return "Bushfire Report Snapshot"

    def get_object(self,*args,**kwargs):
        bushfire = super().get_object(*args,**kwargs)
        if bushfire.report_status == Bushfire.STATUS_INITIAL:
            raise views.HttpResponseRedirectException(HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":bushfire.id})))
        elif bushfire.report_status > Bushfire.STATUS_REVIEWED:
            raise views.HttpResponseRedirectException(HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":bushfire.id})))
        else:
            snapshot = bushfire.final_snapshot
            if not snapshot:
                raise Exception("The final snapshot of the bushfire Report({}) is missing.".format(bushfire.fire_number))

            return snapshot
                
class SubmittedBushfireEditView(views.EditView):
    title = "Edit Submitted Bushfire Report"
    model = Bushfire
    form_class = SubmittedBushfireEditForm
    urlpattern = 'bushfire/<int:pk>/submitted/'
    urlname = "submitted_bushfire_update"

    def get(self,*args,**kwargs):
        resp = super().get(*args,**kwargs)
        if self.object.report_status == Bushfire.STATUS_INITIAL:
            return HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":self.object.id}))
        elif self.object.report_status > Bushfire.STATUS_INITIAL_AUTHORISED and self.object.report_status <= Bushfire.STATUS_REVIEWED:
            return HttpResponseRedirect(reverse("bfrs:final_bushfire_snapshot",kwargs={"pk":self.object.id}))
        elif self.object.report_status > Bushfire.STATUS_REVIEWED:
            return resp
        else:
            return resp
            
class AuthorisedBushfireEditView(views.EditView):
    title = "Edit Authorised Bushfire Report"
    model = Bushfire
    form_class = AuthorisedBushfireEditForm
    urlpattern = 'bushfire/<int:pk>/authorised/'
    urlname = "authorised_bushfire_update"

    def get(self,*args,**kwargs):
        resp = super().get(*args,**kwargs)
        if self.object.report_status == Bushfire.STATUS_INITIAL:
            return HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":self.object.id}))
        elif self.object.report_status == Bushfire.STATUS_INITIAL_AUTHORISED:
            return HttpResponseRedirect(reverse("bfrs:submitted_bushfire_update",kwargs={"pk":self.object.id}))
        elif self.object.report_status > Bushfire.STATUS_FINAL_AUTHORISED and self.object.report_status <= Bushfire.STATUS_REVIEWED:
            return HttpResponseRedirect(reverse("bfrs:final_bushfire_snapshot",kwargs={"pk":self.object.id}))
        elif self.object.report_status > Bushfire.STATUS_REVIEWED:
            return resp
        else:
            return resp
            
class InvalidBushfireEditView(views.EditView):
    model = Bushfire
    form_class = InvalidBushfireEditForm
    urlpattern = 'bushfire/<int:pk>/invalid/'
    urlname = "invalid_bushfire_update"

    @property
    def title(self):
        if self.object.report_status == Bushfire.STATUS_INVALIDATED:
            return "Edit Invalidated Bushfire Report"
        elif self.object.report_status == Bushfire.STATUS_MERGED:
            return "Edit Merged Bushfire Report"
        elif self.object.report_status == Bushfire.STATUS_DUPLICATED:
            return "Edit Duplicated Bushfire Report"
        else:
            return "Edit Bushfire Report"

    def get(self,*args,**kwargs):
        resp = super().get(*args,**kwargs)
        if self.object.report_status == Bushfire.STATUS_INITIAL:
            return HttpResponseRedirect(reverse("bfrs:initial_bushfire_update",kwargs={"pk":self.object.id}))
        elif self.object.report_status == Bushfire.STATUS_INITIAL_AUTHORISED:
            return HttpResponseRedirect(reverse("bfrs:submitted_bushfire_update",kwargs={"pk":self.object.id}))
        elif self.object.report_status > Bushfire.STATUS_INITIAL_AUTHORISED and self.object.report_status <= Bushfire.STATUS_REVIEWED:
            return HttpResponseRedirect(reverse("bfrs:final_bushfire_snapshot",kwargs={"pk":self.object.id}))
        else:
            return resp
            
