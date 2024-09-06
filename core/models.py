from django.db import models

class Asset(models.Model):
    ASSET_CATEGORIES = [
        ('electronics', 'Electronics'),
        ('building', 'Building'),
        ('furniture', 'Furniture'),
        ('equipment', 'Equipment'),
        ('vehicle', 'Vehicle'),
    ]
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=100, choices=ASSET_CATEGORIES)
    name = models.CharField(max_length=100)
    date = models.DateField()
    asset_value = models.DecimalField(max_digits=10, decimal_places=2)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('broken', 'Broken')
    ])
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    tag_number = models.CharField(max_length=50, unique=True, editable=False, blank=True, null=True)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
    
    def __str__(self):
        return f"{self.name} ({self.category})"

    def save(self, *args, **kwargs):
        # Generate the tag number if it hasn't been set
        if not self.tag_number:
            if self.id is None:
                # Save the instance to generate an ID if it's not already set
                super().save(*args, **kwargs)
            self.tag_number = self.generate_tag_number()
        super().save(*args, **kwargs)

    def generate_tag_number(self):
        if self.id is None:
            return "TAG-000000"  # Default value if ID is not set
        prefix = self.category[:3].upper()  # First three letters of the category in uppercase
        return f"{prefix}-{self.id:06d}"  # E.g., ELE-000001



