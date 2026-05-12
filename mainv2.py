import tkinter as tk
# from tkinter import ttk
import psutil

def get_processes():
    processes = []
    total_processes = []

    for proc in psutil.process_iter():
        try:
            name = proc.name()

            if name == "System Idle Process" or name == "Idle":
                continue

            cpu = proc.cpu_percent()
            ram = round(proc.memory_info().rss / (1024 * 1024), 2)

            io = proc.io_counters()
            ssd = round((io.read_bytes + io.write_bytes) / (1024 * 1024), 2)

            processes.append([name, cpu, ram, ssd])


        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    cpu_total = psutil.cpu_percent()
    ram_total = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    io = psutil.disk_io_counters()
    ssd_total = round((io.read_bytes + io.write_bytes) / (1024 ** 3), 2)

    total_processes.append(cpu_total)
    total_processes.append(ram_total)
    total_processes.append(ssd_total)

    return processes, total_processes

processes, total_processes = get_processes()


def refresh():
    processes, total_processes = get_processes()


    for widget in summary_frame.winfo_children():
        widget.destroy()

    tk.Label(summary_frame, text="Total", font=("Arial", 14, "bold"), bg="lightgray").grid(row=0, column=2, columnspan=3, sticky="W", pady=10)
    tk.Label(summary_frame, text=f"{total_processes[0]} %", font=("Arial", 14), bg="lightgray").grid(row=0, column=5, columnspan=3, sticky="E", pady=10)
    tk.Label(summary_frame, text=f"{total_processes[1]} GB", font=("Arial", 14), bg="lightgray").grid(row=0, column=8, columnspan=3, sticky="E", pady=10)
    tk.Label(summary_frame, text=f"{total_processes[2]} GB", font=("Arial", 14), bg="lightgray").grid(row=0, column=11, columnspan=3, sticky="E", padx=(0, 10), pady=10)


    for widget in processes_frame.winfo_children():
        widget.destroy()

    i = 0
    for proc in processes[:21]:
        tk.Label(processes_frame, text=i + 1, font=("Arial", 14), bg="lightgray").grid(row=i, column=0, columnspan=2, sticky="W", padx=(10, 0))
        tk.Label(processes_frame, text=proc[0], font=("Arial", 14), bg="lightgray").grid(row=i, column=2, columnspan=3, sticky="W")
        tk.Label(processes_frame, text=f"{proc[1]} %", font=("Arial", 14), bg="lightgray").grid(row=i, column=5, columnspan=3, sticky="E")
        tk.Label(processes_frame, text=f"{proc[2]} MB", font=("Arial", 14), bg="lightgray").grid(row=i, column=8, columnspan=3, sticky="E")
        tk.Label(processes_frame, text=f"{proc[3]} MB", font=("Arial", 14), bg="lightgray").grid(row=i, column=11, columnspan=3, sticky="E", padx=(0, 10))
        i += 1


    root.after(1000, refresh)


root = tk.Tk()
root.title("QuantumForte")
window_width = 1380
window_height = 860
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)
root.iconbitmap("./assets/QFLogo.ico")


logo = tk.PhotoImage(file="./assets/QFLogo.png")
search_icon = tk.PhotoImage(file="./assets/Search.png")
sort_icon = tk.PhotoImage(file="./assets/sort.png")
letter_icon = tk.PhotoImage(file="./assets/letter.png")
cpu_icon = tk.PhotoImage(file="./assets/CPU.png")
ram_icon = tk.PhotoImage(file="./assets/RAM.png")
ssd_icon = tk.PhotoImage(file="./assets/SSD.png")
numer_icon = tk.PhotoImage(file="./assets/hashtag.png")
process_icon = tk.PhotoImage(file="./assets/process_name.png")


top_bar = tk.Frame(root, bg="lightgray", height=120, relief="solid", bd=2)
top_bar.pack(side="top", fill="x", padx=10, pady=(10, 0))
top_bar.pack_propagate(False)

main_content = tk.Frame(root)
main_content.pack(side="top", fill="both", expand=True)

sidebar = tk.Frame(main_content, bg="lightgray", relief="solid", bd=2)
sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)

content_center = tk.Frame(main_content, bg="lightgray", relief="solid", bd=2)
content_center.pack(side="left", fill="y", padx=(10, 0), pady=10)

content_right = tk.Frame(main_content, bg="lightgray", width=420, relief="solid", bd=2)
content_right.pack(side="left", fill="both", padx=10, pady=10)
content_right.pack_propagate(False)

