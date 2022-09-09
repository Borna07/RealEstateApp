from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Document
from dashboard.Bitno import *
import pandas as pd

def index(request):
    all_data = Document.objects.all()
    fields = ["city","calendar_week", "raw_entries", "clean_entries", 
    "avg_price_sqrm", "avg_size", "avg_year"]

    df = pd.DataFrame.from_records(Document.objects.all().values_list("city","calendar_week", "raw_entries", "clean_entries", 
                                "avg_price_sqrm", "avg_size", "avg_year"), columns = fields)
    print(df)
    df.to_excel("Django_Objects.xlsx")
    # queryset = Document.objects.values_list(fields)
    # df = pd.DataFrame(list(queryset), columns=fields) 
    # print(df)

    return HttpResponse("Hello, world. You're at the polls index.")