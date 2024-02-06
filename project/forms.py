from django import forms
from .models import Advs, Newspaper, Company,Category,SubCategory,Province,Municipality,District,Officer
from account.models import Action

class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Advs
        fields = ['company', 'newspaper', 'publish_date', 'caption','size']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Set newspaper and company fields as dropdowns
        self.fields['newspaper'] = forms.ModelChoiceField(queryset=Newspaper.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['company'] = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

        # Set publish_date as DateInput
        self.fields['publish_date'] = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

        # Set caption as CharField
        self.fields['caption'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['size'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control','step': 'any', 'min': '0'}))
        
        # Set dropdowns for Page and Color/BW
        page_choices = [('front', 'Front'), ('inside', 'Inside'), ('back', 'Back')]
        color_bw_choices = [('color', 'Color'), ('bw', 'B/W')]

        self.fields['page'] = forms.ChoiceField(choices=page_choices, widget=forms.Select(attrs={'class': 'form-control'}), required=True, label='Page')
        self.fields['color_bw'] = forms.ChoiceField(choices=color_bw_choices, widget=forms.Select(attrs={'class': 'form-control'}), required=True, label='Color/BW')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'category', 'sub_category', 'province', 'district', 'municipality', 'website', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the widgets and add additional attributes as needed
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['category'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['sub_category'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['province'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['district'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['municipality'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['website'].widget = forms.URLInput(attrs={'class': 'form-control'})
        self.fields['address'].widget = forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3,}
        )


        # Add queryset to category field
        self.fields['category'].queryset = Category.objects.all()

        # Add queryset to sub_category field
        self.fields['sub_category'].queryset = SubCategory.objects.all()

        # Add queryset to province field
        self.fields['province'].queryset = Province.objects.all()
                
        self.fields['district'].queryset = District.objects.none()
        
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['district'].queryset = District.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.province.district_set.order_by('name')
        
        self.fields['municipality'].queryset = Municipality.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['municipality'].queryset = Municipality.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['municipality'].queryset = self.instance.district.municipality_set.order_by('name')

        
        
class PaperForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('National', 'National'),
        ('Provincial', 'Provincial'),
        ('Local', 'Local'),
    )
    LEVEL_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    front_bw = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'min': '0'}))
    front_color = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'min': '0'}))
    inside_bw = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'min': '0'}))
    inside_color = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'min': '0'}))
    back_bw = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'min': '0'}))
    back_color = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'min': '0'}))


    class Meta:
        model = Newspaper
        fields = ['name', 'type', 'level', 'front_bw', 'front_color', 'inside_bw', 'inside_color', 'back_bw', 'back_color']
        

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['description', 'officer']

    def __init__(self, company, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3}
        )
        self.fields['officer'].widget = forms.Select(attrs={'class': 'form-control'})
        
        # Add queryset to officer field based on the company
        self.fields['officer'].queryset = Officer.objects.filter(company=company)

        
        

        
      
       