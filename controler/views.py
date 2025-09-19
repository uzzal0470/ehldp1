from django.shortcuts import render , redirect ,get_object_or_404
from main.models import User , History , Event
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import AddBalanceForm , WithdrawRequestForm
from django.contrib import messages
from django.utils.timezone import now
from .forms import UserSearchForm, BalanceChangeForm
from .models import WithdrawRequest , T
from django.core.cache import cache  # temporary token store


@user_passes_test(lambda u: u.is_superuser)
def process_withdraw_requests(request):
    requests = WithdrawRequest.objects.filter(status='pending')

    if request.method == "POST":
        action = request.POST.get("action")
        request_id = request.POST.get("request_id")
        reason = request.POST.get("reason", "")

        try:
            w_request = WithdrawRequest.objects.get(id=request_id)
            if action == "accept":
                w_request.status = "accepted"
                w_request.processed_at = now()
                w_request.save()
                History.objects.create(
                    student=w_request.user,
                    balance=f"-{w_request.amount}",
                    why="Withdraw Approved"
                    )
                messages.success(request, "The withdraw was Approved")
            elif action == "reject":
                w_request.user.balance =str(int(w_request.user.balance)+int(w_request.amount)) 
                w_request.user.save()
                w_request.status = "rejected"
                w_request.reason = reason
                w_request.processed_at = now()
                w_request.save()
                History.objects.create(
                    student=w_request.user,
                    balance=0,
                    why=f"Withdraw Rejected: {reason}"
                )
                messages.info(request, f"{w_request.user.username} Request was Rejected .")

        except WithdrawRequest.DoesNotExist:
            messages.error(request, "No such Request .")

        return redirect("process-withdraw")

    return render(request, "withdraw_requests.html", {"requests": requests})
@user_passes_test(lambda u: u.is_superuser)
def controller_page(request):
    user_obj = None
    search_form = UserSearchForm()
    balance_form = None

    if request.method == "POST":
        if 'username' in request.POST:
            search_form = UserSearchForm(request.POST)
            if search_form.is_valid():
                username = search_form.cleaned_data['username']
                try:
                    user_obj = User.objects.get(username=username)
                    balance_form = BalanceChangeForm()  # empty form
                except User.DoesNotExist:
                    messages.error(request, "Student Not Found")

        if 'amount' in request.POST:
            search_form = UserSearchForm(request.POST)  # to preserve username
            balance_form = BalanceChangeForm(request.POST)
            if search_form.is_valid() and balance_form.is_valid():
                username = search_form.cleaned_data['username']
                try:
                    print("Hes")
                    user_obj = User.objects.get(username=username)
                    amount = balance_form.cleaned_data['amount']
                    action = balance_form.cleaned_data['action']
                    reason = balance_form.cleaned_data['reason']

                    if action == "add":
                        user_obj.balance =int(user_obj.balance)+ int(amount)
                        user_obj.save()
                        History.objects.create(student=user_obj, balance=f'+{amount}', why=f"{reason}")
                        messages.success(request, f"Succes to add {amount} taka on student ID {username}")
                        return redirect('balance-control')
                    elif action == "remove":
                        if int(user_obj.balance) >= int(amount):
                            user_obj.balance =int(user_obj.balance) - int(amount)
                            History.objects.create(student=user_obj, balance=f"-{amount}", why=f"Succes to cut {amount} taka to student ID {username}")
                            messages.error(request, f"Succes to cut {amount} taka to student ID {username}")
                            return redirect('balance-control')
                        else:
                            messages.error(request, "Insufucient Balance")
                    user_obj.save()
                except User.DoesNotExist:
                    messages.error(request, "Student Not Found")

    return render(request, "controller_page.html", {
        "search_form": search_form,
        "balance_form": balance_form,
        "user_obj": user_obj
    })


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    pending_users = User.objects.filter(active_permision=False)
    react_user = User.objects.filter(active_permision=True)
    event = Event.objects.get(id=1)
    total_users = User.objects.count()
    tra = T.objects.all()
    total_active_users = len(User.objects.filter(active_permision=True))
    total_withdraws = WithdrawRequest.objects.count()
    recent_withdraws = WithdrawRequest.objects.order_by('-created_at')[:5]
    context = {
        'pending_users': pending_users,
        'total_users': total_users,
        'total_withdraws': total_withdraws,
        'recent_withdraws': recent_withdraws,
        'react':react_user,
        'active':total_active_users,
        'event':event,
        'tra':tra
    }
    if request.method == 'POST':
        text = request.POST.get('event')
        if not text:
            event.text = 'none'
            event.save()
        else:
            event.text = text
            event.save()
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.active_permision = True
    user.save()
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def decline_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')


@user_passes_test(lambda u: u.is_superuser)
def admin_profile(request):
    user = None
    if request.method == 'POST':
        username = request.POST.get('username')
        cache.add('u' ,username)
        try:
            user = User.objects.get(username = username)

        except:
            user = None
        if request.method == 'POST':
            password = request.POST.get('password')
            u = User.objects.get(username = cache.get('u'))
            u.set_password(password)
            u.save()
            print(password , 'Was save')


    return render(request , 'admin_profile.html' , {
        "user_":user
    })
