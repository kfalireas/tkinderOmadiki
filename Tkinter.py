
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.dates as mdates

warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    url = "https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv"
    df = pd.read_csv(url)
    df.set_index('id',inplace=True)                                                                         #To id θα γίνει το νέο index
    
    # Δημιουργούμε το γραφικό περιβάλλον
    create_gui(df)

def create_gui(df):
    root = tk.Tk()
    root.title("Covid-19 Greece Data Analysis")
    root.geometry("800x800") #Μεγαλωσα το dimension του αρχικου παραθυρου για να φαινεται και η φωτογραφια
    root.configure(bg="#dfe3ee")  # Ανοιχτό γκρι-μπλε φόντο, μπορούμε απο οποιαδήποτε παλέτα να πάρουμε χρώματα και να αλλάξουμε το γκρι αμα θέλετε αλλα ειναι το πιο ευδιακρίτο χρώμα απο αυτά που δοκίμασα

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 16), background="#dfe3ee")
    style.configure("TFrame", background="#dfe3ee")

    # Εδω μπορούμε να προσθέσουμε μια εικόνα αμα θέλουμε, θα κάνει λίγο πιο ωραίο το αρχικό παράθυρο
    try:
        logo = tk.PhotoImage(file="covid-19.png")
        logo_label = ttk.Label(root, image=logo)
        logo_label.pack(pady=10)
    except:
        pass

    title_label = ttk.Label(root, text="Covid-19 Greece Data Analysis")
    title_label.pack(pady=20)

    # Δημιουργία πλαισίου για τις κατηγορίες
    frame = ttk.Frame(root)
    frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Πλαίσιο για τα κουμπιά
    data_frame = ttk.Labelframe(frame, text="Data Analysis", padding=20)
    data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    vis_frame = ttk.Labelframe(frame, text="Visualizations", padding=20)
    vis_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # Προσθέτουμε κουμπιά για κάθε συνάρτηση
    ttk.Button(data_frame, text="Compare Dates", command=lambda: compare_dates(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Pie Chart 1", command=lambda: pie_1(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="ICU - Pie Chart 2", command=lambda: icu(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Vaccinations and Actives", command=lambda: vaccinations_and_actives(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Cases and Deaths", command=lambda: cases_deaths(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Hospitalized", command=lambda: hospitalized(df)).pack(pady=5, fill=tk.X)

    root.mainloop()

def compare_dates(df):

    print("Καρτέλα Ημερήσιας Επισκόπησης: (Προηγούμενη Μέρα-Τωρινή Μέρα-Ποσοστιαία Διαφορά)")
    copied_df = df.copy(deep=True)                                                                          #Δημιουργία Αντιγράφου και μετονομασία στήλεων
    copied_df.rename(columns={'date':'Ημερομηνία','new_cases':'Νέα Κρούσματα','confirmed':'Επιβεβαιομένα Κρούσματα','new_deaths':'Νέες Απώλειες','total_deaths':'Συνολικές Απώλειες',
                       'new_tests':'Νέα Τέστ','positive_tests':"Θετικά Τέστ",'new_selftest':'Νέα Σελφτέστ','new_ag_tests':'Νέα Τέστ Αντισωμάτων',
                       'ag_tests':'Τέστ Αντισωμάτων','total_tests':'Συνολικά Τέστ','new_critical':'Νέοι Νοσηλευόμενοι Σε Κρίσιμη','total_vaccinated_crit':'Εμβολιασμένοι Σε Κρίσιμη',
                       'total_unvaccinated_crit':'Μη Εμβολιασμένοι Σε Κρίσιμη','total_critical':'Συνολικός Αριθμός Νοσηλευόμενων Σε Κρίσιμη','hospitalized':'Σε Νοσηλεία','icu_percent':'Ποσοστό σε ΜΕΘ',
                       'icu_out':'Εκτώς της ΜΕΘ','new_active':'Νέα Ενεργά Κρούσματα','active':'Ενεργά Κρούσματα','recovered':'Που Εχει Αναρρώσει','total_vaccinations':'Συνολικοί Εμβολιασμοί','reinfections':'Επαναμολύνσεις'},inplace=True)
    copied_df = copied_df.drop(columns=['total_selftest','total_foreign','total_unknown','beds_percent','discharged','total_domestic','total_reinfections'])       #Αφαίρεση κάποιων δεδομένων



    col_start = copied_df.columns.get_loc('Νέα Κρούσματα')                  #Επιλέγω ποιες στήλες θα εμφανιστούν
    col_end = copied_df.columns.get_loc('Επαναμολύνσεις')
    df3 = copied_df.iloc[[-2,-1],col_start:col_end]                          # Επιλέγω 2 τελευταίες γραμμές (2 τελευταίες μέρες)
    pct = df3.pct_change()                                                   #Υπολογίζω ποσοστιαία διαφορά των δύο μερών
    pct2 = pct.drop(pct.index[[0]])

    pct3 = pd.concat([df3,pct2])                                             #Ενώνω τις 2 καρτέλες,θα προβληθούν σε μορφή αναστρόφου πίνακα
    pct3.index = ['Προηγούμενη','Τωρινή','Διαφορά']
    print(pct3.transpose())

     # Δημιουργία νέου παραθύρου για εμφάνιση δεδομένων
    
    data_window = tk.Toplevel()
    data_window.title("Compare Dates")
    data_window.geometry("600x400")
    data_window.configure(bg="#f0f0f0")

    text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    text_area.insert(tk.INSERT, pct3.transpose().to_string())

def cases_deaths(df):
    df.date = pd.to_datetime(df.date)                                                                      # Μετατρέπω το date Σε datetime Αντικείμενο για να Διαχειριστώ τον Χρόνο 
    month_df = df.resample('M', on='date').sum()                                                           # Το df θα Διαμορφωθεί σε Αθροίσματα Μηνών

    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True)
    fig.suptitle('Καρτέλα Κρουσμάτων και Απωλειών')
    ax[0].plot(month_df.index, month_df.confirmed, 'b--^', label='Επιβεβαιομένα Κρούσματα')                 # 3 plots σε 3 Οριζόντιους Άξονες
    ax[1].plot(month_df.index, month_df.new_cases, 'r-o', label='Νέα Κρούσματα')
    ax[2].plot(month_df.index, month_df.total_deaths, 'g-s', label='Συνολικές Απώλειες')

    ax[0].set_title("Επιβεβαιομένα Κρούσματα")                                                              # Τίτλοι
    ax[0].set_ylabel('Αριθμός Κρουσμάτων')

    ax[1].set_title('Νέα Κρούσματα')                                              
    ax[1].set_xlabel('Ημερομηνίες')
    ax[1].set_ylabel('Αριθμός Κρουσμάτων')
    ax[2].set_title("Συνολικός Αριθμός Θανάτων")
    ax[2].set_ylabel('Αριθμός Θανάτων')

    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%B %Y"))                                          # Διαμόρφωση ημερομηνιών (Μήνας-Χρόνος)
    plt.xticks(rotation=90)

    ax[0].legend()
    ax[1].legend(loc='upper left')
    ax[2].legend()
    ax[0].ticklabel_format(axis="y", style='plain')                                                         # Αφαίρεση scientific notation
    ax[2].ticklabel_format(axis="y", style='plain')                                                         # Αφαίρεση scientific notation
    plt.tight_layout()
    plt.show()

def vaccinations_and_actives(df):
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True)                                                # 3 plots σε 3 Άξονες
    fig.suptitle('Καρτέλα Συνολικής Εξέλιξης Επαναμολύνσεων,Ενεργών Κρουσμάτων και Εμβολιασμών')

    ax[0].plot(df.date, df.total_reinfections, 'm-', label="Επαναμολύνσεις")                             # plot για Επαναμολύνσεις
    ax[1].plot(df.date, df.active, 'r--', label="Ενεργά")                                                # plot για Ενεργά Κρούσματα
    ax[2].plot(df.date, df.total_vaccinations, 'c.', label="Εμβολιασμοί")                                # plot για Εμβολιασμούς

    ax[0].set_title("Επαναμολύνσεις")
    ax[1].set_title("Ενεργά Κρούσματα")
    ax[2].set_title("Συνολικοί Εμβολιασμοί")
    ax[0].ticklabel_format(axis="y", style='plain')                                                       # Αφαίρεση scientific notation σε 1ο,3ο Άξονα
    ax[2].ticklabel_format(axis="y", style='plain')

    plt.xticks(df.date[::120])                                                                             # Ημερομηνίες Ανα Τετράμηνα
    plt.xticks(df.date[::120])
    plt.xticks(df.date[::120])

    ax[2].set_xlabel('Ημερομηνίες (Ανα Τετράμηνα)')                                                        # Τίτλοι στους Άξονες
    ax[0].set_ylabel("Αριθμός Επαναμολύνσεων")
    ax[1].set_ylabel("Αριθμός Κρουσμάτων")
    ax[2].set_ylabel("Αριθμός Εμβολιασμών")

    ax[0].legend()
    ax[1].legend(loc='upper left')
    ax[2].legend(loc='upper left')
    
    plt.tight_layout()
    plt.show()

