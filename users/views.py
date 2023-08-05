from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreateForm,ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import UserCreateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Friendship,CustomUser
from django.db.models import Q

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        sent_requests=user.friendship_sent.filter(sender=user,status='accepted')[:]
        received_requests=user.friendship_received.filter(receiver=user,status='accepted')[:]
        friends =sent_requests.union(received_requests)
        friend_requests=user.friendship_received.filter(receiver=user,status='pending')[:]
        non_friends = CustomUser.objects.exclude(Q(friendship_sent__receiver=user) |Q(friendship_received__sender=user)
        ).order_by('-date_joined')[:10]
        context = {
            'user': user,
            'friends': friends,
            'friend_requests':friend_requests,
            'non_friends':non_friends
    }
        return render(request, 'users/profile.html', context)

class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, receiver_id):
        sender = request.user
        receiver = CustomUser.objects.get(id=receiver_id)
        
        friendship = Friendship.objects.create(sender=sender,receiver=receiver,status='pending')
        
        friendship.save()
        messages.success(request, 'Friend request sent successfully.')
        return redirect('profile')

class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, friendship_id):
        friendship = Friendship.objects.get(id=friendship_id)
        friendship.status = 'accepted'
        friendship.save()
        messages.success(request, 'Friend request accepted.')
        return redirect('profile')

class RejectFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, friendship_id):
        friendship = Friendship.objects.get(id=friendship_id)
        friendship.status = 'declined'
        friendship.save()
        messages.success(request, 'Friend request declined.')
        return redirect('profile')

class UnfriendView(LoginRequiredMixin, View):
    def post(self, request, friend_id):
        friendship = Friendship.objects.filter(sender=request.user, receiver_id=friend_id).first()
        if friendship:
            friendship.delete()
            messages.success(request, 'Unfriended successfully.')
        else:
            friendship=Friendship.objects.filter(receiver=request.user,receiver_id=request.user.id)
            friendship.delete()
            messages.success(request, 'Unfriended successfully.')
        return redirect('profile')
class GetInTouchView(LoginRequiredMixin,View):
    def get(self,request,id):
        
        user=CustomUser.objects.get(id=id)
        sent_requests=user.friendship_sent.filter(sender=user,status='accepted')[:]
        received_requests=user.friendship_received.filter(receiver=user,status='accepted')[:]
        friends =sent_requests.union(received_requests)
        friend_requests=user.friendship_received.filter(receiver=user,status='pending')[:]
        context = {
            'user': user,
            'friends': friends,
            'friend_requests':friend_requests
    }
        
        return render(request,'users/get_in_touch.html',context)
    



# Create your views here.
class RegisterView(View):
    def get(self,request):
        create_form = UserCreateForm()
        context = {
            'form': create_form
        }
        return render(request,'users/register.html',context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('login')

        else:
            context = {
                'form': create_form
            }

        return render(request,'users/register.html',context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'users/login.html', context)
    def post(self,request):



        login_form=AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user=login_form.get_user()
            login(request, user)
            messages.success(request,'you have successfully logged in')
            return redirect('landing_page')

        else:
            return render(request, 'users/login.html', {'login_form':login_form})



        


    
    
    


# class ProfileView(LoginRequiredMixin,View):
#     def get(self,request):
        
        
        
        
class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.info(request,'you have succesfully logged out')
        return redirect('landing_page')
    
class ProfileUpdate(View):
    def get(self,request):
        edit_form=ProfileUpdateForm(instance=request.user)
        context={
            'edit_form':edit_form
        }
        return render(request,'users/profile_update.html',context)
    def post(self,request):
        edit_form=ProfileUpdateForm(data=request.POST,
                                    
                                instance=request.user,
                                files=request.FILES)
        
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request,'you have succesfully your profile !')
            return redirect('profile')
        else:
            context={
            'edit_form':edit_form
            }
            return render(request,'users/profile_update.html',context)
            