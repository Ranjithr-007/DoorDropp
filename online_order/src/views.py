import datetime
import uuid
# import random
import json
import xlwt
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.forms import formset_factory
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

# from .models import *
from .forms import *


# Common Functions
def generate_activity_log(request, category="", user="", action=""):
    now = datetime.datetime.now()
    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
    if action and user and category:
        ActivityLogs(
            activity="{} {} {} by {} on {}".format(category, user, action, request.session['admin']['email'],
                                                   formatted)).save()


def create_activity_log(request, category="", user="", action=""):
    now = datetime.datetime.now()
    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
    if action and user and category:
        ActivityLogs(
            activity="{} {} {} on {}".format(category, user, action, formatted)).save()


def send_welcome_mail(name=None, user_mail=None, mobile=None, password=None, flag=None):
    proj_name = "DoorDropp"
    base_link = settings.BASE_URL_DEF
    subject = "Your {} Account Created!".format(proj_name)
    if flag == 'agent':
        base_link = base_link + "agent"
        welcome_msg = "Hello {}, \n\nYour registration as a delivery agent with {} has been successfully completed. " \
                      "You can now login our system via the following link. We have attached login credentials to " \
                      "this email.\n\nLogin Link = {}\nMobile = {}\nPassword = {}\n\nYou can change the password " \
                      "after logging into the system. If you have any queries? " \
                      "Feel free to contact our support.\n\n\n\nwith regards,\n\nAdministrator\nTeam {}\nIzado " \
                      "Solutions Pvt. Ltd.\nKozhikode, Kerala, India\ninfo@izado.in\n+919495495516 | " \
                      "+919562023962".format(name, proj_name, base_link, mobile, password, proj_name)
    elif flag == 'business':
        base_link = base_link + "business"
        welcome_msg = "Hello {}, \n\nYour registration as a business with {} has been successfully completed. You can " \
                      "now login our system via the following link. We have attached login credentials to this " \
                      "email.\n\nLogin Link = {}\nMobile = {}\nPassword = {}\n\nYou can change the password after " \
                      "logging into the system. If you have any queries? Feel " \
                      "free to contact our support.\n\n\n\nwith regards,\n\nAdministrator\nTeam {}\nIzado Solutions " \
                      "Pvt. Ltd.\nKozhikode, Kerala, India\ninfo@izado.in\n+919495495516 " \
                      " | +919562023962".format(name, proj_name, base_link, mobile, password, proj_name)
    else:
        return False

    response = send_mail(subject=subject, recipient_list=[user_mail], from_email=settings.EMAIL_HOST_USER,
                         message=welcome_msg)
    return True


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyCQkEmnaTcFv-hA9FGeHwuZalH-FP9pxtg",' \
           '        authDomain: "doordropp-izado.firebaseapp.com",' \
           '        projectId: "doordropp-izado",' \
           '        storageBucket: "doordropp-izado.appspot.com",' \
           '        messagingSenderId: "406377898482",' \
           '        appId: "1:406377898482:web:667085aea826451a874b6b",' \
           '        measurementId: "G-D9C7XYKG5W"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")


# Admin Functions Start Here
# ----------------------------------------------------------------------------------------------------------------------
def session_required_admin(function):
    def _function(request, *args, **kwargs):
        if request.session.get('admin') is None:
            return redirect('admin_login')
        else:
            return function(request, *args, **kwargs)

    return _function


def login_from_session_admin(request):
    if request.session.has_key('admin'):
        if request.session['admin']:
            return redirect('admin_home')
    return redirect('admin_login')


class getLoginAdmin(View):
    def get(self, request):
        return render(request, "sys_admin/login_page.html", {})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        record = User.objects.filter(is_superuser=True, email=email).exists()
        if not record:
            messages.add_message(request, messages.WARNING, 'Admin does not exist in this email')
            return redirect('admin_login')
        auth = authenticate(email=email, password=password)
        if auth:
            if auth.is_superuser:
                request.session['admin'] = {
                    'id': auth.id,
                    'email': auth.email,
                }
                return redirect('admin_home')
        else:
            messages.add_message(request, messages.WARNING, 'Username or password mismatch')
            return redirect('admin_login')


def logout_admin(request):
    del request.session['admin']
    return redirect('admin_index')


@session_required_admin
def admin_home(request):
    return render(request, 'sys_admin/admin_dash.html', {})


@session_required_admin
def add_delivery_agent(request):
    form = AddDeliveryAgentForm(request.POST or None)
    delivery_agents = DeliveryAgent.objects.all().order_by('-id')
    all_area = Area.objects.filter(is_active=True).order_by('area')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    mobile = form.cleaned_data['mobile'].strip()
                    if DeliveryAgent.objects.filter(
                            ~Q(id=int(request.POST.get('key'))) & Q(mobile__exact=mobile)).exists():
                        messages.add_message(request, messages.WARNING,
                                             'Delivery agent already registered with mobile number {}.'.format(mobile))
                        return redirect('addDeliveryAgent')

                    delivery_agent = DeliveryAgent.objects.get(id=int(request.POST.get('key')))
                    delivery_agent.name = form.cleaned_data['name']
                    delivery_agent.mobile = mobile
                    delivery_agent.email = form.cleaned_data['email']
                    delivery_agent.payment_percentage = form.cleaned_data['payment_percentage']
                    delivery_agent.address = form.cleaned_data['address']
                    delivery_agent.area_specified = form.cleaned_data['area_specified']
                    delivery_agent.save()

                    messages.add_message(request, messages.SUCCESS, 'Delivery agent successfully updated.')
                    generate_activity_log(request, category='Delivery agent', user=form.cleaned_data['name'],
                                          action='updated')
                else:
                    mobile = form.cleaned_data['mobile'].strip()
                    if DeliveryAgent.objects.filter(mobile__exact=mobile).exists():
                        messages.add_message(request, messages.WARNING,
                                             'Delivery agent already registered with mobile number {}.'.format(mobile))
                        return redirect('addDeliveryAgent')

                    delivery_agent = form.save(commit=False)

                    code = uuid.uuid4().hex[:2].upper()
                    rand = random.randint(10, 99)
                    created_password = str(rand) + form.cleaned_data['name'].strip().replace(" ", '') + code
                    password = make_password(created_password)
                    delivery_agent.mobile = mobile

                    if form.cleaned_data['email']:
                        mail_response = send_welcome_mail(name=form.cleaned_data['name'],
                                                          user_mail=form.cleaned_data['email'], mobile=mobile,
                                                          password=created_password, flag='agent')
                        delivery_agent.password = password
                    else:
                        delivery_agent.password = make_password('password')

                    delivery_agent.save()

                    messages.add_message(request, messages.SUCCESS, 'Delivery agent successfully registered')
                    generate_activity_log(request, category='Delivery agent', user=form.cleaned_data['name'],
                                          action='registered')

                return redirect('addDeliveryAgent')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addDeliveryAgent')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during registration. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addDeliveryAgent')

    return_dict = {
        'delivery_agents': delivery_agents,
        'form': form,
        'all_area': all_area
    }
    return render(request, 'sys_admin/add_delivery_agent.html', return_dict)


