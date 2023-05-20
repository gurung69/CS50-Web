from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name='create'),
    path('listing/<int:id>', views.view, name='view'),
    path('listing/<int:id>/tg_wl', views.toggle_watchlist, name='tg_wl'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('category', views.categories, name='category'),
    path('category/<str:category>', views.category_listing, name='category_listing'),
    path('listing/<int:id>/comment', views.comment, name="comment"),
    path('listing/<int:id>/close', views.close, name="close"),
    path('bids', views.bids, name='bids'),
    path('selling', views.selling, name='selling')
]
