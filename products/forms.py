from .models import Product,Categories,Source
from django import forms

class ProductFilterForm(forms.Form):
    FILTER_CHOICES = (
        ('PriceAsc', '價格-低到高'),
        ('PriceDesc', '價格-高到低'),
    )

    filter_by = forms.ChoiceField(label="", required="",help_text="",choices = FILTER_CHOICES,widget=forms.Select(attrs={'class':'sorting','onchange': 'submit();'}))

class ProductSourceForm(forms.Form):
    SOURCE_CHOICES = [
        ('shopee','蝦皮購物'),
        ('ruten','露天拍賣'),
        ('yahoo','Yahoo拍賣'),
        ('momo','momo購物'),
        ('etmall','東森購物')
    ]
    source = forms.MultipleChoiceField(
        label="",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'onchange': 'submit();','class':"checkmark" }),
        choices=SOURCE_CHOICES,
    )

class ProductPriceForm(forms.Form):
    min_price = forms.CharField(label="", required="",help_text="", widget=forms.TextInput(attrs={'id':'minamount'}))
    max_price = forms.CharField(label="", required="",help_text="",widget=forms.TextInput(attrs={'id':'maxamount'}))
