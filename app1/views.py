import json
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, NGORegistrationForm, EventRegistrationForm
from .models import Volunteer, UserRegistration, NGO, Contact
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import HelpRequest
from django.http import HttpResponseRedirect
from functools import wraps
from .models import FriendRequest, Friendship
from functools import wraps
from django.http import HttpResponseRedirect
from django.db.models import Q
# Root/homepage view
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import UserRegistration, FriendRequest, Friendship
from django.db.utils import IntegrityError


def index(request):
    return render(request, 'app1/index.html')

# User login view with plain text password
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            try:
                user = UserRegistration.objects.get(username=username)
                
                # Plain text password comparison
                if user.password == password:
                    request.session['user_id'] = user.id
                    return JsonResponse({
                        'success': True,
                        'redirect_url': '/'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid password'
                    })
                    
            except UserRegistration.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Username not found'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format'
            })
            
    return render(request, 'app1/UserLogin.html')

# User registration view
def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save with plain text password
            form.save()
            messages.success(request, "User registered successfully!")
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'app1/Registration.html', {'form': form})

# NGO registration view
def ngo_registration(request):
    if request.method == 'POST':
        form = NGORegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization registered successfully!")
            return redirect('index')
    else:
        form = NGORegistrationForm()
    return render(request, 'app1/NGORegister.html', {'form': form})

# Volunteer form view
def volunteer_form_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        availability = request.POST.get("availability")
        message = request.POST.get("message")
        skills = request.POST.get("skills")
        work = request.POST.get("work")

        Volunteer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            availability=availability,
            message=message,
            skills=skills,
            work=work
        )

        return redirect('index')

    volunteers = Volunteer.objects.all()
    paginator = Paginator(volunteers, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "app1/index.html", {"volunteers": page_obj})

# Volunteers list view
def volunteers_list_view(request):
    volunteers = Volunteer.objects.all()
    paginator = Paginator(volunteers, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "app1/volunteers_list.html", {"volunteers": page_obj})

# Contact form view
def contact_form_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('index')

    return render(request, "app1/index.html")

# Event registration view
def event_register(request):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EventRegistrationForm()
    return render(request, 'app1/EventRegister.html', {'form': form})

def ngo_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            try:
                ngo = NGO.objects.get(username=username)
                
                # Plain text password comparison for NGO
                if ngo.password == password:
                    request.session['ngo_id'] = ngo.id
                    return JsonResponse({
                        'success': True,
                        'redirect_url': '/'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid password'
                    })
                    
            except NGO.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Organization username not found'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format'
            })
            
    return render(request, 'app1/NGOLogin.html')

def health_tracker(request):
    return render(request, 'app1/health_tracker.html')  # Assuming the page is saved as health_tracker.html

def profile(request):
    # Get session IDs
    user_id = request.session.get('user_id')
    ngo_id = request.session.get('ngo_id')
    
    # Clear both contexts initially
    context = {}
    
    if ngo_id:
        # If NGO is logged in, fetch NGO data
        try:
            ngo_data = NGO.objects.get(id=ngo_id)
            context = {
                'is_ngo': True,
                'organization_name': ngo_data.organization_name,
                'contact_person': ngo_data.contact_person,
                'contact_email': ngo_data.contact_email,
                'contact_number': ngo_data.contact_number,
                'organization_address': ngo_data.organization_address,
                'area_of_focus': ngo_data.area_of_focus
            }
        except NGO.DoesNotExist:
            return redirect('ngo_login')
        return render(request, 'app1/profile.html', context)
        
    elif user_id:
        # If user is logged in, fetch user data
        try:
            user_data = UserRegistration.objects.get(id=user_id)
            context = {
                'is_ngo': False,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'contact_number': user_data.contact_number,
                'address': user_data.address,
                'age': user_data.age,
                'interests': user_data.interests,
            }
        except UserRegistration.DoesNotExist:
            return redirect('user_login')
        return render(request, 'app1/profile.html', context)
    
    # If neither user nor NGO is logged in, redirect to login
    return redirect('user_login')

def logout(request):
    # Clear all session data
    request.session.flush()
    # You can also add a success message if you want
    messages.success(request, "Successfully logged out!")
    return redirect('index')



def is_ngo_user(request):
    return request.session.get('ngo_id') is not None

def is_normal_user(request):
    return request.session.get('user_id') is not None



def help_request_form(request):
    if not request.session.get('user_id'):
        messages.error(request, "You must be logged in as a user to access this page.")
        return redirect('user_login')
    return render(request, 'app1/Help.html')

def submit_help_request(request):
    if request.method == 'POST':
        if not request.session.get('user_id'):
            messages.error(request, "You must be logged in to submit a help request.")
            return redirect('user_login')
        
        try:
            # Create new help request in database
            HelpRequest.objects.create(
                full_name=request.POST.get('full_name'),
                age=request.POST.get('age'),
                contact=request.POST.get('contact'),
                location=request.POST.get('location'),
                help_type=request.POST.get('help_type'),
                description=request.POST.get('description'),
                urgency=request.POST.get('urgency')
            )
            messages.success(request, "Your help request has been submitted successfully.")
            return redirect('index')
            
        except Exception as e:
            messages.error(request, f"Error submitting help request: {str(e)}")
            return redirect('help_request_form')
            
    return redirect('help_request_form')

