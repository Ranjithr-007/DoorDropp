
from django.urls import path
# from django.conf.urls import url
from .views import *

urlpatterns = [

    # ADMIN URLS
    path('admin', login_from_session_admin, name='admin_index'),
    path('admin-login', getLoginAdmin.as_view(), name='admin_login'),
    path('admin-logout', logout_admin, name='admin_logout'),
    path('admin-home', admin_home, name='admin_home'),

    # path('enableUser/<int:pk>/', enable_user, name='enableUser'),
    # path('disableUser/<int:pk>/', disable_user, name='disableUser'),

    path('add-delivery-agent', add_delivery_agent, name='addDeliveryAgent'),
    path('edit-delivery-agent', edit_delivery_agent, name='editDeliveryAgent'),
    path('delete-delivery-agent/<int:pk>/', delete_delivery_agent, name='deleteDeliveryAgent'),
    path('enable-delivery-agent/<int:pk>/', enable_delivery_agent, name='enableDeliveryAgent'),
    path('disable-delivery-agent/<int:pk>/', disable_delivery_agent, name='disableDeliveryAgent'),

    path('add-business', add_business, name='addBusiness'),
    path('edit-business', edit_business, name='editBusiness'),
    path('delete-business/<int:pk>/', delete_business, name='deleteBusiness'),
    path('enable-business/<int:pk>/', enable_business, name='enableBusiness'),
    path('disable-business/<int:pk>/', disable_business, name='disableBusiness'),
    #
    path('add-district', add_district, name='addDistrict'),
    path('edit-district', edit_district, name='editDistrict'),
    path('delete-district/<int:pk>/', delete_district, name='deleteDistrict'),
    path('enable-district/<int:pk>/', enable_district, name='enableDistrict'),
    path('disable-district/<int:pk>/', disable_district, name='disableDistrict'),
    #
    path('add-village', add_village, name='addVillage'),
    path('edit-village', edit_village, name='editVillage'),
    path('delete-village/<int:pk>/', delete_village, name='deleteVillage'),
    path('enable-village/<int:pk>/', enable_village, name='enableVillage'),
    path('disable-village/<int:pk>/', disable_village, name='disableVillage'),
    #
    path('add-area', add_area, name='addArea'),
    path('edit-area', edit_area, name='editArea'),
    path('delete-area/<int:pk>/', delete_area, name='deleteArea'),
    path('enable-area/<int:pk>/', enable_area, name='enableArea'),
    path('disable-area/<int:pk>/', disable_area, name='disableArea'),
    path('enable-area-restriction/<int:pk>/', enable_area_restriction, name='enableAreaRestriction'),
    path('disable-area-restriction/<int:pk>/', disable_area_restriction, name='disableAreaRestriction'),
    #
    path('add-unit', add_units, name='addUnit'),
    path('edit-unit', edit_units, name='editUnit'),
    path('delete-unit/<int:pk>/', delete_units, name='deleteUnit'),
    path('enable-unit/<int:pk>/', enable_units, name='enableUnit'),
    path('disable-unit/<int:pk>/', disable_units, name='disableUnit'),
    #
    path('add-payment-method', add_payment_method, name='addPaymentMethod'),
    path('edit-payment-method', edit_payment_method, name='editPaymentMethod'),
    path('delete-payment-method/<int:pk>/', delete_payment_method, name='deletePaymentMethod'),
    path('enable-payment-method/<int:pk>/', enable_payment_method, name='enablePaymentMethod'),
    path('disable-payment-method/<int:pk>/', disable_payment_method, name='disablePaymentMethod'),
    #
    path('add-banner-image', add_banner_image, name='addBannerImages'),
    path('edit-banner-image', edit_banner_image, name='editBannerImages'),
    path('delete-banner-image/<int:pk>/', delete_banner_image, name='deleteBannerImages'),
    path('enable-banner-image/<int:pk>/', enable_banner_image, name='enableBannerImages'),
    path('disable-banner-image/<int:pk>/', disable_banner_image, name='disableBannerImages'),
    #
    path('add-category', add_store_category, name='addCategory'),
    path('edit-category', edit_store_category, name='editCategory'),
    path('delete-category/<int:pk>/', delete_store_category, name='deleteCategory'),
    path('enable-category/<int:pk>/', enable_store_category, name='enableCategory'),
    path('disable-category/<int:pk>/', disable_store_category, name='disableCategory'),
    #
    path('add-settings', default_settings, name='addSettings'),
    #
    path('activityLogs', activity_logs, name='activityLogs'),
    path('exportActivityLogs', export_activity_logs, name='exportActivityLogs'),
    #
    path('agent-payment-home', agent_payment_home, name='agent_payment_home'),
    path('agent-payment-history', agent_payment_history, name='agent_payment_history'),
    path('agent-transaction-history', agent_transaction_history, name='agent_transaction_history'),
    path('agent-transaction-payment/<int:tr>/<str:tp>/', agent_transaction_payment, name='agent_transaction_payment'),
    path('agent-all-pending-transaction-payment/<str:trans>/<str:tp>/<str:amt>/<int:ag>/', agent_all_pending_transaction_payment, name='agent_all_pending_transaction_payment'),

    path('business-payment-home', business_payment_home, name='business_payment_home'),
    path('business-payment-history', business_payment_history, name='business_payment_history'),
    path('business-transaction-history', business_transaction_history, name='business_transaction_history'),
    path('business-transaction-payment/<int:tr>/', business_transaction_payment, name='business_transaction_payment'),
    path('business-all-pending-transaction-payment/<str:trans>/<str:amt>/<int:bs>/', business_all_pending_transaction_payment, name='business_all_pending_transaction_payment'),

    # Common User
    path('', login_from_session_user, name='user_index'),
    path('login', getLoginUser.as_view(), name='user_login'),
    path('register', register_user, name='user_register'),
    path('get-area', get_area_of_village, name='get_area'),
    path('check-mobile', check_user_mobile, name='check_mobile'),
    path('reset-password', reset_password, name='reset_password'),
    path('send-request', password_change_request, name='password_change_request'),
    path('verify-security/<int:pk>/', security_question_valid, name='security_question_valid'),
    path('verify-otp/<int:pk>/', email_otp_verification, name='verify_otp'),
    path('resend-otp/<int:pk>/', resend_otp, name='resend_otp'),
    path('set-new-password/<int:pk>/', set_new_password, name='set_new_password'),
    path('logout', logout_user, name='user_logout'),
    path('home/<int:ar>/', user_home, name='user_home'),
    path('get-fcm', user_fcm_token_save, name='user_fcm_token_save'),
    path('business-list/<int:category>/<int:ar>/', business_list, name='business_list'),
    path('new-order/<int:shop>/', new_order, name='new_order'),
    path('new-order-by-call', new_order_by_call, name='new_order_by_call'),
    path('profile', user_profile, name='user_profile'),
    path('my-notifications', user_notifications, name='user_notifications'),
    path('my-orders', my_orders, name='my_orders'),
    path('check-delivery', user_delivery_home, name='user_delivery_home'),
    path('delivery-info/<int:delivery>/', user_delivery_details, name='user_delivery_details'),
    path('order-confirmation/<int:order>/', order_confirmation, name='order_confirmation'),
    path('order-placed/<int:order>/', order_placed, name='order_placed'),
    path('order-details/<int:order>/', order_details, name='order_details'),
    path('cancel-order/<int:order>/', cancel_order, name='cancel_order'),
    path('update-user-notification', update_user_notification, name='update_user_notification'),
    path('get-user-unread-notification', get_user_unread_notification, name='get_user_unread_notification'),

    # Delivery Agent - Add by System Admin
    path('agent', login_from_session_agent, name='agent_index'),
    path('agent-login', getLoginAgent.as_view(), name='agent_login'),
    path('agent-logout', logout_agent, name='agent_logout'),
    path('agent-home', agent_home, name='agent_home'),
    path('agent-fcm', delivery_agent_fcm_token_save, name='delivery_agent_fcm_token_save'),
    path('get-new-delivery-orders', get_new_delivery_orders, name='get_new_delivery_orders'),
    path('check-out-completed-delivery', check_out_completed_delivery, name='check_out_completed_delivery'),
    path('delivery-history', delivery_history, name='delivery_history'),
    path('take-delivery-order/<int:delivery>/', take_delivery_order, name='take_delivery_order'),
    path('pick-an-order/<int:delivery>/<int:order>/', pick_order_from_shop, name='pick_order_from_shop'),
    path('agent-delivery-info/<int:delivery>/', agent_delivery_info, name='agent_delivery_info'),
    path('individual-order-info/<int:order>/', individual_user_order_info, name='individual_user_order_info'),
    path('agent-change-password', agent_change_password, name='agent_change_password'),
    path('agent-profile', agent_profile, name='agent_profile'),
    path('agent-notifications', agent_notifications, name='agent_notifications'),
    path('agent-transactions', agent_transactions, name='agent_transactions'),
    path('agent-payments', agent_payments, name='agent_payments'),
    path('agent-reset-password', reset_password_agent, name='reset_password_agent'),
    path('update-agent-notification', update_agent_notification, name='update_agent_notification'),
    path('get-agent-unread-notification', get_agent_unread_notification, name='get_agent_unread_notification'),


    # Business - Add by System Admin
    path('business', login_from_session_business, name='business_index'),
    path('business-login', getLoginBusiness.as_view(), name='business_login'),
    path('business-logout', logout_business, name='business_logout'),
    path('business-home', business_home, name='business_home'),
    path('business-fcm', business_fcm_token_save, name='business_fcm_token_save'),
    path('get-new-orders', get_new_orders, name='get_new_orders'),
    path('order-processing/<int:order>/', order_processing, name='order_processing'),
    path('reject-order/<int:order>/', reject_order, name='reject_order'),
    path('remove-item/<int:order>/<int:pk>/', delete_item_from_order, name='delete_item_from_order'),
    path('review-order/<int:order>/<int:order_type>/', review_order, name='review_order'),
    path('business-profile', business_profile, name='business_profile'),
    path('order-history', order_history, name='order_history'),
    path('order-info/<int:order>/', order_info, name='order_info'),
    path('business-transactions', business_transactions, name='business_transactions'),
    path('business-payments', business_payments, name='business_payments'),
    path('business-notifications', business_notifications, name='business_notifications'),
    path('business-change-password', business_change_password, name='business_change_password'),
    path('reset-password-business', reset_password_business, name='reset_password_business'),
    path('update-business-notification', update_business_notification, name='update_business_notification'),
    path('get-business-unread-notification', get_business_unread_notification, name='get_business_unread_notification'),

    path('firebase-messaging-sw.js', showFirebaseJS, name="show_firebase_js"),
]



