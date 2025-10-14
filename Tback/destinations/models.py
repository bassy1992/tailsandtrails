from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Destination(models.Model):
    DURATION_CHOICES = [
        ('1_day', '1 Day'),
        ('2_days', '2 Days'),
        ('3_days', '3 Days'),
        ('4_days', '4 Days'),
        ('5_days', '5 Days'),
        ('6_days', '6 Days'),
        ('7_days', '7 Days'),
        ('7_plus_days', '7+ Days'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    max_group_size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    reviews_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='destinations')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['rating']),
            models.Index(fields=['is_featured']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def duration_display(self):
        return dict(self.DURATION_CHOICES).get(self.duration, self.duration)
    
    @property
    def price_category(self):
        if self.price is None:
            return 'unknown'
        if self.price < 300:
            return 'budget'
        elif self.price <= 600:
            return 'mid'
        else:
            return 'luxury'

class DestinationHighlight(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='highlights')
    highlight = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['destination', 'highlight']
    
    def __str__(self):
        return f"{self.destination.name} - {self.highlight}"

class DestinationInclude(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='includes')
    item = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['destination', 'item']
    
    def __str__(self):
        return f"{self.destination.name} - {self.item}"

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.destination.name} - Image {self.id}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['destination', 'user']
        indexes = [
            models.Index(fields=['destination', 'is_active']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.first_name} - {self.destination.name} ({self.rating} stars)"

class AddOnCategory(models.Model):
    CATEGORY_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('transport', 'Transport'),
        ('meals', 'Meals'),
        ('medical', 'Medical & Insurance'),
        ('experience', 'Experience'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Add-on Categories"
    
    def __str__(self):
        return self.display_name

class AddOnOption(models.Model):
    PRICING_TYPE_CHOICES = [
        ('per_person', 'Per Person'),
        ('per_group', 'Per Group'),
        ('fixed', 'Fixed Price'),
    ]
    
    category = models.ForeignKey(AddOnCategory, on_delete=models.CASCADE, related_name='options')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='addon_options')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE_CHOICES, default='per_person')
    is_default = models.BooleanField(default=False, help_text="Is this the default/included option?")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order', 'name']
        unique_together = ['category', 'destination', 'name']
    
    def __str__(self):
        return f"{self.destination.name} - {self.category.display_name}: {self.name}"
    
    @property
    def price_display(self):
        if self.price == 0:
            return "Included"
        elif self.pricing_type == 'per_person':
            return f"+GH₵{self.price} per person"
        elif self.pricing_type == 'per_group':
            return f"+GH₵{self.price} per group"
        else:
            return f"+GH₵{self.price}"

class ExperienceAddOn(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='experience_addons')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., '2 hours', 'Half day'")
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        unique_together = ['destination', 'name']
    
    def __str__(self):
        return f"{self.destination.name} - {self.name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    BOOKING_TYPE_CHOICES = [
        ('destination', 'Destination Tour'),
        ('ticket', 'Event Ticket'),
    ]
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='bookings')
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='destination')
    participants = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['booking_date']),
            models.Index(fields=['status']),
            models.Index(fields=['booking_type']),
            models.Index(fields=['booking_type', 'status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import uuid
            self.booking_reference = f"TN{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_destination_booking(self):
        return self.booking_type == 'destination'
    
    @property
    def is_ticket_booking(self):
        return self.booking_type == 'ticket'
    
    def __str__(self):
        booking_type_display = dict(self.BOOKING_TYPE_CHOICES).get(self.booking_type, self.booking_type)
        return f"{self.booking_reference} - {self.destination.name} ({booking_type_display})"

class BookingAddOn(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='selected_addons')
    addon_option = models.ForeignKey(AddOnOption, on_delete=models.CASCADE, blank=True, null=True)
    experience_addon = models.ForeignKey(ExperienceAddOn, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [
            ['booking', 'addon_option'],
            ['booking', 'experience_addon']
        ]
    
    def __str__(self):
        if self.addon_option:
            return f"{self.booking.booking_reference} - {self.addon_option.name}"
        elif self.experience_addon:
            return f"{self.booking.booking_reference} - {self.experience_addon.name}"
        return f"{self.booking.booking_reference} - Unknown Add-on"