from django.urls import path
from .import views


app_name = 'library'
urlpatterns = [
    path('', views.index, name='home'),
    path('record', views.record, name='record'),
    path('record_list', views.record_list, name='record_list'),
    path("record/detail/<uuid:id>/", views.record_detail, name="record_detail"),
    path("record/delete/<uuid:id>/", views.delete_record, name="delete_record"),
    path("player/<uuid:id>/", views.play_book, name="play_book"),
    path('search', views.search, name='search'),
    path('search/delete/<uuid:id>/', views.delete_search, name='delete_search'),
    path('search_result/<uuid:id>/', views.search_result, name='search_result'),
    path('previous_search', views.previous_search, name='previous_search'),
    path('books', views.books, name='books'),
    path('search_bar', views.search_bar, name='search_bar'),
    path('upload', views.add_book, name='add_book'),
    path('Error/<str:e>', views.error, name='error'),
]
