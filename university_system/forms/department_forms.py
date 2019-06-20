from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms

from university_system.forms import form_manager


class DepartmentForm(forms.Form):
    Titles = form_manager.get_title_list()
    parent_department_id = forms.ChoiceField(choices=Titles, label='Belongs to', widget=forms.Select())
    Level = [
        ('DepartmentLevel.university', 'University'),
        ('DepartmentLevel.chair', 'Faculty'),
        ('DepartmentLevel.group', 'Group'),
    ]
    level = forms.ChoiceField(choices=Level, label='Level', widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.render_required_fields = False
        self.helper.layout = Layout(
            Fieldset('Registration info',
                     'parent_department_id',
                     'level')
        )


class DepartmentInfoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    description = forms.CharField(label="About", widget=forms.Textarea(), required=False)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'), label='Date', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('General Info',
                     'title',
                     'date',
                     'description')
        )


class HeadForm(forms.Form):
    name = forms.CharField(label="First name", max_length=50, required=False)
    surname = forms.CharField(label="Last Name", max_length=50, required=False)
    patronymic = forms.CharField(label="Middle Name", max_length=50, required=False)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'), label='BirthDay', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('General Info',
                     'name',
                     'surname',
                     'patronymic',
                     'date')
        )
