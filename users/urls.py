from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = 'users'

urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('forgotten-password/', views.ForgottenPasswordView.as_view(), name='forgotten-password'),

    # AJAX function views
    path('email/', views.email, name='email'),
    url(r'^verification/(?P<uidb64>.+)/(?P<token>.+)/$', views.verification, name='verification'),
]