def pie_1(df):
    fig, axes = plt.subplots(nrows=2,ncols=2, figsize=(8,7))                                              # 4 pie charts σε 2 Οριζόντιους Άξονες και 2 Κάθετους
    fig.suptitle('Καρτέλα Ποσοστών')

    tot_reinf =  df.iloc[-1,29]                                                                           #Eπαναμολύνσεις
    tot_vacc = df.iloc[-1,27]                                                                             # Eμβολιασμοί
    confirmed = df.iloc[-1,2]                                                                             # Eπιβεβαιομενα

    Colors_1 = ['forestgreen','darkviolet','yellow']
    naming = 'Επαναμολύνσεις','Εμβολιασμοί','Επιβεβαιομένα Κρούσματα'
    axes[0,0].pie([tot_reinf,tot_vacc,confirmed],labels=naming,colors=Colors_1,autopct='%1.1f%%')         # πρώτο pie chart
    axes[0,0].set_title("Ποσοστό Επαναμολύνσεων,Εμβολιασμών και Άγνωστων Κρουσμάτων")

    Colors_2 = ['cyan','darkolivegreen','orangered']
    naming_2 = 'Εμβολιασμένοι', 'Ανεμβολίαστοι', 'Συνολικός Αριθμός'
    x = df['total_vaccinated_crit'].sum()                                                                 #Αθροισμα Εμβολιασμένων Σε Κρίσιμη Κατάσταση
    y = df['total_unvaccinated_crit'].sum()                                                               #Αθροισμα Ανεμβολίαστων Σε Κρίσιμη Κατάσταση
    z = df['total_critical'].sum()                                                                        # Συνολικός Αριθμός Σε Κρίσιμη Κατάσταση
    axes[0,1].pie([x, y, z], labels=naming_2,colors=Colors_2, autopct='%1.1f%%')                          # Δεύτερο pie 
    axes[0,1].set_title("Συνολικό Ποσοστό Ανθρώπων Σε Κρίσιμη Κατάσταση")

    domestic = df.iloc[-1,25]                                                                              # Εγχώρια Κρούσματα
    foreign = df.iloc[-1,24]                                                                               # Ξένα 
    naming_3 = 'Εγχώρια','Ξένα'
    Colors_3 = ['lightblue','red']
    axes[1,0].pie([domestic,foreign],labels=naming_3,colors=Colors_3,autopct='%1.1f%%')                    # Τρίτο pie
    axes[1,0].set_title('Ποσοστό Εγχωρίων και Ξένων Κρουσμάτων')

    cases = df.iloc[-1,2]                                                                                  # Επιβεβαιομένα Κρούσματα
    uknown = df.iloc[-1,26]                                                                                # Αγνωστα Κρούσματα
    naming_4 = 'Επιβεβαιομένα','Άγνωστα'
    Colors_4 = ['crimson','turquoise']
    axes[1, 1].pie([cases, uknown], labels=naming_4,colors=Colors_4,autopct='%1.1f%%')                      # Τέταρτο pie
    axes[1,1].set_title('Ποσοστό Επιβεβαιομένων και Αγνώστων Κρουσμάτων')

    plt.tight_layout()
    plt.show()

