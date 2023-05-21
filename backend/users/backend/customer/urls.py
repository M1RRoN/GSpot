from django.urls import path, include
from rest_framework.routers import DefaultRouter

from customer.views.v1.customer_registration_view import CustomerRegistrationView
from customer.views.v1.friends import FriendshipViewSet

router = DefaultRouter()
router.register(r'users', FriendshipViewSet)

urlpatterns = [
    path(
        'registration/',
        CustomerRegistrationView.as_view(),
    ),
    path('', include(router.urls)),
]
