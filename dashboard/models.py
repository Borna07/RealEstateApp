from django.db import models

# Create your models here.

def only_filename(instance, filename):
    return filename


class Document(models.Model):
    # description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=only_filename)   
    document_raw = models.FileField(upload_to=only_filename, default="Some String")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    calendar_week = models.CharField(max_length=200, null=True)
    raw_entries = models.IntegerField(null=True)
    clean_entries = models.IntegerField(null=True)
    city = models.CharField(max_length=200, null=True)
    avg_price_sqrm = models.IntegerField(null=True, default=0)
    avg_size = models.IntegerField(null=True, default=0)
    avg_year = models.IntegerField(null=True, default=0)

    highest_price = models.IntegerField(null=True, default=0)
    highest_price_link = models.URLField(max_length = 200, default="Some String")
    highest_price_sqrm = models.IntegerField(null=True, default=0)
    highest_price_sqrm_link = models.URLField(max_length = 200, default="Some String")
    lowest_price = models.IntegerField(null=True, default=0)
    lowest_price_link =models.URLField(max_length = 200, default="Some String")
    lowest_price_sqrm = models.IntegerField(null=True, default=0)
    lowest_price_sqrm_link = models.URLField(max_length = 200, default="Some String")

    def __str__(self):
        return self.document.name