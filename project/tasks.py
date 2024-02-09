from celery import shared_task
from django.core.mail import EmailMessage
from django.db.models import Count, Sum
from datetime import datetime
from .models import Advs
from account.models import ProvinceAdmin, User
from django.contrib.auth import get_user_model
import pandas as pd
import os
from django.apps import apps
from celery import Celery
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

from io import BytesIO  # Import BytesIO

@shared_task(bind=True)
def generate_and_send_excel(self):
    
    try:
        # Get all objects of Advs
        advs_data = Advs.objects.values(
            'company__name',
            'company__province__name',
        ).annotate(
            publish_frequency=Count('company'),
            budget_spent=Sum('balance'),
            size=Sum('size')
        )

        # Create a DataFrame from the queried data
        df = pd.DataFrame(advs_data, columns=["company__name", "company__province__name", "publish_frequency", "budget_spent", "size"])

        # Rename columns to match your requirements
        df = df.rename(columns={
            'company__name': 'Customer Name',
            'company__province__name': 'Province',
            'publish_frequency': 'Publish Frequency',
            'budget_spent': 'Budget Spent',
            'size': 'Size (CC)'
        })

        # Group by 'Province' and create a dictionary of DataFrames
        province_dfs = {}
        for province, province_data in df.groupby('Province'):
            province_dfs[province] = province_data

        # Fetch admin province objects
        admin_provinces = ProvinceAdmin.objects.all()

        # Iterate through admin provinces and send emails
        for admin_province in admin_provinces:
            province_name = admin_province.province.name

            if province_name in province_dfs:
                # Attach the corresponding DataFrame to the email
                province_df = province_dfs[province_name]
                excel_file_path = f'daily_digest_{province_name}.xlsx'
                province_df.to_excel(excel_file_path, index=False)

                # Email content
                subject = 'Daily Digest'
                message = f'Here is the daily digest for {admin_province}.'
                
                # Attach the Excel file
                from_email = settings.DEFAULT_FROM_EMAIL
                email = EmailMessage(subject, message, from_email, [admin_province.admin.email])
                email.attach_file(excel_file_path)

                # Send the email
                email.send()
                
    except Exception as e:
        logger.error(f"Error in generate_and_send_excel: {e}")
        raise
