# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 16:33:06 2023

@author: Stian
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leser inn CSV-filen
data = pd.read_csv('snoedybder_vaer_en_stasjon_dogn.csv', delimiter=';')  # Antar at dataene er tabulatorseparert

# Konverterer 'Tid(norsk normaltid)' til datetidsformat
data['Tid(norsk normaltid)'] = pd.to_datetime(data['Tid(norsk normaltid)'], errors='coerce')

# Gjør sånn at det blir unike år i datasettet
unique_years = data['Tid(norsk normaltid)'].dt.year.unique()

# Lager lister for å lagre antall penværsdager og år
penvaer_days_per_year = []
years_with_enough_data = []

# Går gjennom hvert år og beregner antall penværsdager
for year in unique_years:
    # Filtrer data for det aktuelle året
    year_data = data[data['Tid(norsk normaltid)'].dt.year == year]
    
    # Sjekker om det er nok data for å være et gyldig år (minst 300 dager)
    if len(year_data) >= 300:
        # Erstatt "-" med NaN og konverter kolonnen til desimaltall
        year_data['Gjennomsnittlig skydekke (døgn)'] = pd.to_numeric(year_data['Gjennomsnittlig skydekke (døgn)'].replace('-', np.nan), errors='coerce')
        
        # Tell antall penværsdager (skydekke <= 3)
        penvaer_days = len(year_data[year_data['Gjennomsnittlig skydekke (døgn)'] <= 3])
        
        # Legger til antall penværsdager og året til listene
        penvaer_days_per_year.append(penvaer_days)
        years_with_enough_data.append(year)

# Lager et plott av antall penværsdager per år
plt.plot(years_with_enough_data, penvaer_days_per_year, marker='o')
plt.title('Antall penværsdager per år')
plt.xlabel('År')
plt.ylabel('Antall penværsdager')
plt.grid(True)

# Sett x-aksen til å vise hvert år
plt.xticks(years_with_enough_data)

plt.show()
