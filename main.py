#Import wichtiger Bibliotheken
import tkinter as tk
import psutil


#Erstellen der Funktion für Datenabruf
def get_processes():
    processes = []      #Leere Liste für die Werte Prozesse
    total_processes = []#Leere Liste für die totalen Werte der Prozesse

    logical_cores = psutil.cpu_count(logical=True)  #Die Anzahl logischen Kerne in der CPU

    for proc in psutil.process_iter():  #Aufzählung aller Prozesse einzeln
        try:
            name = proc.name()
            if name == "System Idle Process" or name == "Idle" or name == "":   #Überprüft ob der Namen des Prozesses Idle oder leer ist
                continue
            name = proc.name().removesuffix(".exe") #Entfernt Suffix .exe
            cpu = round(proc.cpu_percent() / logical_cores, 1)  #Gibt die CPU Auslastung in Prozent an (pro Prozess)
            ram = round(proc.memory_info().rss / 1024**2, 2)    #Gibt die RAM Auslastung an ( / 1024** -> Angabe in MB) (pro Prozess)
            io = proc.io_counters() #Gibt die systemweite I/O Statistik an (inkl Read und Write Werten)
            ssd = round((io.read_bytes + io.write_bytes) / 1024**3, 2)  #Addiert die Werte von geschriebenen und gelesenen Daten in GB (pro Prozess)

            processes.append([name, cpu, ram, ssd]) #Fügt die Dateien in die vorher definierte Liste ein

        except (psutil.NoSuchProcess, psutil.AccessDenied): #Fängt Fehler ab, falls man keinen Zugriff auf einen Przess hat oder dieser nicht existiert
            continue

    cpu_total = psutil.cpu_percent()    #Gibt die totale CPU-Auslastung in % an
    ram_total = round(psutil.virtual_memory().used / (1024**3), 2)  #Gibt die totale RAM-Auslastung in GB an
    io = psutil.disk_io_counters()  #Gibt die systemweite I/O Statistik an (inkl Read und Write Werten)
    ssd_total = round((io.read_bytes + io.write_bytes) / (1024**3), 2)  #Gibt die Totale Read und Write Auslastung der SSD an

    # Hängt die Variabeln an die vorher definierte Liste an
    total_processes.append(cpu_total)
    total_processes.append(ram_total)
    total_processes.append(ssd_total)

    return processes, total_processes   #Gibt die Prozess-Werte und Totalen Werte an


sort_key = [1]  #Definiert den Startwert des Sortierschlüssels

#Definiert die Funktion um den Wert des Sortierschlüssels zu ändern (wichtig für Buttons)
def sort_name():
    sort_key[0] = 0

def sort_cpu():
    sort_key[0] = 1

def sort_ram():
    sort_key[0] = 2

def sort_ssd():
    sort_key[0] = 3

#Definiert die Funktion um
def sort_key_func(x):
    if sort_key[0] == 0:
        return x[0]
    return x[sort_key[0]]


