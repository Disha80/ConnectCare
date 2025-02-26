from django.db import models

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