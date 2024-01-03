from django.contrib import admin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views
from .views import *
app_name = "rackapp"
urlpatterns = [

    path('api/cust-registration/', CustRegistrationView.as_view(), name='cust-registration-api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/category/', views.category_list),
    path('api/add-to-cart/<int:pro_id>', AddToCartView.as_view(), name='add-to-cart'),
    path('api/products/', ProductView.as_view(), name='products'),
    path("api/mycart/", MyCartView.as_view(), name="mycart"),
    path('api/manage_cart/<int:cp_id>/', ManageCartAPIView.as_view(), name='manage_cart'),
]