#Definiert die Funktion um Werte zu updaten wie zB die Prozesswerte oder die Totalen Werte
def refresh():
    reverse = sort_key[0] != 0  #gibt True zurück, wenn es nicht nach Namen sortiert wird
    processes, total_processes = get_processes()    #Ruft die Funktion auf für die Werte
    processes = sorted(processes, key=sort_key_func, reverse=reverse)   #Sortiert die Prozesse nach Sortierschlüssel

    #Zerstört alle Widgets, die aktuallisiert werde müssen
    for widget in summary_frame.winfo_children():
        widget.destroy()
    for widget in processes_frame.winfo_children():
        widget.destroy()
    for widget in cpu_frame.winfo_children():
        widget.destroy()
    for widget in ram_frame.winfo_children():
        widget.destroy()
    for widget in ssd_frame.winfo_children():
        widget.destroy()

    #Erstellt zwei Grids für die Anordnung von Widgets
    for i in range(15):
        summary_frame.columnconfigure(i, minsize=60, weight=0)
        processes_frame.columnconfigure(i, minsize=60, weight=0)

    #Erstellt die Label für die Totalen Werte. Nutzt die Liste mit Indizen, Schriftart, Hintergrundfarbe und ordnet es im Grid an
    tk.Label(summary_frame, text="Total", font=("Arial", 12, "bold"), bg="#F5F5F5").grid(row=0, column=2, columnspan=4, sticky="W", pady=10)
    tk.Label(summary_frame, text=f"{total_processes[0]} %", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=6, columnspan=3, sticky="E", pady=10)
    tk.Label(summary_frame, text=f"{total_processes[1]} GB", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=9, columnspan=3, sticky="E", pady=10)
    tk.Label(summary_frame, text=f"{total_processes[2]} GB", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=12, columnspan=3, sticky="E", padx=(0, 10), pady=10)

    #Erstellt 20 Labels für die Prozesse. Nützt i von enumerate für die Nr. und proc für die Werte.
    for i, proc in enumerate(processes[:20]):
        tk.Label(processes_frame, text=i + 1, font=("Arial", 12), bg="#F5F5F5").grid(row=i, column=0, columnspan=2, sticky="W", padx=(10, 0))
        tk.Label(processes_frame, text=proc[0], font=("Arial", 12), bg="#F5F5F5").grid(row=i, column=2, columnspan=4, sticky="W")
        tk.Label(processes_frame, text=f"{proc[1]} %", font=("Arial", 12), bg="#F5F5F5").grid(row=i, column=6, columnspan=3, sticky="E")
        tk.Label(processes_frame, text=f"{proc[2]} MB", font=("Arial", 12), bg="#F5F5F5").grid(row=i, column=9, columnspan=3, sticky="E")
        tk.Label(processes_frame, text=f"{proc[3]} GB", font=("Arial", 12), bg="#F5F5F5").grid(row=i, column=12, columnspan=3, sticky="E", padx=(0, 10))

    #Definiert Variabeln; Anzahl Prozesse, CPU Prozesse, Anzahl echte Kerne und logische Kerne
    processes_count = len(psutil.pids())
    cpu_frequency = round(psutil.cpu_freq().current / 1000, 2)
    real_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    #Erstellt die Labels für die allgemeinen Werte der CPU indem es die vorher definierten Variabeln nutzt
    cpu_titel_label = tk.Label(cpu_frame, image=cpu_icon, text="Prozessor ", compound="right", font=("Arial", 14, "bold"), bg="#B8AFD5")
    cpu_titel_label.pack(side="top", anchor="nw", padx=10, pady=10)
    right_line = tk.Frame(cpu_frame, bg="#C2C2C2", height=2)
    right_line.pack(side="top", fill="x")
    cpu_props_total = tk.Label(cpu_frame, text=f"Auslastung: {total_processes[0]} %", font=("Arial", 12), bg="#F5F5F5")
    cpu_props_total.pack(side="top", anchor="nw", padx=10, pady=(5, 0))
    cpu_props_count = tk.Label(cpu_frame, text=f"Anzahl Prozesse: {processes_count}", font=("Arial", 12), bg="#F5F5F5")
    cpu_props_count.pack(side="top", anchor="nw", padx=10)
    cpu_props_freq = tk.Label(cpu_frame, text=f"Frequenz: {cpu_frequency} GHz", font=("Arial", 12), bg="#F5F5F5")
    cpu_props_freq.pack(side="top", anchor="nw", padx=10)
    cpu_props_real = tk.Label(cpu_frame, text=f"Echte Kerne: {real_cores}", font=("Arial", 12), bg="#F5F5F5")
    cpu_props_real.pack(side="top", anchor="nw", padx=10)
    cpu_props_log = tk.Label(cpu_frame, text=f"Logische Kerne: {logical_cores}", font=("Arial", 12), bg="#F5F5F5")
    cpu_props_log.pack(side="top", anchor="nw", padx=10, pady=(0, 10))

    # Definiert Variabeln; Anzahl RAM in GB, Benutzter RAM in %, Verfügbarer RAM in GB
    ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    ram_usage_percent = psutil.virtual_memory().percent
    ram_available_mb = round(psutil.virtual_memory().available / (1024**3), 1)

    # Erstellt die Labels für die allgemeinen Werte des RAMs indem es die vorher definierten Variabeln nutzt
    ram_titel_label = tk.Label(ram_frame, image=ram_icon, text="Arbeitsspeicher ", compound="right", font=("Arial", 14, "bold"), bg="#C0D5AF")
    ram_titel_label.pack(side="top", anchor="nw", padx=10, pady=10)
    right_line = tk.Frame(ram_frame, bg="#C2C2C2", height=2)
    right_line.pack(side="top", fill="x")
    ram_props_total = tk.Label(ram_frame, text=f"Total Arbeitsspeicher: {ram_gb} GB", font=("Arial", 12), bg="#F5F5F5")
    ram_props_total.pack(side="top", anchor="nw", padx=10, pady=(5, 0))
    ram_props_usage = tk.Label(ram_frame, text=f"In Verwendung (GB): {total_processes[1]} GB", font=("Arial", 12), bg="#F5F5F5")
    ram_props_usage.pack(side="top", anchor="nw", padx=10)
    ram_props_freq = tk.Label(ram_frame, text=f"In Verwendung (%): {ram_usage_percent} %", font=("Arial", 12), bg="#F5F5F5")
    ram_props_freq.pack(side="top", anchor="nw", padx=10)
    ram_props_free = tk.Label(ram_frame, text=f"Zur Verfügung: {ram_available_mb} GB", font=("Arial", 12), bg="#F5F5F5")
    ram_props_free.pack(side="top", anchor="nw", padx=10, pady=(0, 10))

    # Definiert Variabeln; Totale Grösse des Datenträgers in TB, benutze Grösse auf de Datenträger in TB, Freie Grösse auf dem Datenträger in TB
    ssd_total_tb = round(psutil.disk_usage("C:\\").total / (1024**4), 1)
    ssd_used_tb = round(psutil.disk_usage("C:\\").used / (1024**4), 1)
    ssd_free_tb = round(ssd_total_tb - ssd_used_tb, 1)

    # Erstellt die Labels für die allgemeinen Werte der SSD indem es die vorher definierten Variabeln nutzt
    ssd_titel_label = tk.Label(ssd_frame, image=ssd_icon, text="Festplatte ", compound="right", font=("Arial", 14, "bold"), bg="#9EADE5")
    ssd_titel_label.pack(side="top", anchor="nw", padx=10, pady=10)
    right_line = tk.Frame(ssd_frame, bg="#C2C2C2", height=2)
    right_line.pack(side="top", fill="x")
    ssd_props_all = tk.Label(ssd_frame, text=f"Total R/W (seit Boot): {total_processes[2]} GB", font=("Arial", 12), bg="#F5F5F5")
    ssd_props_all.pack(side="top", anchor="nw", padx=10, pady=(5, 0))
    ssd_props_total = tk.Label(ssd_frame, text=f"Grösse: {ssd_total_tb} TB", font=("Arial", 12), bg="#F5F5F5")
    ssd_props_total.pack(side="top", anchor="nw", padx=10)
    ssd_props_used = tk.Label(ssd_frame, text=f"Belegt: {ssd_used_tb} TB", font=("Arial", 12), bg="#F5F5F5")
    ssd_props_used.pack(side="top", anchor="nw", padx=10)
    ssd_props_free = tk.Label(ssd_frame, text=f"Frei: {ssd_free_tb} TB", font=("Arial", 12), bg="#F5F5F5")
    ssd_props_free.pack(side="top", anchor="nw", padx=10, pady=(0, 10))

    root.after(1000, refresh)   #Gibt die Zeit an, wie oft es refreshen soll und refresht anschliessend


