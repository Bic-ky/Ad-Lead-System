from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from .models import Advs


def calculate_adv_spend(company_id):
    # Filter Advs by the given company_id and annotate with the spend of type * size
    queryset = Advs.objects.filter(company_id=company_id).annotate(
        spend=Coalesce(F('adv_type') * F('size'), 1.0)
    )

    # Aggregate the spends to get the total spend
    total_spend = queryset.aggregate(total_spend=Sum('spend'))['total_spend']

    return total_spend
