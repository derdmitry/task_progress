from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^add_target', views.add_target, name='add_target'),
url(r'^edit_target/(.+)', views.edit_target, name='edit_target'),
url(r'^progress', views.progress, name='progress'),
url(r'^delete_target/(.+)', views.delete_target, name='delete_target'),
url(r'^register/$', views.register, name='register'),
url(r'^login/$', views.user_login, name='login'),
url(r'^logout/$', views.user_logout, name='logout'),

]

