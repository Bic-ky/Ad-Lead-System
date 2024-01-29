from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from .models import Advs,Newspaper,Province,District,Municipality
from .forms import NewspaperForm,CompanyForm,PaperForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages


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
        messages.success(request, 'Lead was added Succesfully')

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
            messages.success(request, 'Company was added Succesfully')
            
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
            messages.success(request, 'Newspaper was added Succesfully')
            
            return redirect('add_newspaper')
    else:
        # If the request method is not POST, create an instance of the form
        form = PaperForm()

    context = {
        'form': form,
    }
    return render(request, 'add_company.html', context)