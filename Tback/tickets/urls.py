from django.urls import path
from . import views
from . import purchase_views

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
    
    # Purchase endpoints
    path('purchase/', purchase_views.create_ticket_purchase, name='create-ticket-purchase'),
    path('purchase/direct/', purchase_views.create_ticket_purchase, name='create-ticket-purchase-direct'),
    path('purchase/<uuid:purchase_id>/', purchase_views.ticket_purchase_details, name='ticket-purchase-details'),
    path('purchase/<uuid:purchase_id>/status/', purchase_views.ticket_purchase_status, name='ticket-purchase-status'),
    path('purchase/<uuid:purchase_id>/complete/', purchase_views.complete_ticket_purchase, name='complete-ticket-purchase'),
    path('purchase/<uuid:purchase_id>/simulate-payment/', purchase_views.simulate_ticket_payment, name='simulate-ticket-purchase'),
    path('purchases/', purchase_views.user_ticket_purchases, name='user-ticket-purchases'),
    path('debug/purchases/', purchase_views.debug_ticket_purchases, name='debug-ticket-purchases'),
]