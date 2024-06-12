import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.dates as mdates
import plotly
import plotly.express as px
import plotly.graph_objects as go
from tkinter import *
import plotly.express as px
from sklearn.linear_model import LinearRegression
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
	ttk.Button(vis_frame, text="Vaccinations and Actives", command=lambda: vaccinations_and_actives(df)).pack(
		pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Cases and Deaths", command=lambda: cases_deaths(df)).pack(pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Hospitalized", command=lambda: hospitalized(df)).pack(pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="New Antibody Tests", command=lambda: new_ag_tests(cdf)).pack(pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Total Antibody Tests", command=lambda: ag_tests(cdf)).pack(pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="New Cases Change Rate", command=lambda: new_cases_rythmos_metavolis(cdf)).pack(
		pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="New Deaths Change Rate", command=lambda: new_deaths_rythmos_metavolis(cdf)).pack(
		pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Total Vaccinations Change Rate",
	           command=lambda: total_vaccinations_rythmos_metavolis(cdf)).pack(pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Total Tests Change Rate", command=lambda: total_tests_rythmos_metavolis(cdf)).pack(
		pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Case Fatality Rate", command=lambda: Case_fatality_rate(cdf)).pack(pady=5,
	                                                                                               fill=tk.X)
	ttk.Button(vis_frame, text="Recovery Rate", command=lambda: Recovery_rate(cdf)).pack(pady=5, fill=tk.X)
	ttk.Button(vis_frame, text="Survivors and Deaths", command=lambda: Epizisantes_thanontes(cdf)).pack(pady=5,
	                                                                                                    fill=tk.X)
	ttk.Button(vis_frame, text="Annual New Deaths", command=lambda: neoi_thanatoi(ethsio_df)).pack(pady=5,
	                                                                                               fill=tk.X)
	ttk.Button(vis_frame, text="Annual New Cases", command=lambda: Nees_molynseis(ethsio_df)).pack(pady=5,
	                                                                                               fill=tk.X)

	def plotly_btn():
		new_window = tk.Tk()
		new_window.title("Plotly Visualizations")
		new_window.geometry("400x400")
		new_window.configure(bg="#dfe3ee")

		style = ttk.Style()
		style.configure("TButton", font=("Helvetica", 12), padding=10)
		style.configure("TFrame", background="#dfe3ee")

		new_frame = ttk.Frame(new_window)
		new_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)

		ttk.Button(new_frame, text="Ποσοστά Εμβολιασμών, Άγνωστων Κρουσμάτων και Επαναμολύνσεων",
		           command=lambda: plotly_pie(df)).pack(pady=5, fill=tk.X)
		ttk.Button(new_frame, text="Καρτέλα αθρώπων σε κρίσιμη κατάσταση", command=lambda: plotlybar(df)).pack(
			pady=5, fill=tk.X)
		ttk.Button(new_frame, text="Κρουσματα, Απώλειες", command=lambda: plotly_line(df)).pack(pady=5,
		                                                                                        fill=tk.X)
		ttk.Button(new_frame, text="Linear regression", command=lambda: linear_regresion(df)).pack(pady=5,
		                                                                                           fill=tk.X)
		ttk.Button(new_frame, text="Mortality Rate", command=lambda: mortality_rate(df)).pack(pady=5, fill=tk.X)

	# CODE GIA KOUMPI
	button_image = PhotoImage(file='icon2.png').subsample(11)
	my_button = Button(root, image=button_image, command=plotly_btn, borderwidth=1)
	my_button.pack(pady=10, side='left')

	root.mainloop()


