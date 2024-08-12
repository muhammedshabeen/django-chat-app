from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='login')
def home(request):
    logined_user = request.user
    
    # Get chat rooms where the logged-in user is either the sender or receiver
    chats = ChatRoom.objects.filter(
        Q(sender_user=logined_user) | Q(receiver_user=logined_user)
    ).distinct()
    
    # Extract chat IDs
    chat_ids = chats.values_list('id', flat=True)
    
    
    # Get users involved in these chat rooms, excluding the logged-in user
    involved_users = CustomUser.objects.filter(
        Q(send_user__in=chat_ids) | Q(recieve_user__in=chat_ids)
    ).exclude(id=logined_user.id).distinct()
    
    # Create a dictionary to map users to their chat IDs
    user_chat_mapping = []
    for user in involved_users:
        user_chats = ChatRoom.objects.filter(
            Q(sender_user=user) | Q(receiver_user=user),
            id__in=chat_ids
        ).values_list('id', flat=True)
        user_chat_mapping.append(user_chats)
    print("user_chat_mapping",user_chat_mapping)
    context = {
        'chats': chats,
        'involved_users': involved_users,
        'user_chat_mapping': user_chat_mapping,
        'request_user':logined_user,
    }
    return render(request,"home_page.html",context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        print("hello",username,password)
        user = authenticate(request, username=username, password=password)
        print("user",user)
        if user is not None:
            login(request, user)
            messages.success(request,"logined successfully")
            return redirect('home')
        else:
            messages.error(request,"username or password is incorrect")
            return redirect('login')
    return render(request,'registration/login.html')


def get_chat_messages(request):
    chat_id = request.GET.get('chat_id')
    print("CHAT_ID",chat_id)
    if chat_id:
        # Fetch messages based on chat_id
        messages = Message.objects.filter(chat_room_id=chat_id).values('user_id', 'content', 'timestamp','user__image').order_by('timestamp')
        print("messages",messages)
        if messages:
            return JsonResponse({'messages': list(messages)})
        else:
            return JsonResponse({'nothing': 'Nothing Found'})
    return JsonResponse({'error': 'Chat ID not provided'}, status=400)


def send_chat_messages(request):
    # Retrieve parameters from GET request
    chat_id = request.GET.get('chat_id')
    user_id = request.GET.get('user_id')
    message_content = request.GET.get('message')
    
    # Log the received parameters
    print("CHAT_ID:", chat_id, "MESSAGE:", message_content, "USER_ID:", user_id)
    
    # Validate parameters
    if not chat_id or not user_id or not message_content:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    
    # Ensure the user exists
    try:
        login_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
    
    # Create and save the message
    try:
        message = Message.objects.create(chat_room_id=chat_id, user=login_user, content=message_content)
        print("Message created:", message)
        return JsonResponse({'success': "Message sent successfully"})
    except Exception as e:
        print("Error creating message:", e)
        return JsonResponse({'error': 'Failed to send message'}, status=500)





def logout_view(request):
    request.session.flush()
    return redirect('login')