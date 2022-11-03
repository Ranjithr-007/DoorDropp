from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import *


# Admin Forms
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


class CommonUserForm(forms.ModelForm):
    # security_question = forms.ModelChoiceField(
    #     required=False,
    #     queryset=SecurityQuestions.objects.filter(is_active=True),
    #     widget=forms.Select(
    #         attrs={}
    #     )
    # )

    class Meta:
        model = CommonUser
        fields = ['name', 'email', 'mobile', 'security_question', 'answer']


class AddDeliveryAgentForm(forms.ModelForm):
    class Meta:
        model = DeliveryAgent
        fields = ['name', 'email', 'mobile', 'address', 'area_specified', 'payment_percentage']


class AddBusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'email', 'mobile', 'address', 'area_specified', 'manager', 'manager_mobile',
                  'secondary_mobile', 'about', 'category', 'payment_percentage']


class AddUnitForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = ['name', 'short_name']


class AddPaymentMethodForm(forms.ModelForm):
    qr_code = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': '-hidden', 'id': 'file-upload', 'multiple': True, 'placeholder': 'Upload Image', 'size': '30'}))

    is_upi = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PaymentMethod
        fields = ['name', 'qr_code', 'is_upi']


class AddBannerImageForm(forms.ModelForm):
    image_url = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': '-hidden', 'id': 'file-upload', 'multiple': True, 'placeholder': 'Upload Image', 'size': '30'}))

    class Meta:
        model = BannerImages
        fields = ['name', 'image_url']


class AddStoreCategoryForm(forms.ModelForm):
    display_image = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': '-hidden', 'id': 'file-upload', 'multiple': True, 'placeholder': 'Upload Image', 'size': '30'}))

    class Meta:
        model = StoreCategory
        fields = ['store_type', 'remarks', 'display_image']


class AddDistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district', 'state']


class AddVillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ['district', 'village']


class AddAreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['village', 'area', 'kilometer_limit']


class DefaultSettingsForm(forms.ModelForm):
    class Meta:
        model = DefaultSettings
        fields = ['normal_order_delivery_charge', 'bulky_order_delivery_charge', 'normal_order_weight_limit',
                  'average_weight_of_normal_item', 'expire_orders_in']


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# User Forms
class OrderDetailsForm(forms.ModelForm):
    item = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': 'required'}))

    quantity = forms.IntegerField(required=True, min_value=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'step': 1, 'min': 0, 'required': 'required'}))

    unit = forms.ModelChoiceField(required=True, queryset=Units.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}))

    class Meta:
        model = OrderDetails
        fields = ['item', 'quantity', 'unit']


class OrderPriceForm(forms.ModelForm):
    item = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': 'required'}))

    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'step': 1, 'min': 0, 'required': 'required'}))

    unit = forms.ModelChoiceField(queryset=Units.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}))
    price = forms.FloatField(min_value=0.0, widget=forms.NumberInput(
        attrs={'class': 'form-control item_price', 'step': 0.1, 'min': 0.0, 'required': 'required'}))

    class Meta:
        model = OrderDetails
        fields = ['item', 'quantity', 'unit', 'price']


class OrderUploadForm(forms.ModelForm):
    order_list_image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': '-hidden', 'id': 'file-upload', 'multiple': True, 'placeholder': 'Upload Image',
               'capture': 'user'}))

    class Meta:
        model = Order
        fields = ['order_list_image']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = CommonUser
        fields = ['name', 'mobile', 'address', 'landmark', 'email']


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Agent Forms

class AgentProfileForm(forms.ModelForm):

    class Meta:
        model = DeliveryAgent
        fields = ['name', 'mobile', 'address', 'email', 'account_no', 'upi_id', 'ifsc']


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Business Forms
class BusinessProfileForm(forms.ModelForm):

    class Meta:
        model = Business
        fields = ['name', 'mobile', 'address', 'manager', 'manager_mobile', 'secondary_mobile', 'about', 'email', 'account_no', 'upi_id', 'ifsc']
