from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

import django_mvc.views
from django_mvc.signals import django_inited

urlpatterns = [
    path('docs/', include('django.contrib.admindocs.urls')),
    path('', include('django.contrib.auth.urls'))
]


import bfrs.urls

handler500 = django_mvc.views.handler500
handler404 = django_mvc.views.handler404

def home_view(request):
    if request.user.is_authenticated():
        return redirect('main')
    else:
        return redirect('login')

urlpatterns = urlpatterns + [
    path("admin/",admin.site.urls),
    path("chaining/",include('smart_selects.urls')),
    path("bfrs/",include(bfrs.urls,namespace=bfrs.urls.app_name)),

    path(r'^$', home_view, name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

django_inited.send(sender="urls")