def icu(df):
    fig, ax = plt.subplots(nrows=3,ncols=1, sharex=True)                                                    # plots σε 3 οριζόντιους άξονες και έναν κάθετο άξονα x να μοιράζεται
    fig.suptitle('Καρτέλα ΜΕΘ')                                                                             # τίτλος καρτέλας

    ax[0].plot(df.date,df.icu_percent,label='Ποσοστό ΜΕΘ',color='r')                                        # πρώτο chart για ποσοστό μεθ
    ax[1].plot(df.date,df.beds_percent,label='Ποσοστό Κρεβατιών',color='b')                                 # δεύτερο chart για κρεβάτια μεθ
    ax[2].plot(df.date,df.icu_out,label='Εκτώς ΜΕΘ',color='g')                                              # τρίτο για όσους βγηκαν απο μεθ

    ax[0].set_title('Νοσηλευόμενοι σε ΜΕΘ')                                                                 # οι τρείς τίτλοι 
    ax[1].set_title('Κρεβάτια ΜΕΘ')
    ax[2].set_title('Νοσηλευόμενοι Εκτώς ΜΕΘ')
    ax[2].set_xlabel('Ημερομηνίες (ανά Τετράμηνα)')
    plt.xticks(df.date[::120])                                                                               # Οι Ημερομηνίες είναι ανά Τετράμηνα

    ax[0].legend()
    ax[1].legend()
    ax[2].legend(loc='upper right')
    plt.tight_layout()
    plt.show()
