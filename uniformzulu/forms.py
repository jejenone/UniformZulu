from django import forms
from recaptcha_django import ReCaptchaField
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _

class ReCaptchaRegistrationForm(RegistrationForm):
	first_name = forms.CharField(_('first name'))
	last_name = forms.CharField(_('last name'))
	recaptcha = ReCaptchaField()