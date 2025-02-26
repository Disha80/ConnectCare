from django.db import models
from django.db.models import Q

class UserRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    age = models.IntegerField()
    interests = models.TextField(blank=True, null=True)
    medical_details = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)  # Ensuring unique usernames
    password = models.CharField(max_length=255)  # Store password as hashed string

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_friends(self):
        friends1 = Friendship.objects.filter(user1=self).values_list('user2', flat=True)
        friends2 = Friendship.objects.filter(user2=self).values_list('user1', flat=True)
        return UserRegistration.objects.filter(id__in=list(friends1) + list(friends2))
    
    def is_friends_with(self, other_user):
        return Friendship.objects.filter(
            (Q(user1=self, user2=other_user) | Q(user1=other_user, user2=self))
        ).exists()
    
    def has_friend_request_from(self, other_user):
        return FriendRequest.objects.filter(
            sender=other_user, 
            receiver=self, 
            status='pending'
        ).exists()
    
    def remove_friend(self, other_user):
        # Remove friendship in both directions
        Friendship.objects.filter(
            Q(user1=self, user2=other_user) | 
            Q(user1=other_user, user2=self)
        ).delete()
        
        # Optional: You might want to delete any related friend requests
        FriendRequest.objects.filter(
            Q(sender=self, receiver=other_user) | 
            Q(sender=other_user, receiver=self)
        ).delete()

class NGO(models.Model):
    organization_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=10)
    organization_address = models.TextField()
    registration_number = models.CharField(max_length=100)
    establishment_year = models.PositiveIntegerField()
    area_of_focus = models.TextField()
    additional_comments = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)  # Ensuring unique usernames for NGOs
    password = models.CharField(max_length=255)  # Store password as hashed string

    def __str__(self):
        return self.organization_name


class EventRegistration(models.Model):
    EVENTS = [
        ('yoga', 'Weekly Yoga Session'),
        ('tech', 'Tech for Seniors'),
        ('music', 'Music Therapy'),
        ('gardening', 'Gardening Club'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    age = models.IntegerField()
    event = models.CharField(max_length=20, choices=EVENTS)
    
    # New field for the specific date
    specific_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event} on {self.specific_date}"


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()  # This will store the address
    availability = models.CharField(max_length=50)
    message = models.TextField()  # This will store the message
    skills = models.TextField()  # New field
    work = models.TextField()    # New field
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
 
class HelpRequest(models.Model):
    HELP_TYPES = [
        ('financial', 'Financial Assistance'),
        ('medical', 'Medical Care'),
        ('housing', 'Housing Support'),
        ('daily', 'Daily Care Support'),
        ('emotional', 'Emotional Support'),
        ('other', 'Other')
    ]
    
    URGENCY_LEVELS = [
        ('immediate', 'Immediate (Within 24 hours)'),
        ('urgent', 'Urgent (Within a week)'),
        ('normal', 'Normal (Within a month)')
    ]
    
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    contact = models.CharField(max_length=15)
    location = models.TextField()
    help_type = models.CharField(max_length=20, choices=HELP_TYPES)
    description = models.TextField()
    urgency = models.CharField(max_length=20, choices=URGENCY_LEVELS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest requests first
    
    def __str__(self):
        return f"{self.full_name} - {self.help_type} ({self.urgency})"





class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    
    sender = models.ForeignKey(UserRegistration, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserRegistration, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} - {self.status}"

class Friendship(models.Model):
    user1 = models.ForeignKey(UserRegistration, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserRegistration, related_name='friends2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username}"