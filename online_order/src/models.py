import random
import string
import json
import requests

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import JSONField


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def random_string_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    order_new_id = 'OD' + random_string_generator()
    OrderObject = instance.__class__

    qs_exists = OrderObject.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id


def unique_delivery_generator(instance):
    delivery_new_id = 'DLR' + random_string_generator()
    OrderObject = instance.__class__

    qs_exists = OrderObject.objects.filter(delivery_id=delivery_new_id).exists()
    if qs_exists:
        return unique_delivery_generator(instance)
    return delivery_new_id


class Country(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.country)

    class meta:
        db_table = "Country"


class State(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.state)

    class meta:
        db_table = "State"


class District(models.Model):
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.district)

    class meta:
        db_table = "District"


class Village(models.Model):
    district = models.ForeignKey('District', on_delete=models.CASCADE, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.village)

    class meta:
        db_table = "Village"


class Area(models.Model):
    village = models.ForeignKey('Village', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Municipality / Village')
    area = models.CharField(max_length=100, null=True, blank=True)
    is_area_restricted_to_deliver = models.BooleanField(default=False, null=True, blank=True)
    kilometer_limit = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.area)

    class meta:
        db_table = "Area"


class StoreCategory(models.Model):
    """
        store_type:
            SuperMarket, Meat Shop, Grocery Shop, Pharmacy, Common Utility Shop, Bakery Shop, Fruit Shop, Hardware
    """
    store_type = models.CharField(max_length=100, null=True, blank=True)
    display_image = models.ImageField(null=True, blank=True, upload_to='Store Category')
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.store_type)

    class meta:
        db_table = "StoreCategory"


class DefaultSettings(models.Model):
    normal_order_delivery_charge = models.FloatField(default=0.0, null=True, blank=True)
    bulky_order_delivery_charge = models.FloatField(default=0.0, null=True, blank=True)
    normal_order_weight_limit = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                                                 verbose_name='normal_order_weight_limit in Kgs')
    average_weight_of_normal_item = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                                                     verbose_name='average_weight_of_normal_item in grams')
    expire_orders_in = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                                        verbose_name='expire_orders_in hrs')
    minimum_order_amount_in_a_day_for_a_user = models.FloatField(default=0.0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.created)

    class meta:
        db_table = "DefaultSettings"


class Units(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    short_name = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.short_name)

    class meta:
        db_table = "Units"


class SecurityQuestions(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.name)

    class meta:
        db_table = "SecurityQuestions"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    qr_code = models.ImageField(null=True, blank=True, upload_to='QR Code')
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_upi = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.name)

    class meta:
        db_table = "PaymentMethod"


class BannerImages(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    image_url = models.ImageField(null=True, blank=True, upload_to='Banner')
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.name)

    class meta:
        db_table = "BannerImages"


class User(AbstractUser):
    is_manager = models.BooleanField(default=False, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    username = None
    mobile = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self, ):
        return str(self.email)

    class meta:
        db_table = "User"


class Account(models.Model):
    admin = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    deposit = models.FloatField(default=0.0, null=True, blank=True)
    current_balance = models.FloatField(default=0.0, null=True, blank=True)
    total_business_commission_credited = models.FloatField(default=0.0, null=True, blank=True)
    total_delivery_commission_credited = models.FloatField(default=0.0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(null=True, blank=True)

    def __str__(self, ):
        return str(self.admin)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Account, self).save(*args, **kwargs)

    class meta:
        db_table = "Account"


class ActivityLogs(models.Model):
    activity = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.activity)

    class meta:
        db_table = "ActivityLogs"


class CommonUser(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    landmark = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False, null=True, blank=True)
    area_specified = models.ForeignKey('Area', on_delete=models.CASCADE, null=True, blank=True)
    security_question = models.ForeignKey('SecurityQuestions', on_delete=models.CASCADE, null=True, blank=True)
    fcm_token = models.TextField(default="", null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.name)

    class meta:
        db_table = "CommonUser"


