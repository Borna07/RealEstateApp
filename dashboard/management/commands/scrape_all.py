from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
from numpy import full
from dashboard.Bitno import *
from datetime import datetime
from RealEstateApp.settings import MEDIA_ROOT
pd.options.mode.chained_assignment = None 



class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    
    def handle(self, *args, **options):

        URL_vz = "https://www.index.hr/oglasi/prodaja-stanova/gid/3278?pojamZup=1166&tipoglasa=1&sortby=1&elementsNum=100&city=1638&naselje=0&cijenaod=0&cijenado=21000000&vezani_na=988-887_562-563_978-1334&num=1"
        URL_rovinj = "https://www.index.hr/oglasi/prodaja-stanova/gid/3278?pojam=&sortby=1&elementsNum=100&cijenaod=0&cijenado=21000000&tipoglasa=1&pojamZup=1154&city=1294&naselje=3374&attr_Int_988=&attr_Int_887=&attr_bit_stan=&attr_bit_brojEtaza=&attr_gr_93_1=&attr_gr_93_2=&attr_Int_978=&attr_Int_1334=&attr_bit_eneregetskiCertifikat=&vezani_na=988-887_562-563_978-1334"
        URL_zg = "https://www.index.hr/oglasi/prodaja-stanova/gid/3278?pojam=&sortby=1&elementsNum=100&cijenaod=0&cijenado=21000000&tipoglasa=1&pojamZup=1153&city=&naselje=&attr_Int_988=&attr_Int_887=&attr_bit_stan=&attr_bit_brojEtaza=&attr_gr_93_1=&attr_gr_93_2=&attr_Int_978=&attr_Int_1334=&attr_bit_eneregetskiCertifikat=&vezani_na=988-887_562-563_978-1334"
        URL_st = "https://www.index.hr/oglasi/prodaja-stanova/gid/3278?pojam=&sortby=1&elementsNum=100&cijenaod=0&cijenado=21000000&tipoglasa=1&pojamZup=1164&grad=1578&naselje=&attr_Int_988=&attr_Int_887=&attr_bit_stan=&attr_bit_brojEtaza=&attr_gr_93_1=&attr_gr_93_2=&attr_Int_978=&attr_Int_1334=&attr_bit_eneregetskiCertifikat=&vezani_na=988-887_562-563_978-1334"
        URL_ri = "https://www.index.hr/oglasi/prodaja-stanova/gid/3278?pojam=&sortby=1&elementsNum=100&cijenaod=0&cijenado=21000000&tipoglasa=1&pojamZup=1162&grad=1511&naselje=&attr_Int_988=&attr_Int_887=&attr_bit_stan=&attr_bit_brojEtaza=&attr_gr_93_1=&attr_gr_93_2=&attr_Int_978=&attr_Int_1334=&attr_bit_eneregetskiCertifikat=&vezani_na=988-887_562-563_978-1334"



        vz = [URL_vz, "Varazdin", "_varazdin"]
        ro = [URL_rovinj, "Rovinj", "_rovinj"]
        ri = [URL_ri, "Rijeka", "_rijeka"]
        st = [URL_st, "Split", "_split"]
        zg = [URL_zg, "Zagreb", "_zagreb"]

        cities = [ri, st, zg]
#        cities = [vz, ro, ri, st, zg]

        for city in cities:
            url = city[0]
            city_name = city[1]
            ime = city[2]
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

            dj_avg_price_sqrm = round(df["???/m??"].mean(),2)
            dj_avg_size = round(df["Stambena povr??ina u m2"].mean(),2)
            dj_avg_year = df[df["Godina izgradnje"] != "No INFO"]["Godina izgradnje"].mode()[0]



            max_df = df[df['Cijena'] == df['Cijena'].max()]
            max = [max_df["Cijena"].values[0], max_df["Link"].values[0]]

            max_per_sqr_df = df[df['???/m??'] == df['???/m??'].max()]
            max_per_sqr = [max_per_sqr_df['???/m??'].values[0], max_per_sqr_df['Link'].values[0]]

            min_df = df[df['Cijena'] == df['Cijena'].min()]
            min = [min_df["Cijena"].values[0], min_df["Link"].values[0]]

            min_per_sqr_df = df[df['???/m??'] == df['???/m??'].min()]
            min_per_sqr = [min_per_sqr_df['???/m??'].values[0], min_per_sqr_df['Link'].values[0]]

            time_now = timezone.now()


            Document.objects.create(
                document = full_ime, document_raw = full_ime_raw, uploaded_at = time_now,
                calendar_week = time_now.isocalendar()[1] , raw_entries = dj_raw_entries, clean_entries = dj_clean_entries,
                city = city_name, avg_price_sqrm = dj_avg_price_sqrm, avg_size = dj_avg_size,
                avg_year = dj_avg_year, highest_price = max[0], highest_price_link = max[1],
                highest_price_sqrm = max_per_sqr[0], highest_price_sqrm_link = max_per_sqr[1],
                lowest_price = min[0], lowest_price_link = min[1], lowest_price_sqrm = min_per_sqr[0],
                lowest_price_sqrm_link = min_per_sqr[1]
            )
            print('%s added' % (city_name))
            self.stdout.write( 'job complete' )




