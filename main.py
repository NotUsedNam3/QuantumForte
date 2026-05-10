# Imports
import tkinter as tk
from tkinter import ttk
import psutil


#get data
def get_processes():
    processes = []

    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            info = proc.info
            name = info['name']
            if name == "System Idle Process" or name == "Idle":
                continue
            cpu = info['cpu_percent']
            ram = round(info['memory_info'].rss / (1024 * 1024), 2)

            io = info.get('io_counters')
            disk = round((io.read_bytes + io.write_bytes) / (1024 * 1024), 2) if io else 0

            processes.append([name, cpu, ram, disk])

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes

processes = get_processes()
for process in processes:
    name = process[0]
    cpu = str(process[1])
    ram = str(process[2])
    disk = str(process[3])

    print("Programm: " + name + " | CPU: " + cpu + " | RAM: " + ram + " | SSD: " + disk)

#Tkinter metadata
root = tk.Tk()
root.title("QuantumForte")
window_width = 1280
window_height = 740
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)
root.iconbitmap("./assets/QFLogo.ico")

#tkinter design UI
style = ttk.Style()
style.configure("ArialBold.TButton", font=("Arial", 15, "bold"))

def link_home():
    root.quit()

for i in range(21):
    root.columnconfigure(i, minsize=60)

for i in range(12):
    root.rowconfigure(i, minsize=60)

photo = tk.PhotoImage(file="./assets/QFLogo.png")
ttk.Label(root, image=photo).grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew", pady=(10, 10), padx=(10, 0))
ttk.Label(root, text="QuantumForte", font=("Impact", 60)).grid(row=0, column=2, rowspan=2, columnspan=9, sticky="nsew", padx=(10, 0))

search = tk.PhotoImage(file="./assets/Search.png")
ttk.Label(root, image=search, text="Suche:", font=("Arial", 15, "bold"  ), compound=tk.LEFT).grid(row=0, column=11, rowspan=1, columnspan=2, sticky="nsew", pady=(10,0), padx=(10, 0))
ttk.Entry(root, font=("Arial", 15)).grid(row=0, column=13, rowspan=1, columnspan=8, sticky="nsew", pady=(10, 0), padx=(0, 10))

home = tk.PhotoImage(file="./assets/Home.png")
ttk.Button(root, image=home, text="Startseite", style="ArialBold.TButton", compound=tk.LEFT, command=link_home).grid(row=1, column=13, rowspan=1, columnspan=8, sticky="nsew", pady=(10, 0), padx=(0, 10))

id_symbol = tk.PhotoImage(file="./assets/hastag.png")
ttk.Label(root, image=id_symbol, text="ID", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=2, column=0, rowspan=1, columnspan=2, sticky="NEW", padx=(10, 0))

process_name = tk.PhotoImage(file="./assets/process_name.png")
ttk.Label(root, image=process_name, text="Prozess", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=2, column=1, rowspan=1, columnspan=3, sticky="NEW")

cpu_symbol = tk.PhotoImage(file="./assets/CPU.png")
ttk.Label(root, image=cpu_symbol, text="CPU", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=2, column=4, rowspan=1, columnspan=2, sticky="NEW")

ram_symbol = tk.PhotoImage(file="./assets/RAM.png")
ttk.Label(root, image=ram_symbol, text="RAM", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=2, column=6, rowspan=1, columnspan=2, sticky="NEW")

ssd_symbol = tk.PhotoImage(file="./assets/SSD.png")
ttk.Label(root, image=ssd_symbol, text="SSD", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=2, column=8, rowspan=1, columnspan=2, sticky="NEW")

process_ids = ""
for ids in range(1, 22):
    process_ids += f"{ids}\n"
ttk.Label(root, text=process_ids, font=("Arial", 15)).grid(row=3, column=0, rowspan=9, columnspan=3, sticky="NW", padx=(10, 0))

processes = get_processes()
process_names = ""
for process in processes[:21]:
    name = process[0]
    process_names += f"{name}\n"
ttk.Label(root, text=process_names, font=("Arial", 15)).grid(row=3, column=1, rowspan=9, columnspan=3, sticky="NW")

processes = get_processes()
process_cpus = ""
for process in processes[:21]:
    cpu = process[1]
    process_cpus += f"{cpu}  %\n"
ttk.Label(root, text=process_cpus, font=("Arial", 15)).grid(row=3, column=4, rowspan=9, columnspan=2, sticky="NW")

processes = get_processes()
process_rams = ""
for process in processes[:21]:
    ram = process[2]
    process_rams += f"{ram}  MB\n"
ttk.Label(root, text=process_rams, font=("Arial", 15)).grid(row=3, column=6, rowspan=9, columnspan=2, sticky="NW")

processes = get_processes()
process_ssds = ""
for process in processes[:21]:
    ssd = process[3]
    process_ssds += f"{ssd}  MB\n"
ttk.Label(root, text=process_ssds, font=("Arial", 15)).grid(row=3, column=8, rowspan=9, columnspan=2, sticky="NW")

ttk.Label(root, image=cpu_symbol, text="Prozessor", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=2, column=10, rowspan=1, columnspan=11, sticky="NW")

cpu_all = psutil.cpu_percent(interval=1)
processes_count = len(psutil.pids())
cpu_frequency = round(psutil.cpu_freq().current / 1000, 2)
real_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)
ttk.Label(root, text=f"Prozesse: {processes_count}\nAuslastung: {cpu_all} %\nGeschwindigkeit: {cpu_frequency} GHz\nKerne: {real_cores}\nLogische Prozessoren: {logical_cores}", font=("Arial", 15)).grid(row=3, column=10, rowspan=4, columnspan=11, sticky="NW")

ttk.Label(root, image=ram_symbol, text="Arbeitsspeicher", font=("Arial", 15, "bold"), compound=tk.RIGHT).grid(row=7, column=10, rowspan=1, columnspan=11, sticky="NW")

ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
ram_usage_percent = psutil.virtual_memory().percent
ram_usage_mb = int(psutil.virtual_memory().used / (1024**2))
ram_available_mb = int(psutil.virtual_memory().available / (1024**2))
ttk.Label(root, text=f"Arbeitsspeicher gesamt: {ram_gb} GB\nAuslastung Prozent: {ram_usage_percent} %\nAuslastung Megabyte: {ram_usage_mb} MB\nVerfügbar: {ram_available_mb} MB\n", font=("Arial", 15)).grid(row=8, column=10, rowspan=4, columnspan=11, sticky="NW")

#loop
root.mainloop()
