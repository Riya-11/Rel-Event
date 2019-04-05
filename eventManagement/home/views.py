from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from events.models import event, invitation
from groups.models import *


# Create your views here.
def index(request):
    events = event.objects.all()
    query = request.GET.get('q')
    if query:
        events = event.objects.filter(name__icontains=query)
        print(events.query)
        if not events:
            events = event.objects.filter(venue__icontains=query)
    else:
        events = event.objects.all()

    return render(request, 'home/landing.html', {'events': events})

@login_required(login_url="/home/login")
def dashboard(request):
    events = event.objects.all()
    invites = invitation.objects.filter(to=request.user)
    group = Group.objects.all()
    group_invites = Group_invite.objects.filter(to=request.user)
    grp = Group.objects.filter(creator=request.user)
    group_requests_rcvd = Group_request.objects.none()

    for g in grp:
        if Group_request.objects.filter(group=g).exists():
            group_requests_rcvd |= Group_request.objects.filter(group = g,request_status=0)

    sent_group_requests = Group_request.objects.filter(request_from=request.user, request_status=0)
    send_requests_group = Group.objects.none()
    for i in group:
        if (not Group.objects.filter(name=i.name,members=request.user).exists() and not Group_request.objects.filter(group=i,request_from=request.user).exists()):
            send_requests_group |= Group.objects.filter(name=i.name)
    print(send_requests_group)
    return render(request, 'home/homepage.html',
                  {'events': events, 'invites': invites, 'group': group, 'group_invites': group_invites,
                   'sent_group_requests': sent_group_requests,
                   'send_group_request': send_requests_group,'group_requests_rcvd':group_requests_rcvd})

# def dashboard(request):
#     events = event.objects.all()
#     invites = invitation.objects.filter(to=request.user)
#     group = Group.objects.all()
#     group_invites = Group_invite.objects.filter(to=request.user)
#     sent_group_requests = Group_request.objects.filter(request_from=request.user, request_status=False)
#     send_requests_group = Group.objects.none()
#     for i in group:
#         if (not Group.objects.filter(name=i.name,members=request.user).exists() and not Group_request.objects.filter(group=i,request_from=request.user).exists()):
#             send_requests_group |= Group.objects.filter(name=i.name)
#     print(send_requests_group)
#     return render(request, 'home/homepage.html',
#                   {'events': events, 'invites': invites, 'group': group, 'group_invites': group_invites,
#                    'sent_group_requests': sent_group_requests,
#                    'send_group_request': send_requests_group})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home:index')
    else:
        logout(request)
        return redirect('home:index')
