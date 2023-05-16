import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import os

def dhondt(df, seats):
        table = np.zeros((len(parties), seats))
        for i in range(seats):
            table[:, i] = df.votes_perc / (i + 1)
        table = np.round(table, 2)
        return table

str1 = "ADANA-15 ADIYAMAN-5 AFYONKARAHİSAR-6 AĞRI-4 AMASYA-3 ANKARA-36 ANTALYA-16 ARTVİN-2 AYDIN-8 BALIKESİR-9 BİLECİK-2 BİNGÖL-3 BİTLİS-3 BOLU-3 BURDUR-3 BURSA-20 ÇANAKKALE-4 ÇANKIRI-2 ÇORUM-4 DENİZLİ-8 \
DİYARBAKIR-12 EDİRNE-4 ELAZIĞ-5 ERZİNCAN-2 ERZURUM-6 ESKİŞEHİR-7 GAZİANTEP-14 GİRESUN-4 GÜMÜŞHANE-2 HAKKARİ-3 HATAY-11 ISPARTA-4 MERSİN-13 İSTANBUL-98 İZMİR-28 KARS-3 KASTAMONU-3 KAYSERİ-10 KIRKLARELİ-3 \
KIRŞEHİR-2 KOCAELİ-13 KONYA-15 KÜTAHYA-5 MALATYA-6 MANİSA-10 KAHRAMANMARAŞ-8 MARDİN-6 MUĞLA-7 MUŞ-4 NEVŞEHİR-3 NİĞDE-3 ORDU-6 RİZE-3 SAKARYA-7 SAMSUN-9 SİİRT-3 SİNOP-2 SİVAS-5 TEKİRDAĞ-7 TOKAT-5 TRABZON-6 \
TUNCELİ-2 ŞANLIURFA-14 UŞAK-3 VAN-8 YOZGAT-4 ZONGULDAK-5 AKSARAY-4 BAYBURT-1 KARAMAN-3 KIRIKKALE-3 BATMAN-5 ŞIRNAK-4 BARTIN-2 ARDAHAN-2 IĞDIR-2 YALOVA-3 KARABÜK-3 KİLİS-2 OSMANİYE-4 DÜZCE-3"

iller = {}
str1 = str1.lower()
str1 = str1.replace("ç", "c").replace("ğ", "g").replace("ı", "i").replace("ö", "o").replace("ş", "s").replace("ü", "u").replace("i̇", "i")
str1 = str1.strip().split(" ")
for i in str1:
    i = i.split("-")
    iller[i[0]] = int(i[1])

try:
    os.mkdir("secim2023_last")
except:
    print("secim2023_last folder already exists")

for i in iller:
    sleep(2)
    url = f"https://www.sozcu.com.tr/secim2023/{i}-secim-sonuclari"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # Find <div class="col-lg-12">
    div = soup.find("div", attrs={"class": "col-lg-12"})

    imgs = div.find_all("img")
    partiler = []
    for j in imgs:
        partiler.append(j["src"].split("/")[-1].split(".")[0])

    # Find <span class="progress-bar bg-zp" data-value="%3.25" style="width: 3%"></span>
    oy_oranlari = {}
    for k in partiler:
        if k == "tip":
            k = 'turkiye-isci-partisi'
        elif k == "bagimsiz":
            continue
        span = div.find_all("span", attrs={"class": f"progress-bar bg-{k}"})
        oy_oranlari[k] = float(span[0]["data-value"].replace("%", ""))

    parties = list(oy_oranlari.keys())
    votes_perc = list(oy_oranlari.values())
    seats = iller[i]

    # Create a DataFrame with parties and votes_perc as columns: df
    df = pd.DataFrame({'parties': parties, 'votes_perc': votes_perc})

    # Print the result of applying dhondt() to df and seats
    table = dhondt(df, seats)
    table_df = pd.DataFrame(table, index=np.array(parties), columns=np.arange(1, seats + 1))
    temp = table.flatten()
    indices = np.argsort(temp)[-seats:]
    index = list(np.unravel_index(indices, table.shape)[::-1])
    index[0] = index[0] + 1
    table_df = table_df.applymap(lambda x: '{:.3f}'.format(x))
    a = table_df.style.apply(lambda x: ['background: green' if (x.name, i) in zip(*index) else '' for i in range(len(x))])

    html = a.to_html()

    # Save Styler as HTML file
    html_file_path = f'secim2023_last/{i}.html'
    with open(html_file_path, 'w') as f:
        f.write(html)

print("Done with scraping!")