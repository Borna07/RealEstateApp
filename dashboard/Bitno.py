from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

import re
from datetime import datetime
from dashboard.models import Document, Rents
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError






def catch_links_all_pages(url):
    oglasi = []
    page1 = requests.get(url)
    soup1 = BeautifulSoup(page1.content, "html.parser")

    #Get all pages with results
    page_nav_class = soup1.find_all('ul', attrs={'class':"pagination"}) 
    page_nav = page_nav_class[0].find_all('li')
    pages = []
    for item in page_nav:
        try:
            link = item.find('a').get('href')
            if link != None:
                prefix = "https://www.index.hr"
                link = prefix + link
                pages.append(link)
        except:
            pass
    
    pages = list(set(pages))
       
    #Scrape all resluts from every page
    for page in pages:        
        web_page = requests.get(page)
        soup1 = BeautifulSoup(web_page.content, "html.parser")
        results = soup1.find_all('div', attrs={'class':"OglasiRezHolder"}) 
        for result in results:
            try:
                link = result.find('a').get('href')
                oglasi.append(link)
            except:
                pass

    return oglasi

def data_dict_index(url):
    page = requests.get(url)    

    soup = BeautifulSoup(page.content, "html.parser")

    my_dict = {}
    osnovno = soup.find_all('li', attrs={'class':'labela'})
    for row in osnovno:
        a = row.text
        b = row.findNextSibling().get_text().replace("\r\n", "")
        my_dict[a] = b
    my_dict["Cijena"] = soup.find('div', attrs={'class':'price'}).find('span').text
    my_dict["Link"] = url

    datum = soup.find_all('div', attrs={'class':'published'})
    regex = r"\d{2}.\d{2}.\d{4}"
    date = re.findall(regex,datum[1].get_text())[0]
    my_dict["Datum"] = date
    
    return my_dict



def fig_year_build(df):
    
    data = df.groupby("Godina izgradnje").median()
    fig_year_build = px.bar(data, x = data.index, y = data["€/m²"], color = data["€/m²"],)
    # title = "Average price per sqrm of year build")
    fig_year_build.update_layout(
    xaxis_title="Year build",)

    plot_div = plot(fig_year_build, output_type='div')

    return plot_div


def size_hist(df):
    # data_price_per_sqm = df1["€/m²"].describe()

    # fig_price_per_sqm = px.bar(data_price_per_sqm , color = data_price_per_sqm,
    # title="Statistical distribution of price per sqrm",
    fig = px.histogram(df, x="Stambena površina u m2", labels = {"value": "€/m²"})
    fig.update_xaxes(range = [0,320])
    plot_div = plot(fig, output_type='div')

    return plot_div


def avg_price_plot(df):
    
    fig = px.line(df, x="calendar_week", y="avg_price_sqrm", markers=True, color = 'city',)
                    # width=800, height=400)
    plot_div = plot(fig, output_type='div')
    title= "Average price per square meter"
    output = [plot_div, title]
    
    return output


def all_cities_plot(df):
    # fields = ["avg_price_sqrm", "avg_size", "avg_year","raw_entries", "clean_entries",]
    fields = ["avg_price_sqrm", "raw_entries", "clean_entries",]

    output = []
    
    for field in fields:
        fig = px.line(df, x="calendar_week", y=field, markers=True, color = 'city')
        plot_div = plot(fig, output_type='div')
        title= field
        output.append([plot_div, title])
    
    return output


def city_plot(df, city_name):
    fields = ["avg_price_sqrm", "avg_size", "avg_year","raw_entries", "clean_entries",]
    output = []
    
    for field in fields:
        fig = px.line(df, x="calendar_week", y=field, markers=True, )
        plot_div = plot(fig, output_type='div')
        title=city_name + " "  +field
        output.append([plot_div, title])
    
    return output


def all_data_table(df):
    bitno = ["Godina izgradnje","Cijena","Stambena površina u m2","€/m²", "Link"]

    fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3,4,5],
        columnwidth = [80,80,80,80,600],
        header=dict(values=list(bitno),
                    #fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[df[i] for i in bitno],
                #fill_color='lavender',
                align='center'))
    ])
    #fig.update_layout(width=1800, height=2000)

    plot_div = plot(fig, output_type='div')

    return plot_div


#Data Scraping Functions

def catch_links_all_pages(url):
    oglasi = []
    page1 = requests.get(url)
    soup1 = BeautifulSoup(page1.content, "html.parser")

    #Extract the number of pages from navigation bar
    page_nav_class = soup1.find_all('ul', attrs={'class':"pagination"}) 
    page_nav = page_nav_class[0].find_all('li')
    
    
    # #Take the last navigation element
    # last = page_nav[-1]
    # #Extract the number and clean data
    # page_number = last.find('a').get('href')[-3:]
    # page_number = re.sub("[^0-9]", "", page_number)
    # fix = "&num="
    
    pages = []

    #Check if there are multiple pages in the navigation
    if not page_nav:

        pages.append(url)

    else:
        #Take the last navigation element
        last = page_nav[-1]
        #Extract the number and clean data
        page_number = last.find('a').get('href')[-3:]
        page_number = re.sub("[^0-9]", "", page_number)
        fix = "&num="
        # print(page_number)

        #Create a list of all pages with links
        pages.append(url)
        for i in range(2,int(page_number)+1):
                link = url + fix + str(i)
                pages.append(link)

        pages = list(set(pages))
       
    #Scrape all resluts from every page
    for page in pages:        
        web_page = requests.get(page)
        soup1 = BeautifulSoup(web_page.content, "html.parser")
        results = soup1.find_all('div', attrs={'class':"OglasiRezHolder"}) 
        for result in results:
            try:
                link = result.find('a').get('href')
                oglasi.append(link)
            except:
                pass

    oglasi = list(set(oglasi))

    return oglasi

