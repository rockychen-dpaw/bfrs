from django.conf.urls import include, url
from bfrs.models import Bushfire
from bfrs import views

urlpatterns = [
    url(r'^create/$', views.BushfireUpdateView.as_view(), name='bushfire_create'),
    url(r'^initial/(?P<pk>\d+)/$', views.BushfireUpdateView.as_view(), name='bushfire_initial'),
    url(r'^initial/snapshot/(?P<pk>\d+)/$', views.BushfireInitialSnapshotView.as_view(), name='initial_snapshot'),
    url(r'^final/(?P<pk>\d+)/$', views.BushfireUpdateView.as_view(), name='bushfire_final'),
    url(r'^final/snapshot/(?P<pk>\d+)/$', views.BushfireFinalSnapshotView.as_view(), name='final_snapshot'),
#    url(r'^export/$', views.BushfireView.as_view(), name='export'),

    url(r'^history/(?P<pk>\d+)/$', views.BushfireHistoryCompareView.as_view(), name='bushfire_history'),
    url(r'report/$', views.ReportView.as_view(), name='bushfire_report'),
    url(r'^bushfire/(?P<bushfireid>\d+)/document/$', views.BushfireDocumentListView.as_view(), name='bushfire_document_list'),
    url(r'^bushfire/(?P<bushfireid>\d+)/document/upload/$', views.BushfireDocumentUploadView.as_view(), name='bushfire_document_upload'),
    url(r'^document/(?P<pk>\d+)/download/$', views.DocumentDownloadView.as_view(), name='document_download'),
    url(r'^document/(?P<pk>\d+)$', views.DocumentUpdateView.as_view(), name='document_update'),
    url(r'^document/(?P<pk>\d+)/edit/$', views.DocumentUpdateView.as_view(), name='document_edit'),
    url(r'^document/(?P<pk>\d+)/view/$', views.DocumentDetailView.as_view(), name='document_view'),
    url(r'^document/(?P<pk>\d+)/delete/$', views.DocumentDeleteView.as_view(), name='document_delete'),
    url(r'^document/(?P<pk>\d+)/archive/$', views.DocumentArchiveView.as_view(), name='document_archive'),
    url(r'^document/(?P<pk>\d+)/unarchive/$', views.DocumentUnarchiveView.as_view(), name='document_unarchive'),
    url(r'^documentcategory/$', views.DocumentCategoryListView.as_view(), name='documentcategory_list'),
    url(r'^documentcategory/create/$', views.DocumentCategoryCreateView.as_view(), name='documentcategory_create'),
    url(r'^documentcategory/(?P<pk>\d+)/$', views.DocumentCategoryUpdateView.as_view(), name='documentcategory_update'),
    url(r'^documentcategory/(?P<pk>\d+)/detail/$', views.DocumentCategoryDetailView.as_view(), name='documentcategory_detail')

]

