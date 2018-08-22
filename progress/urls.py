from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^show', views.trial, name='show'), #исправлена вьюшка на show1
#url(r'^trial', views.trial, name='trial'), #проба
url(r'^add_target', views.add_target, name='add_target'),
#url(r'^error', views.add_target, name='add_target'),
url(r'^edit_target/(.+)', views.edit_target, name='edit_target'),
#url(r'^edit_progress/(.+)', views.edit_progress, name='edit_progress'),
url(r'^progress', views.progress, name='progress'),
url(r'^delete_target/(.+)', views.delete_target, name='delete_target'),
url(r'^register/$', views.register, name='register'),
url(r'^login/$', views.user_login, name='login'),
url(r'^logout/$', views.user_logout, name='login'),

]

