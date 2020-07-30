from django.urls import path
from backend import *
from api.views import *

urlpatterns = [
    path('', HelloWord.as_view()),
    path('ong', OngAPI.as_view()),
    path('ong/<int:id>', OngAPI.as_view()),
    path('ongs', OngAPIList.as_view()),
    path('need/product', NeedProductAPI.as_view()),
    path('need/product/<int:id>', NeedProductAPI.as_view()),
    path('need/bill', NeedBillAPI.as_view()),
    path('need/bill/<int:id>', NeedBillAPI.as_view()),
    path('tags/', TagAPI.as_view()),
    path('grantor', GrantorAPI.as_view()),   
]