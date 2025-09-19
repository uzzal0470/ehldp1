from django.forms import fields
from django import forms

class AddBalanceForm(forms.Form):
    why = fields.CharField(max_length=100)
    balance = fields.CharField(max_length=7)
    
class WithdrawRequestForm(forms.Form):
    action = forms.ChoiceField(choices=[("bkash" , "Bkash"), ("nagad","Nagad"),('rocket',"Rocket")])
    amount = fields.CharField(label="Amount", max_length=6)

class UserSearchForm(forms.Form):
    username = forms.CharField(label="Student ID", max_length=150)

class BalanceChangeForm(forms.Form):
    amount = forms.CharField(label="Amount")
    action = forms.ChoiceField(choices=[("add" , "Add Balance"), ("remove","Remove Balance")])
    reason = forms.CharField(label="Why", max_length=255)