def compare_dates(df):
	print("Καρτέλα Ημερήσιας Επισκόπησης: (Προηγούμενη Μέρα-Τωρινή Μέρα-Ποσοστιαία Διαφορά)")
	copied_df = df.copy(deep=True)  # Δημιουργία Αντιγράφου και μετονομασία στήλεων
	copied_df.rename(
		columns={'date': 'Ημερομηνία', 'new_cases': 'Νέα Κρούσματα', 'confirmed': 'Επιβεβαιομένα Κρούσματα',
		         'new_deaths': 'Νέες Απώλειες', 'total_deaths': 'Συνολικές Απώλειες',
		         'new_tests': 'Νέα Τέστ', 'positive_tests': "Θετικά Τέστ", 'new_selftest': 'Νέα Σελφτέστ',
		         'new_ag_tests': 'Νέα Τέστ Αντισωμάτων',
		         'ag_tests': 'Τέστ Αντισωμάτων', 'total_tests': 'Συνολικά Τέστ',
		         'new_critical': 'Νέοι Νοσηλευόμενοι Σε Κρίσιμη',
		         'total_vaccinated_crit': 'Εμβολιασμένοι Σε Κρίσιμη',
		         'total_unvaccinated_crit': 'Μη Εμβολιασμένοι Σε Κρίσιμη',
		         'total_critical': 'Συνολικός Αριθμός Νοσηλευόμενων Σε Κρίσιμη', 'hospitalized': 'Σε Νοσηλεία',
		         'icu_percent': 'Ποσοστό σε ΜΕΘ',
		         'icu_out': 'Εκτώς της ΜΕΘ', 'new_active': 'Νέα Ενεργά Κρούσματα', 'active': 'Ενεργά Κρούσματα',
		         'recovered': 'Που Εχει Αναρρώσει', 'total_vaccinations': 'Συνολικοί Εμβολιασμοί',
		         'reinfections': 'Επαναμολύνσεις'}, inplace=True)
	copied_df = copied_df.drop(
		columns=['total_selftest', 'total_foreign', 'total_unknown', 'beds_percent', 'discharged',
		         'total_domestic', 'total_reinfections'])  # Αφαίρεση κάποιων δεδομένων

	col_start = copied_df.columns.get_loc('Νέα Κρούσματα')  # Επιλέγω ποιες στήλες θα εμφανιστούν
	col_end = copied_df.columns.get_loc('Επαναμολύνσεις')
	refined_df = copied_df.iloc[[-2, -1], col_start:col_end]  # Επιλέγω 2 τελευταίες γραμμές (2 τελευταίες μέρες)
	pct = refined_df.pct_change()  # Υπολογίζω ποσοστιαία διαφορά των δύο μερών
	second_df = pct.drop(pct.index[[0]])  # pct.drop(index=[1540])

	final_df = pd.concat([refined_df, second_df])  # Ενώνω τις 2 καρτέλες,θα προβληθούν σε μορφή αναστρόφου πίνακα
	final_df.index = ['Προηγούμενη', 'Τωρινή', 'Διαφορά']
	print(final_df.transpose())

	# Δημιουργία νέου παραθύρου για εμφάνιση δεδομένων

	data_window = tk.Toplevel()
	data_window.title("Compare Dates")
	data_window.geometry("600x400")
	data_window.configure(bg="#f0f0f0")

	text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=80, height=20)
	text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

	text_area.insert(tk.INSERT, final_df.transpose().to_string())


def cases_deaths(df):
	df.date = pd.to_datetime(df.date)  # Μετατρέπω το date Σε datetime Αντικείμενο για να Διαχειριστώ τον Χρόνο
	month_df = df.resample('M', on='date').sum()  # Το df θα Διαμορφωθεί σε Αθροίσματα Μηνών

	fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True)
	fig.suptitle('Καρτέλα Κρουσμάτων και Απωλειών')
	ax[0].plot(month_df.index, month_df.confirmed, 'b--^',
	           label='Επιβεβαιομένα Κρούσματα')  # 3 plots σε 3 Οριζόντιους Άξονες
	ax[1].plot(month_df.index, month_df.new_cases, 'r-o', label='Νέα Κρούσματα')
	ax[2].plot(month_df.index, month_df.total_deaths, 'g-s', label='Συνολικές Απώλειες')

	ax[0].set_title("Επιβεβαιομένα Κρούσματα")  # Τίτλοι
	ax[0].set_ylabel('Αριθμός Κρουσμάτων')

	ax[1].set_title('Νέα Κρούσματα')
	ax[1].set_xlabel('Ημερομηνίες')
	ax[1].set_ylabel('Αριθμός Κρουσμάτων')
	ax[2].set_title("Συνολικός Αριθμός Θανάτων")
	ax[2].set_ylabel('Αριθμός Θανάτων')

	ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%B %Y"))  # Διαμόρφωση ημερομηνιών (Μήνας-Χρόνος)
	plt.xticks(rotation=90)

	ax[0].legend()
	ax[1].legend(loc='upper left')
	ax[2].legend()
	ax[0].ticklabel_format(axis="y", style='plain')  # Αφαίρεση scientific notation
	ax[2].ticklabel_format(axis="y", style='plain')  # Αφαίρεση scientific notation
	plt.tight_layout()
	plt.show()


