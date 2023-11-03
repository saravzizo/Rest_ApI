from .views import GET,POST,PATCH,DELETE, FETCH
from django.urls import path  
  
urlpatterns =    [  
    path('fetch_all/', FETCH.as_view()),  
    path('get/<int:id>/', GET.as_view()),
    path('post/', POST.as_view()),  
    path('patch/<int:id>/', PATCH.as_view()) ,
    path('delete/<int:id>/', DELETE.as_view()) 
]