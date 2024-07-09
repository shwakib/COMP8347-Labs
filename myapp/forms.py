from django import forms
from myapp.models import Order


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
        ('T', 'Test Option'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)


class SearchForm(forms.Form):
    CATEGORIES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]

    name = forms.CharField(
        required=False,
        max_length=100,
        label='Your Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your name'
        })
    )

    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.RadioSelect,
        required=False,
        label='Select a category:'
    )

    max_price = forms.IntegerField(
        required=True,
        label='Maximum Price',
        min_value=0
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'status']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': u'Member name', }
