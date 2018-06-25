from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^signin$', views.signin, name='signin'),
    # url(r'^success$', views.success, name='success'),
    url(r'^users/show/(?P<id>\d+)$', views.show, name='show'),
    url(r'^users/post_message/(?P<id>\d+)$', views.post_message, name='post_message'),
    url(r'^users/post_comment/(?P<indi_id>\d+)/(?P<msg_id>\d+)$', views.post_comment, name='post_comment'),
    url(r'^dashboard/admin$', views.dashadmin, name='dashadmin'),
    url(r'^users/new$', views.add_new, name='add_new'),
    url(r'^users/edit/(?P<id>\d+)$', views.admin_edit_user_page, name='admin_edit_user_page'),
    url(r'^users/(?P<id>\d+)/admin_edit_user_info$', views.admin_edit_user_info, name='admin_edit_user_info'),
    url(r'^users/(?P<id>\d+)/admin_edit_user_pwd$', views.admin_edit_user_pwd, name='admin_edit_user_pwd'),
    url(r'^users/edit$', views.edit_user_page, name='edit_user_page'),
    url(r'^users/(?P<id>\d+)/edit_user_info$', views.edit_user_info, name='edit_user_info'),
    url(r'^users/(?P<id>\d+)/edit_user_pwd$', views.edit_user_pwd, name='edit_user_pwd'),
    url(r'^users/(?P<id>\d+)/edit_user_desc$', views.edit_user_desc, name='edit_user_desc'),
    url(r'^dashboard$', views.dash, name='dash'),
    url(r'^logout$', views.logout, name='logout')
]