logo_label = tk.Label(top_bar, image=logo, bg="lightgray")
logo_label.pack(side="left", padx=10, pady=10)

title_label = tk.Label(top_bar, text="QuantumForte", font=("Impact", 60), bg="lightgray")
title_label.pack(side="left", padx=(10, 0))


sort_label = tk.Label(sidebar, image=sort_icon)
sort_label.pack(side="top", padx=10, pady=(10,0))

sort_line = tk.Frame(sidebar, bg="#000000", height=2)
sort_line.pack(side="top", fill="x", pady=(10, 0))

letter_button = tk.Button(sidebar, image=letter_icon)
letter_button.pack(side="top", padx=10, pady=(10,0))

cpu_button = tk.Button(sidebar, image=cpu_icon)
cpu_button.pack(side="top", padx=10, pady=(10,0))

ram_button = tk.Button(sidebar, image=ram_icon)
ram_button.pack(side="top", padx=10, pady=(10,0))

ssd_button = tk.Button(sidebar, image=ssd_icon)
ssd_button.pack(side="top", padx=10, pady=(10,0))


header_frame = tk.Frame(content_center, bg="lightgray")
header_frame.pack(side="top", fill="x")

for i in range(14):
    header_frame.columnconfigure(i, minsize=60)

tk.Label(header_frame, image=numer_icon, text="Nr. ", compound="right", font=("Arial", 16, "bold"), bg="lightgray").grid(row=0, column=0, columnspan=2, sticky="W", padx=(10, 0), pady=10)
tk.Label(header_frame, image=process_icon, text="Prozess ", compound="right", font=("Arial", 16, "bold"), bg="lightgray").grid(row=0, column=2, columnspan=3, sticky="W", pady=10)
tk.Label(header_frame, image=cpu_icon, text="CPU ", compound="right", font=("Arial", 16, "bold"), bg="lightgray").grid(row=0, column=5, columnspan=3, sticky="E", pady=10)
tk.Label(header_frame, image=ram_icon, text="RAM ", compound="right", font=("Arial", 16, "bold"), bg="lightgray").grid(row=0, column=8, columnspan=3, sticky="E", pady=10)
tk.Label(header_frame, image=ssd_icon, text="SSD ", compound="right", font=("Arial", 16, "bold"), bg="lightgray").grid(row=0, column=11, columnspan=3, sticky="E", padx=(0, 10), pady=10)

stats_line = tk.Frame(content_center, bg="#000000", height=2)
stats_line.pack(side="top", fill="x")


summary_frame = tk.Frame(content_center, bg="lightgray")
summary_frame.pack(side="top", fill="x")

for i in range(14):
    summary_frame.columnconfigure(i, minsize=60)

stats_line2 = tk.Frame(content_center, bg="#000000", height=2)
stats_line2.pack(side="top", fill="x", pady=(0, 10))


processes_frame = tk.Frame(content_center, bg="lightgray")
processes_frame.pack(side="top", fill="x")

for i in range(14):
    processes_frame.columnconfigure(i, minsize=60)


cpu_frame = tk.Frame(content_right, bg="lightgray", relief="solid", bd=2)
cpu_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=(10,0))

cpu_titel_label = tk.Label(cpu_frame, image=cpu_icon, text="Prozessor ", compound="right", font=("Arial", 16, "bold"), bg="lightgray")
cpu_titel_label.pack(side="top", anchor="nw", padx=10, pady=10)

right_line = tk.Frame(cpu_frame, bg="#000000", height=2)
right_line.pack(side="top", fill="x")

processes_count = len(psutil.pids())
cpu_frequency = round(psutil.cpu_freq().current / 1000, 2)
real_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)

cpu_props_total = tk.Label(cpu_frame, text=f"Auslastung: {total_processes[0]} %", font=("Arial", 14), bg="lightgray")
cpu_props_total.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

cpu_props_count = tk.Label(cpu_frame, text=f"Anzahl Prozesse: {processes_count}", font=("Arial", 14), bg="lightgray")
cpu_props_count.pack(side="top", anchor="nw", padx=10)

cpu_props_freq = tk.Label(cpu_frame, text=f"Frequenz: {cpu_frequency} GHz", font=("Arial", 14), bg="lightgray")
cpu_props_freq.pack(side="top", anchor="nw", padx=10)

cpu_props_real = tk.Label(cpu_frame, text=f"Echte Kerne: {real_cores}", font=("Arial", 14), bg="lightgray")
cpu_props_real.pack(side="top", anchor="nw", padx=10)

