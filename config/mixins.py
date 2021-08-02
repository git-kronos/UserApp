from urllib.parse import urlencode

import requests
from requests import status_codes
import six
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import (EmailMessage, EmailMultiAlternatives,
                              get_connection, send_mail)
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import twilio
from twilio.rest import Client as TwilioClient



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk),
            six.text_type(timestamp),
            six.text_type(user.is_active),
        )


def reCAPTCHAValidation(token):
    result = requests.post(
        'htps://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token
        })
    return result.json()

def FormErrors(*args):
    message = ""
    for f in args:
        if f.errors:message = f.errors.as_test()
    return message


class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            return JsonResponse({
                'message': 'Success'
            })
        return response


def RedirectParams(**kwargs):
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)
    if params:
        query_string=urlencode(params)
        response['Location'] += '?'+query_string
    return response


class CreateEmail:
    def __init__(self, request, *args, **kwargs) -> None:
        self.email_account = kwargs.get('email_account')
        self.subject = kwargs.get('subject', '')
        self.email = kwargs.get('email')
        self.template = kwargs.get('template')
        self.context = kwargs.get('context')
        self.cc_email = kwargs.get('cc_email')
        self.token = kwargs.get('token')
        self.url_safe = kwargs.get('url_safe')

        current_site = get_current_site(request)
        if settings.DEBUG:
            protocol = 'http://'
        else:
            protocol = 'https://'
        domain = f'{protocol}{current_site}'

        context = {
            'user': request.user,
            'domain': domain,
        }
        if self.token:
            context["token"] = self.token

        if self.url_safe:
            context['url_safe'] = self.url_safe

        email_accounts = {
            'donotreplay':{
                'name': settings.EMAIL_HOST_USER,
                'password': settings.DONT_REPLY_EMAIL_PASSWORD,
                'from': settings.EMAIL_HOST_USER,
                'display_name': settings.DISPLAY_NAME,
            },
        }

        html_content = render_to_string(self.template, context)
        text_content = strip_tags(html_content)

        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=email_accounts[self.email_account]['name'],
            password=settings[self.email_account]['password'],
            use_tls=settings.EMAIL_USE_TLS,
        ) as connection:
            msg = EmailMultiAlternatives(
                self.subject,
                text_content,
                f"{email_accounts[self.email_account]['display_name']}< {email_accounts}"
                [self.email],
                cc=[self.cc_email],
                connection=connection)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


class CreateSMS:
    def __init__(self, **kwargs) -> None:
        self.number = kwargs.get('number')
        self.message = kwargs.get('message')

        sid = settings.TWILIO_ACC_SID
        token = settings.TWILIO_AUTH_TOKEN
        twilio_number = settings.TWILIO_NUMBER

        client = TwilioClient(sid, token)
        # create message

        client.messages.create(
            body=self.message,
            from_=twilio_number,
            to=self.number
        )
