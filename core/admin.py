import csv
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Sum
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from .models import *

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'location', 'condition', 'is_active', 'asset_value', 'tag_number')
    list_filter = ('category', 'condition', 'is_active')
    search_fields = ('name', 'serial_number', 'location', 'assigned_to')
    # list_editable = ('is_active',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    actions = ['export_assets_report_csv']

    def export_assets_report_csv(self, request, queryset):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="assets_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Tag Number', 'Name', 'Category', 'Date Recorded', 'Location', 'Condition', 'Is Active', 'Asset Value (USD)'])

        # Write data rows
        for asset in queryset:
            writer.writerow([
                asset.tag_number if asset.tag_number else "N/A",
                asset.name if asset.name else "N/A",
                asset.category if asset.category else "N/A",
                asset.date if asset.date else "N/A",
                asset.location if asset.location else "N/A",
                asset.condition if asset.condition else "N/A",
                'Yes' if asset.is_active else 'No',
                f"${asset.asset_value:,.2f}" if asset.asset_value else "$0.00"
            ])

        # Calculate summary information
        total_assets = queryset.count()
        total_value = queryset.aggregate(total_value=Sum('asset_value'))['total_value']
        broken_assets = queryset.filter(condition='broken').count()

        writer.writerow([])
        writer.writerow(['Summary'])
        writer.writerow(['Total Assets', total_assets])
        writer.writerow(['Total Value (USD)', f"${total_value:,.2f}" if total_value else "$0.00"])
        writer.writerow(['Total Broken Assets', broken_assets])

        return response

    export_assets_report_csv.short_description = "Export Selected Assets as CSV"

    
