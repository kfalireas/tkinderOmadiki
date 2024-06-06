
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import tkinter as tk
from tkinter import ttk, scrolledtext

warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    url = "https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv"
    df = pd.read_csv(url)
    df.set_index('id',inplace=True)                                                                         #To id θα γίνει το νέο index
    
    df.set_index('id',inplace=True)                                                                         #To id θα γίνει το νέο index
    # Δημιουργούμε το γραφικό περιβάλλον
    create_gui(df)

def create_gui(df):
    root = tk.Tk()
    root.title("Covid-19 Greece Data Analysis")
    root.geometry("800x600")
    root.configure(bg="#dfe3ee")  # Ανοιχτό γκρι-μπλε φόντο, μπορούμε απο οποιαδήποτε παλέτα να πάρουμε χρώματα και να αλλάξουμε το γκρι αμα θέλετε αλλα ειναι το πιο ευδιακρίτο χρώμα απο αυτά που δοκίμασα

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 16), background="#dfe3ee")
    style.configure("TFrame", background="#dfe3ee")

    # Εδω μπορούμε να προσθέσουμε μια εικόνα αμα θέλουμε, θα κάνει λίγο πιο ωραίο το αρχικό παράθυρο
    try:
        logo = tk.PhotoImage(file="logo.png")  
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
    ttk.Button(vis_frame, text="Pie Chart 2", command=lambda: pie_2(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Vaccinations and Actives", command=lambda: vaccinations_and_actives(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Cases and Deaths", command=lambda: cases_deaths(df)).pack(pady=5, fill=tk.X)
    ttk.Button(vis_frame, text="Hospitalized", command=lambda: hospitalized(df)).pack(pady=5, fill=tk.X)

    root.mainloop()

def compare_dates(df):

    df.set_index('id',inplace=True)                                                                         #To id θα γίνει το νέο index
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
