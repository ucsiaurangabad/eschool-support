from django.conf.urls.static import static 
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name = "index"),
    path('makepayment/',views.makePayment, name="makepayment"),
    path('handlepayment/',views.handlepayment, name="handlepayment"),

]
