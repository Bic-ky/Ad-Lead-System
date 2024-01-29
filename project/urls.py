from django.urls import path 
from . import views

urlpatterns = [
   path('addlead/', views.add_lead , name='add_lead' ),
   path('addcompany/', views.add_company , name='add_company' ),
   path('addnewspaper/', views.add_newspaper , name='add_newspaper' ),



    
]