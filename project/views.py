from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from .models import Advs,Newspaper,Province,District,Municipality,Company,Officer
from account.models import ProvinceAdmin,Action
from .forms import NewspaperForm,CompanyForm,PaperForm,ActionForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .filters import CompanyFilter
from django.http import JsonResponse,HttpResponse
from datetime import date


def calculate_adv_spend(company_id):
    # Filter Advs by the given company_id and annotate with the spend of type * size
    queryset = Advs.objects.filter(company_id=company_id).annotate(
        spend=Coalesce(F('adv_type') * F('size'), 1.0)
    )

    # Aggregate the spends to get the total spend
    total_spend = queryset.aggregate(total_spend=Sum('spend'))['total_spend']

    return total_spend


def add_lead(request):
    if request.method == 'POST':
        company_id = request.POST.get('company')
        newspaper_id = request.POST.get('newspaper')
        publish_date = request.POST.get('publish_date')
        caption = request.POST.get('caption')
        size = request.POST.get('size')
        page=request.POST.get('page')
        color_bw=request.POST.get('color_bw')
        
        
        selected_newspaper = Newspaper.objects.get(pk=newspaper_id)
        if page == 'front':
            front_value = selected_newspaper.front_bw if color_bw == 'bw' else selected_newspaper.front_color
            sum_amount=front_value

        elif page == 'inside':
            inside_value = selected_newspaper.inside_bw if color_bw == 'bw' else selected_newspaper.inside_color
            sum_amount=inside_value
            
        elif page == 'back':
            back_value = selected_newspaper.back_bw if color_bw == 'bw' else selected_newspaper.back_color
            sum_amount=back_value
                    
        balance = sum_amount * float(size)
        adv_type= page+color_bw
        
        # Create Advs instance and save to the database
        advs = Advs.objects.create(
            company_id=company_id,
            newspaper_id=newspaper_id,
            publish_date=publish_date,
            caption=caption,
            size=float(size),
            adv_type=adv_type,
            balance=balance
        )
        

        return redirect('add_lead')  

    # Render the form page with an instance of the NewspaperForm
    context = {
        'form': NewspaperForm(),
    }
    return render(request, 'add_lead.html', context)

def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            # Save the form data if it's valid
            form.save()
           
            return redirect('add_company')
    else:
        # If the request method is not POST, create an instance of the form
        form = CompanyForm()

    context = {
        'form': form,
    }
    return render(request, 'add_company.html', context)


def add_newspaper(request):
    if request.method == 'POST':
        form = PaperForm(request.POST)
        if form.is_valid():
            # Save the form data if it's valid
            form.save()
            
            
            return redirect('add_newspaper')
    else:
        # If the request method is not POST, create an instance of the form
        form = PaperForm()

    context = {
        'form': form,
    }
    return render(request, 'add_newspaper.html', context)


def company(request):
    admin = request.user

    try:
        # Fetch all ProvinceAdmin objects related to the admin
        province_admins = ProvinceAdmin.objects.filter(admin=admin)

        # Extract provinces from ProvinceAdmin objects
        provinces = [province_admin.province for province_admin in province_admins]

        # Fetch all companies
        all_companies = Company.objects.all()

        # Filter all companies based on the list of provinces
        company_filter = CompanyFilter(request.GET, queryset=all_companies)
        all_companies_filtered = company_filter.qs

        # Fetch my companies and apply the same filters
        mycompany = Company.objects.filter(province__in=provinces)
        mycompany_filter = CompanyFilter(request.GET, queryset=mycompany)
        mycompany_filtered = mycompany_filter.qs

    except ProvinceAdmin.DoesNotExist:
        # Handle the case where ProvinceAdmin does not exist for the admin
        all_companies_filtered = Company.objects.none()
        mycompany_filtered = Company.objects.none()

    context = {
        'company': all_companies_filtered,
        'mycompany': mycompany_filtered,
        'filter': company_filter,
    }

    return render(request, 'company_list.html', context)


def company_profile(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    officers = Officer.objects.filter(company=company)
    actions = Action.objects.filter(company=company)
    user = request.user
    today = date.today()

    if request.method == 'POST':
        form = ActionForm(company, request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.company = company
            action.date = today
            action.admin = user
            form.save()  # Assuming you have a save method in your ActionForm
    else:
        form = ActionForm(company)

    context = {
        'company': company,
        'officers': officers,
        'actions': actions,
        'form': form,
    }
    return render(request, 'company_profile.html', context)


    

def get_districts(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).order_by('name')
    options = '<option value="">Select District</option>'
    
    for district in districts:
        options += f'<option value="{district.id}">{district.name}</option>'
    
    return HttpResponse(options)

# views.py
def get_municipalities(request):
    district_id = request.GET.get('district_id')
    municipalities = Municipality.objects.filter(district_id=district_id).order_by('name')
    options = '<option value=""> Select Municiplaity</option>'

    for municipality in municipalities:
        options += f'<option value="{municipality.id}">{municipality.name}</option>'

    return HttpResponse(options)