#Erstellt ein neues Fenster in Tkinter (root)
root = tk.Tk()
root.title("QuantumForte")  #Namen des Fensters
root.configure(bg="#F5F5F5")    #Farbe des Fensters
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Schaut die Grösse des Bildschirms an. Ab einer gewissen Grösse wird es im Fenster Modus geöffnet
if screen_width > 1920 and screen_height > 1080:
    window_width = 1380
    window_height = 770
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root.resizable(False, False)
    root.iconbitmap("./assets/QFLogo.ico")
else:
    root.state("zoomed")

#Ladet alle Bilde die genutzt werden (./asset Ordner)
logo = tk.PhotoImage(file="./assets/QFLogo.png")
search_icon = tk.PhotoImage(file="./assets/Search.png")
sort_icon = tk.PhotoImage(file="./assets/sort.png")
letter_icon = tk.PhotoImage(file="./assets/letter.png")
cpu_icon = tk.PhotoImage(file="./assets/CPU.png")
ram_icon = tk.PhotoImage(file="./assets/RAM.png")
ssd_icon = tk.PhotoImage(file="./assets/SSD.png")
numer_icon = tk.PhotoImage(file="./assets/hashtag.png")
process_icon = tk.PhotoImage(file="./assets/process_name.png")


#Definiert alle Frames, die benötigt werden; top_bar, main_content, sidebar, content_center, header_frame, stats_line, summary_frame, stats_line2, process_frame, cpu_frame, ram_frame, ssd_frame
top_bar = tk.Frame(root, bg="#F5F5F5", height=120, relief="groove", bd=2)
top_bar.pack(side="top", fill="x", padx=10, pady=(10, 0))
top_bar.pack_propagate(False)

