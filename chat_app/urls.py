from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login',user_login,name='login'),
    path('get_chat_messages/', get_chat_messages, name='get_chat_messages'),
    path('send_chat_messages/', send_chat_messages, name='send_chat_messages'),
    path('logout',logout_view,name='logout'),
    path('view_page', view_page, name='view_page'),
    path('re', re, name='re'),
    path('publish_message/', publish_message, name='publish_message'),
]