def hospitalized(df):
    df.date = pd.to_datetime(df.date)                                                                   # Μετατρέπω το date Σε datetime Αντικείμενο για να Διαχειριστώ τον Χρόνο 
    new_df = df.resample('M', on='date').mean()                                                         # Διαμορφώνω σε Μήνες και Βρίσκω Μέσους Όρους

    hospital = new_df.loc[
    new_df['hospitalized'] > 0]                                                                          # Κάνω slice για να Απομονώσω το dataframe που έχει μη Αρνητικό Αριθμό Νοσηλευόμενων
    hospitalized = hospital.iloc[:, 16]

    fig, ax = plt.subplots()
    ax.bar(hospital.index, hospitalized, label="Νοσηλευόμενοι", width=25)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%B %Y"))
    ax.autoscale(enable=True, axis='x', tight=True)
    plt.xticks(rotation=90)

    plt.title("Κάρτα Μέσου Όρου Νοσηλευόμενων")
    plt.xlabel("Ημερομηνίες")
    plt.ylabel("Αριθμός Νοσηλευόμενων")
    plt.show()


if __name__ == "__main__":
    main()
    print("Τέλος Προγράμματος!")


# AK
cdata='https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv'
pdf=pd.read_csv(cdata)


TotalPopulation=10306774
cdf=pdf.copy()
cdf['date'] = pd.to_datetime(cdf['date'])

# Ημερήσια επισκόπηση των ελέγχων αντισωμάτων

def new_ag_tests():
    cdf.plot(x="date",y="new_ag_tests")
    plt.title("Νέα τεστ αντισωμάτων ανά ημέρα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Τεστ")
    plt.show()
   
#Hmerisia_ag=cdf['new_ag_tests'].iloc[-1]
#print(Hmerisia_ag)

new_ag_tests()

# Συνολική εξέλιξη των ελέγχων αντισωμάτων
def ag_tests():
    cdf.plot(x="date",y="ag_tests")
    plt.title("Συνολικά τεστ αντισωμάτων ")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Συνολικά τεστ")
    plt.show()

Synolika_ag=cdf['ag_tests'].iloc[-1]
#print(Synolika_ag)

ag_tests()


# Ρυμθμός μεταβολής νέων κρουσμάτων

cdf['new_cases_rythmos_metavolis'] = cdf['new_cases'].pct_change() * 100
def new_cases_rythmos_metavolis():
    cdf.plot(x="date",y="new_cases_rythmos_metavolis")
    plt.title("Ρυμθμός μεταβολής νέων κρουσμάτων")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Ρυθμός νέων κρουσμάτων")
    plt.show()

new_cases_rythmos_metavolis()

# Ρυθμός μεταβολής νέων θανάτων

cdf['new_deaths_rythmos_metavolis'] = cdf['new_deaths'].pct_change() * 100

