# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:29:42 2023

@author: Stian
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leser inn CSV-filen
data = pd.read_csv('snoedybder_vaer_en_stasjon_dogn.csv', delimiter=';')  

# Konverterer 'Tid(norsk normaltid)' til datetidsformat
data['Tid(norsk normaltid)'] = pd.to_datetime(data['Tid(norsk normaltid)'], errors='coerce')

# Gjør sånn at det blir unike år i datasettet
unique_years = data['Tid(norsk normaltid)'].dt.year.unique()

# lister for å lagre høyeste middelvind og medianvind per år
highest_mean_wind_per_year = []
median_wind_per_year = []
years_with_enough_data = []

# Går gjennom hvert år og beregner høyeste middelvind og medianvind
for year in unique_years:
    # Filtrer data for det aktuelle året
    year_data = data[data['Tid(norsk normaltid)'].dt.year == year]
    
    # Sjekk om det er nok data for å være gyldig (minst 300 dager)
    if len(year_data) >= 300:
        # Erstatter "-" med NaN og konverter kolonnen til desimaltall
        year_data['Høyeste middelvind (døgn)'] = pd.to_numeric(year_data['Høyeste middelvind (døgn)'].replace('-', np.nan), errors='coerce')
        
        # Beregner høyeste middelvind for året
        highest_mean_wind = year_data['Høyeste middelvind (døgn)'].max()
        highest_mean_wind_per_year.append(highest_mean_wind)
        
        # Lager en liste over vindhastighetene for å finne medianen
        wind_values = year_data['Høyeste middelvind (døgn)'].dropna().tolist()
        
        # Beregn medianvindstyrke for året
        median_wind = np.median(sorted(wind_values))
        median_wind_per_year.append(median_wind)
        
        # Legger til året til listen over gyldige år
        years_with_enough_data.append(year)

# Lager et plott av medianvindstyrke og høyeste middelvind per år
plt.plot(years_with_enough_data, median_wind_per_year, label='Medianvindstyrke', marker='o')
plt.plot(years_with_enough_data, highest_mean_wind_per_year, label='Høyeste Middelvind', marker='o')
plt.title('Medianvindstyrke og Høyeste Middelvind per år')
plt.xlabel('År')
plt.ylabel('Vindstyrke (m/s)')
plt.legend()
plt.grid(True)
plt.show()