def data_dict_index(url):
    page = requests.get(url)    

    soup = BeautifulSoup(page.content, "html.parser")

    my_dict = {}
    osnovno = soup.find_all('li', attrs={'class':'labela'})
    for row in osnovno:
        a = row.text
        b = row.findNextSibling().get_text().replace("\r\n", "")

        if a in my_dict.keys():
            if b < my_dict[a]:
                my_dict[a] = b
            else:
                pass
        else:
            my_dict[a] = b
    
    my_dict["Cijena"] = soup.find('div', attrs={'class':'price'}).find('span').text
    my_dict["Link"] = url

    datum = soup.find_all('div', attrs={'class':'published'})
    regex = r"\d{2}.\d{2}.\d{4}"
    date = re.findall(regex,datum[1].get_text())[0]
    my_dict["Datum"] = date
    return my_dict

def dataframe_cleaner(df):
    #df = pd.DataFrame(data_list)

    #Data Cleaning

    #Drop rows w/o sqm, convert sqm to float
    df = df[df['Stambena površina u m2'].notna()]
    df["Stambena površina u m2"] = df["Stambena površina u m2"].str.replace(",",".")
    df["Stambena površina u m2"] = df["Stambena površina u m2"].astype('float')

    #Convert price to float, remove no price rows, rempve unrealistic low prices
    df["Cijena"] = df["Cijena"].str.replace("€","")

    df["Cijena"] = df["Cijena"].str.replace(".","")
    df["Cijena"] = df["Cijena"].str.replace(",",".")

    df["Cijena"] = df["Cijena"].str.replace(" ","")

    df = df[df["Cijena"] != "0,00 "]
    df["Cijena"] = df["Cijena"].astype('float')
    df = df[df["Cijena"] > 10000]

    #Replace Nan with "No info"
    df['Godina izgradnje'].fillna('No INFO', inplace=True)

    #Remove where m2 == 0
    df = df[df["Stambena površina u m2"] > 10]
    df = df[df["Stambena površina u m2"] < 10000]




    #Add a price per sqm meter column
    df["€/m²"] = round(df["Cijena"] / df["Stambena površina u m2"],2)

    #Convert Datum to datetime
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

    #Calculate days online
    df['Days Online'] = ( pd.Timestamp('now') - df['Datum']).dt.days

    return df


def dataframe_cleaner_rent(df):
    #df = pd.DataFrame(data_list)

    #Data Cleaning

    #Drop rows w/o sqm, convert sqm to float
    df = df[df['Stambena površina u m2'].notna()]
    df["Stambena površina u m2"] = df["Stambena površina u m2"].str.replace(",",".")
    df["Stambena površina u m2"] = df["Stambena površina u m2"].astype('float')

    #Convert price to float, remove no price rows, rempve unrealistic low prices
    df["Cijena"] = df["Cijena"].str.replace("€","")

    df["Cijena"] = df["Cijena"].str.replace(".","")
    df["Cijena"] = df["Cijena"].str.replace(",",".")

    df["Cijena"] = df["Cijena"].str.replace(" ","")

    df = df[df["Cijena"] != "0,00 "]
    df["Cijena"] = df["Cijena"].astype('float')

    #Replace Nan with "No info"
    df['Godina izgradnje'].fillna('No INFO', inplace=True)


    #Remove where m2 == 0
    df = df[df["Cijena"] > 100]
    df = df[df["Cijena"] < 5000]

    #Remove where m2 == 0
    df = df[df["Stambena površina u m2"] > 10]
    df = df[df["Stambena površina u m2"] < 10000]




    #Add a price per sqm meter column
    df["€/m²"] = round(df["Cijena"] / df["Stambena površina u m2"],2)

    #Convert Datum to datetime
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

    #Calculate days online
    df['Days Online'] = ( pd.Timestamp('now') - df['Datum']).dt.days

    return df

def data_median_for_chart(dataframe: pd.DataFrame, group_colum: str, values_column: str):
    data = dataframe.groupby(group_colum).median()
    labels = data.index.tolist()
    data_values = data[values_column].values.tolist()

    return [labels, data_values]

def data_median_for_chart_plt(dataframe: pd.DataFrame, group_colum: str, values_column: str):
    
    data = dataframe.groupby(group_colum).median()
    fig_year_build = px.bar(data, x = data.index, y = data[values_column], color = data[values_column],)
    # title = "Average price per sqrm of year build")
    fig_year_build.update_layout(
    xaxis_title="Year build",)

    plot_div = plot(fig_year_build, output_type='div')

    return plot_div

def price_plot(dataframe: pd.DataFrame, x_labels: str, y_values: str, color_values : str):
    
    fig = px.line(dataframe, x=x_labels, y=y_values, markers=True, color = color_values,)
                    # width=800, height=400)
    plot_div = plot(fig, output_type='div')

    
    return plot_div

def table_from_df(dataframe: pd.DataFrame, columns_list: list, sort_by: str):
    lines_df = dataframe[columns_list]
    #Sort table according to price
    lines_df = lines_df.sort_values(by=[sort_by])
    table_list = lines_df.values.tolist()

    return table_list

