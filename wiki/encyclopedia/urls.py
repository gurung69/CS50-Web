from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name='wiki'),
    path("create", views.create_page, name='create'),
    path('edit/<str:title>', views.edit_page, name='edit'),
    path('random', views.random_page, name='random')
]