main_content = tk.Frame(root)
main_content.pack(side="top", fill="both", expand=True)

sidebar = tk.Frame(main_content, bg="#F5F5F5", relief="groove", bd=2)
sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)

content_center = tk.Frame(main_content, bg="#F5F5F5", relief="groove", bd=2)
content_center.pack(side="left", fill="y", padx=(10, 0), pady=10)

content_right = tk.Frame(main_content, bg="#F5F5F5", width=420, relief="groove", bd=2)
content_right.pack(side="left", fill="both", padx=10, pady=10)
content_right.pack_propagate(False)

header_frame = tk.Frame(content_center, bg="#F5F5F5")
header_frame.pack(side="top", fill="x")

stats_line = tk.Frame(content_center, bg="#C2C2C2", height=2)
stats_line.pack(side="top", fill="x")

summary_frame = tk.Frame(content_center, bg="#F5F5F5")
summary_frame.pack(side="top", fill="x")

stats_line2 = tk.Frame(content_center, bg="#C2C2C2", height=2)
stats_line2.pack(side="top", fill="x", pady=(0, 10))

processes_frame = tk.Frame(content_center, bg="#F5F5F5")
processes_frame.pack(side="top", fill="x")

cpu_frame = tk.Frame(content_right, bg="#F5F5F5", relief="groove", bd=2)
cpu_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=(10, 0))

ram_frame = tk.Frame(content_right, bg="#F5F5F5", relief="groove", bd=2)
ram_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=(10, 0))

ssd_frame = tk.Frame(content_right, bg="#F5F5F5", relief="groove", bd=2)
ssd_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=(10, 0))


#Erstellt drei Grids für die Anordnung von Widgets
for i in range(15):
    header_frame.columnconfigure(i, minsize=60, weight=0)
    summary_frame.columnconfigure(i, minsize=60, weight=0)
    processes_frame.columnconfigure(i, minsize=60, weight=0)

logo_label = tk.Label(top_bar, image=logo, bg="#F5F5F5")    #Das Logo von QuantumForte
logo_label.pack(side="left", padx=10, pady=10)