cpu_props_log = tk.Label(cpu_frame, text=f"Logische Kerne: {logical_cores}", font=("Arial", 14), bg="lightgray")
cpu_props_log.pack(side="top", anchor="nw", padx=10, pady=(0, 10))


ram_frame = tk.Frame(content_right, bg="lightgray", width=480, relief="solid", bd=2)
ram_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=(10,0))

ram_titel_label = tk.Label(ram_frame, image=ram_icon, text="Arbeitsspeicher ", compound="right", font=("Arial", 16, "bold"), bg="lightgray")
ram_titel_label.pack(side="top", anchor="nw", padx=10, pady=10)

right_line = tk.Frame(ram_frame, bg="#000000", height=2)
right_line.pack(side="top", fill="x")

ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
ram_usage_percent = psutil.virtual_memory().percent
ram_available_mb = round(psutil.virtual_memory().available / (1024**3), 1)

ram_props_total = tk.Label(ram_frame, text=f"Total Arbeitsspeicher: {ram_gb} GB", font=("Arial", 14), bg="lightgray")
ram_props_total.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

ram_props_usage = tk.Label(ram_frame, text=f"In Verwendung (GB): {total_processes[1]} GB", font=("Arial", 14), bg="lightgray")
ram_props_usage.pack(side="top", anchor="nw", padx=10)

ram_props_freq = tk.Label(ram_frame, text=f"In Verwendung (%): {ram_usage_percent} %", font=("Arial", 14), bg="lightgray")
ram_props_freq.pack(side="top", anchor="nw", padx=10)

ram_props_free = tk.Label(ram_frame, text=f"Zur Verfügung: {ram_available_mb} GB", font=("Arial", 14), bg="lightgray")
ram_props_free.pack(side="top", anchor="nw", padx=10)

ram_props_placeholer = tk.Label(ram_frame, text="", font=("Arial", 14), bg="lightgray")
ram_props_placeholer.pack(side="top", anchor="nw", padx=10, pady=(0, 10))


ssd_frame = tk.Frame(content_right, bg="lightgray", relief="solid", bd=2)
ssd_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=(10,0))

ssd_titel_label = tk.Label(ssd_frame, image=ssd_icon, text="Festplatte ", compound="right", font=("Arial", 16, "bold"), bg="lightgray")
ssd_titel_label.pack(side="top", anchor="nw", padx=10, pady=10)

right_line = tk.Frame(ssd_frame, bg="#000000", height=2)
right_line.pack(side="top", fill="x")

ssd_total_gb = round(psutil.disk_usage('C:\\').total / (1024**4), 1)
ssd_used_gb = round(psutil.disk_usage('C:\\').used / (1024**4), 1)
io = psutil.disk_io_counters()
ssd_read = round(io.read_bytes / (1024**3), 2)
ssd_write = round(io.write_bytes / (1024**3), 2)

ssd_props_all = tk.Label(ssd_frame, text=f"Total R/W (seit Boot): {total_processes[2]} GB", font=("Arial", 14), bg="lightgray")
ssd_props_all.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

ssd_props_read = tk.Label(ssd_frame, text=f"Gelesen (seit Boot): {ssd_read} GB", font=("Arial", 14), bg="lightgray")
ssd_props_read.pack(side="top", anchor="nw", padx=10)

ssd_props_write = tk.Label(ssd_frame, text=f"Geschrieben (seit Boot): {ssd_write} GB", font=("Arial", 14), bg="lightgray")
ssd_props_write.pack(side="top", anchor="nw", padx=10)

ssd_props_total = tk.Label(ssd_frame, text=f"Grösse: {ssd_total_gb} TB", font=("Arial", 14), bg="lightgray")
ssd_props_total.pack(side="top", anchor="nw", padx=10)

ssd_props_used = tk.Label(ssd_frame, text=f"Belegt: {ssd_used_gb} TB", font=("Arial", 14), bg="lightgray")
ssd_props_used.pack(side="top", anchor="nw", padx=10, pady=(0, 10))


refresh()
root.mainloop()


"""
search_frame = tk.Frame(top_bar, bg="lightgray")
search_frame.pack(side="right", anchor="n", padx=10, pady=10)

search_entry = tk.Entry(search_frame, font=("Arial", 16), bg="white")
search_entry.pack(side="right")

search_label = tk.Label(search_frame, image=search_icon, text="Suche:", compound="left", font=("Arial", 16, "bold"), bg="lightgray")
search_label.pack(side="right", padx=(0, 5))
"""
