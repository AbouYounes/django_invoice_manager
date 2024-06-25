from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

from django import forms
from django.contrib.auth.models import User



#def superuser_required(
#    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
#):
#    """
#    Decorator for views that checks that the user is logged in and if the user is a superuser,
#    redirecting to the log-in page if necessary.
#    """
#    actual_decorator = user_passes_test(
#        lambda u: u.is_active and u.is_superusr,
#        login_url=login_url,
#        redirect_field_name=redirect_field_name,
#    )
#    if function:
#        return actual_decorator(function)
#    return actual_decorator



class LoginRequiredSuperuserMixim(UserPassesTestMixin):

    """ Mixin for superuser """

    def test_func(self):
        return self.request.user.is_staff
    


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)    
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']