
from django_mvc import views

from ..models import (Bushfire,)
from ..forms import (BushfireListForm,)

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

