from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    Title=models.TextField()
    
    def __str__(self):
        return self.Title
    
    
class Vehicle(models.Model):
    price_choices=[('hour','per hour'),('half_day','per half_day'),('day','per day')]
    type_choices=[('Bicycle','Bicycle'),('Bike','Bike'),('Car','Car'),('Van','Van')]
    image=models.ImageField(upload_to='vehicles/')
    title=models.TextField()
    type=models.TextField(max_length=10,choices=type_choices)
    location = models.CharField(max_length=200, default='Chennai')
    price=models.IntegerField() 
    price_type=models.CharField(max_length=10,choices=price_choices,default='hour')
    description=models.TextField(max_length=5000,default='''Our rental vehicles are well-maintained, reliable, and designed to give you a smooth and comfortable journey. 
                                 Whether you need a vehicle for daily travel, business trips, or weekend getaways, we offer flexible rental plans at affordable prices.
                                 All vehicles are regularly serviced to ensure safety and performance.''')
    
    
    def __str__(self):
        return self.title
  


    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    
    


class Rental(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rentals'
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='rentals'
    )
    delivery_address = models.TextField()
    pickup_time = models.DateTimeField()
    return_time = models.DateTimeField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle}"
    
    def update_status(self):
        """Automatically update status based on current time"""
        # Don't change cancelled or completed rentals
        if self.status == 'cancelled' or self.status == 'completed':
            return
        
        now = timezone.now()
        
        if now < self.pickup_time:
            # Before pickup time - rental is pending
            self.status = 'pending'
        elif self.pickup_time <= now < self.return_time:
            # Between pickup and return time - rental is active
            self.status = 'active'
        elif now >= self.return_time:
            # After return time - rental is completed
            self.status = 'completed'
        
        self.save()