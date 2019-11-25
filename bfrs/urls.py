from .views import (BushfireListView,)

app_name = "bfrs"
urlpatterns = []

urlpatterns.extend(BushfireListView.urlpatterns())