class DeliveryAgent(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    account_no = models.CharField(max_length=30, null=True, blank=True)
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    upi_id = models.CharField(max_length=50, null=True, blank=True)
    payment_percentage = models.FloatField(default=0.0, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    fcm_token = models.TextField(default="", null=True, blank=True)
    # is_mobile_verified = models.BooleanField(default=False, null=True, blank=True)
    # is_email_verified = models.BooleanField(default=False, null=True, blank=True)
    area_specified = models.ForeignKey('Area', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.name)

    class meta:
        db_table = "DeliveryAgent"


class Business(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_accept_credit = models.BooleanField(default=False, null=True, blank=True)
    credit_users = models.ManyToManyField('CommonUser', blank=True)
    account_no = models.CharField(max_length=30, null=True, blank=True)
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    upi_id = models.CharField(max_length=50, null=True, blank=True)
    payment_percentage = models.FloatField(default=0.0, null=True, blank=True)
    manager = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    manager_mobile = models.CharField(max_length=10, null=True, blank=True)
    secondary_mobile = models.CharField(max_length=15, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    fcm_token = models.TextField(default="", null=True, blank=True)
    # is_mobile_verified = models.BooleanField(default=False, null=True, blank=True)
    # is_email_verified = models.BooleanField(default=False, null=True, blank=True)
    area_specified = models.ForeignKey('Area', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('StoreCategory', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self, ):
        return str(self.name)

    class meta:
        db_table = "Business"


class Order(models.Model):
    """
        status =>
            0 - default case( notification inactive case)
            1 - when user opened an order.
            2 - business review the order and accept, send estimated invoice
            3 - business review the order and reject, send the reason
            4 - when user confirm the order after review invoice
            5 - when user placed the order after confirm
            6 - when order packing completed
            7 - when delivery agent pickup the order
            8 - when order is delivered and collect payment
            9 - when user is don't accept the order
            10 - when delivery agent do payment to business
            11 - when business confirm the payment
            12 - when user cancel the order (Unable to cancel the order after confirmation)

        order_type =>
            0 - default case
            1 - Order from user form
            2 - Order from user req sheet
            3 - Order from user phone call
    """
    common_user = models.ForeignKey('CommonUser', on_delete=models.SET_NULL, null=True, blank=True)
    business = models.ForeignKey('Business', on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=15, null=True, blank=True)
    order_list_image = models.ImageField(null=True, blank=True, upload_to='Order')
    order_bill = models.ImageField(null=True, blank=True, upload_to='Order Bill')
    order_details = models.ManyToManyField('OrderDetails', blank=True, related_name='order_details')
    order_item_not_available = models.ManyToManyField('OrderDetails', blank=True,
                                                      related_name='order_item_not_available')
    order_type = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    total_weight_in_kg = models.FloatField(default=0.0, null=True, blank=True)
    order_total_items = models.PositiveSmallIntegerField(null=True, default=0, blank=True)
    order_amount = models.FloatField(default=0.0, null=True, blank=True)
    expected_delivery_charge = models.FloatField(default=0.0, null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_expired = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(editable=False, null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)

    def __str__(self, ):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if self.id:
            if self.order_type == 1:
                if self.order_details:
                    self.order_total_items = self.order_details.all().count()
        return super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ On delete """
        if self.order_details:
            all_orders = self.order_details.all()
            if all_orders:
                for i in all_orders:
                    i.delete()
        if self.order_item_not_available:
            all_orders_not_available = self.order_item_not_available.all()
            if all_orders_not_available:
                for i in all_orders_not_available:
                    i.delete()

        return super(Order, self).delete(*args, **kwargs)

    class meta:
        db_table = "Order"


class OrderDetails(models.Model):
    item = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    unit = models.ForeignKey('Units', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self, ):
        return str(self.item)

    class meta:
        db_table = "OrderDetails"


class OrderDelivery(models.Model):
    """
        status =>
            0. default
            1. Open delivery for a user(pickup the order)
            2. Agent take the delivery order
            3. Delivery complete and confirm payment
            4. Delivery failed for a reason
    """
    delivery_agent = models.ForeignKey('DeliveryAgent', on_delete=models.SET_NULL, null=True, blank=True)
    common_user = models.ForeignKey('CommonUser', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_id = models.CharField(max_length=15, null=True, blank=True)
    orders = models.ManyToManyField('Order', blank=True, related_name='orders_available')
    picked_orders = models.ManyToManyField('Order', blank=True, related_name='picked_orders')
    delivery_charge = models.FloatField(default=0.0, null=True, blank=True)
    total_user_orders_amount = models.FloatField(default=0.0, null=True, blank=True)
    total_amount_to_collect = models.FloatField(default=0.0, null=True, blank=True)
    verify_total_amount = models.BooleanField(default=False, null=True, blank=True)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    is_delivered = models.BooleanField(default=False, null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    area_specified = models.ForeignKey('Area', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self, ):
        return str(self.delivery_id)

    class meta:
        db_table = "OrderDelivery"


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def pre_save_create_delivery_id(sender, instance, *args, **kwargs):
    if not instance.delivery_id:
        instance.delivery_id = unique_delivery_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)
pre_save.connect(pre_save_create_delivery_id, sender=OrderDelivery)


class UserNotifications(models.Model):
    """
        When to be Notified =>
            1 - an order is placed
            2 - business review the order and accept, send estimated invoice
            3 - business review the order and reject, send the reason
            4 - when user confirm the order after review invoice
    """
    message = models.CharField(max_length=2000, null=True, blank=True)
    common_user = models.ForeignKey('CommonUser', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    delivery_order = models.ForeignKey('OrderDelivery', on_delete=models.CASCADE, null=True, blank=True)
    header = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_send = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.message

    class meta:
        db_table = "UserNotification"


@receiver(post_save, sender=UserNotifications)
def send_push_notification_to_user(sender, instance, **kwargs):
    created = False
    if 'created' in kwargs:
        if kwargs['created']:
            if not instance.is_send:
                try:
                    token = instance.common_user.fcm_token
                    url = "https://fcm.googleapis.com/fcm/send"
                    body = {
                        "notification": {
                            "title": instance.header,
                            "body": instance.message,
                            "click_action": instance.url,
                            "icon": "{}static/img/logo.png".format(settings.BASE_URL_DEF)
                        },
                        "to": token
                    }
                    headers = {"Content-Type": "application/json",
                               "Authorization": "key={}".format(settings.FIREBASE_SERVER_KEY)}
                    data = requests.post(url, data=json.dumps(body), headers=headers)
                    if data.status_code == 200:
                        instance.is_send = True
                        instance.save()
                    created = True
                except Exception as e:
                    print(e)

    # If signal is from object creation, return
    if created:
        return


class DeliveryAgentNotification(models.Model):
    """
        When to be Notified =>
            1 - an order ready to pickup
            2 - business review the order and accept, send estimated invoice
            3 - business review the order and reject, send the reason
            4 - when user confirm the order after review invoice
    """
    message = models.CharField(max_length=500, null=True, blank=True)
    delivery_agent = models.ForeignKey('DeliveryAgent', on_delete=models.CASCADE, null=True, blank=True)
    delivery_order = models.ForeignKey('OrderDelivery', on_delete=models.CASCADE, null=True, blank=True)
    header = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_send = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.message

    class meta:
        db_table = "DeliveryAgentNotification"


@receiver(post_save, sender=DeliveryAgentNotification)
def send_push_notification_to_agent(sender, instance, **kwargs):
    created = False
    if 'created' in kwargs:
        if kwargs['created']:
            if not instance.is_send:
                try:
                    token = instance.delivery_agent.fcm_token
                    url = "https://fcm.googleapis.com/fcm/send"
                    body = {
                        "notification": {
                            "title": instance.header,
                            "body": instance.message,
                            "click_action": instance.url,
                            "icon": "{}static/img/logo.png".format(settings.BASE_URL_DEF)
                        },
                        "to": token
                    }
                    headers = {"Content-Type": "application/json",
                               "Authorization": "key={}".format(settings.FIREBASE_SERVER_KEY)}
                    data = requests.post(url, data=json.dumps(body), headers=headers)
                    if data.status_code == 200:
                        instance.is_send = True
                        instance.save()
                    created = True
                except Exception as e:
                    print(e)

    # If signal is from object creation, return
    if created:
        return


class BusinessNotification(models.Model):
    """
        When to be Notified =>
            1 - an order is placed
            2 - business review the order and accept, send estimated invoice
            3 - business review the order and reject, send the reason
            4 - when user confirm the order after review invoice
    """
    message = models.CharField(max_length=500, null=True, blank=True)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    header = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_send = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.message

    class meta:
        db_table = "BusinessNotification"


@receiver(post_save, sender=BusinessNotification)
def send_push_notification_to_business(sender, instance, **kwargs):
    created = False
    if 'created' in kwargs:
        if kwargs['created']:
            if not instance.is_send:
                try:
                    token = instance.business.fcm_token
                    url = "https://fcm.googleapis.com/fcm/send"
                    body = {
                        "notification": {
                            "title": instance.header,
                            "body": instance.message,
                            "click_action": instance.url,
                            "icon": "{}static/img/logo.png".format(settings.BASE_URL_DEF)
                        },
                        "to": token
                    }
                    headers = {"Content-Type": "application/json",
                               "Authorization": "key={}".format(settings.FIREBASE_SERVER_KEY)}
                    data = requests.post(url, data=json.dumps(body), headers=headers)
                    if data.status_code == 200:
                        instance.is_send = True
                        instance.save()
                    created = True
                except Exception as e:
                    print(e)

    # If signal is from object creation, return
    if created:
        return


class BusinessTransactions(models.Model):
    transaction_id = models.CharField(max_length=25, null=True, blank=True)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    total_amount = models.FloatField(default=0.0, null=True, blank=True)
    platform_amount = models.FloatField(default=0.0, null=True, blank=True)
    is_completed = models.BooleanField(default=False, null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.transaction_id

    class meta:
        db_table = "BusinessTransactions"


class AgentTransactions(models.Model):
    transaction_id = models.CharField(max_length=25, null=True, blank=True)
    delivery_agent = models.ForeignKey('DeliveryAgent', on_delete=models.CASCADE, null=True, blank=True)
    is_cod = models.BooleanField(default=False, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    total_amount = models.FloatField(default=0.0, null=True, blank=True)
    platform_amount = models.FloatField(default=0.0, null=True, blank=True)
    total_order_amount = models.FloatField(default=0.0, null=True, blank=True)
    gross_amount = models.FloatField(default=0.0, null=True, blank=True)
    is_completed = models.BooleanField(default=False, null=True, blank=True)
    delivery_order = models.ForeignKey('OrderDelivery', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.transaction_id

    class meta:
        db_table = "AgentTransactions"


class AgentPayment(models.Model):
    reference_id = models.CharField(max_length=50, null=True, blank=True)
    is_debit = models.BooleanField(default=False, null=True, blank=True)
    is_credit = models.BooleanField(default=False, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    pay_by = models.CharField(max_length=50, null=True, blank=True)
    delivery_agent = models.ForeignKey('DeliveryAgent', on_delete=models.CASCADE, null=True, blank=True)
    transactions = models.ManyToManyField('AgentTransactions', blank=True)

    def __str__(self):
        return self.delivery_agent.name

    class meta:
        db_table = "AgentPayment"


class BusinessPayment(models.Model):
    reference_id = models.CharField(max_length=50, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    pay_by = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, null=True, blank=True)
    transactions = models.ManyToManyField('BusinessTransactions', blank=True)

    def __str__(self):
        return self.business.name

    class meta:
        db_table = "BusinessPayment"


def random_transaction_id_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_transaction_id_generator(instance):
    order_new_id = 'TR' + random_transaction_id_generator()
    OrderObject = instance.__class__

    qs_exists = OrderObject.objects.filter(transaction_id=order_new_id).exists()
    if qs_exists:
        return unique_transaction_id_generator(instance)
    return order_new_id


def pre_save_create_transaction_id(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_transaction_id_generator(instance)


pre_save.connect(pre_save_create_transaction_id, sender=BusinessTransactions)
pre_save.connect(pre_save_create_transaction_id, sender=AgentTransactions)