def vaccinations_and_actives(df):
	fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True)  # 3 plots σε 3 Άξονες
	fig.suptitle('Καρτέλα Συνολικής Εξέλιξης Επαναμολύνσεων,Ενεργών Κρουσμάτων και Εμβολιασμών')

	ax[0].plot(df.date, df.total_reinfections, 'm-', label="Επαναμολύνσεις")  # plot για Επαναμολύνσεις
	ax[1].plot(df.date, df.active, 'r--', label="Ενεργά")  # plot για Ενεργά Κρούσματα
	ax[2].plot(df.date, df.total_vaccinations, 'c.', label="Εμβολιασμοί")  # plot για Εμβολιασμούς

	ax[0].set_title("Επαναμολύνσεις")
	ax[1].set_title("Ενεργά Κρούσματα")
	ax[2].set_title("Συνολικοί Εμβολιασμοί")
	ax[0].ticklabel_format(axis="y", style='plain')  # Αφαίρεση scientific notation σε 1ο,3ο Άξονα
	ax[2].ticklabel_format(axis="y", style='plain')

	plt.xticks(df.date[::120])  # Ημερομηνίες Ανα Τετράμηνα
	plt.xticks(df.date[::120])
	plt.xticks(df.date[::120])

	ax[2].set_xlabel('Ημερομηνίες (Ανα Τετράμηνα)')  # Τίτλοι στους Άξονες
	ax[0].set_ylabel("Αριθμός Επαναμολύνσεων")
	ax[1].set_ylabel("Αριθμός Κρουσμάτων")
	ax[2].set_ylabel("Αριθμός Εμβολιασμών")

	ax[0].legend()
	ax[1].legend(loc='upper left')
	ax[2].legend(loc='upper left')

	plt.tight_layout()
	plt.show()


