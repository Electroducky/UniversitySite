from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, Row, Column
from django import forms

from university_system.forms import form_manager


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "university_system.settings")
#

class LoginForm(forms.Form):
    login = forms.SlugField(label="Login")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('login', placeholder='Login'),
            Field('password', placeholder='Password'))


class UserForm(forms.Form):
    Role = [
        ('Role.student', 'Student'),
        ('Role.admin', 'Admin')
    ]
    Type = [
        ('Type.student', 'Student'),
        ('Type.admin', 'Admin')
    ]
    role = forms.ChoiceField(choices=Role, label='Role', widget=forms.Select(), required=False)
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=False)
    type = forms.ChoiceField(choices=Type, label='Type', widget=forms.Select(),
                             required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Registration info',
                     Row(
                         Column('login', css_class='col-md-6 mb-0'),
                         Column('password', css_class='col-md-6 mb-0')
                     ),
                     Row(
                         Column('type',
                                css_class='col-md-6 mb-0 '),
                         Column('role',
                                css_class='col-md-6 mb-0')
                     )))


class UserInfoForm(forms.Form):
    Sex = [
        ('Sex.male', 'male'),
        ('Sex.female', 'female')
    ]

    name = forms.CharField(label="First name", max_length=50, required=False)
    surname = forms.CharField(label="Last name", max_length=50, required=False)
    patronymic = forms.CharField(label="Middle name", max_length=50, required=False)
    sex = forms.ChoiceField(choices=Sex, label='Sex', widget=forms.RadioSelect(), required=False)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'), required=False)
    description = forms.CharField(label="About", widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Name',
                     'name',
                     'surname',
                     'patronymic'),
            Fieldset('General info',
                     Div(InlineRadios('sex')),
                     'date',
                     'description'
                     )
        )
        # TabHolder(Tab('Date', 'date', css_class='datepicker'),
        # #           Tab('More Info', 'description')))


class StudentInfoForm(forms.Form):
    Sex = [
        ('Sex.male', 'male'),
        ('Sex.female', 'female')
    ]

    name = forms.CharField(label="First name", max_length=50, required=False)
    surname = forms.CharField(label="Last name", max_length=50, required=False)
    patronymic = forms.CharField(label="Middle name", max_length=50, required=False)
    sex = forms.ChoiceField(choices=Sex, label='Sex', widget=forms.RadioSelect(), required=False)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'), label='BirthDay', required=False)
    description = forms.CharField(label="About", widget=forms.Textarea(), required=False)
    Group = form_manager.get_title_list('DepartmentLevel.group')
    department_id = forms.ChoiceField(choices=Group, label='Group', widget=forms.Select(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-personal-data-form'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Name',
                     'name',
                     'surname',
                     'patronymic'),
            Fieldset('General info',
                     Div(InlineRadios('sex')),
                     'date',
                     'description',
                     'department_id'
                     )
        )
