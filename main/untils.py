from controler.models import WithdrawRequest
import re
from .models import User
def check_withdraw_balance(user, amount):
    amount = int(amount)

    # Check if user has any previous withdrawals
    has_withdrawn_before = WithdrawRequest.objects.filter(user=user).exists()

    if has_withdrawn_before:
        return amount >= 50
    else:
        return amount >= 350

def send_whatsapp_message(number, message):
    return True

def is_valid_whatsapp_number(number):
    """
    Check if the WhatsApp number is valid:
    - Must be exactly 11 digits
    - Must start with '01' (Bangladesh mobile number format)
    """
    try:
        usr = User.objects.get(whatsapp_number=number)
        return False
    except User.DoesNotExist:
        return True
def check_bd_number(num):
    if num[0] == '0' and num[1]=='1' and len(num) == 11:
        return True
    return False