def pie_1(df):
	fig, axes = plt.subplots(nrows=2, ncols=2,
	                         figsize=(8, 7))  # 4 pie charts σε 2 Οριζόντιους Άξονες και 2 Κάθετους
	fig.suptitle(f'Καρτέλα Επισκόπησης {datetime.datetime.now().date()}')

	tot_reinf = df.iloc[-1, 29]  # Eπαναμολύνσεις
	tot_vacc = df.iloc[-1, 27]  # Eμβολιασμοί
	confirmed = df.iloc[-1, 2]  # Eπιβεβαιομενα

	Colors_1 = ['forestgreen', 'darkviolet', 'yellow']
	naming = 'Επαναμολύνσεις', 'Εμβολιασμοί', 'Επιβεβαιομένα Κρούσματα'
	axes[0, 0].pie([tot_reinf, tot_vacc, confirmed], labels=naming, colors=Colors_1,
	               autopct='%1.1f%%')  # πρώτο pie chart
	axes[0, 0].set_title("Ποσοστό Επαναμολύνσεων,Εμβολιασμών και Άγνωστων Κρουσμάτων")

	Colors_2 = ['cyan', 'darkolivegreen', 'orangered']
	naming_2 = 'Εμβολιασμένοι', 'Ανεμβολίαστοι', 'Συνολικός Αριθμός'
	x = df['total_vaccinated_crit'].sum()  # Αθροισμα Εμβολιασμένων Σε Κρίσιμη Κατάσταση
	y = df['total_unvaccinated_crit'].sum()  # Αθροισμα Ανεμβολίαστων Σε Κρίσιμη Κατάσταση
	z = df['total_critical'].sum()  # Συνολικός Αριθμός Σε Κρίσιμη Κατάσταση
	axes[0, 1].pie([x, y, z], labels=naming_2, colors=Colors_2, autopct='%1.1f%%')  # Δεύτερο pie
	axes[0, 1].set_title("Συνολικό Ποσοστό Ανθρώπων Σε Κρίσιμη Κατάσταση")

	domestic = df.iloc[-1, 25]  # Εγχώρια Κρούσματα
	foreign = df.iloc[-1, 24]  # Ξένα
	naming_3 = 'Εγχώρια', 'Ξένα'
	Colors_3 = ['lightblue', 'red']
	axes[1, 0].pie([domestic, foreign], labels=naming_3, colors=Colors_3, autopct='%1.1f%%')  # Τρίτο pie
	axes[1, 0].set_title('Ποσοστό Εγχωρίων και Ξένων Κρουσμάτων')

	cases = df.iloc[-1, 2]  # Επιβεβαιομένα Κρούσματα
	uknown = df.iloc[-1, 26]  # Αγνωστα Κρούσματα
	naming_4 = 'Επιβεβαιομένα', 'Άγνωστα'
	Colors_4 = ['crimson', 'turquoise']
	axes[1, 1].pie([cases, uknown], labels=naming_4, colors=Colors_4, autopct='%1.1f%%')  # Τέταρτο pie
	axes[1, 1].set_title('Ποσοστό Επιβεβαιομένων και Αγνώστων Κρουσμάτων')

	plt.tight_layout()
	plt.show()


def icu(df):
	fig, ax = plt.subplots(nrows=3, ncols=1,
	                       sharex=True)  # plots σε 3 οριζόντιους άξονες και έναν κάθετο άξονα x να μοιράζεται
	fig.suptitle('Καρτέλα ΜΕΘ')  # τίτλος καρτέλας

	ax[0].plot(df.date, df.icu_percent, label='Ποσοστό ΜΕΘ', color='r')  # πρώτο chart για ποσοστό μεθ
	ax[1].plot(df.date, df.beds_percent, label='Ποσοστό Κρεβατιών', color='b')  # δεύτερο chart για κρεβάτια μεθ
	ax[2].plot(df.date, df.icu_out, label='Εκτώς ΜΕΘ', color='g')  # τρίτο για όσους βγηκαν απο μεθ

	ax[0].set_title('Νοσηλευόμενοι σε ΜΕΘ')  # οι τρείς τίτλοι
	ax[1].set_title('Κρεβάτια ΜΕΘ')
	ax[2].set_title('Νοσηλευόμενοι Εκτώς ΜΕΘ')
	ax[2].set_xlabel('Ημερομηνίες (ανά Τετράμηνα)')
	ax[0].set_ylabel("Νοσηλευόμενοι σε ΜΕΘ")
	ax[1].set_ylabel("Αριθμός Κρεβατιών")
	ax[2].set_ylabel("Νοσηλευόμενοι Εκτώς ΜΕΘ")
	plt.xticks(df.date[::120])  # Οι Ημερομηνίες είναι ανά Τετράμηνα

	ax[0].legend()
	ax[1].legend()
	ax[2].legend(loc='upper right')
	plt.tight_layout()
	plt.show()


def hospitalized(df):
	df.date = pd.to_datetime(df.date)  # Μετατρέπω το date Σε datetime Αντικείμενο για να Διαχειριστώ τον Χρόνο
	new_df = df.resample('M', on='date').mean()  # Διαμορφώνω σε Μήνες και Βρίσκω Μέσους Όρους

	hospital = new_df.loc[
		new_df[
			'hospitalized'] > 0]  # Κάνω slice για να Απομονώσω το dataframe που έχει μη Αρνητικό Αριθμό Νοσηλευόμενων
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


# AK
cdata = 'https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv'
pdf = pd.read_csv(cdata)

