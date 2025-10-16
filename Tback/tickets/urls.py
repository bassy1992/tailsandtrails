from django.urls import path
from . import views

urlpatterns = [
    # Ticket endpoints
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('<slug:slug>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('categories/', views.TicketCategoryListView.as_view(), name='ticket-categories'),
    
    # Add-on endpoints
    path('<int:ticket_id>/addons/', views.get_ticket_addons, name='ticket-addons'),
    path('calculate-total/', views.calculate_booking_total, name='calculate-booking-total'),
    path('book-with-addons/', views.create_booking_with_addons, name='create-booking-with-addons'),
    path('booking/<str:booking_reference>/', views.get_booking_details, name='booking-details'),
]