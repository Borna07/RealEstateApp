from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Document
from dashboard.Bitno import *
import pandas as pd
from pathlib import Path

from RealEstateApp.settings import MEDIA_ROOT


def index(request):

    #all_data = Document.objects.all()

    fields = ["city","calendar_week", "raw_entries", "clean_entries", 
    "avg_price_sqrm", "avg_size", "avg_year"]

    # if request.method == "POST":
    #     city_name = request.POST.get("df")
    #     datasets = Document.objects.filter(city=city_name)
    # else:
    #     city_name = "Zagreb"
    #     datasets = Document.objects.filter(city=city_name)
    #     queryset = Document.objects.values_list(fields)
    #     df = pd.DataFrame(list(queryset), columns=fields)     

    city_name = "Zagreb"
    datasets = Document.objects.filter(city=city_name).values_list("city","calendar_week", "raw_entries", "clean_entries", "avg_price_sqrm", "avg_size", "avg_year")
    df = pd.DataFrame(list(datasets), columns=fields) 

    plot = city_plot(df, city_name)

    context = {'plot':plot}


    return render(request, 'dashboard/index.html',context)


def deepDive(request):
    all_data = Document.objects.all()

    if request.method == "POST":
        selected_dataset_id = request.POST.get("df")
        dataset = Document.objects.get(id = selected_dataset_id)

    else:
        last_dataset_id = Document.objects.latest("uploaded_at").id
        dataset = Document.objects.get(id = last_dataset_id)

    general_data = [dataset.clean_entries, dataset.avg_price_sqrm, dataset.avg_size, dataset.avg_year]


    REPORT_DIR = Path(MEDIA_ROOT) / str(dataset)

    df = pd.read_excel(REPORT_DIR, index_col=0)

    #Test für Chart.js
    data = df.groupby("Godina izgradnje").median()

    labels = data.index.tolist()
    data_values = data["€/m²"].values.tolist()


    year_build = fig_year_build(df)
    price_per_sqm = fig_price_per_sqm(df)




    #Create table with important data
    lines_df = df[["Godina izgradnje","Cijena","Stambena površina u m2","€/m²", "Link"]]
    #Sort table according to price
    lines_df = lines_df.sort_values(by=["Cijena"])
    lines = lines_df.values.tolist()

    context = {'file_download':dataset.document,'price_per_sqm':price_per_sqm, 'labels':labels, 'values':data_values ,'general_data':general_data, 
            'lines':lines,'year_build': year_build, "price_per_sqm":price_per_sqm,
            "max": [dataset.highest_price, dataset.highest_price_link],
            "max_per_sqr" : [dataset.highest_price_sqrm, dataset.highest_price_sqrm_link], "min" : [dataset.lowest_price, dataset.lowest_price_link], 
            "min_per_sqr" : [dataset.lowest_price_sqrm, dataset.lowest_price_sqrm_link]}

    return render(request, 'dashboard/index.html',context)



    #EXCEL FROM MODEL
    # fields = ["city","calendar_week", "raw_entries", "clean_entries", 
    # "avg_price_sqrm", "avg_size", "avg_year"]

    # df = pd.DataFrame.from_records(Document.objects.all().values_list("city","calendar_week", "raw_entries", "clean_entries", 
    #                             "avg_price_sqrm", "avg_size", "avg_year"), columns = fields)
    # df.to_excel("Django_Objects.xlsx")
    # queryset = Document.objects.values_list(fields)
    # df = pd.DataFrame(list(queryset), columns=fields) 
    # print(df)