def new_deaths_rythmos_metavolis():
    cdf.plot(x="date",y="new_deaths_rythmos_metavolis")
    plt.title("Ρυμθμός μεταβολής νέων θανάτων")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Ρυθμός νέων θανάτων")
    plt.show()

new_deaths_rythmos_metavolis()

# Ρυθμός μεταβολής συνολικών εμβολιασμών

cdf['total_vaccinations_rythmos_metavolis'] = cdf['total_vaccinations'].pct_change() * 100

def total_vaccinations_rythmos_metavolis():
    cdf.plot(x="date",y="total_vaccinations_rythmos_metavolis")
    plt.title("Ρυμθμός μεταβολής συνολικών εμβολιασμών")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Ρυθμός συνολικών εμβολιασμών")
    plt.show()

total_vaccinations_rythmos_metavolis()

# Ρυθμός μεταβολής συνολικών τεστ    

cdf['total_tests_rythmos_metavolis'] = cdf['total_tests'].pct_change() * 100

def total_tests_rythmos_metavolis():
    cdf.plot(x="date",y="total_tests_rythmos_metavolis")
    plt.title("Ρυμθμός μεταβολής συνολικών τεστ")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Ρυθμός συνολικών τεστ")
    plt.show()

total_tests_rythmos_metavolis()

# Case fatality rate

cdf['case_fatality_rate'] = cdf['total_deaths']/cdf['confirmed']*100

def Case_fatality_rate():
    cdf.plot(x="date",y="case_fatality_rate")
    plt.title("Θνητότητα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Θνητότητα")
    plt.show()

Case_fatality_rate()

# Recovery rate

cdf['Recovery_rate'] = cdf['recovered']/cdf['confirmed']*100

def Recovery_rate():
    cdf.plot(x="date",y="Recovery_rate")
    plt.title("Δείκτης επιβίωσης")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Δείκτης επιβίωσης")
    plt.show()

Recovery_rate()


# Επιζήσαντες και θανόντες από το σύνολο του πλυθησμού στην Ελλάδα με Pie
def Epizisantes_thanontes():
    tl_deaths=float(cdf['total_deaths'].iloc[-1])
    Total_survived=float(TotalPopulation-tl_deaths)
    slices=[Total_survived,tl_deaths]
    explode=(0,0.1)
    labels=['Επιζήσαντες','Απεβίωσαν']
    plt.pie(slices,labels=labels,autopct='%1.1f%%',explode=explode)
    plt.title('Επιζήσαντες και θανόντες από τον κορωνοιό στην Ελλάδα')
    plt.show()

Epizisantes_thanontes()

# Δημιουργούμε ένα column με τα χρόνια
cdf['year'] = cdf['date'].dt.year



# Σιγουρεύουμε ότι ειναι νούμερα και αλλάζουμε σε 0 όσα δεν είναι
cdf['new_deaths'] = pd.to_numeric(cdf['new_deaths'], errors='coerce').fillna(0)
cdf['new_critical'] = pd.to_numeric(cdf['new_cases'], errors='coerce').fillna(0)

# Δημιουργόυμε dataframe με τα αθροίσματα ανά έτος
ethsio_df = cdf.groupby('year')[['new_deaths','new_cases']].sum()

# Bar chart για νέους θανάτους
def neoi_thanatoi():
    plt.bar(ethsio_df.index, ethsio_df['new_deaths'], width=0.4, color='black', label='New Deaths')
    plt.xticks(ethsio_df.index,rotation=45)
    plt.xlabel('Έτος')
    plt.ylabel('Μέτρηση')
    plt.title('Νεόι θάνατοι ανά έτος')
    plt.legend()
    plt.show()

neoi_thanatoi()

# Bar chart για νέες μολύνσεις

def Nees_molynseis():
    plt.bar(ethsio_df.index, ethsio_df['new_cases'], width=0.4, color='red', label='New Cases')
    plt.xticks(ethsio_df.index,rotation=45)
    plt.xlabel('Έτος')
    plt.ylabel('Μέτρηση')
    plt.title('Νέες μολύνσεις ανά έτος')
    plt.legend()
    plt.show()

Nees_molynseis()



