import django_filters
from django import forms
from .models import Company,Category,SubCategory,Province,District,Municipality

class CompanyFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label='Select Category',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    sub_category = django_filters.ModelChoiceFilter(
        queryset=SubCategory.objects.all(),
        empty_label='Select Sub Category',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        empty_label='Select Province',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.all(),
        empty_label='Select District',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    municipality = django_filters.ModelChoiceFilter(
        queryset=Municipality.objects.all(),
        empty_label='Select Municipality',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Company
        fields = ['category', 'sub_category', 'province', 'district', 'municipality']
