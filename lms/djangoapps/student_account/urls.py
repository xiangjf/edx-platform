from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = []

if settings.FEATURES.get('ENABLE_COMBINED_LOGIN_REGISTRATION'):
    urlpatterns += patterns(
        'student_account.views',
        url(r'^login/$', 'login_and_registration_form', {'initial_mode': 'login'}, name='account_login'),
        url(r'^register/$', 'login_and_registration_form', {'initial_mode': 'register'}, name='account_register'),
        url(r'^password$', 'password_change_request_handler', name='password_change_request'),
        #syw
        url(r'^sslogin/$', 'login_and_registration_form', {'initial_mode': 'ssologin'}, name='account_ssologin'),
        #syw
    )

urlpatterns += patterns(
    'student_account.views',
    url(r'^finish_auth$', 'finish_auth', name='finish_auth'),
    url(r'^settings$', 'account_settings', name='account_settings'),
)
