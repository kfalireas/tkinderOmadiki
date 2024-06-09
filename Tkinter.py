import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import tkinter as tk
from tkinter import ttk, scrolledtext

warnings.simplefilter(action='ignore', category=FutureWarning)

TotalPopulation = 10306774

def main():
    url = "https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('id', inplace=True)  # Το id θα γίνει το νέο index
    
    # Δημιουργούμε το γραφικό περιβάλλον
    create_gui(df)

def create_gui(df):
    root = tk.Tk()
    root.title("Covid-19 Greece Data Analysis")
    root.geometry("800x800")  # Μεγαλώσαμε το dimension του αρχικού παραθύρου για να φαίνεται και η φωτογραφία
    root.configure(bg="#dfe3ee")  # Ανοιχτό γκρι-μπλε φόντο

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 16), background="#dfe3ee")
    style.configure("TFrame", background="#dfe3ee")

    # Εδώ μπορούμε να προσθέσουμε μια εικόνα αν θέλουμε
    try:
        logo = tk.PhotoImage(file="covid-19.png")
        logo_label = ttk.Label(root, image=logo)
        logo_label.pack(pady=10)
    except:
        pass

    title_label = ttk.Label(root, text="Covid-19 Greece Data Analysis")
    title_label.pack(pady=20)

    # Πλαίσιο για τα κουμπιά "Data Analysis"
    data_frame = ttk.Labelframe(root, text="Data Analysis", padding=20)
    data_frame.pack(pady=10, fill=tk.X)

    # Πλαίσιο με scrollbar για τα κουμπιά "Visualizations"
    vis_frame_container = ttk.Frame(root)
    vis_frame_container.pack(pady=10, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(vis_frame_container)
    scrollbar = ttk.Scrollbar(vis_frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    vis_frame = ttk.Labelframe(scrollable_frame, text="Visualizations", padding=10)
    vis_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Προσθέτουμε κουμπιά για το πλαίσιο "Data Analysis"
    ttk.Button(data_frame, text="Compare Dates", command=lambda: compare_dates(df)).pack(pady=5, fill=tk.X)

    # Προσθέτουμε κουμπιά για το πλαίσιο "Visualizations"
    ttk.Button(vis_frame, text="Pie Chart 1", command=lambda: pie_1(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="ICU", command=lambda: icu(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Vaccinations and Actives", command=lambda: vaccinations_and_actives(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Cases and Deaths", command=lambda: cases_deaths(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Hospitalized", command=lambda: hospitalized(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="New Antibody Tests", command=lambda: new_ag_tests(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Total Antibody Tests", command=lambda: ag_tests(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="New Cases Change Rate", command=lambda: new_cases_rythmos_metavolis(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="New Deaths Change Rate", command=lambda: new_deaths_rythmos_metavolis(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Total Vaccinations Change Rate", command=lambda: total_vaccinations_rythmos_metavolis(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Total Tests Change Rate", command=lambda: total_tests_rythmos_metavolis(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Case Fatality Rate", command=lambda: Case_fatality_rate(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Recovery Rate", command=lambda: Recovery_rate(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Survivors and Deaths", command=lambda: Epizisantes_thanontes(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Annual New Deaths", command=lambda: neoi_thanatoi(cdf)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Annual New Cases", command=lambda: Nees_molynseis(cdf)).pack(pady=5, fill=tk.X)

    root.mainloop()

def compare_dates(df):
    print("Καρτέλα Ημερήσιας Επισκόπησης: (Προηγούμενη Μέρα-Τωρινή Μέρα-Ποσοστιαία Διαφορά)")
    copied_df = df.copy(deep=True)
    copied_df.rename(columns={'date':'Ημερομηνία','new_cases':'Νέα Κρούσματα','confirmed':'Επιβεβαιομένα Κρούσματα','new_deaths':'Νέες Απώλειες','total_deaths':'Συνολικές Απώλειες',
                       'new_tests':'Νέα Τέστ','positive_tests':"Θετικά Τέστ",'new_selftest':'Νέα Σελφτέστ','new_ag_tests':'Νέα Τέστ Αντισωμάτων',
                       'ag_tests':'Τέστ Αντισωμάτων','total_tests':'Συνολικά Τέστ','new_critical':'Νέοι Νοσηλευόμενοι Σε Κρίσιμη','total_vaccinated_crit':'Εμβολιασμένοι Σε Κρίσιμη',
                       'total_unvaccinated_crit':'Μη Εμβολιασμένοι Σε Κρίσιμη','total_critical':'Συνολικός Αριθμός Νοσηλευόμενων Σε Κρίσιμη','hospitalized':'Σε Νοσηλεία','icu_percent':'Ποσοστό σε ΜΕΘ',
                       'icu_out':'Εκτώς της ΜΕΘ','new_active':'Νέα Ενεργά Κρούσματα','active':'Ενεργά Κρούσματα','recovered':'Που Εχει Αναρρώσει','total_vaccinations':'Συνολικοί Εμβολιασμοί','reinfections':'Επαναμολύνσεις'},inplace=True)
    copied_df = copied_df.drop(columns=['total_selftest','total_foreign','total_unknown','beds_percent','discharged','total_domestic','total_reinfections'])

    col_start = copied_df.columns.get_loc('Νέα Κρούσματα')
    col_end = copied_df.columns.get_loc('Επαναμολύνσεις')
    df3 = copied_df.iloc[[-2,-1],col_start:col_end]
    pct = df3.pct_change()
    pct2 = pct.drop(pct.index[[0]])

    pct3 = pd.concat([df3,pct2])
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
    fig, (ax1, ax2) = plt.subplots(nrows=2,ncols=1)                         #Δημιουργώ καρτέλα με 2 subplots
    ax1.plot(df.date,df.confirmed,label="Επιβεβαιωμένα Κρούσματα")
    ax2.plot(df.date,df.total_deaths,'g--',label="Συνολικές Απώλειες")

    ax1.set_title("Επιβεβαιωμένα Κρούσματα")
    ax1.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax1.set_ylabel("Κρούσματα")
    plt.sca(ax1)                                                            # Θέτω άξονα ax1
    plt.xticks(df.date[::182])                                              #Ο άξωνας χ (ημερομηνίες) θα είναι ανα εξάμηνα

    ax2.set_title("Συνολικές Απώλειες")
    ax2.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax2.set_ylabel("Απώλειες")
    plt.ticklabel_format(axis="y", style='plain')                           #Αφαίρεση scientific notation
    plt.sca(ax2)                                                            # Θέτω άξονα ax2
    plt.xticks(df.date[::182])

    ax1.legend()
    ax2.legend()
    plt.tight_layout()
    plt.show()

def pie_1(df):
    fig, axes = plt.subplots(nrows=2,ncols=1, figsize=(8,7))                                             # 2 pie charts σε 2 οριζόντιους άξονες και έναν κάθετο

    tot_reinf =  df.iloc[-1,29]                                                                          # Eπαναμολύνσεις της τελευταίας Μέρας
    tot_vacc = df.iloc[-1,27]                                                                            # εμβολιασμοί της τελευταίας Μερας
    tot_unkn = df.iloc[-1,26]                                                                            # αγνωστα κρούσματα της τελευταίας Μέρας

    Colors_1 = ['forestgreen','darkviolet','yellow']
    naming = 'Συνολικές Επαναμολύνσεις','Συνολικοί Εμβολιασμοί','Συνολικά Αγνωστα Κρούσματα'
    axes[0].pie([tot_reinf,tot_vacc,tot_unkn],labels=naming,colors=Colors_1,autopct='%1.1f%%')          # πρώτο pie chart
    axes[0].set_title("Ποσοστό Συνολικών Επαναμολύνσεων,Εμβολιασμών και Άγνωστων Κρουσμάτων")

    Colors_2 = ['cyan','darkolivegreen','orangered']
    naming_2 = 'Εμβολιασμένοι', 'Ανεμβολίαστοι', 'Συνολικός Αριθμός'
    x = df['total_vaccinated_crit'].sum()                                                              #Αθροισμα Εμβολιασμένων Σε Κρίσιμη Κατάσταση
    y = df['total_unvaccinated_crit'].sum()                                                            #Αθροισμα Ανεμβολίαστων Σε Κρίσιμη Κατάσταση
    z = df['total_critical'].sum()                                                                     # Συνολικός Αριθμός Ανθρώπων Σε Κρίσιμη Κατάσταση
    axes[1].pie([x, y, z], labels=naming_2,colors=Colors_2, autopct='%1.1f%%')                         # δεύτερο pie chart
    axes[1].set_title("Συνολικό Ποσοστό Ανθρώπων Σε Κρίσιμη Κατάσταση")

    plt.tight_layout()
    plt.show()

def icu(df):

    fig, ax = plt.subplots(nrows=3,ncols=1, sharex=True)                                          # plots σε 3 οριζόντιους άξονες και έναν κάθετο άξονα x να μοιράζεται
    fig.suptitle('Καρτέλα ΜΕΘ')                                                                   # τίτλος καρτέλας

    ax[0].plot(df.date,df.icu_percent,label='Ποσοστό ΜΕΘ',color='r')                              # πρώτο chart για ποσοστό μεθ
    ax[1].plot(df.date,df.beds_percent,label='Ποσοστό Κρεβατιών',color='b')                       # δεύτερο chart για κρεβάτια μεθ
    ax[2].plot(df.date,df.icu_out,label='Εκτώς ΜΕΘ',color='g')                                    # τρίτο για όσους βγηκαν απο μεθ

    ax[0].set_title('Νοσηλευόμενοι σε ΜΕΘ')                                                        # οι τρείς τίτλοι 
    ax[1].set_title('Κρεβάτια ΜΕΘ')
    ax[2].set_title('Νοσηλευόμενοι Εκτώς ΜΕΘ')
    plt.xticks(df.date[::182])                                                                     # Οι ημερομηνίες είναι ανα εξάμηνα

    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    plt.tight_layout()
    plt.show()

def vaccinations_and_actives(df):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)                                   # δύο διαγράματα σε δύο οριζόντιους άξονες

    ax1.plot(df.date, df.total_vaccinations, label="Αριθμός εμβολιασμών")              # πρώτο διάγραμμα εμβολιασμών
    ax2.plot(df.date, df.active,'r--', label="Ενεργά Κρούσματα")                       # δεύτερο διάγραμμα ενεργών 


    ax1.set_title("Συνολικοί εμβολιασμοί")                                              # Ονομασία και τίτλοι αξόνων
    ax1.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax1.set_ylabel("Εμβολιασμοί")
    plt.sca(ax1)                                                                         # Θέτω άξονα ax1
    plt.ticklabel_format(axis="y", style='plain')                                        #Αφαίρεση scientific notation
    plt.xticks(df.date[::182])                                                           #Ημερομηνίες ανα εξάμηνα


    ax2.set_title("Συνολική Εξέλιξη Ενεργών Κρουσμάτων")                                 # Tίτλοι
    ax2.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax2.set_ylabel("Αριθμός Ενεργών Κρουσμάτων")
    plt.sca(ax2)                                                                         # Θέτω άξονα ax2
    plt.xticks(df.date[::182])

    ax1.legend()
    ax2.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

def hospitalized(df):
    hospital = df.loc[df['hospitalized']>0]          # Κάνω slice για να βρώ απομονώσω το dataframe που έχει μηδέν νοσηλείες
    hospital_date = hospital.iloc[:,0]               # Hμερομηνίες στο συγκεκριμένο frame
    hospitalized = hospital.iloc[:,16]               # Nοσηλείες

    plt.bar(hospital_date,hospitalized,label="Νοσηλευόμενοι",width=1)

    plt.title("Κάρτα Νοσηλευόμενων")
    plt.xlabel("Ημερομηνίες")
    plt.ylabel("Αριθμός Νοσηλευόμενων")
    plt.xticks(hospital_date[::100])
    plt.show()

if __name__ == "__main__":
    main()
    print("Τέλος Προγράμματος!")
    
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

def new_deaths_rythmos_metavolis(cdf):
    cdf.plot(x="date",y="new_deaths_rythmos_metavolis")
    plt.title("Ρυμθμός μεταβολής νέων θανάτων")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Ρυθμός νέων θανάτων")
    plt.show()

new_deaths_rythmos_metavolis()

# Ρυθμός μεταβολής συνολικών εμβολιασμών

cdf['total_vaccinations_rythmos_metavolis'] = cdf['total_vaccinations'].pct_change() * 100

def total_vaccinations_rythmos_metavolis(cdf):
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

def Case_fatality_rate(cdf):
    cdf.plot(x="date",y="case_fatality_rate")
    plt.title("Θνητότητα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Θνητότητα")
    plt.show()

Case_fatality_rate()

# Recovery rate

cdf['Recovery_rate'] = cdf['recovered']/cdf['confirmed']*100

def Recovery_rate(cdf):
    cdf.plot(x="date",y="Recovery_rate")
    plt.title("Δείκτης επιβίωσης")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Δείκτης επιβίωσης")
    plt.show()

Recovery_rate()


# Επιζήσαντες και θανόντες από το σύνολο του πλυθησμού στην Ελλάδα με Pie
def Epizisantes_thanontes(cdf):
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
def neoi_thanatoi(cdf):
    plt.bar(ethsio_df.index, ethsio_df['new_deaths'], width=0.4, color='black', label='New Deaths')
    plt.xticks(ethsio_df.index,rotation=45)
    plt.xlabel('Έτος')
    plt.ylabel('Μέτρηση')
    plt.title('Νεόι θάνατοι ανά έτος')
    plt.legend()
    plt.show()

neoi_thanatoi()

# Bar chart για νέες μολύνσεις

def Nees_molynseis(cdf):
    plt.bar(ethsio_df.index, ethsio_df['new_cases'], width=0.4, color='red', label='New Cases')
    plt.xticks(ethsio_df.index,rotation=45)
    plt.xlabel('Έτος')
    plt.ylabel('Μέτρηση')
    plt.title('Νέες μολύνσεις ανά έτος')
    plt.legend()
    plt.show()

Nees_molynseis()
 
