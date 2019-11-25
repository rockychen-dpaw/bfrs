
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
    default_order = ("modified","name","id")
    order_mapping = {
        "modified":("modified","name","id"),
        "-modified":("-modified","name","id"),
        "name":("name","id"),
        "-name":("-name","id"),
        "region":("region","district","burn_id"),
        "-region":("-region","district","burn_id"),
        "district":("district","burn_id"),
        "-district":("-district","burn_id"),
        "year":("financial_year","burn_id"),
        "-year":("-financial_year","burn_id"),
        "modified":("modified","burn_id"),
        "-modified":("-modified","burn_id"),
    }

    @classmethod
    def _get_extra_urlpatterns(cls):
        return [
        ]

    """
    def update_context_data(self,context):
        super().update_context_data(context)
    """

