from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, Row, Column, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    helper = FormHelper()
    helper.form_show_labels = True
    helper.help_text_inline = True
    # helper.label_class = 'col-lg-2'
    helper.field_class = 'col-sm-'
    helper.labels_uppercase = False
    helper.add_input(Submit('submit', 'Rejestracja'))

    class Meta:
        model = User
        fields = ['username']