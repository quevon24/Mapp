from django.conf.urls import url
from django.contrib import admin
from administrar import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'dental.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', views.home, name='home'),
    url(r'^login/$',login, {'template_name': 'loginform.html'}),
    url(r'^logout/$',logout, {'next_page': '/'}),
    url(r'^registrar/$',views.registrar, name='registrar'),
]
