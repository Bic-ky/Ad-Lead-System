from django.urls import path 
from . import views

urlpatterns = [
   path('addlead/', views.add_lead , name='add_lead' ),
   path('addcompany/', views.add_company , name='add_company' ),
   path('addnewspaper/', views.add_newspaper , name='add_newspaper' ),
   path('company/',views.company, name='company'),
   path('get_districts/', views.get_districts, name='get_districts'),
   path('get_municipalities/', views.get_municipalities, name='get_municipalities'),
   path('company/profile/<int:company_id>/', views.company_profile, name='company_profile'),
    
]