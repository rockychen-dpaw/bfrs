from .views import (BushfireListView,InitialBushfireEditView,InitialBushfireSnapshotView,FinalBushfireSnapshotView,SubmittedBushfireEditView,AuthorisedBushfireEditView,InvalidBushfireEditView)

app_name = "bfrs"
urlpatterns = []

urlpatterns.extend(BushfireListView.urlpatterns())
urlpatterns.extend(InitialBushfireEditView.urlpatterns())
urlpatterns.extend(InitialBushfireSnapshotView.urlpatterns())
urlpatterns.extend(SubmittedBushfireEditView.urlpatterns())
urlpatterns.extend(FinalBushfireSnapshotView.urlpatterns())
urlpatterns.extend(AuthorisedBushfireEditView.urlpatterns())
urlpatterns.extend(InvalidBushfireEditView.urlpatterns())
