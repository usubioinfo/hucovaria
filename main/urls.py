from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
	path('', views.home, name='home'),
	path('search/', views.search, name='search'),
	path('datasets/', views.datasets, name='datasets'),
	path('tmp/', views.makeQuery, name='query'),
	path('help/', views.help, name='help'),
	path('results/<str:result_id>/table/', views.TableView.as_view(), name='table'),
	path('results/<str:result_id>/network/', views.network, name='network'),
]

# urlpatterns = []
