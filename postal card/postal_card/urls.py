from django.urls import re_path

from postal_card import views

urlpatterns = [
    re_path('^$', views.introduce, name='introduce_company')
]