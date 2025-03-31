from django.db import models
from datetime import date


class FoodCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Many-to-Many relationship for multiple categories
    categories = models.ManyToManyField(FoodCategory, related_name="items")

    image = models.ImageField(upload_to="items/")

    # New fields
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    is_deliverable = models.BooleanField(
        default=True, help_text="Is available for delivery?"
    )
    is_veg = models.BooleanField(default=True, help_text="Is the item vegetarian?")

    def __str__(self):
        return self.name


class AboutUs(models.Model):
    description = models.TextField(blank=False)

    def __str__(self):
        return "About Us"


class Feedback(models.Model):
    user_name = models.CharField(max_length=15)
    description = models.TextField(blank=False)
    rating = models.IntegerField()
    image = models.ImageField(upload_to="Media/feedback/", blank=True)

    def __str__(self):
        return self.user_name


class BookTable(models.Model):
    name = models.CharField(max_length=15)
    phone_number = models.CharField(
        max_length=10
    )
    email = models.EmailField()
    total_person = models.IntegerField()
    booking_date = models.DateField()

    def __str__(self):
        return self.name


#Coupon Model
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, help_text="Brief description of the coupon")
    
    # Discount type: Percentage or Flat amount
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('flat', 'Flat Amount'),
    ]
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        """Check if the coupon is valid"""
        today = date.today()
        return self.is_active and self.valid_from <= today <= self.valid_to

    def __str__(self):
        return f"{self.code} - {self.discount_type} - {self.discount_value}"


# Offer Model
class Offer(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    # ForeignKey relationship to apply offer to multiple items
    items = models.ManyToManyField('Items', related_name='offers')
    
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        """Check if the offer is valid"""
        today = date.today()
        return self.is_active and self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.name} - {self.discount_percentage}%"