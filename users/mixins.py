from config.mixins import CreateSMS
import random
import string

import phonenumbers
import pycountry
import six

from .models import UserToken


class ActivateTwoStep:
    def __init__(self, **kwargs) -> None:

        self.user = kwargs.get('user')
        self.token = kwargs.get('token')

        size = 6
        chars = string.digits
        code = ''.join(random.choice(chars) for _ in range(size))

        ut = UserToken.objects.create(
            user = self.user,
            token=self.token,
            two_step_code=code,
            is_sms = True
        )

        country_code = pycountry.countries.get(name=self.user.userprofile.country).alpha_2
        number_object = phonenumbers.parse(self.user.userprofile.telephone, country_code)
        telephone = f'+{number_object.country_code}{number_object.national_number}'

        send_sms = CreateSMS(
            number=telephone,
            message=f'Your verification code is: {code}'
        )
