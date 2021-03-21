from . import views
from django.urls import path

app_name='woodshophome'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('forgotpass/',views.forgot_password, name='forgot_password' ),
    path('capturepass/',views.capture_password, name='capture-password'),
    path('signup/',views.signup, name="signup"),
    path('logout/',views.user_logout,name='logout'),
    path('placeorder/',views.place_order,name='place_order'),
    path('',views.home,name='woodshophome-home'),
    path('checkstatus/',views.order_status,name='woodshophome-order_status'),
    path('checkstatus/<int:id>',views.order_status_details,name='woodshophome-orderorder_status_details_status'),
]