@session_required_admin
def edit_delivery_agent(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = DeliveryAgent.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['name'] = data.name
            return_data['email'] = data.email
            return_data['mobile'] = data.mobile
            return_data['payment_percentage'] = data.payment_percentage
            return_data['address'] = data.address
            return_data['area_specified'] = data.area_specified.id

            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_delivery_agent(request, pk=None):
    try:
        delivery_agent = DeliveryAgent.objects.get(id=pk)
        DeliveryAgent.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Delivery Agent successfully deleted.')
        generate_activity_log(request, category='Delivery Agent', user=delivery_agent.name, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addDeliveryAgent')


@session_required_admin
def enable_delivery_agent(request, pk=None):
    try:
        if pk:
            agent = DeliveryAgent.objects.get(id=pk)
            DeliveryAgent.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Delivery Agent enabled successfully.')
            generate_activity_log(request, category='Delivery Agent', user=agent.name, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addDeliveryAgent')


@session_required_admin
def disable_delivery_agent(request, pk=None):
    try:
        if pk:
            agent = DeliveryAgent.objects.get(id=pk)
            DeliveryAgent.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Delivery Agent disabled successfully.')
            generate_activity_log(request, category='Delivery Agent', user=agent.name, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addDeliveryAgent')


@session_required_admin
def add_business(request):
    form = AddBusinessForm(request.POST or None)
    all_business = Business.objects.all().order_by('-id')
    all_area = Area.objects.filter(is_active=True).order_by('area')
    all_category = StoreCategory.objects.filter(is_active=True).order_by('store_type')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    mobile = form.cleaned_data['mobile'].strip()

                    if Business.objects.filter(~Q(id=int(request.POST.get('key'))) & Q(mobile__exact=mobile)).exists():
                        messages.add_message(request, messages.WARNING,
                                             'Business already registered with mobile number {}.'.format(mobile))
                        return redirect('addBusiness')

                    business = Business.objects.get(id=request.POST.get('key'))
                    business.name = form.cleaned_data['name']
                    business.email = form.cleaned_data['email'].strip()
                    business.mobile = mobile
                    business.address = form.cleaned_data['address']
                    business.payment_percentage = form.cleaned_data['payment_percentage']
                    business.area_specified = form.cleaned_data['area_specified']
                    business.category = form.cleaned_data['category']
                    business.manager = form.cleaned_data['manager']
                    business.manager_mobile = form.cleaned_data['manager_mobile']
                    business.secondary_mobile = form.cleaned_data['secondary_mobile']
                    business.about = form.cleaned_data['about']
                    business.save()

                    messages.add_message(request, messages.SUCCESS, 'Business successfully updated.')
                    generate_activity_log(request, category='Business', user=business.name,
                                          action='updated')
                else:
                    mobile = form.cleaned_data['mobile'].strip()
                    if Business.objects.filter(mobile__iexact=mobile).exists():
                        messages.add_message(request, messages.WARNING,
                                             'Business already registered with mobile number {}.'.format(mobile))
                        return redirect('addBusiness')

                    business = form.save(commit=False)
                    code = uuid.uuid4().hex[:2].upper()
                    rand = random.randint(10, 99)
                    created_password = str(rand) + form.cleaned_data['name'].strip().replace(" ", '') + code
                    password = make_password(created_password)
                    business.mobile = mobile

                    if form.cleaned_data['email']:
                        mail_response = send_welcome_mail(name=form.cleaned_data['name'],
                                                          user_mail=form.cleaned_data['email'], mobile=mobile,
                                                          password=created_password, flag='business')
                    else:
                        password = make_password('password')
                    business.password = password
                    business.save()

                    messages.add_message(request, messages.SUCCESS, 'Business successfully registered')

                    generate_activity_log(request, category='Business', user=form.cleaned_data['name'],
                                          action='registered')

                return redirect('addBusiness')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addBusiness')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during registration. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addBusiness')

    return_dict = {
        'all_business': all_business,
        'form': form,
        'all_area': all_area,
        'all_category': all_category,
    }
    return render(request, 'sys_admin/add_business.html', return_dict)


@session_required_admin
def edit_business(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = Business.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['name'] = data.name
            return_data['email'] = data.email
            return_data['mobile'] = data.mobile
            return_data['address'] = data.address
            return_data['payment_percentage'] = data.payment_percentage
            return_data['manager'] = data.manager
            return_data['manager_mobile'] = data.manager_mobile
            return_data['secondary_mobile'] = data.secondary_mobile
            return_data['about'] = data.about
            return_data['area_specified'] = data.area_specified.id
            return_data['category'] = data.category.id

            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_business(request, pk=None):
    try:
        business = Business.objects.get(id=pk)
        Business.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Business successfully deleted.')
        generate_activity_log(request, category='Business', user=business.name, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addBusiness')


@session_required_admin
def enable_business(request, pk=None):
    try:
        if pk:
            business = Business.objects.get(id=pk)
            Business.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Business enabled successfully.')
            generate_activity_log(request, category='Business', user=business.name, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addBusiness')


@session_required_admin
def disable_business(request, pk=None):
    try:
        if pk:
            business = Business.objects.get(id=pk)
            Business.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Business disabled successfully.')
            generate_activity_log(request, category='Business', user=business.name, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addBusiness')


@session_required_admin
def add_units(request):
    form = AddUnitForm(request.POST or None)
    all_units = Units.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if Units.objects.filter(
                            ~Q(id=request.POST.get('key')) & Q(name__iexact=form.cleaned_data['name'])).exists():
                        messages.add_message(request, messages.WARNING, 'Unit already exist')
                        return redirect('addUnit')
                    unit = Units.objects.get(id=request.POST.get('key'))
                    unit.name = form.cleaned_data['name']
                    unit.short_name = form.cleaned_data['short_name']
                    unit.save()
                    messages.add_message(request, messages.SUCCESS, 'Unit successfully updated.')
                    generate_activity_log(request, category='Unit', user=unit.name,
                                          action='updated')
                else:
                    if Units.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        messages.add_message(request, messages.WARNING, 'Unit already exist')
                        return redirect('addUnit')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Unit successfully added')
                    generate_activity_log(request, category='Unit', user=form.cleaned_data['name'],
                                          action='added')

                return redirect('addUnit')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addUnit')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addUnit')

    return_dict = {
        'all_units': all_units,
        'form': form,
    }
    return render(request, 'sys_admin/add_units.html', return_dict)


@session_required_admin
def edit_units(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = Units.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['name'] = data.name
            return_data['short_name'] = data.short_name
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_units(request, pk=None):
    try:
        unit = Units.objects.get(id=pk)
        Units.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Unit successfully deleted.')
        generate_activity_log(request, category='Unit', user=unit.name, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addUnit')


@session_required_admin
def enable_units(request, pk=None):
    try:
        if pk:
            unit = Units.objects.get(id=pk)
            Units.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Unit enabled successfully.')
            generate_activity_log(request, category='Unit', user=unit.name, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addUnit')


@session_required_admin
def disable_units(request, pk=None):
    try:
        if pk:
            unit = Units.objects.get(id=pk)
            Units.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Unit disabled successfully.')
            generate_activity_log(request, category='Unit', user=unit.name, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addUnit')


@session_required_admin
def add_store_category(request):
    form = AddStoreCategoryForm(request.POST or None, request.FILES or None)
    all_category = StoreCategory.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if StoreCategory.objects.filter(~Q(id=request.POST.get('key')) & Q(
                            store_type__iexact=form.cleaned_data['store_type'])).exists():
                        messages.add_message(request, messages.WARNING, 'Category already exist')
                        return redirect('addCategory')
                    category = StoreCategory.objects.get(id=request.POST.get('key'))
                    category.store_type = form.cleaned_data['store_type']
                    category.remarks = form.cleaned_data['remarks']
                    if form.cleaned_data['display_image']:
                        category.display_image = form.cleaned_data['display_image']
                    category.save()
                    messages.add_message(request, messages.SUCCESS, 'Category successfully updated.')
                    generate_activity_log(request, category='Category', user=category.store_type,
                                          action='updated')
                else:
                    if StoreCategory.objects.filter(store_type__exact=form.cleaned_data['store_type']).exists():
                        messages.add_message(request, messages.WARNING, 'Category already exist')
                        return redirect('addCategory')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Category successfully added')
                    generate_activity_log(request, category='Category', user=form.cleaned_data['store_type'],
                                          action='added')

                return redirect('addCategory')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addCategory')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addCategory')

    return_dict = {
        'all_category': all_category,
        'form': form,
    }
    return render(request, 'sys_admin/add_store_category.html', return_dict)


@session_required_admin
def edit_store_category(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = StoreCategory.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['store_type'] = data.store_type
            return_data['remarks'] = data.remarks
            if data.display_image:
                return_data['display_image'] = data.display_image.url
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_store_category(request, pk=None):
    try:
        category = StoreCategory.objects.get(id=pk)
        StoreCategory.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Category successfully deleted.')
        generate_activity_log(request, category='Category', user=category.store_type, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addCategory')


@session_required_admin
def enable_store_category(request, pk=None):
    try:
        if pk:
            category = StoreCategory.objects.get(id=pk)
            StoreCategory.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Category enabled successfully.')
            generate_activity_log(request, category='Category', user=category.store_type, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addCategory')


@session_required_admin
def disable_store_category(request, pk=None):
    try:
        if pk:
            category = StoreCategory.objects.get(id=pk)
            StoreCategory.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Category disabled successfully.')
            generate_activity_log(request, category='Category', user=category.store_type, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addCategory')


@session_required_admin
def add_district(request):
    form = AddDistrictForm(request.POST or None)
    all_districts = District.objects.all().order_by('-id')
    all_states = State.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if District.objects.filter(
                            ~Q(id=request.POST.get('key')) & Q(district__iexact=form.cleaned_data['district']) & Q(
                                state=form.cleaned_data['state'])).exists():
                        messages.add_message(request, messages.WARNING, 'District already exist')
                        return redirect('addDistrict')
                    district_object = District.objects.get(id=request.POST.get('key'))
                    district_object.district = form.cleaned_data['district']
                    district_object.state = form.cleaned_data['state']
                    district_object.save()
                    messages.add_message(request, messages.SUCCESS, 'District successfully updated.')
                    generate_activity_log(request, category='District', user=district_object.district,
                                          action='updated')
                else:
                    if District.objects.filter(Q(district__iexact=form.cleaned_data['district']) & Q(
                            state=form.cleaned_data['state'])).exists():
                        messages.add_message(request, messages.WARNING, 'District already exist')
                        return redirect('addDistrict')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'District successfully added')
                    generate_activity_log(request, category='District', user=form.cleaned_data['district'],
                                          action='added')

                return redirect('addDistrict')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addDistrict')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addDistrict')

    return_dict = {
        'all_districts': all_districts,
        'all_states': all_states,
        'form': form,
    }
    return render(request, 'sys_admin/add_district.html', return_dict)


@session_required_admin
def edit_district(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = District.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['state'] = data.state.id
            return_data['district'] = data.district
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_district(request, pk=None):
    try:
        district = District.objects.get(id=pk)
        District.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'District successfully deleted.')
        generate_activity_log(request, category='District', user=district.district, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addDistrict')


@session_required_admin
def enable_district(request, pk=None):
    try:
        if pk:
            district = District.objects.get(id=pk)
            District.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'District enabled successfully.')
            generate_activity_log(request, category='District', user=district.district, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addDistrict')


@session_required_admin
def disable_district(request, pk=None):
    try:
        if pk:
            district = District.objects.get(id=pk)
            District.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'District disabled successfully.')
            generate_activity_log(request, category='District', user=district.district, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addDistrict')


@session_required_admin
def add_village(request):
    form = AddVillageForm(request.POST or None)
    all_districts = District.objects.all().order_by('-id')
    all_villages = Village.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if Village.objects.filter(
                            ~Q(id=request.POST.get('key')) & Q(village__iexact=form.cleaned_data['village']) & Q(
                                district=form.cleaned_data['district'])).exists():
                        messages.add_message(request, messages.WARNING, 'Village already exist')
                        return redirect('addVillage')
                    village_object = Village.objects.get(id=request.POST.get('key'))
                    village_object.district = form.cleaned_data['district']
                    village_object.village = form.cleaned_data['village']
                    village_object.save()
                    messages.add_message(request, messages.SUCCESS, 'Village successfully updated.')
                    generate_activity_log(request, category='Village', user=village_object.village,
                                          action='updated')
                else:
                    if Village.objects.filter(Q(village__iexact=form.cleaned_data['village']) & Q(
                            district=form.cleaned_data['district'])).exists():
                        messages.add_message(request, messages.WARNING, 'Village already exist')
                        return redirect('addVillage')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Village successfully added')
                    generate_activity_log(request, category='Village', user=form.cleaned_data['village'],
                                          action='added')

                return redirect('addVillage')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addVillage')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addVillage')

    return_dict = {
        'all_districts': all_districts,
        'all_villages': all_villages,
        'form': form,
    }
    return render(request, 'sys_admin/add_village.html', return_dict)


@session_required_admin
def edit_village(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = Village.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['district'] = data.district.id
            return_data['village'] = data.village
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_village(request, pk=None):
    try:
        village = Village.objects.get(id=pk)
        Village.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Village successfully deleted.')
        generate_activity_log(request, category='Village', user=village.village, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addVillage')


@session_required_admin
def enable_village(request, pk=None):
    try:
        if pk:
            village = Village.objects.get(id=pk)
            Village.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Village enabled successfully.')
            generate_activity_log(request, category='Village', user=village.village, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addVillage')


@session_required_admin
def disable_village(request, pk=None):
    try:
        if pk:
            village = Village.objects.get(id=pk)
            Village.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Village disabled successfully.')
            generate_activity_log(request, category='Village', user=village.village, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addVillage')


@session_required_admin
def add_area(request):
    form = AddAreaForm(request.POST or None)
    all_areas = Area.objects.all().order_by('-id')
    all_villages = Village.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if Area.objects.filter(
                            ~Q(id=request.POST.get('key')) & Q(area__iexact=form.cleaned_data['area']) & Q(
                                village=form.cleaned_data['village'])).exists():
                        messages.add_message(request, messages.WARNING, 'Area already exist')
                        return redirect('addArea')
                    area_object = Area.objects.get(id=request.POST.get('key'))
                    area_object.area = form.cleaned_data['area']
                    area_object.village = form.cleaned_data['village']
                    area_object.kilometer_limit = form.cleaned_data['kilometer_limit']
                    area_object.save()
                    messages.add_message(request, messages.SUCCESS, 'Area successfully updated.')
                    generate_activity_log(request, category='Area', user=area_object.area,
                                          action='updated')
                else:
                    if Area.objects.filter(Q(area__iexact=form.cleaned_data['area']) & Q(
                            village=form.cleaned_data['village'])).exists():
                        messages.add_message(request, messages.WARNING, 'Area already exist')
                        return redirect('addArea')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Area successfully added')
                    generate_activity_log(request, category='Area', user=form.cleaned_data['area'],
                                          action='added')

                return redirect('addArea')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addArea')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addArea')

    return_dict = {
        'all_areas': all_areas,
        'all_villages': all_villages,
        'form': form,
    }
    return render(request, 'sys_admin/add_area.html', return_dict)


@session_required_admin
def edit_area(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = Area.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['kilometer_limit'] = data.kilometer_limit
            return_data['area'] = data.area
            return_data['village'] = data.village.id
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_area(request, pk=None):
    try:
        area = Area.objects.get(id=pk)
        Area.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Area successfully deleted.')
        generate_activity_log(request, category='Area', user=area.area, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addArea')


@session_required_admin
def enable_area(request, pk=None):
    try:
        if pk:
            area = Area.objects.get(id=pk)
            Area.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Area enabled successfully.')
            generate_activity_log(request, category='Area', user=area.area, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addArea')


@session_required_admin
def disable_area(request, pk=None):
    try:
        if pk:
            area = Area.objects.get(id=pk)
            Area.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Area disabled successfully.')
            generate_activity_log(request, category='Area', user=area.area, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addArea')


@session_required_admin
def enable_area_restriction(request, pk=None):
    try:
        if pk:
            area = Area.objects.get(id=pk)
            Area.objects.filter(id=pk).update(is_area_restricted_to_deliver=True)
            messages.add_message(request, messages.SUCCESS, 'Area Delivery Restriction enabled successfully.')
            generate_activity_log(request, category='Area Delivery Restriction', user=area.area, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addArea')


@session_required_admin
def disable_area_restriction(request, pk=None):
    try:
        if pk:
            area = Area.objects.get(id=pk)
            Area.objects.filter(id=pk).update(is_area_restricted_to_deliver=False)
            messages.add_message(request, messages.SUCCESS, 'Area Delivery Restriction disabled successfully.')
            generate_activity_log(request, category='Area Delivery Restriction', user=area.area, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addArea')


@session_required_admin
def add_payment_method(request):
    form = AddPaymentMethodForm(request.POST or None, request.FILES or None)
    all_payment_method = PaymentMethod.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if PaymentMethod.objects.filter(
                            ~Q(id=request.POST.get('key')) & Q(name__iexact=form.cleaned_data['name'])).exists():
                        messages.add_message(request, messages.WARNING, 'Payment Method already exist')
                        return redirect('addPaymentMethod')
                    payment_method = PaymentMethod.objects.get(id=request.POST.get('key'))
                    payment_method.name = form.cleaned_data['name']
                    payment_method.is_upi = form.cleaned_data['is_upi']
                    if form.cleaned_data['qr_code']:
                        payment_method.qr_code = form.cleaned_data['qr_code']
                    payment_method.save()
                    messages.add_message(request, messages.SUCCESS, 'Payment Method successfully updated.')
                    generate_activity_log(request, category='Payment Method', user=payment_method.name,
                                          action='updated')
                else:
                    if PaymentMethod.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        messages.add_message(request, messages.WARNING, 'Payment Method already exist')
                        return redirect('addPaymentMethod')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Payment Method successfully added')
                    generate_activity_log(request, category='Payment Method', user=form.cleaned_data['name'],
                                          action='added')

                return redirect('addPaymentMethod')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addPaymentMethod')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addPaymentMethod')

    return_dict = {
        'all_payment_method': all_payment_method,
        'form': form,
    }
    return render(request, 'sys_admin/add_payment_methods.html', return_dict)


@session_required_admin
def edit_payment_method(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = PaymentMethod.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['name'] = data.name
            return_data['is_upi'] = data.is_upi
            if data.qr_code:
                return_data['qr_code'] = data.qr_code.url
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_payment_method(request, pk=None):
    try:
        payment_method = PaymentMethod.objects.get(id=pk)
        PaymentMethod.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Payment Method successfully deleted.')
        generate_activity_log(request, category='Payment Method', user=payment_method.name, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addPaymentMethod')


@session_required_admin
def enable_payment_method(request, pk=None):
    try:
        if pk:
            payment_method = PaymentMethod.objects.get(id=pk)
            PaymentMethod.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Payment Method enabled successfully.')
            generate_activity_log(request, category='Payment Method', user=payment_method.name, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addPaymentMethod')


@session_required_admin
def disable_payment_method(request, pk=None):
    try:
        if pk:
            payment_method = PaymentMethod.objects.get(id=pk)
            PaymentMethod.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Payment Method disabled successfully.')
            generate_activity_log(request, category='Payment Method', user=payment_method.name, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addPaymentMethod')


@session_required_admin
def add_banner_image(request):
    form = AddBannerImageForm(request.POST or None, request.FILES or None)
    all_banner_image = BannerImages.objects.all().order_by('-id')
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.POST.get('key'):
                    if BannerImages.objects.filter(
                            ~Q(id=request.POST.get('key')) & Q(name__iexact=form.cleaned_data['name'])).exists():
                        messages.add_message(request, messages.WARNING, 'Banner Image already exist')
                        return redirect('addBannerImages')
                    banner_image = BannerImages.objects.get(id=request.POST.get('key'))
                    banner_image.name = form.cleaned_data['name']
                    if form.cleaned_data['image_url']:
                        banner_image.image_url = form.cleaned_data['image_url']
                    banner_image.save()
                    messages.add_message(request, messages.SUCCESS, 'Banner Image successfully updated.')
                    generate_activity_log(request, category='Banner Image', user=banner_image.name,
                                          action='updated')
                else:
                    if BannerImages.objects.filter(name__exact=form.cleaned_data['name']).exists():
                        messages.add_message(request, messages.WARNING, 'Banner Image already exist')
                        return redirect('addBannerImages')

                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Banner Image successfully added')
                    generate_activity_log(request, category='Banner Image', user=form.cleaned_data['name'],
                                          action='added')

                return redirect('addBannerImages')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
                return redirect('addBannerImages')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addBannerImages')

    return_dict = {
        'all_banner_image': all_banner_image,
        'form': form,
    }
    return render(request, 'sys_admin/add_banner_images.html', return_dict)


@session_required_admin
def edit_banner_image(request):
    return_data = {}
    id = request.GET.get('id')
    id = json.loads(id)

    if id:
        try:
            data = BannerImages.objects.get(id=int(id))
            return_data['id'] = data.id
            return_data['name'] = data.name
            if data.image_url:
                return_data['image_url'] = data.image_url.url
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


@session_required_admin
def delete_banner_image(request, pk=None):
    try:
        banner_image = BannerImages.objects.get(id=pk)
        BannerImages.objects.get(id=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Banner Image successfully deleted.')
        generate_activity_log(request, category='Banner Image', user=banner_image.name, action='deleted')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addBannerImages')


@session_required_admin
def enable_banner_image(request, pk=None):
    try:
        if pk:
            banner_image = BannerImages.objects.get(id=pk)
            BannerImages.objects.filter(id=pk).update(is_active=True)
            messages.add_message(request, messages.SUCCESS, 'Banner Image enabled successfully.')
            generate_activity_log(request, category='Banner Image', user=banner_image.name, action='enabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addBannerImages')


@session_required_admin
def disable_banner_image(request, pk=None):
    try:
        if pk:
            banner_image = BannerImages.objects.get(id=pk)
            BannerImages.objects.filter(id=pk).update(is_active=False)
            messages.add_message(request, messages.SUCCESS, 'Banner Image disabled successfully.')
            generate_activity_log(request, category='Banner Image', user=banner_image.name, action='disabled')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong! please try again later.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('addBannerImages')


@session_required_admin
def default_settings(request):
    if DefaultSettings.objects.all().exists():
        current_settings = DefaultSettings.objects.all()[0]
        form = DefaultSettingsForm(request.POST or None, instance=current_settings)
        if DefaultSettings.objects.filter(~Q(id=current_settings.id)).exists():
            DefaultSettings.objects.filter(~Q(id=current_settings.id)).delete()
    else:
        form = DefaultSettingsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Default Settings successfully updated.')
                generate_activity_log(request, category='Default Settings', user='Settings - 1',
                                      action='updated')
                return redirect('admin_home')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
            return redirect('addSettings')
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during operation. Make sure all '
                                                            'recommended fields are given.')
            return redirect('addSettings')
    return render(request, 'sys_admin/settings.html', {'form': form})


@session_required_admin
def activity_logs(request):
    if request.method == 'POST':
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')

        filter_data = {}

        if date_from and date_to:
            filter_data['created_at__date__range'] = date_from, date_to
        else:
            if date_from:
                filter_data['created_at__date__gte'] = date_from
            if date_to:
                filter_data['created_at__date__lte'] = date_to

        all_activity_logs = ActivityLogs.objects.filter(**filter_data).order_by('-id')
        all_activity_ids_search = [i.id for i in all_activity_logs]
        request.session['all_activity_ids_search'] = all_activity_ids_search
    else:
        all_activity_logs = ActivityLogs.objects.all().order_by('-id')
        all_activity_ids_search = [i.id for i in all_activity_logs]
        request.session['all_activity_ids_search'] = all_activity_ids_search

    return render(request, 'sys_admin/activity_logs.html', {'all_activity_logs': all_activity_logs})


@session_required_admin
def export_activity_logs(request):
    all_activity_ids_search = request.session['all_activity_ids_search']
    if all_activity_ids_search:
        all_activity_logs_in_session = [ActivityLogs.objects.get(id=i) for i in all_activity_ids_search]
        if all_activity_logs_in_session:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="ActivityLog-{}.xls"'.format(
                str(datetime.datetime.today().strftime("%d-%m-%Y_%H:%M:%S")))

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Activity Logs')  # this will make a sheet named Users Data

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Activity Log', 'Date']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            rows = []
            for activity in all_activity_logs_in_session:
                # column 1, 2
                row_data = [activity.activity, activity.created_at.strftime("%d %b, %Y  %I:%M %p")]
                rows.append(row_data)
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response
    else:
        messages.add_message(request, messages.WARNING, 'No activity logs to export!')
        return redirect('activityLogs')


@session_required_admin
def agent_payment_home(request):
    all_delivery_agents = DeliveryAgent.objects.filter(is_active=True).order_by('name')
    all_agent_data = []

    for i in all_delivery_agents:
        agent = DeliveryAgent.objects.get(id=i.id)
        data = {
            "agent_amount_due_cod": 0,
            "platform_amount_due_cod": 0,
            "agent_amount_due": 0,
            "all_incomplete_trans_cod_count": 0,
            "all_incomplete_trans_count": 0,
            "total_amount": 0,
            "total_gross_amount": 0,
            "agent": agent.name,
            "agent_id": agent.id,
            "area": agent.area_specified.area,
            "mobile": agent.mobile,
            "payment_percentage": agent.payment_percentage,
            "transaction_ids": [],
        }

        if AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False, is_cod=True).exists():
            all_incomplete_trans_cod = AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False,
                                                                        is_cod=True)
            data["all_incomplete_trans_cod_count"] = all_incomplete_trans_cod.count()
            for j in all_incomplete_trans_cod:
                data["agent_amount_due_cod"] = data["agent_amount_due_cod"] + j.amount
                data["platform_amount_due_cod"] = data["platform_amount_due_cod"] + j.total_order_amount + j.platform_amount
                data['transaction_ids'].append(j.id)
                data['total_gross_amount'] = data['total_gross_amount'] + j.gross_amount

        if AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False, is_cod=False).exists():
            all_incomplete_trans = AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False,
                                                                    is_cod=False)
            data["all_incomplete_trans_count"] = all_incomplete_trans.count()
            for k in all_incomplete_trans:
                data["agent_amount_due"] = data["agent_amount_due"] + k.amount
                data['transaction_ids'].append(k.id)
                data['total_gross_amount'] = data['total_gross_amount'] + k.gross_amount

        if data["all_incomplete_trans_cod_count"]:
            data["total_amount"] = data["total_amount"] - data["platform_amount_due_cod"]
        if data["all_incomplete_trans_count"]:
            if data["total_amount"] > 0:
                data["total_amount"] = data["total_amount"] - data["agent_amount_due"]
            else:
                data["total_amount"] = data["total_amount"] + data["agent_amount_due"]

        if data['transaction_ids']:
            data['transaction_ids'] = str(data['transaction_ids']).replace('[', '').replace(']', '')
        all_agent_data.append(data)

    if request.method == 'POST':
        pass

    return_dict = {
        'all_agent_data': all_agent_data,
    }
    return render(request, 'sys_admin/agent_payment_home.html', return_dict)


@session_required_admin
def agent_payment_history(request):
    all_delivery_agents = DeliveryAgent.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        delivery_agent = request.POST.get('delivery_agent')
        payment_type = request.POST.get('payment_type')

        filter_data = {}
        if delivery_agent:
            filter_data['delivery_agent'] = DeliveryAgent.objects.get(id=delivery_agent)

        if payment_type:
            if payment_type == 'debit':
                filter_data['is_debit'] = True
            else:
                filter_data['is_credit'] = True

        if date_from and date_to:
            filter_data['created__date__range'] = date_from, date_to
        else:
            if date_from:
                filter_data['created__date__gte'] = date_from
            if date_to:
                filter_data['created__date__lte'] = date_to

        all_agent_payment = AgentPayment.objects.filter(**filter_data).order_by('-id')

    else:
        all_agent_payment = AgentPayment.objects.all().order_by('-id')

    return_dict = {
        'all_agent_payment': all_agent_payment,
        'all_delivery_agents': all_delivery_agents,
    }
    return render(request, 'sys_admin/agent_payment_history.html', return_dict)


@session_required_admin
def agent_transaction_history(request):
    all_delivery_agents = DeliveryAgent.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        delivery_agent = request.POST.get('delivery_agent')
        payment_status = request.POST.get('payment_status')

        filter_data = {}
        if delivery_agent:
            filter_data['delivery_agent'] = DeliveryAgent.objects.get(id=delivery_agent)

        if payment_status:
            if payment_status == 'completed':
                filter_data['is_completed'] = True
            else:
                filter_data['is_completed'] = False

        if date_from and date_to:
            filter_data['created__date__range'] = date_from, date_to
        else:
            if date_from:
                filter_data['created__date__gte'] = date_from
            if date_to:
                filter_data['created__date__lte'] = date_to

        all_agent_transactions = AgentTransactions.objects.filter(**filter_data).order_by('-id')

    else:
        all_agent_transactions = AgentTransactions.objects.all().order_by('-id')

    return_dict = {
        'all_agent_transactions': all_agent_transactions,
        'all_delivery_agents': all_delivery_agents,
    }
    return render(request, 'sys_admin/agent_transaction_history.html', return_dict)


@session_required_admin
def agent_transaction_payment(request, tr=None, tp=None):
    if tr and tp:
        transaction = AgentTransactions.objects.get(id=tr)
        return_dict = {
            'transaction': transaction,
            'tp': tp,
            'tr': tr,
        }
        if tp == 'credit':
            if request.method == 'POST':
                try:
                    payment_obj = AgentPayment()
                    payment_obj.delivery_agent = transaction.delivery_agent
                    payment_obj.reference_id = request.POST.get('reference_id')
                    payment_obj.pay_by = request.POST.get('pay_by')
                    payment_obj.is_credit = True
                    payment_obj.is_paid = True
                    payment_obj.amount = transaction.gross_amount - transaction.amount
                    payment_obj.save()

                    transaction.is_completed = True
                    transaction.save()
                    payment_obj.transactions.add(transaction)

                    DeliveryAgentNotification(
                        message="Your payment of {} is received of delivery order {}. Feel free to contact our "
                                "support team for any issues".format(payment_obj.amount,
                                                                     transaction.delivery_order.delivery_id),
                        delivery_agent=transaction.delivery_agent,
                        url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                        header="Your payment of {} is received!".format(payment_obj.amount),
                    ).save()

                    now = datetime.datetime.now().astimezone()
                    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                    ActivityLogs(
                        activity="Payment of {} is credited to Admin Account from Agent {} in area {} on {}".format(
                            payment_obj.amount, transaction.delivery_agent.name,
                            transaction.delivery_agent.area_specified.area, formatted)
                    ).save()

                    messages.add_message(request, messages.SUCCESS, 'Amount {} is successfully credited to Admin Account!'.format(str(transaction.gross_amount - transaction.platform_amount)))
                    return redirect('agent_transaction_history')
                except Exception as e:
                    messages.add_message(request, messages.WARNING, e)
                return  redirect('agent_transaction_payment', tr=tr, tp=tp)
            return render(request, 'sys_admin/agent_transaction_payment.html', return_dict)
        elif tp == 'debit':
            if request.method == 'POST':
                try:
                    payment_obj = AgentPayment()
                    payment_obj.delivery_agent = transaction.delivery_agent
                    payment_obj.reference_id = request.POST.get('reference_id')
                    payment_obj.pay_by = request.POST.get('pay_by')
                    payment_obj.is_debit = True
                    payment_obj.is_paid = True
                    payment_obj.amount = transaction.amount
                    payment_obj.save()

                    transaction.is_completed = True
                    transaction.save()
                    payment_obj.transactions.add(transaction)

                    DeliveryAgentNotification(
                        message="A payment of {} is processed reference to delivery order {}. Feel free to contact our "
                                "support team for any issues".format(payment_obj.amount,
                                                                     transaction.delivery_order.delivery_id),
                        delivery_agent=transaction.delivery_agent,
                        url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                        header="Payment of {} is processed!".format(payment_obj.amount),
                    ).save()

                    now = datetime.datetime.now().astimezone()
                    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                    ActivityLogs(
                        activity="Payment of {} is debited from Admin Account for Agent {} in area {} on {}".format(
                            payment_obj.amount, transaction.delivery_agent.name,
                            transaction.delivery_agent.area_specified.area, formatted)
                    ).save()

                    messages.add_message(request, messages.SUCCESS,
                                         'Amount {} is successfully debited from Admin Account!'.format(
                                             str(transaction.amount)))
                    return redirect('agent_transaction_history')
                except Exception as e:
                    messages.add_message(request, messages.WARNING, e)
                return redirect('agent_transaction_payment', tr=tr, tp=tp)
            return render(request, 'sys_admin/agent_transaction_payment.html', return_dict)
    else:
        messages.add_message(request, messages.WARNING, 'Payment Type is needed to proceed payment request!')
        return redirect('agent_transaction_history')


@session_required_admin
def agent_all_pending_transaction_payment(request, trans=None, tp=None, amt=None, ag=None):
    if trans and tp and amt and ag:
        try:
            arr_trans = trans.split(',')
            transactions = AgentTransactions.objects.filter(id__in=arr_trans).order_by('id')
            agent = DeliveryAgent.objects.get(id=ag)
            return_dict = {
                'transactions': transactions,
                'amt': amt,
                'ag': ag,
                'tp': tp,
                'trans': trans,
                'agent': agent,
            }
            if tp == 'credit':
                if request.method == 'POST':
                    try:
                        payment_obj = AgentPayment()
                        payment_obj.delivery_agent = agent
                        payment_obj.reference_id = request.POST.get('reference_id')
                        payment_obj.pay_by = request.POST.get('pay_by')
                        payment_obj.is_credit = True
                        payment_obj.is_paid = True
                        payment_obj.amount = float(amt)
                        payment_obj.save()
                        for i in transactions:
                            i.is_completed = True
                            i.save()
                            payment_obj.transactions.add(i)

                        DeliveryAgentNotification(
                            message="Your payment of {} is received for all pending transactions. Feel free to "
                                    "contact our support team for any issues".format(payment_obj.amount),
                            delivery_agent=agent,
                            url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                            header="Your payment of {} is received!".format(payment_obj.amount),
                        ).save()

                        now = datetime.datetime.now().astimezone()
                        formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                        ActivityLogs(
                            activity="Payment of {} is credited to Admin Account from Agent {} in area {} on {}".format(
                                payment_obj.amount, agent.name, agent.area_specified.area, formatted)
                        ).save()

                        messages.add_message(request, messages.SUCCESS, 'All pending transactions are processed')
                        return redirect('agent_payment_home')
                    except Exception as e:
                        messages.add_message(request, messages.WARNING, e)
                    return redirect('agent_all_pending_transaction_payment', trans=trans, tp=tp, amt=amt, ag=ag)
                return render(request, 'sys_admin/agent_all_pending_transaction_payment.html', return_dict)
            elif tp == 'debit':
                if request.method == 'POST':
                    try:
                        payment_obj = AgentPayment()
                        payment_obj.delivery_agent = agent
                        payment_obj.reference_id = request.POST.get('reference_id')
                        payment_obj.pay_by = request.POST.get('pay_by')
                        payment_obj.is_debit = True
                        payment_obj.is_paid = True
                        payment_obj.amount = float(amt)
                        payment_obj.save()
                        for i in transactions:
                            i.is_completed = True
                            i.save()
                            payment_obj.transactions.add(i)

                        DeliveryAgentNotification(
                            message="A payment of {} is processed for all pending transactions. Feel free to contact "
                                    "our support team for any issues".format(payment_obj.amount),
                            delivery_agent=agent,
                            url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                            header="Payment of {} is processed!".format(payment_obj.amount),
                        ).save()

                        now = datetime.datetime.now().astimezone()
                        formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                        ActivityLogs(
                            activity="Payment of {} is debited from Admin Account for Agent {} in area {} on {}".format(
                                payment_obj.amount, agent.name, agent.area_specified.area, formatted)
                        ).save()

                        messages.add_message(request, messages.SUCCESS, 'All pending transactions are processed')
                        return redirect('agent_payment_home')
                    except Exception as e:
                        messages.add_message(request, messages.WARNING, e)
                    return redirect('agent_all_pending_transaction_payment', trans=trans, tp=tp, amt=amt, ag=ag)
                return render(request, 'sys_admin/agent_all_pending_transaction_payment.html', return_dict)
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
            return redirect('agent_payment_home')
    else:
        messages.add_message(request, messages.WARNING, 'Payment Type is needed to proceed payment request!')
        return redirect('agent_payment_home')


@session_required_admin
def business_payment_home(request):
    all_business = Business.objects.filter(is_active=True).order_by('name')
    all_business_data = []

    for i in all_business:
        business = Business.objects.get(id=i.id)
        data = {
            "amount_due": 0,
            "platform_amount": 0,
            "total_amount": 0,
            "business": business.name,
            "mobile": business.mobile,
            "area": business.area_specified.area,
            "business_id": business.id,
            "payment_percentage": business.payment_percentage,
            "all_incomplete_trans": 0,
            "transaction_ids": [],
        }
        if BusinessTransactions.objects.filter(business=business, is_completed=False).exists():
            all_incomplete_trans = BusinessTransactions.objects.filter(business=business, is_completed=False)
            data['all_incomplete_trans'] = all_incomplete_trans.count()
            for j in all_incomplete_trans:
                data['amount_due'] = data['amount_due'] + j.amount
                data['platform_amount'] = data['platform_amount'] + j.platform_amount
                data['total_amount'] = data['total_amount'] + j.total_amount
                data['transaction_ids'].append(j.id)

        if data['transaction_ids']:
            data['transaction_ids'] = str(data['transaction_ids']).replace('[', '').replace(']', '')
        all_business_data.append(data)

    if request.method == 'POST':
        pass

    return_dict = {
        'all_business_data': all_business_data,
    }
    return render(request, 'sys_admin/business_payment_home.html', return_dict)


@session_required_admin
def business_payment_history(request):
    all_business = Business.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        business = request.POST.get('business')

        filter_data = {}
        if business:
            filter_data['business'] = Business.objects.get(id=business)

        if date_from and date_to:
            filter_data['created__date__range'] = date_from, date_to
        else:
            if date_from:
                filter_data['created__date__gte'] = date_from
            if date_to:
                filter_data['created__date__lte'] = date_to

        all_business_payment = BusinessPayment.objects.filter(**filter_data).order_by('-id')
    else:
        all_business_payment = BusinessPayment.objects.all().order_by('-id')

    return_dict = {
        'all_business_payment': all_business_payment,
        'all_business': all_business,
    }
    return render(request, 'sys_admin/business_payment_history.html', return_dict)


@session_required_admin
def business_transaction_history(request):
    all_business = Business.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        business = request.POST.get('business')
        payment_status = request.POST.get('payment_status')

        filter_data = {}
        if business:
            filter_data['business'] = Business.objects.get(id=business)

        if payment_status:
            if payment_status == 'completed':
                filter_data['is_completed'] = True
            else:
                filter_data['is_completed'] = False

        if date_from and date_to:
            filter_data['created__date__range'] = date_from, date_to
        else:
            if date_from:
                filter_data['created__date__gte'] = date_from
            if date_to:
                filter_data['created__date__lte'] = date_to

        all_business_transactions = BusinessTransactions.objects.filter(**filter_data).order_by('-id')

    else:
        all_business_transactions = BusinessTransactions.objects.all().order_by('-id')

    return_dict = {
        'all_business_transactions': all_business_transactions,
        'all_business': all_business,
    }
    return render(request, 'sys_admin/business_transaction_history.html', return_dict)


@session_required_admin
def business_transaction_payment(request, tr=None):
    transaction = BusinessTransactions.objects.get(id=tr)
    return_dict = {
        'transaction': transaction,
        'tr': tr,
    }
    if request.method == 'POST':
        try:
            payment_obj = BusinessPayment()
            payment_obj.business = transaction.business
            payment_obj.reference_id = request.POST.get('reference_id')
            payment_obj.pay_by = request.POST.get('pay_by')
            payment_obj.is_paid = True
            payment_obj.amount = transaction.total_amount - transaction.platform_amount
            payment_obj.save()

            transaction.is_completed = True
            transaction.save()
            payment_obj.transactions.add(transaction)

            BusinessNotification(
                business=transaction.business,
                header='Payment of {} is processed!!'.format(payment_obj.amount),
                url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
                message="Payment of {} is processed. Feel free to contact our support team for any issues".format(payment_obj.amount)
            ).save()

            now = datetime.datetime.now().astimezone()
            formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
            ActivityLogs(
                activity="Payment of {} is debited from Admin Account for Business {} in area {} on {}".format(payment_obj.amount, transaction.transaction_id, transaction.business.name, transaction.business.area_specified.area, formatted)
            ).save()

            messages.add_message(request, messages.SUCCESS, 'Transaction {} is completed'.format(transaction.transaction_id))
            return redirect('business_transaction_history')
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('business_transaction_payment', tr=tr)
    return render(request, 'sys_admin/business_transaction_payment.html', return_dict)


@session_required_admin
def business_all_pending_transaction_payment(request, trans=None, amt=None, bs=None):
    try:
        arr_trans = trans.split(',')
        transactions = BusinessTransactions.objects.filter(id__in=arr_trans).order_by('id')
        business = Business.objects.get(id=bs)
        return_dict = {
            'transactions': transactions,
            'amt': amt,
            'bs': bs,
            'trans': trans,
            'business': business,
        }
        if request.method == 'POST':
            try:
                payment_obj = BusinessPayment()
                payment_obj.business = business
                payment_obj.reference_id = request.POST.get('reference_id')
                payment_obj.pay_by = request.POST.get('pay_by')
                payment_obj.is_paid = True
                payment_obj.amount = float(amt)
                payment_obj.save()
                for i in transactions:
                    i.is_completed = True
                    i.save()
                    payment_obj.transactions.add(i)

                BusinessNotification(
                    business=business,
                    header='Payment of {} is processed!!'.format(payment_obj.amount),
                    url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
                    message="Payment of {} is processed. Feel free to contact our support team for any issues".format(payment_obj.amount)
                ).save()

                now = datetime.datetime.now().astimezone()
                formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                ActivityLogs(
                    activity="Payment of {} is debited from Admin Account for Business {} in area {} on {}".format(
                        payment_obj.amount, request.POST.get('reference_id'), business.name,
                        business.area_specified.area, formatted)
                ).save()

                messages.add_message(request, messages.SUCCESS, 'All pending transactions are processed')
                return redirect('business_payment_home')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
            return redirect('business_all_pending_transaction_payment', trans=trans, amt=amt, bs=bs)
        return render(request, 'sys_admin/business_all_pending_transaction_payment.html', return_dict)
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
        return redirect('business_payment_home')


# Admin Functions End Here
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================

# User Functions Start Here
# ----------------------------------------------------------------------------------------------------------------------
def session_required_user(function):
    def _function(request, *args, **kwargs):
        if request.session.get('user') is None:
            return redirect('user_login')
        else:
            return function(request, *args, **kwargs)

    return _function


def login_from_session_user(request):
    if request.session.has_key('user'):
        if request.session['user']:
            return redirect('user_home', ar=request.session['user']['area'])
    return redirect('user_login')


class getLoginUser(View):
    def get(self, request):
        form = CommonUserForm(request.POST or None)
        all_village = Village.objects.filter(is_active=True).order_by('village')
        all_area = Area.objects.filter(is_active=True).order_by('area')
        all_security_questions = SecurityQuestions.objects.filter(is_active=True).order_by('name')
        return_dict = {
            'form': form,
            'all_village': all_village,
            'all_area': all_area,
            'all_security_questions': all_security_questions,
        }
        return render(request, "user/login_page.html", return_dict)

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        record = CommonUser.objects.filter(mobile=mobile).exists()
        if not record:
            messages.add_message(request, messages.WARNING, 'User does not exist in this mobile number')
            return redirect('user_login')
        common_user_obj = CommonUser.objects.get(mobile__iexact=mobile)
        match_password = check_password(password, common_user_obj.password)
        if match_password:
            request.session['user'] = {
                'id': common_user_obj.id,
                'name': common_user_obj.name,
                'mobile': common_user_obj.mobile,
                'area': common_user_obj.area_specified.id,
            }
            return redirect('user_home', ar=common_user_obj.area_specified.id)
        else:
            messages.add_message(request, messages.WARNING, 'Username or password mismatch')
            return redirect('user_login')


def logout_user(request):
    del request.session['user']
    return redirect('user_index')


# def register_user(request):
#     form = CommonUserForm(request.POST or None)
#     all_village = Village.objects.filter(is_active=True).order_by('village')
#     all_area = Area.objects.filter(is_active=True).order_by('area')
#     all_security_questions = SecurityQuestions.objects.filter(is_active=True).order_by('name')
#     if request.method == 'POST':
#         if form.is_valid():
#             try:
#                 if CommonUser.objects.filter(mobile__iexact=form.cleaned_data['mobile']).exists():
#                     messages.add_message(request, messages.WARNING,
#                                          'User already registered with {}'.format(form.cleaned_data['mobile']))
#                     return redirect('user_register')
#
#                 password = request.POST.get('password')
#                 conf_password = request.POST.get('conf_password')
#                 if password != conf_password:
#                     messages.add_message(request, messages.WARNING, 'Password mismatched')
#                     return redirect('user_register')
#                 user = form.save(commit=False)
#                 user.password = make_password(password)
#                 user.area_specified = Area.objects.get(id=int(request.POST.get('area')))
#                 user.save()
#
#                 messages.add_message(request, messages.SUCCESS, 'Your registration successfully completed')
#                 create_activity_log(request, category='User', user=form.cleaned_data['name'], action='registered')
#                 return redirect('user_index')
#             except Exception as e:
#                 messages.add_message(request, messages.WARNING, e)
#                 return redirect('user_register')
#         else:
#             messages.add_message(request, messages.WARNING, 'Something went wrong during registration. Make sure all '
#                                                             'recommended fields are given.')
#             return redirect('user_register')
#
#     return_dict = {
#         'form': form,
#         'all_village': all_village,
#         'all_area': all_area,
#         'all_security_questions': all_security_questions,
#     }
#     return render(request, "user/registration.html", return_dict)


def register_user(request):
    form = CommonUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                if CommonUser.objects.filter(mobile__iexact=form.cleaned_data['mobile']).exists():
                    messages.add_message(request, messages.WARNING,
                                         'User already registered with {}'.format(form.cleaned_data['mobile']))
                    return redirect('user_login')

                password = request.POST.get('password')
                conf_password = request.POST.get('conf_password')
                if password != conf_password:
                    messages.add_message(request, messages.WARNING, 'Password mismatched')
                    return redirect('user_login')
                user = form.save(commit=False)
                user.password = make_password(password)
                user.area_specified = Area.objects.get(id=int(request.POST.get('area')))
                if request.POST.get('security_question'):
                    user.security_question = SecurityQuestions.objects.get(id=int(request.POST.get('security_question')))
                user.save()

                messages.add_message(request, messages.SUCCESS, 'Your registration successfully completed')
                create_activity_log(request, category='User', user=form.cleaned_data['name'], action='registered')
                return redirect('user_index')
            except Exception as e:
                messages.add_message(request, messages.WARNING, e)
        else:
            messages.add_message(request, messages.WARNING, 'Something went wrong during registration. Make sure all '
                                                            'recommended fields are given.')
    else:
        messages.add_message(request, messages.WARNING, 'Invalid request')

    return redirect('user_login')


def get_area_of_village(request):
    return_data = {}
    village_id = request.GET.get('village_id')
    village_id = json.loads(village_id)
    if village_id:
        try:
            data = Area.objects.filter(village=int(village_id))
            area = []
            for i in data:
                state_data = {
                    'id': i.id,
                    'name': i.area
                }
                area.append(state_data)
            return_data['data'] = area
            return_data['status'] = 'SUCCESS'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['data'] = None
            return_data['error'] = e
    else:
        return_data['status'] = 'FAILED'
        return_data['data'] = None
        return_data['error'] = 'Primary key is not valid'

    return JsonResponse(return_data)


def reset_password(request):
    request.session['RESET_PASSWORD'] = {}
    if request.method == 'POST':
        try:
            if request.POST.get('email') and request.POST.get('mobile'):
                if CommonUser.objects.filter(email__iexact=request.POST.get('email'),
                                             mobile=request.POST.get('mobile')).exists():
                    user = CommonUser.objects.get(email__iexact=request.POST.get('email'),
                                                  mobile=request.POST.get('mobile'))
                    request.session['RESET_PASSWORD']['OTP'] = random.randint(1000, 9999)
                    expire = datetime.datetime.now().astimezone() + datetime.timedelta(minutes=5)
                    request.session['RESET_PASSWORD']['EXPIRE'] = float(expire.timestamp())

                    subject = "Reset password verification!"
                    message = "<p>Hello,<br><br>Your reset password request is successfully placed. Please provide " \
                              "below <strong>OTP</strong> for verification.</p><br><h3>" \
                              "OTP&nbsp;&nbsp;=&nbsp;&nbsp;{}</h3><br><p>Please note that" \
                              " this OTP will expire in 5 minutes</p>".format(request.session['RESET_PASSWORD']['OTP'])
                    send_mail(subject=subject, recipient_list=[request.POST.get('email')],
                              from_email=settings.EMAIL_HOST_USER, message=message, html_message=message)
                    return redirect('verify_otp', pk=user.id)
                else:
                    messages.add_message(request, messages.WARNING,
                                         'No user registered with this mobile number and email!')
            else:
                messages.add_message(request, messages.WARNING, 'Registered email and mobile is required!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('reset_password')
    return render(request, 'user/reset_password_start.html', {})


def password_change_request(request):
    if request.method == 'POST':
        try:
            if request.POST.get('mobile'):
                if CommonUser.objects.filter(mobile__iexact=request.POST.get('mobile')).exists():
                    user = CommonUser.objects.get(mobile__iexact=request.POST.get('mobile'))
                    if user.security_question and user.answer:
                        return redirect('security_question_valid', pk=user.id)
                    else:
                        messages.add_message(request, messages.WARNING, "Sorry! You didn't selected security question "
                                                                        "during registration, you can't process this "
                                                                        "request")
                else:
                    messages.add_message(request, messages.WARNING, 'No user registered with this mobile number!')
            else:
                messages.add_message(request, messages.WARNING, 'Registered mobile number is required!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('password_change_request')
    return render(request, 'user/password_change_request.html', {})


def security_question_valid(request, pk=None):
    user = CommonUser.objects.get(id=pk)
    if request.method == 'POST':
        try:
            if request.POST.get('answer') == user.answer:
                messages.add_message(request, messages.SUCCESS, 'Your answer is verified!')
                return redirect('set_new_password', pk=user.id)
            else:
                messages.add_message(request, messages.WARNING, 'You entered answer is wrong!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('security_question_valid', pk=pk)
    return render(request, 'user/security_question_valid.html', {'user': user, 'pk': pk})


def email_otp_verification(request, pk=None):
    if request.method == 'POST':
        try:
            otp = request.POST.get('otp_value')
            expire_time = datetime.datetime.fromtimestamp(request.session['RESET_PASSWORD']['EXPIRE'])
            if expire_time:
                if datetime.datetime.now().astimezone() < expire_time.astimezone():
                    if int(otp) == int(request.session['RESET_PASSWORD']['OTP']):
                        messages.add_message(request, messages.SUCCESS, 'OTP is verified!')
                        request.session['RESET_PASSWORD'] = {}
                        return redirect('set_new_password', pk=pk)
                    else:
                        messages.add_message(request, messages.WARNING, 'Entered OTP is invalid!')
                else:
                    messages.add_message(request, messages.WARNING, 'Entered OTP is expired! Please resend OTP')
                    request.session['RESET_PASSWORD'] = {}
            else:
                messages.add_message(request, messages.WARNING, 'Entered OTP is expired! Please resend OTP')
                request.session['RESET_PASSWORD'] = {}
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('verify_otp', pk=pk)
    return render(request, 'user/otp_verification.html', {'pk': pk})


def resend_otp(request, pk=None):
    user = CommonUser.objects.get(id=pk)
    request.session['RESET_PASSWORD'] = {}
    request.session['RESET_PASSWORD']['OTP'] = random.randint(1000, 9999)
    expire = datetime.datetime.now().astimezone() + datetime.timedelta(minutes=5)
    request.session['RESET_PASSWORD']['EXPIRE'] = expire.timestamp()

    subject = "Reset password verification!"
    message = "<p>Hello,<br><br>Your reset password request is successfully placed. Please provide " \
              "below <strong>OTP</strong> for verification.</p><br><h3>" \
              "OTP&nbsp;&nbsp;=&nbsp;&nbsp;{}</h3><br><p>Please note that" \
              " this OTP will expire in 5 minutes</p>".format(request.session['RESET_PASSWORD']['OTP'])
    send_mail(subject=subject, recipient_list=[user.email],
              from_email=settings.EMAIL_HOST_USER, message=message, html_message=message)
    return redirect('verify_otp', pk=pk)


def set_new_password(request, pk=None):
    if request.method == 'POST':
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        if password and conf_password:
            if password != conf_password:
                messages.add_message(request, messages.WARNING, 'Password mismatched')
                return redirect('set_new_password', pk=pk)
            user = CommonUser.objects.get(id=pk)
            user.password = make_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password is successfully changed!')
            return redirect('user_login')
        else:
            messages.add_message(request, messages.WARNING, 'Password is required!')
            return redirect('set_new_password', pk=pk)
    return render(request, 'user/reset_password_main.html', {'pk': pk})


def check_user_mobile(request):
    return_data = {}
    mobile = request.GET.get('mobile')
    mobile = json.loads(mobile)
    if mobile:
        try:
            if CommonUser.objects.filter(mobile__iexact=mobile).exists():
                return_data['status'] = 'FAILED'
                return_data['message'] = 'A user already registered with this mobile'
            else:
                return_data['status'] = 'SUCCESS'
                return_data['message'] = 'ok'
        except Exception as e:
            return_data['status'] = 'SYSTEM-FAILED'
            return_data['error'] = e
    else:
        return_data['status'] = 'SYSTEM-FAILED'
        return_data['error'] = 'Mobile is not valid'
    return JsonResponse(return_data)


@session_required_user
def user_home(request, ar=None):
    if request.method == 'POST':
        if 'change_area' in request.POST:
            area = request.POST.get('area')
            if area:
                return redirect('user_home', ar=area)

    all_banner_images = BannerImages.objects.filter(is_active=True)
    all_area = Area.objects.filter(is_active=True).order_by('area', 'village__village')
    all_category = StoreCategory.objects.filter(is_active=True).order_by('store_type')

    current_area_obj = Area.objects.get(id=ar)
    all_business_in_area = Business.objects.filter(area_specified=current_area_obj, is_active=True).order_by('name')

    all_category_to_display = []
    for i in all_category:
        for j in all_business_in_area:
            if j.category == i:
                if i not in all_category_to_display:
                    all_category_to_display.append(i)

    return_dict = {
        'all_banner_images': all_banner_images,
        'all_area': all_area,
        'all_category_to_display': all_category_to_display,
        'ar': ar,
    }

    return render(request, "user/homepage.html", return_dict)


@csrf_exempt
@session_required_user
def user_fcm_token_save(request):
    token = request.POST.get("token")
    try:
        if token:
            user = CommonUser.objects.get(id=request.session['user']['id'])
            user.fcm_token = token
            user.save()

            return HttpResponse("True")
        else:
            pass
    except Exception as e:
        print(e)
        pass

    return HttpResponse("False")


@session_required_user
def business_list(request, category=None, ar=None):
    if request.method == 'POST':
        pass

    all_banner_images = BannerImages.objects.filter(is_active=True)
    all_area = Area.objects.filter(is_active=True).order_by('area', 'village__village')
    all_category = StoreCategory.objects.filter(is_active=True).order_by('store_type')

    current_area_obj = Area.objects.get(id=ar)
    current_category_obj = StoreCategory.objects.get(id=category)
    all_business_in_area = Business.objects.filter(area_specified=current_area_obj, is_active=True).order_by('name')
    all_business_in_area_with_category = Business.objects.filter(area_specified=current_area_obj,
                                                                 category=current_category_obj,
                                                                 is_active=True).order_by('name')

    is_address_added = False
    common_user = CommonUser.objects.get(id=request.session['user']['id'])
    if common_user.address:
        is_address_added = True

    all_category_to_display = []
    for i in all_category:
        for j in all_business_in_area:
            if j.category == i:
                if i not in all_category_to_display:
                    all_category_to_display.append(i)

    return_dict = {
        'all_category_to_display': all_category_to_display,
        'all_banner_images': all_banner_images,
        'all_area': all_area,
        'all_business_in_area_with_category': all_business_in_area_with_category,
        'ar': ar,
        'category': category,
        'is_address_added': is_address_added,
    }

    return render(request, "user/business_list.html", return_dict)


@session_required_user
def new_order(request, shop=None):
    business = Business.objects.get(id=int(shop))
    order_details_formset = formset_factory(OrderDetailsForm)
    formset = order_details_formset(request.POST or None)
    form = OrderUploadForm(request.POST or None, request.FILES or None)

    all_category = StoreCategory.objects.filter(is_active=True)
    all_business_in_area = Business.objects.filter(area_specified=business.area_specified, is_active=True)
    all_category_to_display = []
    for i in all_category:
        for j in all_business_in_area:
            if j.category == i:
                if i not in all_category_to_display:
                    all_category_to_display.append(i)

    if request.method == 'POST':
        try:
            if 'by_form' in request.POST:
                if formset.is_valid():
                    order_obj = Order()
                    order_obj.common_user = CommonUser.objects.get(id=request.session['user']['id'])
                    order_obj.business = business
                    order_obj.order_type = 1
                    order_obj.status = 1
                    order_obj.save()
                    for fr in formset:
                        order_details_obj = fr.save()
                        order_obj.order_details.add(order_details_obj)

                    BusinessNotification(
                        business=business,
                        order=order_obj,
                        header='New order is opened!!',
                        url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
                        message="An order {} opened by a user {}, please review as soon as possible".format(
                            order_obj.order_id, order_obj.common_user.name)
                    ).save()

                    now = datetime.datetime.now().astimezone()
                    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                    ActivityLogs(
                        activity="An Order {}(using form) opened by {} from {} in {} area on {}".format(
                            order_obj.order_id,
                            order_obj.common_user.name,
                            business.name,
                            business.area_specified.area,
                            formatted)
                    ).save()

                    messages.add_message(request, messages.SUCCESS,
                                         'Your order to {} is now open and {} will review the order and send updates!'.format(
                                             order_obj.order_id, business.name))
                    return redirect('user_home', ar=business.area_specified.id)
                else:
                    messages.add_message(request, messages.WARNING,
                                         'Unable to process the request. '
                                         'Make sure you entered proper values')
                    return redirect('new_order', shop=shop)

            elif 'by_upload_sheet' in request.POST:
                if form.is_valid():
                    order_obj = form.save(commit=False)
                    order_obj.common_user = CommonUser.objects.get(id=request.session['user']['id'])
                    order_obj.business = business
                    order_obj.order_type = 2
                    order_obj.status = 1
                    order_obj.save()

                    BusinessNotification(
                        business=business,
                        order=order_obj,
                        header='New order is opened!!',
                        url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
                        message="An order {} opened by a user {}, please review as soon as possible".format(
                            order_obj.order_id, order_obj.common_user.name)
                    ).save()

                    now = datetime.datetime.now().astimezone()
                    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                    ActivityLogs(
                        activity="An Order {}(using upload sheet) opened by {} from {} in {} area on {}".format(
                            order_obj.order_id,
                            order_obj.common_user.name,
                            business.name,
                            business.area_specified.area,
                            formatted
                        )
                    ).save()

                    messages.add_message(request, messages.SUCCESS,
                                         'Your order to {} is now open and {} will review the order and send updates!'.format(
                                             order_obj.order_id, business.name))
                    return redirect('user_home', ar=business.area_specified.id)
                else:
                    messages.add_message(request, messages.WARNING,
                                         'Unable to process the request. '
                                         'Make sure you entered proper values')
                    return redirect('new_order', shop=shop)
            else:
                messages.add_message(request, messages.WARNING, 'Please choose any method to order, you can order by '
                                                                'using form, upload sheet and by call')
                return redirect('new_order', shop=shop)
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('new_order', shop=shop)

    return_dict = {
        'shop': shop,
        'business': business,
        'formset': formset,
        'ar': business.area_specified.id,
        'all_category_to_display': all_category_to_display,
        'form': form,
    }

    return render(request, 'user/new_order.html', return_dict)


@session_required_user
def new_order_by_call(request):
    return_data = {}
    business_id = request.GET.get('business_id')
    business_id = json.loads(business_id)
    if business_id:
        try:
            order_obj = Order()
            business = Business.objects.get(id=int(business_id))
            order_obj.common_user = CommonUser.objects.get(id=request.session['user']['id'])
            order_obj.business = business
            order_obj.order_type = 3
            order_obj.status = 1
            order_obj.save()
            return_data['status'] = 'SUCCESS'
            return_data['area_id'] = int(business.area_specified.id)
            return_data['message'] = 'Order successfully opened'

            BusinessNotification(
                business=business,
                order=order_obj,
                header='New order is opened!!',
                url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
                message="An order {} opened by a user {}, please review as soon as possible".format(order_obj.order_id,
                                                                                                    order_obj.common_user.name)
            ).save()

            now = datetime.datetime.now().astimezone()
            formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
            ActivityLogs(
                activity="An Order {}(using call) opened by {} from {} in {} area on {}".format(order_obj.order_id,
                                                                                                order_obj.common_user.name,
                                                                                                business.name,
                                                                                                business.area_specified.area,
                                                                                                formatted)).save()

        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = str(e)
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Business id is required!'
    return JsonResponse(return_data)


@session_required_user
def order_confirmation(request, order=None):
    order_object = Order.objects.get(id=order)
    if request.method == 'POST':
        try:
            def_settings = None
            try:
                def_settings = DefaultSettings.objects.all()[0]
            except IndexError:
                pass

            order_object = Order.objects.get(id=order)
            if order_object.order_type == 1:
                all_order_items = order_object.order_details.all()
                tot_weight = 0.0
                for i in all_order_items:
                    if i.unit.short_name == 'KG' or i.unit.short_name == 'G':
                        if i.unit.short_name == 'KG':
                            tot_weight = tot_weight + i.quantity
                        if i.unit.short_name == 'G':
                            tot_weight = tot_weight + i.quantity / 1000
                    else:
                        if def_settings:
                            tot_weight = tot_weight + i.quantity * def_settings.average_weight_of_normal_item / 1000
                        else:
                            tot_weight = tot_weight + i.quantity * 0.3

                order_object.total_weight_in_kg = tot_weight
            else:
                pass

            order_object.status = 4
            if def_settings:
                if order_object.total_weight_in_kg > float(def_settings.normal_order_weight_limit):
                    order_object.expected_delivery_charge = def_settings.bulky_order_delivery_charge
                else:
                    order_object.expected_delivery_charge = def_settings.normal_order_delivery_charge
            else:
                order_object.expected_delivery_charge = 20.0

            order_object.save()

            now = datetime.datetime.now().astimezone()
            formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
            ActivityLogs(activity="Order {} confirmed by {} from {} in {} area on {}".format(order_object.order_id,
                                                                                             order_object.common_user.name,
                                                                                             order_object.business.name,
                                                                                             order_object.business.area_specified.area,
                                                                                             formatted)).save()

            messages.add_message(request, messages.SUCCESS, "You successfully proceed the order")
            return redirect('order_placed', order=order)
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))

        return redirect('order_confirmation', order=order)

    return_dict = {
        'order_object': order_object,
        'order': order,
    }
    return render(request, "user/order_confirm.html", return_dict)


@session_required_user
def order_placed(request, order=None):
    order_object = Order.objects.get(id=order)
    if request.method == 'POST':
        try:
            Order.objects.filter(id=int(order)).update(status=5)
            order_object = Order.objects.get(id=int(order))

            BusinessNotification(
                business=order_object.business,
                order=order_object,
                header='Order {} is placed!!'.format(order_object.order_id),
                url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
                message="Order {} is placed by {}".format(order_object.order_id,
                                                          order_object.common_user.name)
            ).save()

            now = datetime.datetime.now().astimezone()
            formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
            ActivityLogs(activity="Order {} placed by {} from {} in {} area on {}".format(order_object.order_id,
                                                                                          order_object.common_user.name,
                                                                                          order_object.business.name,
                                                                                          order_object.business.area_specified.area,
                                                                                          formatted)).save()

            messages.add_message(request, messages.SUCCESS,
                                 "Order {} successfully placed".format(order_object.order_id))
            return redirect('user_home', ar=request.session['user']['area'])
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))

        return redirect('order_placed', order=order)

    return_dict = {
        'order_object': order_object,
        'order': order,
    }
    return render(request, "user/order_place.html", return_dict)


@session_required_user
def order_details(request, order=None):
    order_object = Order.objects.get(id=order)
    if request.method == 'POST':
        pass
    return_dict = {
        'order_object': order_object,
        'order': order,
    }
    return render(request, "user/order_details.html", return_dict)


@session_required_user
def cancel_order(request, order=None):
    try:
        order_object = Order.objects.get(id=order)
        Order.objects.filter(id=order).update(status=12)
        messages.add_message(request, messages.SUCCESS, 'Order {} is cancelled.'.format(order_object.order_id))

        BusinessNotification(
            business=order_object.business,
            order=order_object,
            header='Order {} is cancelled!!'.format(order_object.order_id),
            url=settings.BASE_URL_DEF + reverse('business_notifications').replace('/', ''),
            message="Order {} is cancelled by {}".format(order_object.order_id,
                                                         order_object.common_user.name)
        ).save()

        now = datetime.datetime.now().astimezone()
        formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
        ActivityLogs(activity="An Order {} is cancelled by {} from {} in {} area on {}".format(order_object.order_id,
                                                                                               order_object.common_user.name,
                                                                                               order_object.business.name,
                                                                                               order_object.business.area_specified.area,
                                                                                               formatted)).save()
    except Exception as e:
        messages.add_message(request, messages.WARNING, e)
    return redirect('user_home', ar=request.session['user']['area'])


@session_required_user
def my_orders(request):
    if request.method == 'POST':
        try:
            common_user = CommonUser.objects.get(id=request.session['user']['id'])

            status = request.POST.get('status')
            order_type = request.POST.get('order_type')
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'common_user': common_user}
            if status:
                filter_data['status'] = int(status)

            if order_type:
                filter_data['order_type'] = int(order_type)

            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_orders = Order.objects.filter(**filter_data).order_by('-id', '-status')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('my_orders')
    else:
        common_user = CommonUser.objects.get(id=request.session['user']['id'])
        all_orders = Order.objects.filter(common_user=common_user).order_by('-id', '-status')[:20]

    return_dict = {
        'all_orders': all_orders,
        'common_user': common_user,
    }
    return render(request, "user/my_orders.html", return_dict)


@session_required_user
def user_delivery_home(request):
    if request.method == 'POST':
        try:
            common_user = CommonUser.objects.get(id=request.session['user']['id'])

            status = request.POST.get('status')
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'common_user': common_user}
            if status:
                filter_data['status'] = int(status)

            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_delivery_orders = OrderDelivery.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('delivery_history')

    else:
        common_user = CommonUser.objects.get(id=request.session['user']['id'])
        all_delivery_orders = OrderDelivery.objects.filter(common_user=common_user).order_by('-id')[:20]

    return_dict = {
        'all_delivery_orders': all_delivery_orders,
    }
    return render(request, "user/delivery.html", return_dict)


@session_required_user
def user_delivery_details(request, delivery=None):
    delivery_object = OrderDelivery.objects.get(id=delivery)
    if request.method == 'POST':
        pass
    return_dict = {
        'delivery_object': delivery_object,
    }
    return render(request, "user/delivery_details.html", return_dict)


@session_required_user
def user_profile(request):
    common_user = CommonUser.objects.get(id=request.session['user']['id'])
    all_village = Village.objects.filter(is_active=True).order_by('village')
    all_area = Area.objects.filter(is_active=True).order_by('area')
    form = UserProfileForm(request.POST or None, instance=common_user)
    if request.method == 'POST':
        try:
            if form.is_valid() and request.POST.get('area_specified'):
                if CommonUser.objects.filter(
                        ~Q(id=request.session['user']['id']) & Q(mobile=form.cleaned_data.get('mobile'))).exists():
                    messages.add_message(request, messages.WARNING, 'User is already exist with this mobile number')
                    return redirect('user_profile')

                user_obj = form.save(commit=False)
                area_specified = Area.objects.get(id=int(request.POST.get('area_specified')))
                user_obj.area_specified = area_specified
                user_obj.save()

                request.session['user'] = {
                    'id': user_obj.id,
                    'name': user_obj.name,
                    'mobile': user_obj.mobile,
                    'area': user_obj.area_specified.id,
                }

                messages.add_message(request, messages.SUCCESS, 'Your profile is successfully updated')
                return redirect('user_home', ar=user_obj.area_specified.id)
            else:
                messages.add_message(request, messages.WARNING, 'Unable to process the request. Make sure you entered '
                                                                'proper values')
                return redirect('user_profile')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('user_profile')

    return_dict = {
        'form': form,
        'all_village': all_village,
        'all_area': all_area,
        'common_user': common_user,
    }
    return render(request, "user/profile.html", return_dict)


@session_required_user
def user_notifications(request):
    common_user = CommonUser.objects.get(id=request.session['user']['id'])
    notification_count = UserNotifications.objects.filter(common_user=common_user, is_read=False).count()
    if notification_count:
        if notification_count < 15:
            all_notifications = UserNotifications.objects.filter(common_user=common_user).order_by('-id')[:15]
        else:
            all_notifications = UserNotifications.objects.filter(common_user=common_user).order_by('-id')[
                                :int(notification_count)]
    else:
        all_notifications = UserNotifications.objects.filter(common_user=common_user).order_by('-id')[:15]
    if request.method == 'POST':
        pass

    return_dict = {
        'all_notifications': all_notifications,
    }
    return render(request, "user/notifications.html", return_dict)


@session_required_user
def update_user_notification(request):
    return_data = {}
    notification_id = request.GET.get('id')
    notification_id = json.loads(notification_id)
    if notification_id:
        try:
            if UserNotifications.objects.filter(id=int(notification_id)).exists():
                user_notify = UserNotifications.objects.get(id=int(notification_id))
                if not user_notify.is_read:
                    user_notify.is_read = True
                    user_notify.save()
                else:
                    return_data['status'] = 'FAILED'
                    return_data['error'] = 'Notification is already updated'
            else:
                return_data['status'] = 'FAILED'
                return_data['error'] = 'No notification is found by this id'
        except Exception as e:
            return_data['status'] = 'FAILED'
            return_data['error'] = str(e)
    else:
        return_data['status'] = 'FAILED'
        return_data['error'] = 'Notification id is required!'
    return JsonResponse(return_data)


@session_required_user
def update_user_notification(request):
    return_data = {}
    common_user = CommonUser.objects.get(id=request.session['user']['id'])
    try:
        if UserNotifications.objects.filter(common_user=common_user, is_read=False).exists:
            UserNotifications.objects.filter(common_user=common_user, is_read=False).update(is_read=True)
            return_data['status'] = 'SUCCESS'
            return_data['error'] = 'All unread notifications are updated'
        else:
            return_data['status'] = 'FAILED'
            return_data['error'] = 'Notifications are already read'
    except Exception as e:
        return_data['status'] = 'FAILED'
        return_data['error'] = str(e)

    return JsonResponse(return_data)


@session_required_user
def get_user_unread_notification(request):
    return_data = {
        'notification_count': 0,
    }
    try:
        common_user = CommonUser.objects.get(id=request.session['user']['id'])
        if UserNotifications.objects.filter(common_user=common_user, is_read=False).exists:
            notification_count = UserNotifications.objects.filter(common_user=common_user, is_read=False).count()
            return_data['notification_count'] = notification_count
            return_data['status'] = 'SUCCESS'
        else:
            return_data['status'] = 'FAILED'
            return_data['error'] = 'No notifications'
    except Exception as e:
        return_data['status'] = 'FAILED'
        return_data['error'] = str(e)
    return JsonResponse(return_data)


# User Functions End Here
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================


# Business Functions Start Here
# ----------------------------------------------------------------------------------------------------------------------
def session_required_business(function):
    def _function(request, *args, **kwargs):
        if request.session.get('business') is None:
            return redirect('business_login')
        else:
            return function(request, *args, **kwargs)

    return _function


def login_from_session_business(request):
    if request.session.has_key('business'):
        if request.session['business']:
            return redirect('business_home')
    return redirect('business_login')


class getLoginBusiness(View):
    def get(self, request):
        return render(request, "business/login_page.html", {})

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        record = Business.objects.filter(mobile__iexact=mobile).exists()
        if not record:
            messages.add_message(request, messages.WARNING, 'Business does not exist in this mobile number')
            return redirect('business_login')
        business = Business.objects.get(mobile__iexact=mobile)
        match_password = check_password(password, business.password)
        if match_password:
            request.session['business'] = {
                'id': business.id,
                'email': business.email,
                'name': business.name,
                'mobile': business.mobile,
            }
            return redirect('business_home')
        else:
            messages.add_message(request, messages.WARNING, 'Username or password mismatch')
            return redirect('business_login')


def logout_business(request):
    del request.session['business']
    return redirect('business_index')


@session_required_business
def business_home(request):
    business = Business.objects.get(id=request.session['business']['id'])
    all_orders_opened = Order.objects.filter(business=business, status=1).order_by('-id')
    all_orders_placed = Order.objects.filter(business=business, status=5).order_by('-id')

    return_dict = {
        'all_orders_opened': all_orders_opened,
        'all_orders_placed': all_orders_placed,
        'business': business,
    }

    return render(request, 'business/business_dash.html', return_dict)


@csrf_exempt
@session_required_business
def business_fcm_token_save(request):
    token = request.POST.get("token")
    try:
        if token:
            business = Business.objects.get(id=request.session['business']['id'])
            business.fcm_token = token
            business.save()
            return HttpResponse("True")
        else:
            print("token is required!!")
            pass
    except Exception as e:
        print(e)
        pass
    return HttpResponse("False")


@session_required_business
def review_order(request, order=None, order_type=None):
    try:
        order_object = Order.objects.get(id=order)
        return_dict = {
            'order_object': order_object,
            'order': order,
            'order_type': order_type,
        }
        if order_type == 1:
            if request.method == 'POST':
                try:
                    if request.POST.get('total'):
                        all_items_in_order = order_object.order_details.all()
                        for i in all_items_in_order:
                            if 'price_{}'.format(i.id) in request.POST:
                                if request.POST.get('price_{}'.format(i.id)):
                                    i.price = float(request.POST.get('price_{}'.format(i.id)))
                                    i.save()

                        order_object.order_amount = float(request.POST.get('total'))
                        order_object.status = 2
                        order_object.save()
                        messages.add_message(request, messages.SUCCESS,
                                             'Order {} successfully reviewed'.format(order_object.order_id))

                        UserNotifications(
                            common_user=order_object.common_user,
                            order=order_object,
                            header='Your order {} is reviewed!!!'.format(order_object.order_id),
                            url=settings.BASE_URL_DEF + reverse('user_notifications').replace('/', ''),
                            message="Your order {} is reviewed by {}, please confirm the order".format(
                                order_object.order_id, order_object.business.name)
                        ).save()

                        return redirect('business_home')
                    else:
                        messages.add_message(request, messages.WARNING, 'Unable to process the request. Make sure you '
                                                                        'entered in all required fields')
                except Exception as e:
                    messages.add_message(request, messages.WARNING, str(e))
                return redirect('review_order', order=order, order_type=order_type)

            return render(request, 'business/review_order_by_form.html', return_dict)
        else:
            # order_formset = formset_factory(OrderPriceForm)
            # formset = order_formset(request.POST or None)
            # return_dict['formset'] = formset
            if request.method == 'POST':
                try:
                    # if formset.is_valid() and request.POST.get('total'):
                    if request.POST.get('total_amount') and request.POST.get('weight') and request.POST.get(
                            'no_of_items'):
                        # for fr in formset:
                        #     order_details_obj = fr.save()
                        #     order_object.order_details.add(order_details_obj)
                        # order_object.order_amount = float(request.POST.get('total'))

                        if request.FILES.get('order_bill'):
                            order_object.order_bill = request.FILES.get('order_bill')

                        order_object.order_amount = float(request.POST.get('total_amount'))
                        order_object.order_total_items = int(request.POST.get('no_of_items'))
                        order_object.total_weight_in_kg = float(request.POST.get('weight'))
                        # #
                        order_object.status = 2
                        order_object.save()
                        messages.add_message(request, messages.SUCCESS,
                                             'Order {} successfully reviewed'.format(order_object.order_id))

                        UserNotifications(
                            common_user=order_object.common_user,
                            order=order_object,
                            header='Your order {} is reviewed!!!'.format(order_object.order_id),
                            url=settings.BASE_URL_DEF + reverse('user_notifications').replace('/', ''),
                            message="Your order {} is reviewed by {}, please confirm the order".format(
                                order_object.order_id, order_object.business.name)
                        ).save()

                        return redirect('business_home')
                    else:
                        messages.add_message(request, messages.WARNING, 'Unable to process the request. Make sure you '
                                                                        'entered in all required fields')

                except Exception as e:
                    messages.add_message(request, messages.WARNING, str(e))
                return redirect('review_order', order=order, order_type=order_type)

            return render(request, 'business/review_order_by_other.html', return_dict)
    except Exception as e:
        messages.add_message(request, messages.WARNING, str(e))

    return redirect('business_home')


@session_required_business
def order_processing(request, order=None):
    try:
        Order.objects.filter(id=order).update(status=6)
        order_object = Order.objects.get(id=order)

        UserNotifications(
            common_user=order_object.common_user,
            order=order_object,
            header='Your order {} is packed!!!'.format(order_object.order_id),
            url=settings.BASE_URL_DEF + reverse('user_notifications').replace('/', ''),
            message="Order {} is packed".format(order_object.order_id)
        ).save()

        now = datetime.datetime.now().astimezone()
        formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
        ActivityLogs(activity="Order {} packed by {} in {} area on {}".format(order_object.order_id,
                                                                              order_object.business.name,
                                                                              order_object.business.area_specified.area,
                                                                              formatted)).save()

        all_agents_in_area = DeliveryAgent.objects.filter(area_specified=order_object.business.area_specified,
                                                          is_active=True)

        if OrderDelivery.objects.filter(common_user=order_object.common_user, is_delivered=False,
                                        area_specified=order_object.business.area_specified,
                                        created__date=datetime.datetime.today().astimezone().date()).exists():

            delivery_case = OrderDelivery.objects.get(common_user=order_object.common_user, is_delivered=False,
                                                      area_specified=order_object.business.area_specified,
                                                      created__date=datetime.datetime.today().astimezone().date())
            delivery_case.orders.add(order_object)
            delivery_case.save()

            if delivery_case.delivery_agent:
                DeliveryAgentNotification(
                    message="New order {} is added to {}({}'s order)".format(
                        order_object.order_id, delivery_case.delivery_id, delivery_case.common_user.name
                    ),
                    delivery_agent=delivery_case.delivery_agent,
                    url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                    header="New order is added to current delivery",
                    delivery_order=delivery_case
                ).save()

            else:
                for i in all_agents_in_area:
                    DeliveryAgentNotification(
                        message="Delivery order {} is still open.New order {} is added to this delivery order. Please "
                                "pick the order..".format(delivery_case.delivery_id, order_object.order_id),
                        delivery_agent=i,
                        delivery_order=delivery_case,
                        url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                        header="Delivery order {} is still open".format(delivery_case.delivery_id)
                    ).save()
        else:
            delivery_object = OrderDelivery()
            delivery_object.common_user = order_object.common_user
            delivery_object.status = 1
            delivery_object.area_specified = order_object.business.area_specified
            delivery_object.save()

            delivery_object.orders.add(order_object)
            delivery_object.save()
            formatted = delivery_object.created.astimezone().strftime("%a  %d-%b-%Y  %I:%M %p")

            for i in all_agents_in_area:
                DeliveryAgentNotification(
                    message="New delivery order {} is open for the user {} on {}. Please pick the order..".format(
                        delivery_object.delivery_id,
                        delivery_object.common_user.name,
                        formatted
                    ),
                    delivery_agent=i,
                    delivery_order=delivery_object,
                    url=settings.BASE_URL_DEF + reverse('agent_notifications').replace('/', ''),
                    header="New delivery order is open"
                ).save()

        messages.add_message(request, messages.SUCCESS, 'Order {} is packed.'.format(order_object.order_id))
    except Exception as e:
        messages.add_message(request, messages.WARNING, str(e))
    return redirect('business_home')


@session_required_business
def delete_item_from_order(request, order=None, pk=None):
    order_object = Order.objects.get(id=order)
    try:
        item_obj = OrderDetails.objects.get(id=pk)
        order_object.order_details.remove(item_obj)
        order_object.order_item_not_available.add(item_obj)
        order_object.save()

    except Exception as e:
        messages.add_message(request, messages.WARNING, str(e))
    return redirect('review_order', order=order, order_type=order_object.order_type)


@session_required_business
def reject_order(request, order=None):
    order_object = Order.objects.get(id=order)
    try:
        order_object = Order.objects.get(id=order)
        order_object.status = 3
        order_object.save()

        UserNotifications(
            common_user=order_object.common_user,
            order=order_object,
            header='Your order {} is rejected!!!'.format(order_object.order_id),
            url=settings.BASE_URL_DEF + reverse('user_notifications').replace('/', ''),
            message="Your order {} is rejected by {}".format(
                order_object.order_id, order_object.business.name)
        ).save()

        now = datetime.datetime.now().astimezone()
        formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
        ActivityLogs(activity="Order {} is rejected by {} in {} area on {}".format(order_object.order_id,
                                                                                   order_object.business.name,
                                                                                   order_object.business.area_specified.area,
                                                                                   formatted)).save()
        messages.add_message(request, messages.SUCCESS,
                             'Order {} is successfully rejected'.format(order_object.order_id))
        return redirect('business_home')
    except Exception as e:
        messages.add_message(request, messages.WARNING, str(e))
    return redirect('review_order', order=order, order_type=order_object.order_type)


@session_required_business
def get_new_orders(request):
    rtn_data = {}
    try:
        business = Business.objects.get(id=request.session['business']['id'])
        all_open_orders = Order.objects.filter(business=business, status=1).order_by('-id')
        all_placed_orders = Order.objects.filter(business=business, status=5).order_by('-id')

        ORDER_TYPE_TEXT = {
            1: 'Order Type : by Form',
            2: 'Order Type : by Upload Sheet',
            3: 'Order Type : by Call',
        }

        arr_open_orders = []
        for i in all_open_orders:
            if i.order_type == 1:
                status_text = "An order was opened. Review the order and update the price"
            elif i.order_type == 2:
                status_text = "An order was opened. Review the order and update the details"
            elif i.order_type == 3:
                status_text = "An order was opened. First call the user and confirm the order, then review it"

            data = {
                'id': i.id,
                'common_user': i.common_user.name,
                'business': i.business.name,
                'order_id': i.order_id,
                'order_type': i.order_type,
                'order_type_text': ORDER_TYPE_TEXT[i.order_type],
                'status': i.status,
                'status_text': status_text,
                'created': str(i.created.astimezone().strftime("%d/%B/%y  %I:%M %p")),
                'url': 'review-order/{}/{}/'.format(i.id, i.order_type),
            }
            arr_open_orders.append(data)

        arr_placed_orders = []
        for i in all_placed_orders:
            data_two = {
                'id': i.id,
                'common_user': i.common_user.name,
                'business': i.business.name,
                'order_id': i.order_id,
                'order_type': i.order_type,
                'order_type_text': ORDER_TYPE_TEXT[i.order_type],
                'status': i.status,
                'status_text': "Order confirmed by {}, processing packing..Please update status when packing is complete".format(
                    i.common_user.name),
                'created': str(i.created.astimezone().strftime("%d/%B/%y  %I:%M %p")),
                'url': 'order-info/{}/'.format(i.id),
                'button_url': 'order-processing/{}/'.format(i.id),
            }
            arr_placed_orders.append(data_two)

        rtn_data['all_open_orders'] = arr_open_orders
        rtn_data['all_placed_orders'] = arr_placed_orders
        rtn_data['status'] = "SUCCESS"

    except Exception as e:
        rtn_data['status'] = "FAILED"
        rtn_data['message'] = str(e)

    return JsonResponse(rtn_data)


@session_required_business
def order_history(request):
    if request.method == 'POST':
        try:
            business = Business.objects.get(id=request.session['business']['id'])

            status = request.POST.get('status')
            order_type = request.POST.get('order_type')
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'business': business}
            if status:
                filter_data['status'] = int(status)

            if order_type:
                filter_data['order_type'] = int(order_type)

            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_orders = Order.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('order_history')
    else:
        all_orders = Order.objects.filter(business=Business.objects.get(id=request.session['business']['id'])).order_by(
            '-id')[:20]

    return_dict = {
        'all_orders': all_orders,
    }
    return render(request, "business/order_history.html", return_dict)


@session_required_business
def order_info(request, order=None):
    order_object = Order.objects.get(id=order)
    if request.method == 'POST':
        pass
    return_dict = {
        'order_object': order_object,
        'order': order,
    }
    return render(request, "business/order_info.html", return_dict)


@session_required_business
def business_transactions(request):
    business = Business.objects.get(id=request.session['business']['id'])
    if request.method == 'POST':
        try:
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'business': business}
            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_transactions = BusinessTransactions.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('business_transactions')
    else:
        all_transactions = BusinessTransactions.objects.filter(business=business).order_by('-id')[:20]

    return_dict = {
        'all_transactions': all_transactions
    }
    return render(request, "business/transaction_history.html", return_dict)


@session_required_business
def business_payments(request):
    business = Business.objects.get(id=request.session['business']['id'])
    amount_due = 0
    if BusinessTransactions.objects.filter(business=business, is_completed=False).exists():
        all_incomplete_trans = BusinessTransactions.objects.filter(business=business, is_completed=False)
        for i in all_incomplete_trans:
            amount_due = amount_due + i.amount

    if request.method == 'POST':
        try:
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'business': business}
            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_transactions = BusinessPayment.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('business_payments')
    else:
        all_transactions = BusinessPayment.objects.filter(business=business).order_by('-id')[:20]

    return_dict = {
        'all_transactions': all_transactions,
        'amount_due': amount_due,
    }
    return render(request, "business/payments.html", return_dict)


@session_required_business
def business_notifications(request):
    business = Business.objects.get(id=request.session['business']['id'])
    notification_count = BusinessNotification.objects.filter(business=business, is_read=False).count()
    if notification_count < 15:
        all_notifications = BusinessNotification.objects.filter(business=business).order_by('-id')[:15]
    else:
        all_notifications = BusinessNotification.objects.filter(business=business).order_by('-id')[:notification_count]
    if request.method == 'POST':
        pass
    return_dict = {
        'all_notifications': all_notifications,
    }
    return render(request, "business/notifications.html", return_dict)


@session_required_business
def update_business_notification(request):
    return_data = {}
    business = Business.objects.get(id=request.session['business']['id'])
    try:
        if BusinessNotification.objects.filter(business=business, is_read=False).exists:
            BusinessNotification.objects.filter(business=business, is_read=False).update(is_read=True)
            return_data['status'] = 'SUCCESS'
            return_data['error'] = 'All unread notifications are updated'
        else:
            return_data['status'] = 'FAILED'
            return_data['error'] = 'All notifications are already read'
    except Exception as e:
        return_data['status'] = 'FAILED'
        return_data['error'] = str(e)

    return JsonResponse(return_data)


@session_required_business
def get_business_unread_notification(request):
    return_data = {
        'notification_count': 0,
    }
    try:
        business = Business.objects.get(id=request.session['business']['id'])
        if BusinessNotification.objects.filter(business=business, is_read=False).exists:
            notification_count = BusinessNotification.objects.filter(business=business, is_read=False).count()
            return_data['notification_count'] = notification_count
            return_data['status'] = 'SUCCESS'
        else:
            return_data['status'] = 'FAILED'
            return_data['error'] = 'No notifications'
    except Exception as e:
        return_data['status'] = 'FAILED'
        return_data['error'] = str(e)
    return JsonResponse(return_data)


@session_required_business
def business_change_password(request):
    if request.method == 'POST':
        try:
            if request.POST.get('old_password') and request.POST.get('new_password') and request.POST.get(
                    'retype_password'):
                if request.POST.get('new_password').strip() != request.POST.get('retype_password').strip():
                    messages.add_message(request, messages.WARNING, 'Password mismatched!')
                    return redirect('business_change_password')

                business = Business.objects.get(id=request.session['business']['id'])
                match_password = check_password(request.POST.get('old_password').strip(), business.password)
                if match_password:
                    business.password = make_password(request.POST.get('new_password').strip())
                    business.save()

                    now = datetime.datetime.now().astimezone()
                    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                    ActivityLogs(activity="Business {} successfully changed password on {}".format(business.name,
                                                                                                   formatted)).save()

                    messages.add_message(request, messages.SUCCESS, 'Password successfully changed')
                    return redirect('business_home')
                else:
                    messages.add_message(request, messages.WARNING,
                                         'Your old password is incorrect!')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Old password and new password is required to change the password!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
        return redirect('business_change_password')
    return render(request, "business/change_password.html")


@session_required_business
def business_profile(request):
    business_obj = Business.objects.get(id=request.session['business']['id'])
    form = BusinessProfileForm(request.POST or None, instance=business_obj)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                now = datetime.datetime.now().astimezone()
                formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                ActivityLogs(activity="Business {} updated profile on {}".format(business_obj.name, formatted)).save()
                messages.add_message(request, messages.SUCCESS, 'Profile successfully updated')
                return redirect('business_home')
            else:
                messages.add_message(request, messages.WARNING, 'Something went wrong! Please try again and make sure '
                                                                'all the recommended fields are entered')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
        return redirect('business_profile')
    return render(request, "business/profile.html", {'form': form})


def reset_password_business(request):
    if request.method == 'POST':
        try:
            if request.POST.get('email') and request.POST.get('mobile'):
                if Business.objects.filter(email__iexact=request.POST.get('email'),
                                           mobile=request.POST.get('mobile')).exists():
                    business = Business.objects.get(email__iexact=request.POST.get('email'),
                                                    mobile=request.POST.get('mobile'))
                    new_password = "{}_{}".format(business.name.strip().replace(" ", "_"), random.randint(0, 1000))
                    business.password = make_password(new_password)

                    subject = "Reset password verification!"
                    message = "<p>Hello {},<br><br>Your reset password request is successfully processed. Your new password will be automatically generated and attached to this mail.<br><br><strong>New Password&emsp;:&emsp;{}</strong><br><br>If you have any query related to this mail, you can contact back to this mail.<br><br>Regards,<br>Admin</p>".format(
                        business.name, new_password)

                    send_mail(subject=subject, recipient_list=[request.POST.get('email')],
                              from_email=settings.EMAIL_HOST_USER, message=message, html_message=message)

                    business.save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Your reset password request is successfully proceed!')
                    return redirect('business_login')
                else:
                    messages.add_message(request, messages.WARNING,
                                         'No business registered with this mobile number and email!')
            else:
                messages.add_message(request, messages.WARNING, 'Registered email and mobile is required!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('reset_password_business')
    return render(request, 'business/reset_password_business.html', {})


# Business Functions End Here
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================


# Agent Functions Start Here
# ----------------------------------------------------------------------------------------------------------------------
def session_required_agent(function):
    def _function(request, *args, **kwargs):
        if request.session.get('deliveryAgent') is None:
            return redirect('agent_login')
        else:
            return function(request, *args, **kwargs)

    return _function


def login_from_session_agent(request):
    if request.session.has_key('deliveryAgent'):
        if request.session['deliveryAgent']:
            return redirect('agent_home')

    return redirect('agent_login')


class getLoginAgent(View):
    def get(self, request):
        return render(request, "delivery_agent/login_page.html", {})

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        record = DeliveryAgent.objects.filter(mobile__iexact=mobile).exists()
        if not record:
            messages.add_message(request, messages.WARNING, 'Agent does not exist in this mobile number')
            return redirect('agent_login')
        agent = DeliveryAgent.objects.get(mobile__iexact=mobile)
        match_password = check_password(password, agent.password)
        if match_password:
            request.session['deliveryAgent'] = {
                'id': agent.id,
                'email': agent.email,
                'name': agent.name,
                'mobile': agent.mobile,
            }
            return redirect('agent_home')
        else:
            messages.add_message(request, messages.WARNING, 'Username or password mismatch')
            return redirect('agent_login')


def logout_agent(request):
    del request.session['deliveryAgent']
    return redirect('agent_index')


@session_required_agent
def agent_home(request):
    no_of_delivery_today = 0
    no_of_delivery_this_week = 0
    no_of_delivery_this_month = 0

    total_amount_collected_today = 0.0
    total_amount_collected_this_week = 0.0
    total_amount_collected_this_month = 0.0

    amount_by_cash_today = 0.0
    amount_by_cash_this_week = 0.0
    amount_by_cash_this_month = 0.0

    amount_by_upi_today = 0.0
    amount_by_upi_this_week = 0.0
    amount_by_upi_this_month = 0.0

    tot_delivery_amount_today = 0.0
    tot_delivery_amount_this_week = 0.0
    tot_delivery_amount_this_month = 0.0

    agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])

    today = datetime.datetime.today().astimezone()
    last_week_date = today - datetime.timedelta(days=7)

    delivery_today = OrderDelivery.objects.filter(delivery_agent=agent, is_delivered=True, created__date=today)
    delivery_this_week = OrderDelivery.objects.filter(delivery_agent=agent, is_delivered=True,
                                                      created__date__range=[last_week_date.date(), today])
    delivery_this_month = OrderDelivery.objects.filter(delivery_agent=agent, is_delivered=True, created__range=[
        datetime.datetime.now().astimezone().replace(day=1, hour=0, minute=0, second=0, microsecond=0), today])

    if delivery_today:
        no_of_delivery_today = delivery_today.count()
        for i in delivery_today:
            total_amount_collected_today = total_amount_collected_today + i.total_amount_to_collect
            tot_delivery_amount_today = tot_delivery_amount_today + i.delivery_charge
            if i.payment_method.is_upi:
                amount_by_upi_today = amount_by_upi_today + i.total_amount_to_collect
            else:
                amount_by_cash_today = amount_by_cash_today + i.total_amount_to_collect

    if delivery_this_week:
        no_of_delivery_this_week = delivery_this_week.count()
        for i in delivery_this_week:
            total_amount_collected_this_week = total_amount_collected_this_week + i.total_amount_to_collect
            tot_delivery_amount_this_week = tot_delivery_amount_this_week + i.delivery_charge
            if i.payment_method.is_upi:
                amount_by_upi_this_week = amount_by_upi_this_week + i.total_amount_to_collect
            else:
                amount_by_cash_this_week = amount_by_cash_this_week + i.total_amount_to_collect

    if delivery_this_month:
        no_of_delivery_this_month = delivery_this_month.count()
        for i in delivery_this_month:
            total_amount_collected_this_month = total_amount_collected_this_month + i.total_amount_to_collect
            tot_delivery_amount_this_month = tot_delivery_amount_this_month + i.delivery_charge
            if i.payment_method.is_upi:
                amount_by_upi_this_month = amount_by_upi_this_month + i.total_amount_to_collect
            else:
                amount_by_cash_this_month = amount_by_cash_this_month + i.total_amount_to_collect

    all_open_delivery_orders = OrderDelivery.objects.filter(area_specified=agent.area_specified, status=1,
                                                            delivery_agent=None).order_by('-id')
    all_processing_delivery_orders = OrderDelivery.objects.filter(area_specified=agent.area_specified, status=2,
                                                                  delivery_agent=agent).order_by('-id')

    return_dict = {
        'no_of_delivery_today': no_of_delivery_today,
        'no_of_delivery_this_week': no_of_delivery_this_week,
        'no_of_delivery_this_month': no_of_delivery_this_month,
        'total_amount_collected_today': total_amount_collected_today,
        'total_amount_collected_this_week': total_amount_collected_this_week,
        'total_amount_collected_this_month': total_amount_collected_this_month,
        'amount_by_cash_today': amount_by_cash_today,
        'amount_by_cash_this_week': amount_by_cash_this_week,
        'amount_by_cash_this_month': amount_by_cash_this_month,
        'amount_by_upi_today': amount_by_upi_today,
        'amount_by_upi_this_week': amount_by_upi_this_week,
        'amount_by_upi_this_month': amount_by_upi_this_month,
        'tot_delivery_amount_today': tot_delivery_amount_today,
        'tot_delivery_amount_this_week': tot_delivery_amount_this_week,
        'tot_delivery_amount_this_month': tot_delivery_amount_this_month,
        'all_open_delivery_orders': all_open_delivery_orders,
        'all_processing_delivery_orders': all_processing_delivery_orders,
    }

    return render(request, 'delivery_agent/agent_dash.html', return_dict)


@csrf_exempt
@session_required_agent
def delivery_agent_fcm_token_save(request):
    token = request.POST.get("token")
    try:
        if token:
            delivery_agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
            delivery_agent.fcm_token = token
            delivery_agent.save()
            return HttpResponse("True")
        else:
            print("token is required!!")
            pass
    except Exception as e:
        print(e)
        pass
    return HttpResponse("False")


@session_required_agent
def take_delivery_order(request, delivery=None):
    try:
        delivery_object = OrderDelivery.objects.get(id=delivery)
        delivery_object.delivery_agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
        delivery_object.status = 2
        delivery_object.save()

        messages.add_message(request, messages.SUCCESS,
                             "Delivery order {} is successfully assigned".format(delivery_object.delivery_id))

        UserNotifications(
            common_user=delivery_object.common_user,
            delivery_order=delivery_object,
            header='Your orders are assigned!!!',
            url=settings.BASE_URL_DEF + reverse('user_notifications').replace('/', ''),
            message="Your order(s) are assigned to delivery agent {}".format(delivery_object.delivery_agent.name)
        ).save()

    except Exception as e:
        messages.add_message(request, messages.WARNING, str(e))
    return redirect('agent_home')


@session_required_agent
def pick_order_from_shop(request, delivery=None, order=None):
    try:
        def_settings = None
        try:
            def_settings = DefaultSettings.objects.all()[0]
        except IndexError:
            pass

        delivery_object = OrderDelivery.objects.get(id=delivery)
        order_obj = Order.objects.get(id=order)
        order_obj.status = 7
        order_obj.save()
        delivery_object.picked_orders.add(order_obj)

        tot_user_order_amount = 0.0
        tot_weight = 0.0
        for i in delivery_object.picked_orders.all():
            tot_user_order_amount = tot_user_order_amount + i.order_amount
            tot_weight = tot_weight + i.total_weight_in_kg

        if def_settings:
            if float(tot_weight) > float(def_settings.normal_order_weight_limit):
                delivery_object.delivery_charge = def_settings.bulky_order_delivery_charge
            else:
                delivery_object.delivery_charge = def_settings.normal_order_delivery_charge
        else:
            if tot_weight > 15:
                delivery_object.delivery_charge = 50.0
            else:
                delivery_object.delivery_charge = 20.0

        delivery_object.total_user_orders_amount = tot_user_order_amount
        delivery_object.total_amount_to_collect = tot_user_order_amount + delivery_object.delivery_charge
        delivery_object.save()

        messages.add_message(request, messages.SUCCESS,
                             "User order {} is added to the delivery {}".format(order_obj.order_id,
                                                                                delivery_object.delivery_id))
    except Exception as e:
        messages.add_message(request, messages.WARNING, str(e))
    return redirect('agent_home')


@session_required_agent
def agent_delivery_info(request, delivery=None):
    delivery_object = OrderDelivery.objects.get(id=delivery)
    all_payment_methods = PaymentMethod.objects.filter(is_active=True).order_by('name')
    if request.method == 'POST':
        try:
            if request.POST.get('payment_method'):
                delivery_object.payment_method = PaymentMethod.objects.get(id=int(request.POST.get('payment_method')))
                delivery_object.status = 3
                delivery_object.verify_total_amount = True
                delivery_object.is_delivered = True
                delivery_object.delivered_time = datetime.datetime.now().astimezone()
                delivery_object.save()
                for i in delivery_object.picked_orders.all():
                    i.status = 8
                    i.save()

                    business_transaction = BusinessTransactions()
                    business_transaction.business = i.business
                    business_transaction.order = i
                    business_transaction.total_amount = i.order_amount
                    if i.business.payment_percentage:
                        business_transaction.platform_amount = (i.business.payment_percentage * i.order_amount) / 100
                        business_transaction.amount = i.order_amount - business_transaction.platform_amount
                    else:
                        business_transaction.platform_amount = (5 * i.order_amount) / 100
                        business_transaction.amount = i.order_amount - business_transaction.platform_amount

                    business_transaction.save()

                messages.add_message(request, messages.SUCCESS, 'Delivery order is successfully completed!')

                UserNotifications(
                    common_user=delivery_object.common_user,
                    delivery_order=delivery_object,
                    header='Your orders are delivered!!!',
                    url=settings.BASE_URL_DEF + reverse('user_notifications').replace('/', ''),
                    message="Your order(s) are delivered"
                ).save()

                agent_transaction = AgentTransactions()
                agent_transaction.delivery_agent = delivery_object.delivery_agent
                agent_transaction.delivery_order = delivery_object
                agent_transaction.total_amount = delivery_object.delivery_charge
                agent_transaction.gross_amount = delivery_object.total_amount_to_collect
                agent_transaction.total_order_amount = delivery_object.total_user_orders_amount
                if delivery_object.delivery_agent.payment_percentage:
                    agent_transaction.amount = delivery_object.delivery_agent.payment_percentage * delivery_object.delivery_charge / 100
                    agent_transaction.platform_amount = delivery_object.delivery_charge - agent_transaction.amount
                else:
                    agent_transaction.amount = 80 * delivery_object.delivery_charge / 100
                    agent_transaction.platform_amount = delivery_object.delivery_charge - agent_transaction.amount

                if not delivery_object.payment_method.is_upi:
                    agent_transaction.is_cod = True

                agent_transaction.save()

                now = datetime.datetime.now().astimezone()
                formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                ActivityLogs(
                    activity="Delivery Order {} successfully completed in {} area by agent {} on {}".format(
                        delivery_object.delivery_id,
                        delivery_object.area_specified.area,
                        delivery_object.delivery_agent.name,
                        formatted
                    )
                ).save()
                return redirect('agent_home')
            else:
                messages.add_message(request, messages.WARNING, 'Payment method is required to submit delivery order!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))

        return redirect('agent_delivery_info', delivery=delivery)

    return_dict = {
        'delivery_object': delivery_object,
        'all_payment_methods': all_payment_methods,
    }
    return render(request, "delivery_agent/delivery_info.html", return_dict)


@session_required_agent
def individual_user_order_info(request, order=None):
    order_object = Order.objects.get(id=order)
    if request.method == 'POST':
        pass
    return_dict = {
        'order_object': order_object,
    }
    return render(request, "delivery_agent/individual_user_order_info.html", return_dict)


@session_required_agent
def check_out_completed_delivery(request):
    agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
    all_completed_delivery_orders = OrderDelivery.objects.filter(
        area_specified=agent.area_specified, status=3, created__date=datetime.datetime.today().astimezone(),
        delivery_agent=agent).order_by('-id')
    if request.method == 'POST':
        pass

    return_dict = {
        'all_completed_delivery_orders': all_completed_delivery_orders,
    }
    return render(request, "delivery_agent/completed_delivery.html", return_dict)


@session_required_agent
def get_new_delivery_orders(request):
    rtn_data = {}
    try:
        agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
        all_open_orders = OrderDelivery.objects.filter(status=1).order_by('-id')
        all_processed_orders = OrderDelivery.objects.filter(delivery_agent=agent, status=2).order_by('-id')

        arr_open_orders = []
        for i in all_open_orders:

            data = {
                'id': i.id,
                'common_user': i.common_user.name,
                'area': i.common_user.area_specified.area,
                'mobile': i.common_user.mobile,
                'landmark': i.common_user.landmark,
                'address': i.common_user.address,
                'orders': [],
                'url': 'take-delivery-order/{}/'.format(i.id),
            }
            for j in i.orders.all():
                orders_data = {
                    'order_id': j.order_id,
                    'business': j.business.name,
                    'order_info_link': 'individual-order-info/{}/'.format(j.id),
                }
                data['orders'].append(orders_data)
            arr_open_orders.append(data)

        arr_processed_orders = []
        for i in all_processed_orders:
            data_two = {
                'id': i.id,
                'common_user': i.common_user.name,
                'area': i.common_user.area_specified.area,
                'mobile': i.common_user.mobile,
                'landmark': i.common_user.landmark,
                'address': i.common_user.address,
                'orders': [],
                'url': 'agent-delivery-info/{}/'.format(i.id),
            }
            for j in i.orders.all():
                orders_data = {
                    'order_id': j.order_id,
                    'business': j.business.name,
                    'order_total_items': j.order_total_items,
                    'order_info_link': 'individual-order-info/{}/'.format(j.id),
                }
                if j not in i.picked_orders.all():
                    url = reverse('pick_order_from_shop', args=[i.id, j.id])
                    element = '<a href="{}"><h2>Pick</h2></a>'.format(url)
                else:
                    element = '<h6>Picked</h6>'

                orders_data['element'] = element

                data_two['orders'].append(orders_data)
            arr_processed_orders.append(data_two)

        rtn_data['all_open_orders'] = arr_open_orders
        rtn_data['all_processed_orders'] = arr_processed_orders
        rtn_data['status'] = "SUCCESS"

    except Exception as e:
        rtn_data['status'] = "FAILED"
        rtn_data['message'] = str(e)

    return JsonResponse(rtn_data)


@session_required_agent
def delivery_history(request):
    if request.method == 'POST':
        try:
            agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])

            status = request.POST.get('status')
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'delivery_agent': agent}
            if status:
                filter_data['status'] = int(status)

            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_delivery_orders = OrderDelivery.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('delivery_history')

    else:
        agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
        all_delivery_orders = OrderDelivery.objects.filter(delivery_agent=agent).order_by('-id')[:20]

    return_dict = {
        'all_delivery_orders': all_delivery_orders,
    }
    return render(request, "delivery_agent/delivery_history.html", return_dict)


@session_required_agent
def agent_transactions(request):
    agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
    if request.method == 'POST':
        try:
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')

            filter_data = {'delivery_agent': agent}
            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_transactions = AgentTransactions.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('agent_transactions')
    else:
        all_transactions = AgentTransactions.objects.filter(delivery_agent=agent).order_by('-id')[:20]

    return_dict = {
        'all_transactions': all_transactions
    }
    return render(request, "delivery_agent/transaction_history.html", return_dict)


@session_required_agent
def agent_payments(request):
    agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
    agent_amount_due_cod = 0
    platform_amount_due_cod = 0
    agent_amount_due = 0
    all_incomplete_trans_cod_count = 0
    all_incomplete_trans_count = 0

    total_amount = 0

    company_account_details = {
        'ACC_NAME': settings.ACC_NAME,
        'ACC_NO': settings.ACC_NO,
        'IFSC': settings.IFSC,
        'BRANCH': settings.BRANCH,
        'ADMIN_UPI_ID': settings.ADMIN_UPI_ID,
    }

    if AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False, is_cod=True).exists():
        all_incomplete_trans_cod = AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False,
                                                                    is_cod=True)
        all_incomplete_trans_cod_count = all_incomplete_trans_cod.count()
        for i in all_incomplete_trans_cod:
            agent_amount_due_cod = agent_amount_due_cod + i.amount
            platform_amount_due_cod = platform_amount_due_cod + i.total_order_amount + i.platform_amount

    if AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False, is_cod=False).exists():
        all_incomplete_trans = AgentTransactions.objects.filter(delivery_agent=agent, is_completed=False, is_cod=False)
        all_incomplete_trans_count = all_incomplete_trans.count()
        for i in all_incomplete_trans:
            agent_amount_due = agent_amount_due + i.amount

    if all_incomplete_trans_cod_count:
        total_amount = platform_amount_due_cod
    if all_incomplete_trans_count:
        total_amount = total_amount - agent_amount_due

    if request.method == 'POST':
        try:
            date_to = request.POST.get('date_to')
            date_from = request.POST.get('date_from')
            payment_type = request.POST.get('payment_type')

            filter_data = {'delivery_agent': agent}
            if payment_type:
                if payment_type == 'credit':
                    filter_data['is_credit'] = True
                elif payment_type == 'debit':
                    filter_data['is_debit'] = True
                else:
                    print("Mis input received -> Payment Type")
            if date_from and date_to:
                filter_data['created__date__range'] = date_from, date_to
            else:
                if date_from:
                    filter_data['created__date__gte'] = date_from
                if date_to:
                    filter_data['created__date__lte'] = date_to

            all_transactions = AgentPayment.objects.filter(**filter_data).order_by('-id')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
            return redirect('agent_payments')
    else:
        all_transactions = AgentPayment.objects.filter(delivery_agent=agent).order_by('-id')[:20]

    return_dict = {
        'all_transactions': all_transactions,
        'agent_amount_due_cod': agent_amount_due_cod,
        'platform_amount_due_cod': platform_amount_due_cod,
        'agent_amount_due': agent_amount_due,
        'all_incomplete_trans_cod_count': all_incomplete_trans_cod_count,
        'all_incomplete_trans_count': all_incomplete_trans_count,
        'payment_percentage': agent.payment_percentage,
        'total_amount': total_amount,
        'company_account_details': company_account_details,
    }
    return render(request, "delivery_agent/payments.html", return_dict)


@session_required_agent
def agent_change_password(request):
    if request.method == 'POST':
        try:
            if request.POST.get('old_password') and request.POST.get('new_password') and request.POST.get(
                    'retype_password'):
                if request.POST.get('new_password').strip() != request.POST.get('retype_password').strip():
                    messages.add_message(request, messages.WARNING, 'Password mismatched!')
                    return redirect('agent_change_password')

                agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
                match_password = check_password(request.POST.get('old_password').strip(), agent.password)
                if match_password:
                    agent.password = make_password(request.POST.get('new_password').strip())
                    agent.save()

                    now = datetime.datetime.now().astimezone()
                    formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                    ActivityLogs(activity="Delivery Agent {} successfully changed password on {}".format(agent.name,
                                                                                                         formatted)).save()

                    messages.add_message(request, messages.SUCCESS, 'Password successfully changed')
                    return redirect('agent_home')
                else:
                    messages.add_message(request, messages.WARNING,
                                         'Your old password is incorrect!')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Old password and new password is required to change the password!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
        return redirect('agent_change_password')

    return render(request, "delivery_agent/change_password.html")


@session_required_agent
def agent_profile(request):
    agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
    form = AgentProfileForm(request.POST or None, instance=agent)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                now = datetime.datetime.now().astimezone()
                formatted = now.strftime("%a  %d-%b-%Y  %I:%M %p")
                ActivityLogs(activity="Delivery Agent {} updated profile on {}".format(agent.name, formatted)).save()
                messages.add_message(request, messages.SUCCESS, 'Profile successfully updated')
                return redirect('agent_home')
            else:
                messages.add_message(request, messages.WARNING, 'Something went wrong! Please try again and make sure '
                                                                'all the recommended fields are entered')
        except Exception as e:
            messages.add_message(request, messages.WARNING, str(e))
        return redirect('agent_profile')
    return render(request, "delivery_agent/profile.html", {'form': form})


@session_required_agent
def agent_notifications(request):
    delivery_agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
    notification_count = DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent, is_read=False).count()
    if notification_count < 15:
        all_notifications = DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent).order_by('-id')[:15]
    else:
        all_notifications = DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent).order_by('-id')[
                            :notification_count]
    if request.method == 'POST':
        pass
    return_dict = {
        'all_notifications': all_notifications,
        'delivery_agent': delivery_agent,
    }
    return render(request, "delivery_agent/notifications.html", return_dict)


@session_required_agent
def update_agent_notification(request):
    return_data = {}
    delivery_agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
    try:
        if DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent, is_read=False).exists:
            DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent, is_read=False).update(is_read=True)
            return_data['status'] = 'SUCCESS'
            return_data['error'] = 'All unread notifications are updated'
        else:
            return_data['status'] = 'FAILED'
            return_data['error'] = 'All notifications are already read'
    except Exception as e:
        return_data['status'] = 'FAILED'
        return_data['error'] = str(e)

    return JsonResponse(return_data)


@session_required_agent
def get_agent_unread_notification(request):
    return_data = {
        'notification_count': 0,
    }
    try:
        delivery_agent = DeliveryAgent.objects.get(id=request.session['deliveryAgent']['id'])
        if DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent, is_read=False).exists:
            notification_count = DeliveryAgentNotification.objects.filter(delivery_agent=delivery_agent,
                                                                          is_read=False).count()
            return_data['notification_count'] = notification_count
            return_data['status'] = 'SUCCESS'
        else:
            return_data['status'] = 'FAILED'
            return_data['error'] = 'No notifications'
    except Exception as e:
        return_data['status'] = 'FAILED'
        return_data['error'] = str(e)
    return JsonResponse(return_data)


