from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms


class AchievementForm(forms.Form):
    Years = [x for x in range(1960, 2019)]
    Category = [
        ('Category.sport', 'Sport'),
        ('Category.education', 'Education'),
        ('Category.social', 'Social')
    ]
    title = forms.CharField(label="Title", max_length=50)
    category = forms.ChoiceField(choices=Category, label="Category", widget=forms.Select())
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'), label='Date', required=False)
    description = forms.CharField(label="About", max_length=50,  required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'category',
            'title',
            'date',
            'description')
