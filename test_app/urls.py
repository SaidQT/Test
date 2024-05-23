from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),	
    path('process',views.create),
    path('dashboard',views.dash),
    path('process2', views.login),
    path('logout', views.reset),
    path('trips/new', views.add_trip),
    path('create',views.trip),
    path('trips/edit/<int:id>', views.edit),
    path('edit/<int:id>',views.process_edit),
    path('trips/<int:id>',views.show),
    path('delete/<int:id>', views.delete),
    path('trips/mytrips', views.trips),
    path('cancel/<int:x>/<int:y>', views.cancel),
    path('join/<int:x>/<int:y>', views.join),
]