from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
from dashboard.Bitno import *
from dashboard.City_info import Info
from datetime import datetime
from RealEstateApp.settings import MEDIA_ROOT
pd.options.mode.chained_assignment = None 
import subprocess



class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    
    def handle(self, *args, **options):

        for city in Info.keys():

            try:

                city_name = city

                url = Info[city_name][2]
                ime = Info[city_name][1]


                #find all pages
                pages = catch_links_all_pages(url)
                
                #scrape all pages
                data_list = []
                for page in pages:
                    try:
                        data_list.append(data_dict_index(page))
                    except:
                        pass

                #create dataframe
                df = pd.DataFrame(data_list)
                current_date = datetime.now().date()
                currentMonth = datetime.now().strftime('%B')
                currentYear = datetime.now().year
                year_month = str(currentYear) + " - " + str(currentMonth)

                #check raw entries, save raw dataframe
                dj_raw_entries = len(df.index)
                
                full_ime_raw = str(current_date) + "_RAW" + ime + ".xlsx"
                raw_path =  MEDIA_ROOT + "/" + full_ime_raw
                dj_df_raw  = df.to_excel(raw_path)

                #clean dataframe
                df = dataframe_cleaner(df)

                full_ime =  str(current_date) + ime + ".xlsx"
                clean_path = MEDIA_ROOT + "/" + full_ime
                dj_df = df.to_excel(clean_path)
                dj_clean_entries = len(df.index)

                dj_avg_price_sqrm = round(df["€/m²"].mean(),2)
                dj_avg_size = round(df["Stambena površina u m2"].mean(),2)
                dj_avg_year = df[df["Godina izgradnje"] != "No INFO"]["Godina izgradnje"].mode()[0]



                max_df = df[df['Cijena'] == df['Cijena'].max()]
                max = [max_df["Cijena"].values[0], max_df["Link"].values[0]]

                max_per_sqr_df = df[df['€/m²'] == df['€/m²'].max()]
                max_per_sqr = [max_per_sqr_df['€/m²'].values[0], max_per_sqr_df['Link'].values[0]]

                min_df = df[df['Cijena'] == df['Cijena'].min()]
                min = [min_df["Cijena"].values[0], min_df["Link"].values[0]]

                min_per_sqr_df = df[df['€/m²'] == df['€/m²'].min()]
                min_per_sqr = [min_per_sqr_df['€/m²'].values[0], min_per_sqr_df['Link'].values[0]]

                med_sale_price = df["Cijena"].mean()

                time_now = timezone.now()





                Document.objects.create(
                    document = full_ime, document_raw = full_ime_raw, uploaded_at = time_now,
                    calendar_week = time_now.isocalendar()[1] , year_calendar_month = year_month, raw_entries = dj_raw_entries, clean_entries = dj_clean_entries,
                    city = city_name, avg_price_sqrm = dj_avg_price_sqrm, avg_size = dj_avg_size,
                    avg_year = dj_avg_year, highest_price = max[0], highest_price_link = max[1],
                    highest_price_sqrm = max_per_sqr[0], highest_price_sqrm_link = max_per_sqr[1],
                    lowest_price = min[0], lowest_price_link = min[1], lowest_price_sqrm = min_per_sqr[0],
                    lowest_price_sqrm_link = min_per_sqr[1], avg_price = med_sale_price
                )
            except:
                pass

                # Add changes to the staging area
        subprocess.run(["git", "add", "."])

        # Create a commit with a message
        subprocess.run(["git", "commit", "-m", "Update database"])

        # Push the commit to the remote repository
        subprocess.run(["git", "push"])


