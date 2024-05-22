import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Ανάγνωση του αρχείου CSV
url = "https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv"
data = pd.read_csv(url)

# Μετατροπή της στήλης 'date' σε datetime
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

# Δημιουργία του γραφικού περιβάλλοντος χρήστη με tkinter
root = tk.Tk()
root.title("COVID-19 Dashboard for Greece")

# Δημιουργία πλαισίων για την εμφάνιση δεδομένων
frame1 = ttk.LabelFrame(root, text="Ημερήσια Επισκόπηση")
frame1.grid(row=0, column=0, padx=10, pady=10)

frame2 = ttk.LabelFrame(root, text="Συνολική Επισκόπηση")
frame2.grid(row=1, column=0, padx=10, pady=10)

frame3 = ttk.LabelFrame(root, text="Εξέλιξη Εμβολιασμών")
frame3.grid(row=0, column=1, padx=10, pady=10)

frame4 = ttk.LabelFrame(root, text="Έλεγχοι Αντισωμάτων")
frame4.grid(row=1, column=1, padx=10, pady=10)

frame5 = ttk.LabelFrame(root, text="Επιδημιολογικοί Δείκτες")
frame5.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Λειτουργίες για την εμφάνιση δεδομένων
def show_daily_overview():
    latest_data = data.iloc[-1]
    previous_data = data.iloc[-2]
    
    daily_info = f"Ημερομηνία: {latest_data['date'].date()}\n" \
                 f"Νέα Κρούσματα: {latest_data['cases']} ({((latest_data['cases'] - previous_data['cases']) / previous_data['cases']) * 100:.2f}% από την προηγούμενη ημέρα)\n" \
                 f"Απώλειες: {latest_data['deaths']}\n" \
                 f"Σε κρίσιμη κατάσταση: {latest_data['intensive_care']}\n" \
                 f"Νοσηλευόμενοι: {latest_data['hospitalized']}"
    
    label_daily.config(text=daily_info)

def show_total_overview():
    total_cases = data['cases'].sum()
    total_deaths = data['deaths'].sum()
    total_intensive_care = data['intensive_care'].sum()
    total_hospitalized = data['hospitalized'].sum()
    
    total_info = f"Συνολικά Κρούσματα: {total_cases}\n" \
                 f"Συνολικές Απώλειες: {total_deaths}\n" \
                 f"Συνολικές Εντατικές Θεραπείες: {total_intensive_care}\n" \
                 f"Συνολικοί Νοσηλευόμενοι: {total_hospitalized}"
    
    label_total.config(text=total_info)

def show_vaccination_overview():
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='date', y='vaccinated', data=data)
    plt.title("Εξέλιξη Εμβολιασμών στην Ελλάδα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Αριθμός Εμβολιασμών")
    plt.grid(True)
    plt.show()

def show_antibody_tests_overview():
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='date', y='antibody_tests', data=data)
    plt.title("Έλεγχοι Αντισωμάτων στην Ελλάδα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Αριθμός Ελέγχων")
    plt.grid(True)
    plt.show()

def show_epidemiological_indicators():
    total_cases = data['cases'].sum()
    total_deaths = data['deaths'].sum()
    total_recovered = data['recovered'].sum()
    
    # Υπολογισμός επιδημιολογικών δεικτών
    case_fatality_rate = (total_deaths / total_cases) * 100
    recovery_rate = (total_recovered / total_cases) * 100
    mortality_rate = (total_deaths / data['population'].iloc[-1]) * 100000  # per 100,000 people
    
    indicator_info = f"Case Fatality Rate: {case_fatality_rate:.2f}%\n" \
                     f"Recovery Rate: {recovery_rate:.2f}%\n" \
                     f"Mortality Rate: {mortality_rate:.2f} per 100,000 people"
    
    label_indicators.config(text=indicator_info)

# Δημιουργία κουμπιών για εμφάνιση δεδομένων
btn_daily = ttk.Button(frame1, text="Ημερήσια Επισκόπηση", command=show_daily_overview)
btn_daily.pack(padx=10, pady=10)

btn_total = ttk.Button(frame2, text="Συνολική Επισκόπηση", command=show_total_overview)
btn_total.pack(padx=10, pady=10)

btn_vaccination = ttk.Button(frame3, text="Εξέλιξη Εμβολιασμών", command=show_vaccination_overview)
btn_vaccination.pack(padx=10, pady=10)

btn_antibody = ttk.Button(frame4, text="Έλεγχοι Αντισωμάτων", command=show_antibody_tests_overview)
btn_antibody.pack(padx=10, pady=10)

btn_indicators = ttk.Button(frame5, text="Επιδημιολογικοί Δείκτες", command=show_epidemiological_indicators)
btn_indicators.pack(padx=10, pady=10)

# Δημιουργία labels για εμφάνιση πληροφοριών
label_daily = ttk.Label(frame1, text="")
label_daily.pack(padx=10, pady=10)

label_total = ttk.Label(frame2, text="")
label_total.pack(padx=10, pady=10)

label_indicators = ttk.Label(frame5, text="")
label_indicators.pack(padx=10, pady=10)

root.mainloop()