TotalPopulation = 10306774
cdf = pdf.copy()
cdf['date'] = pd.to_datetime(cdf['date'])


# Ημερήσια επισκόπηση των ελέγχων αντισωμάτων

def new_ag_tests(cdf):
	cdf.plot(x="date", y="new_ag_tests")
	plt.title("Νέα τεστ αντισωμάτων ανά ημέρα")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Τεστ")
	plt.show()


# Συνολική εξέλιξη των ελέγχων αντισωμάτων
def ag_tests(cdf):
	cdf.plot(x="date", y="ag_tests")
	plt.title("Συνολικά τεστ αντισωμάτων ")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Συνολικά τεστ")
	plt.show()

	
# Ρυμθμός μεταβολής νέων κρουσμάτων
cdf['new_cases_rythmos_metavolis'] = cdf['new_cases'].pct_change() * 100

def new_cases_rythmos_metavolis(cdf):
	cdf.plot(x="date", y="new_cases_rythmos_metavolis")
	plt.title("Ρυμθμός μεταβολής νέων κρουσμάτων")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Ρυθμός νέων κρουσμάτων")
	plt.show()

# Ρυθμός μεταβολής νέων θανάτων
cdf['new_deaths_rythmos_metavolis'] = cdf['new_deaths'].pct_change() * 100

def new_deaths_rythmos_metavolis(cdf):
	cdf.plot(x="date", y="new_deaths_rythmos_metavolis")
	plt.title("Ρυμθμός μεταβολής νέων θανάτων")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Ρυθμός νέων θανάτων")
	plt.show()


# Ρυθμός μεταβολής συνολικών εμβολιασμών
cdf['total_vaccinations_rythmos_metavolis'] = cdf['total_vaccinations'].pct_change() * 100

def total_vaccinations_rythmos_metavolis(cdf):
	cdf.plot(x="date", y="total_vaccinations_rythmos_metavolis")
	plt.title("Ρυμθμός μεταβολής συνολικών εμβολιασμών")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Ρυθμός συνολικών εμβολιασμών")
	plt.show()


# Ρυθμός μεταβολής συνολικών τεστ
cdf['total_tests_rythmos_metavolis'] = cdf['total_tests'].pct_change() * 100

def total_tests_rythmos_metavolis(cdf):
	cdf.plot(x="date", y="total_tests_rythmos_metavolis")
	plt.title("Ρυμθμός μεταβολής συνολικών τεστ")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Ρυθμός συνολικών τεστ")
	plt.show()


# Case fatality rate

cdf['case_fatality_rate'] = cdf['total_deaths'] / cdf['confirmed'] * 100

def Case_fatality_rate(cdf):
	cdf.plot(x="date", y="case_fatality_rate")
	plt.title("Θνητότητα")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Θνητότητα")
	plt.show()


# Recovery rate

cdf['Recovery_rate'] = cdf['recovered'] / cdf['confirmed'] * 100


def Recovery_rate(cdf):
	cdf.plot(x="date", y="Recovery_rate")
	plt.title("Δείκτης επιβίωσης")
	plt.xlabel("Ημερομηνία")
	plt.ylabel("Δείκτης επιβίωσης")
	plt.show()


# Επιζήσαντες και θανόντες από το σύνολο του πλυθησμού στην Ελλάδα με Pie
def Epizisantes_thanontes(cdf):
	tl_deaths = float(cdf['total_deaths'].iloc[-1])
	Total_survived = float(TotalPopulation - tl_deaths)
	slices = [Total_survived, tl_deaths]
	explode = (0, 0.1)
	labels = ['Επιζήσαντες', 'Απεβίωσαν']
	plt.pie(slices, labels=labels, autopct='%1.1f%%', explode=explode)
	plt.title('Επιζήσαντες και θανόντες από τον κορωνοιό στην Ελλάδα')
	plt.show()