title_label = tk.Label(top_bar, text="QuantumForte", font=("Impact", 60), bg="#F5F5F5") #Der Titel (gross und sichtbar)
title_label.pack(side="left", padx=(10, 0))

color_frame = tk.Frame(top_bar, bg="#F5F5F5")   #Frame für die Farben oben rechts
color_frame.pack(side="right")

color_frame_top = tk.Frame(color_frame, bg="#F5F5F5")   #Frame für die Farben oben
color_frame_top.pack(side="top")

tk.Frame(color_frame_top, bg="#C0D5AF", width=116, height=48).pack(side="right", padx=(0, 10), pady=(10, 0))    #Farbe 1
tk.Frame(color_frame_top, bg="#B8AFD5", width=116, height=48).pack(side="right", padx=(10, 0), pady=(10, 0))    #Farbe 2

color_frame_bottom = tk.Frame(color_frame, bg="#F5F5F5")    #Frame für die Farben unten
color_frame_bottom.pack(side="top")

tk.Frame(color_frame_bottom, bg="#9EADE5", width=116, height=48).pack(side="right", padx=(0, 10), pady=(0, 10)) #Farbe 3
tk.Frame(color_frame_bottom, bg="#C2C2C2", width=116, height=48).pack(side="right", padx=(10, 0), pady=(0, 10)) #Farbe 4

sort_label = tk.Label(sidebar, image=sort_icon, relief="raised")    #Das Sortier-Icon
sort_label.pack(side="top", padx=10, pady=(10, 0))

sort_line = tk.Frame(sidebar, bg="#C2C2C2", height=2)   #Eine Trennlinie
sort_line.pack(side="top", fill="x", pady=(10, 0))

#Die vier Buttons, die man zum Sortieren nutzen kann (inkl Command)
letter_button = tk.Button(sidebar, image=letter_icon, command=sort_name, bg="#C2C2C2")
letter_button.pack(side="top", padx=10, pady=(10, 0))

cpu_button = tk.Button(sidebar, image=cpu_icon, command=sort_cpu, bg="#B8AFD5")
cpu_button.pack(side="top", padx=10, pady=(10, 0))

ram_button = tk.Button(sidebar, image=ram_icon, command=sort_ram, bg="#C0D5AF")
ram_button.pack(side="top", padx=10, pady=(10, 0))

ssd_button = tk.Button(sidebar, image=ssd_icon, command=sort_ssd, bg="#9EADE5")
ssd_button.pack(side="top", padx=10, pady=(10, 0))

#Die Titel (Nr., Namen, CPU, RAM, SSD) für die Prozesse im Grid angeordnet
tk.Label(header_frame, image=numer_icon, text="Nr. ", compound="right", font=("Arial", 14, "bold"), bg="#F5F5F5").grid(row=0, column=0, columnspan=2, sticky="W", padx=(10, 0), pady=10)
tk.Label(header_frame, image=process_icon, text="Prozess ", compound="right", font=("Arial", 14, "bold"), bg="#C2C2C2").grid(row=0, column=2, columnspan=4, sticky="W", pady=10)
tk.Label(header_frame, image=cpu_icon, text="CPU ", compound="right", font=("Arial", 14, "bold"), bg="#B8AFD5").grid(row=0, column=6, columnspan=3, sticky="E", pady=10)
tk.Label(header_frame, image=ram_icon, text="RAM ", compound="right", font=("Arial", 14, "bold"), bg="#C0D5AF").grid(row=0, column=9, columnspan=3, sticky="E", pady=10)
tk.Label(header_frame, image=ssd_icon, text="SSD ", compound="right", font=("Arial", 14, "bold"), bg="#9EADE5").grid(row=0, column=12, columnspan=3, sticky="E", padx=(0, 10), pady=10)


refresh()   #Ruft die refresh-Funktion auf um alles zu aktualisieren
root.mainloop() #Beendet den Main-Loop
