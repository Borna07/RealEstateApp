from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Document
from dashboard.Bitno import *
import pandas as pd
from pathlib import Path

from RealEstateApp.settings import MEDIA_ROOT






def index(request):


    fields = ["city","calendar_week", "raw_entries", "clean_entries", 
    "avg_price_sqrm", "avg_size", "avg_year"]

    
    datasets_values = Document.objects.all().values_list("city","calendar_week", "raw_entries", "clean_entries", 
                                "avg_price_sqrm", "avg_size", "avg_year")
    df = pd.DataFrame.from_records(datasets_values, columns = fields)

    # datasets = Document.objects.filter(city=city_name).values_list("city","calendar_week", "raw_entries", "clean_entries", "avg_price_sqrm", "avg_size", "avg_year")
    # df = pd.DataFrame(list(datasets), columns=fields) 

    df['calendar_week'] = df['calendar_week'].astype(int)

    x_values = list(df['calendar_week'].unique())
    datasets_zg = Document.objects.filter(city="Zagreb").values_list("city","calendar_week", "raw_entries", "clean_entries", 
                                "avg_price_sqrm", "avg_size", "avg_year")
    datasets_st = Document.objects.filter(city="Split").values_list("city","calendar_week", "raw_entries", "clean_entries", 
                                "avg_price_sqrm", "avg_size", "avg_year")
    datasets_ri = Document.objects.filter(city="Rijeka").values_list("city","calendar_week", "raw_entries", "clean_entries", 
                                "avg_price_sqrm", "avg_size", "avg_year")

    y_zg = [value[4] for value in datasets_zg]
    y_st = [value[4] for value in datasets_st]
    y_ri = [value[4] for value in datasets_ri]


    plot = all_cities_plot(df)

    context = {'plot':plot, 'y_zg':y_zg, 'y_ri':y_ri, 'y_st':y_st,'x_values':x_values}


    return render(request, 'dashboard/index.html',context)


def get_city_data(request, city_name=None):


    #all_data = Document.objects.all()

    fields = ["city","calendar_week", "raw_entries", "clean_entries", 
    "avg_price_sqrm", "avg_size", "avg_year"]


    datasets = Document.objects.filter(city=city_name)
    datasets_values = datasets.values_list("city","calendar_week", "raw_entries", "clean_entries", "avg_price_sqrm", "avg_size", "avg_year")
    df = pd.DataFrame(list(datasets_values), columns=fields) 



    #Test für Chart.js
    x_values = [value[1] for value in datasets_values]
    raw_entries = [value[2] for value in datasets_values]
    clean_entries = [value[3] for value in datasets_values]
    avg_price_sqrm = [value[4] for value in datasets_values]
    avg_size = [value[5] for value in datasets_values]
    avg_year = [value[6] for value in datasets_values]

    avg_size = zip(x_values, avg_size)
    avg_year = zip(x_values, avg_year)

    plot = city_plot(df, city_name)

    context = {'datasets' : datasets,'plot':plot,'x_values':x_values, 'raw_entries':raw_entries, 'clean_entries': clean_entries,
    'avg_price_sqrm':avg_price_sqrm, 'avg_size':avg_size, 'avg_year': avg_year}


    return render(request, 'dashboard/city_name.html',context)


def deepDive(request, city_name=None, week = None):
    datasets = Document.objects.all()


    dataset = Document.objects.get(city = city_name, calendar_week = week)

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


    context = {'datasets' : datasets, 'file_download':dataset.document,'price_per_sqm':price_per_sqm, 'labels':labels, 'values':data_values ,'general_data':general_data, 
            'lines':lines,'year_build': year_build, "price_per_sqm":price_per_sqm,
            "max": [dataset.highest_price, dataset.highest_price_link],
            "max_per_sqr" : [dataset.highest_price_sqrm, dataset.highest_price_sqrm_link], "min" : [dataset.lowest_price, dataset.lowest_price_link], 
            "min_per_sqr" : [dataset.lowest_price_sqrm, dataset.lowest_price_sqrm_link]}

    return render(request, 'dashboard/deepdive.html',context)




# def deepDive(request):
#     datasets = Document.objects.all()

#     if request.method == "POST":
#         selected_dataset_id = request.POST.get("df")
#         dataset = Document.objects.get(id = selected_dataset_id)

#     else:
#         last_dataset_id = Document.objects.latest("uploaded_at").id
#         dataset = Document.objects.get(id = last_dataset_id)

#     general_data = [dataset.clean_entries, dataset.avg_price_sqrm, dataset.avg_size, dataset.avg_year]


#     REPORT_DIR = Path(MEDIA_ROOT) / str(dataset)

#     df = pd.read_excel(REPORT_DIR, index_col=0)

#     #Test für Chart.js
#     data = df.groupby("Godina izgradnje").median()

#     labels = data.index.tolist()
#     data_values = data["€/m²"].values.tolist()


#     year_build = fig_year_build(df)
#     price_per_sqm = fig_price_per_sqm(df)

#     #Create table with important data
#     lines_df = df[["Godina izgradnje","Cijena","Stambena površina u m2","€/m²", "Link"]]
#     #Sort table according to price
#     lines_df = lines_df.sort_values(by=["Cijena"])
#     lines = lines_df.values.tolist()

#     context = {'datasets' : datasets, 'file_download':dataset.document,'price_per_sqm':price_per_sqm, 'labels':labels, 'values':data_values ,'general_data':general_data, 
#             'lines':lines,'year_build': year_build, "price_per_sqm":price_per_sqm,
#             "max": [dataset.highest_price, dataset.highest_price_link],
#             "max_per_sqr" : [dataset.highest_price_sqrm, dataset.highest_price_sqrm_link], "min" : [dataset.lowest_price, dataset.lowest_price_link], 
#             "min_per_sqr" : [dataset.lowest_price_sqrm, dataset.lowest_price_sqrm_link]}

#     return render(request, 'dashboard/deepdive.html',context)



    #EXCEL FROM MODEL
    # fields = ["city","calendar_week", "raw_entries", "clean_entries", 
    # "avg_price_sqrm", "avg_size", "avg_year"]

    # df = pd.DataFrame.from_records(Document.objects.all().values_list("city","calendar_week", "raw_entries", "clean_entries", 
    #                             "avg_price_sqrm", "avg_size", "avg_year"), columns = fields)
    # df.to_excel("Django_Objects.xlsx")
    # queryset = Document.objects.values_list(fields)
    # df = pd.DataFrame(list(queryset), columns=fields) 
    # print(df)