# Δημιουργούμε ένα column με τα χρόνια
cdf['year'] = cdf['date'].dt.year
# Σιγουρεύουμε ότι ειναι νούμερα και αλλάζουμε σε 0 όσα δεν είναι
cdf['new_deaths'] = pd.to_numeric(cdf['new_deaths'], errors='coerce').fillna(0)
cdf['new_critical'] = pd.to_numeric(cdf['new_cases'], errors='coerce').fillna(0)
# Δημιουργόυμε dataframe με τα αθροίσματα ανά έτος
ethsio_df = cdf.groupby('year')[['new_deaths', 'new_cases']].sum()


# Bar chart για νέους θανάτους
def neoi_thanatoi(ethsio_df):
	plt.bar(ethsio_df.index, ethsio_df['new_deaths'], width=0.4, color='black', label='New Deaths')
	plt.xticks(ethsio_df.index, rotation=45)
	plt.xlabel('Έτος')
	plt.ylabel('Μέτρηση')
	plt.title('Νεόι θάνατοι ανά έτος')
	plt.legend()
	plt.show()


# Bar chart για νέες μολύνσεις

def Nees_molynseis(ethsio_df):
	plt.bar(ethsio_df.index, ethsio_df['new_cases'], width=0.4, color='red', label='New Cases')
	plt.xticks(ethsio_df.index, rotation=45)
	plt.xlabel('Έτος')
	plt.ylabel('Μέτρηση')
	plt.title('Νέες μολύνσεις ανά έτος')
	plt.legend()
	plt.show()


def plotly_pie(df):
	tot_reinf = df.iloc[-1, 29]
	tot_vacc = df.iloc[-1, 27]
	tot_unkn = df.iloc[-1, 26]

	labels = ['Συνολικές Επαναμολύνσεις', 'Συνολικοί Εμβολιασμοί', 'Συνολικά Άγνωστα Κρούσματα']
	values = [tot_reinf, tot_vacc, tot_unkn]

	fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
	fig.update_layout(title_text="Ποσοστά Συνολικών Επαναμολύνσεων, Εμβολιασμών και Άγνωστων Κρουσμάτων",
	                  title_x=0.5)
	fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))

	fig.show()


def plotlybar(df):
	# cvs info
	new_critical = df.iloc[:, 13].sum()
	total_vaccinated_crit = df.iloc[:, 14].sum()
	total_unvaccinated_crit = df.iloc[:, 15].sum()
	total_critical = df.iloc[:, 12].sum()

	# labels values gia bar chart
	labels = ['Total Vaccinated Critical', 'Total Unvaccinated Critical', 'Total critical', 'New critical']
	values = [new_critical, total_vaccinated_crit, total_unvaccinated_crit, total_critical]

	# dimiourgia bar chart
	fig = go.Figure([go.Bar(x=labels, y=values)])

	# layout
	fig.update_layout(
		title='Critical Cases Summary',
		xaxis_title='Category',
		yaxis_title='Total Count',
		template='plotly_white'
	)

	# emfanisi
	fig.show()


def plotly_pie(df):
	tot_reinf = df.iloc[-1, 29]
	tot_vacc = df.iloc[-1, 27]
	tot_unkn = df.iloc[-1, 26]

	labels = ['Συνολικές Επαναμολύνσεις', 'Συνολικοί Εμβολιασμοί', 'Συνολικά Άγνωστα Κρούσματα']
	values = [tot_reinf, tot_vacc, tot_unkn]

	fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
	fig.update_layout(title_text="Ποσοστά Συνολικών Επαναμολύνσεων, Εμβολιασμών και Άγνωστων Κρουσμάτων", title_x=0.5)


	fig.show()

def plotlybar(df):

	# cvs info
	new_critical = df.iloc[:, 13].sum()
	total_vaccinated_crit = df.iloc[:, 14].sum()
	total_unvaccinated_crit = df.iloc[:, 15].sum()
	total_critical = df.iloc[:, 12].sum()

	# labels values gia bar chart
	labels = ['Total Vaccinated Critical', 'Total Unvaccinated Critical', 'Total critical', 'New critical']
	values = [new_critical, total_vaccinated_crit, total_unvaccinated_crit, total_critical]

	# dimiourgia bar chart
	fig = go.Figure([go.Bar(x=labels, y=values)])


	# layout
	fig.update_layout(
		title='Critical Cases Summary',
		xaxis_title='Category',
		yaxis_title='Total Count',
		template='plotly_white'
	)

	# emfanisi
	fig.show()