def view_help_requests(request):
    if not request.session.get('ngo_id'):
        messages.error(request, "You must be logged in as an NGO to view help requests.")
        return redirect('ngo_login')
        
    # Get all help requests from database
    help_requests_list = HelpRequest.objects.all()
    
    # Set up pagination
    paginator = Paginator(help_requests_list, 9)  # 9 requests per page
    page_number = request.GET.get('page', 1)
    help_requests = paginator.get_page(page_number)
    
    return render(request, 'app1/help_requests.html', {'help_requests': help_requests})

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, "Please log in to access this feature.")
            return HttpResponseRedirect('/login/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

####################################################################################################



@custom_login_required
def search_users(request):
    query = request.GET.get('q', '')
    current_user = UserRegistration.objects.get(id=request.session.get('user_id'))
    
    if query:
        users = UserRegistration.objects.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        ).exclude(id=current_user.id)[:20]
    else:
        users = UserRegistration.objects.exclude(id=current_user.id)[:20]
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}",
            'is_friend': current_user.is_friends_with(user),
            'has_request': user.has_friend_request_from(current_user)
        })
    
    return render(request, 'app1/search_users.html', {
        'users': users_data,
        'query': query
    })
@custom_login_required
def send_friend_request(request, user_id):
    if request.method == 'POST':
        from_user = UserRegistration.objects.get(id=request.session.get('user_id'))
        to_user = UserRegistration.objects.get(id=user_id)
        
        # Check if the user is trying to send a request to themselves
        if from_user.id == to_user.id:
            return JsonResponse({
                'status': 'error', 
                'message': 'You cannot send a friend request to yourself.'
            }, status=400)
        
        # Check if they are already friends
        if from_user.is_friends_with(to_user):
            return JsonResponse({
                'status': 'error', 
                'message': 'You are already friends with this user.'
            }, status=400)
        
        # Check if a request already exists (in either direction)
        existing_request = FriendRequest.objects.filter(
            (Q(sender=from_user, receiver=to_user) | Q(sender=to_user, receiver=from_user)),
            status='pending'
        ).first()
        
        if existing_request:
            if existing_request.sender == from_user:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'You have already sent a friend request to this user.'
                }, status=400)
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'This user has already sent you a friend request. Please check your friend requests.'
                }, status=400)
        
        # Create new friend request
        try:
            FriendRequest.objects.create(
                sender=from_user,
                receiver=to_user,
                status='pending'
            )
            return JsonResponse({
                'status': 'success', 
                'message': 'Friend request sent successfully!'
            })
        except IntegrityError:
            return JsonResponse({
                'status': 'error', 
                'message': 'A friend request already exists between these users.'
            }, status=400)
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request method.'
    }, status=400)

@custom_login_required
def handle_friend_request(request, request_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        friend_request = get_object_or_404(
            FriendRequest, 
            id=request_id, 
            receiver_id=request.session.get('user_id')
        )
        
        if action == 'accept':
            # Create friendship
            Friendship.objects.create(
                user1=friend_request.sender,
                user2=friend_request.receiver
            )
            
            # Update request status
            friend_request.status = 'accepted'
            friend_request.save()
            
            return JsonResponse({'status': 'success', 'message': 'Friend request accepted'})
        
        elif action == 'reject':
            # Update request status
            friend_request.status = 'rejected'
            friend_request.save()
            
            return JsonResponse({'status': 'success', 'message': 'Friend request rejected'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@custom_login_required
def friend_requests(request):
    user = UserRegistration.objects.get(id=request.session.get('user_id'))
    received_requests = FriendRequest.objects.filter(
        receiver=user,
        status='pending'
    ).select_related('sender')
    
    return render(request, 'app1/friend_requests.html', {
        'requests': received_requests
    })

@custom_login_required
def friends_list(request):
    user = UserRegistration.objects.get(id=request.session.get('user_id'))
    friends = user.get_friends()
    
    return render(request, 'app1/friends_list.html', {
        'friends': friends
    })
# Add to views.py
def remove_friend(request, friend_id):
    if request.method == 'POST':
        try:
            current_user = UserRegistration.objects.get(id=request.session.get('user_id'))
            friend_to_remove = UserRegistration.objects.get(id=friend_id)
            
            # Remove the friendship
            current_user.remove_friend(friend_to_remove)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': f'Successfully removed {friend_to_remove.first_name} {friend_to_remove.last_name} from friends.'
                })
            return redirect('friends_list')
            
        except UserRegistration.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error', 
                    'message': 'User not found'
                }, status=404)
            messages.error(request, 'User not found')
            return redirect('friends_list')