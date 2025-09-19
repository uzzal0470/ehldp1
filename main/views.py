from django.shortcuts import render , redirect , get_object_or_404
from .forms import SignupForm
from django.contrib.auth import login , get_user_model , logout ,get_user
from django.contrib.auth.views import PasswordChangeView
from .models import History , Refer , Event
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from controler.forms import WithdrawRequestForm
from controler.models import WithdrawRequest , T
from django.contrib import messages
import uuid
from .untils import *
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.core.cache import cache  # temporary token store

User = get_user_model()


def whatsapp_password_reset_request(request):
    if request.method == "POST":
        number = request.POST.get("whatsapp_number")
        try:
            user = User.objects.get(whatsapp_number=number)
        except User.DoesNotExist:
            messages.error(request, "No user found with this WhatsApp number.")
            return redirect('whatsapp_password_reset')
        
        token = str(uuid.uuid4())
        cache.set(token, user.pk, timeout=300) # Akhane password reset url 5 minutes por kaj korbe na

        link = request.build_absolute_uri(reverse("whatsapp_password_reset_confirm", args=[token]))
        send_whatsapp_message(number, f"Your password reset link: {link}")
        messages.success(request, "Reset link sent to your WhatsApp number.")
    return render(request, "whatsapp_password_reset.html")

class Password_Change(PasswordChangeView):
    template_name = 'password_change.html'

def whatsapp_password_reset_confirm(request, token):
    user_id = cache.get(token)
    if not user_id:
        messages.error(request, "Invalid or expired token.")
        return redirect("whatsapp_password_reset")
    
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        new_password = request.POST.get("password")
        user.set_password(new_password)
        user.save()
        cache.delete(token)
        messages.success(request, "Password successfully changed. You can now log in.")
        return redirect("home")
    
    return render(request, "whatsapp_password_reset_confirm.html", {"token": token})

@login_required
def refer_history(request):
    refer_history = Refer.objects.filter(refered_from=request.user).order_by('-time')
    return render(request , 'refer_history.html' , {'all_refer':refer_history})



def home(request):
    user = get_user(request)
    tra = T.objects.all()
    event = Event.objects.get(id=1)
    return render(request , 'home.html', {"user":user , 'event':event , 'tra':tra})

def signup_view(request):
    if get_user(request).is_authenticated:
        return redirect('home')
    ref_code = request.GET.get('ref')
    referred_by = None
    if ref_code:
        try:
            referred_by = User.objects.get(referral_code=ref_code)
            cache.add('referred_by' , referred_by , 300)
        except:
            referred_by = None

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            whatsapp_number = form.cleaned_data.get('whatsapp_number')
            contry = form.cleaned_data.get('country')
            if contry == 'bangladesh':
                if not check_bd_number(whatsapp_number):
                    messages.error(request , 'The number you enter is incorect ')
                    return redirect('signup')
            print(whatsapp_number)
            if not is_valid_whatsapp_number(whatsapp_number):
                print("Hello")
                messages.error(request, "Wrong Number This number was use an another account")
                return render(request, "signup.html", {"form": form})

            user = form.save(commit=True)
            login(request , user)
            if cache.get('referred_by'):
                referred_by = cache.get('referred_by')
                print("i am in ref code succes" , referred_by)
                user.referred_by = referred_by
                user.save()

            
            History.objects.create(
                    student=user,
                    balance='+100',
                    why="Signup Bonus"
                )
            if cache.get('referred_by'):
                referred_by = cache.get('referred_by')
                print("All done" , referred_by)
                # 1 Taka referral bonus
                referred_by.balance = int(referred_by.balance)+1
                referred_by.save()
                refer = Refer.objects.create(refered_from = referred_by,refered_student=user)
                refer.save()
                History.objects.create(
                    student=referred_by,
                    balance='+1',
                    why="Referral Bonus"
                )
                cache.delete('referred_by')
            return redirect("profile")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def Login_view(request):
    if request.method == 'POST':
        ID = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        try:
            try:
                user = User.objects.get(username=ID)
            except User.DoesNotExist:
                user = User.objects.get(whatsapp_number = ID)
        except:
            messages.error(request , 'The Student Dose Not Exist .')
        if user:
            if user.check_password(password):
                login(request , user)
                return redirect('home')
            else:
                messages.error(request , 'The Password was incorrect ')
    return render(request , 'login.html')

@login_required
@csrf_exempt
def profile_view(request):
    usr = request.user
    ref = Refer.objects.filter(refered_student = request.user).order_by('-time')
    return render(request , 'profile.html' , {'user':usr , 'ref':ref})

@login_required
def history_view(request):
    withdraw = WithdrawRequest.objects.filter(user=request.user).order_by('-created_at')[::-1]
    all_history = History.objects.filter(student = request.user).order_by('date')[::-1]
    return render(request , 'history.html',{
        "history":all_history,
        'withdraw':withdraw
        })

@login_required
def withdraw_request_view(request):
    if request.method == "POST":
        form = WithdrawRequestForm(request.POST)
        if form.is_valid():
            amount = int(form.cleaned_data["amount"])
            action = form.cleaned_data["action"]
            user_balance = int(request.user.balance)

            if amount > user_balance:
                messages.error(request, "Insufficient Balance!")
                return redirect('withdraw-request')

            # Custom minimum balance check based on withdrawal history
            if not check_withdraw_balance(request.user, amount):
                if WithdrawRequest.objects.filter(user=request.user).exists():
                    messages.error(request, "Minimum withdraw amount is 50 tk!")
                else:
                    messages.error(request, "Minimum withdraw amount for your first withdrawal is 350 tk! the second withdraw you can 50 tk")
                return redirect('withdraw-request')

            # Deduct balance
            user = request.user
            user.balance = user_balance - amount
            user.save()

            bank_name = {
                'bkash': 'Bkash',
                'nagad': 'Nagad',
            }.get(action, 'Rocket')
            if not WithdrawRequest.objects.filter(user=request.user).exists():
                amount = amount - 300
            WithdrawRequest.objects.create(
                user=user,
                amount=amount,
                reason='Withdraw',
                bank=bank_name
            )

            messages.success(request, "Your withdrawal request has been received. It will be processed shortly.")
            return redirect("withdraw-request")
    else:
        form = WithdrawRequestForm()

    return render(request, "withdraw.html", {"form": form})

def withdraw_history_view(request):
    withdraw_history = WithdrawRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "withdraw_his.html", {'history':withdraw_history})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")
