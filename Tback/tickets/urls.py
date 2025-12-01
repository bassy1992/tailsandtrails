from django.urls import path
from . import views, purchase_views

app_name = 'tickets'

urlpatterns = [
    # Categories and Venues
    path('categories/', views.TicketCategoryListView.as_view(), name='category-list'),
    path('venues/', views.VenueListView.as_view(), name='venue-list'),
    path('venues/<slug:slug>/', views.VenueDetailView.as_view(), name='venue-detail'),
    
    # Tickets
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('featured/', views.FeaturedTicketsView.as_view(), name='featured-tickets'),
    path('popular/', views.PopularTicketsView.as_view(), name='popular-tickets'),
    path('upcoming/', views.UpcomingTicketsView.as_view(), name='upcoming-tickets'),
    path('<slug:slug>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    
    # Purchases (Original)
    path('purchase/create/', views.TicketPurchaseCreateView.as_view(), name='purchase-create'),
    path('purchases/', views.TicketPurchaseListView.as_view(), name='purchase-list'),
    path('purchases/<uuid:purchase_id>/', views.TicketPurchaseDetailView.as_view(), name='purchase-detail'),
    
    # Direct Ticket Purchases (Separate from Payment model)
    path('purchase/direct/', purchase_views.create_ticket_purchase, name='direct-purchase-create'),
    path('purchase/<uuid:purchase_id>/status/', purchase_views.ticket_purchase_status, name='purchase-status'),
    path('purchase/<uuid:purchase_id>/complete/', purchase_views.complete_ticket_purchase, name='purchase-complete'),
    path('purchase/<uuid:purchase_id>/details/', purchase_views.ticket_purchase_details, name='purchase-details'),
    path('purchase/<uuid:purchase_id>/simulate-payment/', purchase_views.simulate_ticket_payment, name='simulate-payment'),
    path('purchases/user/', purchase_views.user_ticket_purchases, name='user-purchases'),
    path('purchases/debug/', purchase_views.debug_ticket_purchases, name='debug-purchases'),
    
    # Ticket Codes
    path('codes/<str:code>/', views.TicketCodeValidateView.as_view(), name='code-validate'),
    path('codes/<str:code>/use/', views.use_ticket_code, name='code-use'),
    
    # Reviews
    path('<int:ticket_id>/reviews/', views.TicketReviewListView.as_view(), name='ticket-reviews'),
    path('reviews/create/', views.TicketReviewCreateView.as_view(), name='review-create'),
    path('reviews/my/', views.UserTicketReviewsView.as_view(), name='user-reviews'),
    
    # Promo Codes
    path('promo/validate/', views.validate_promo_code, name='promo-validate'),
    
    # Statistics
    path('stats/', views.ticket_stats, name='ticket-stats'),
    path('stats/user/', views.user_ticket_stats, name='user-ticket-stats'),
]