def reset_password_agent(request):
    if request.method == 'POST':
        try:
            if request.POST.get('email') and request.POST.get('mobile'):
                if DeliveryAgent.objects.filter(email__iexact=request.POST.get('email'),
                                                mobile=request.POST.get('mobile')).exists():
                    agent = DeliveryAgent.objects.get(email__iexact=request.POST.get('email'),
                                                      mobile=request.POST.get('mobile'))
                    new_password = "{}_{}".format(agent.name.strip().replace(" ", "_"), random.randint(0, 1000))
                    agent.password = make_password(new_password)

                    subject = "Reset password verification!"
                    message = "<p>Hello {},<br><br>Your reset password request is successfully processed. Your new password will be automatically generated and attached to this mail.<br><br><strong>New Password&emsp;:&emsp;{}</strong><br><br>If you have any query related to this mail, you can contact back to this mail.<br><br>Regards,<br>Admin</p>".format(
                        agent.name, new_password)

                    send_mail(subject=subject, recipient_list=[request.POST.get('email')],
                              from_email=settings.EMAIL_HOST_USER, message=message, html_message=message)

                    agent.save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Your reset password request is successfully proceed!')
                    return redirect('agent_login')
                else:
                    messages.add_message(request, messages.WARNING,
                                         'No agent registered with this mobile number and email!')
            else:
                messages.add_message(request, messages.WARNING, 'Registered email and mobile is required!')
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
        return redirect('reset_password_agent')
    return render(request, 'delivery_agent/reset_password_agent.html', {})

# Agent Functions End Here
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