def plotly_line(df):
	dates = df.iloc[:, 0]
	krousmata = df.iloc[:, 2]
	apolies = df.iloc[:, 4]

	data = pd.DataFrame({'year': dates, 'ΚΡΟΥΣΜΑΤΑ': krousmata, 'ΑΠΩΛΕΙΕΣ': apolies})

	# plotly express
	fig = px.line(data, x='year', y=['ΚΡΟΥΣΜΑΤΑ', 'ΑΠΩΛΕΙΕΣ'], markers=True)
	fig.show()


def linear_regresion(df):

	url = "https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv"
	df = pd.read_csv(url)

	# date column kai krousmata column
	date = df.iloc[:, 1]
	krousmata = df.iloc[:, 3]

	# kainourio df
	df2 = pd.DataFrame(date)

	# date column apo string se datetime format
	df2['date'] = pd.to_datetime(df2['date'])

	# xorizo hmerominies gia na einai se sosto format
	df2['year'] = df2['date'].dt.year
	df2['month'] = df2['date'].dt.month
	df2['day'] = df2['date'].dt.day

	# eisago sosto format gia to model
	X = df2[['year', 'month', 'day']]  # Features
	y = krousmata  # Target variable

	# Linear regression
	model = LinearRegression()
	model.fit(X, y)

	# pairno thn teleutaia hmerominia apo to cvs kai dimiourgo hmerominies gia ena xrono meta
	future_dates = pd.date_range(start=df2['date'].max(), periods=365, freq='D')

	# xorizoume se xronia mines kai meres to sequence apo melontika dates
	future_year = future_dates.year
	future_month = future_dates.month
	future_day = future_dates.day

	#xrisimopoio column_stack oste na dimiourgiso 2d array gia to model
	future_X = np.column_stack((future_year, future_month, future_day))

	future_predictions = model.predict(future_X)

	# data kai trendline
	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=df['date'], y=krousmata,
		mode='markers',
		name='ΚΡΟΥΣΜΑΤΑ ΑΠΟ ΤΩΡΙΝΑ ΔΕΔΟΜΕΝΑ',
		opacity=0.65
	))

	# linear regression gia dates apo cvs
	fig.add_trace(go.Scatter(
		x=df['date'], y=model.predict(X),
		mode='lines',
		name='ΓΡΑΜΜΗ ΤΑΣΗΣ',
		line=dict(color='darkblue')
	))

	# linear regression gia melontikes hmerominies
	fig.add_trace(go.Scatter(
		x=future_dates, y=future_predictions,
		mode='lines',
		name='ΜΕΛΛΟΝΤΙΚΑ ΚΡΟΥΣΜΑΤΑ',
		line=dict(color='red')
	))
	fig.update_layout(title='COVID-19 ΜΕΛΛΟΝΤΙΚΗ ΠΡΟΒΛΕΨΗ ΚΡΟΥΣΜΑΤΩΝ - LINEAR REGRESSION')

	fig.show()



def mortality_rate(df):
	confirmed_cases = df.iloc[:, 2]
	deaths = df.iloc[:, 4]
	date2 = df.iloc[:, 0]
	mortality_rate = (deaths / confirmed_cases) * 100

	# graph settings-emfanisi
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=date2, y=mortality_rate, mode='lines', name='Mortality Rate',
	                         line=dict(color='blue', width=2)))
	fig.update_layout(
		title='Mortality Rate Σε χρονικη περιοδο',
		xaxis_title='Date',
		yaxis_title='Mortality Rate (%)',
		xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),
		yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),
		font=dict(family="Arial", size=12, color="black"),
		plot_bgcolor='rgba(0, 0, 0, 0)'
	)
	fig.show()


if __name__ == "__main__":
	main()
	print("Τέλος Προγράμματος!")
