import tkinter as tk
from tkinter import ttk
import psutil

root = tk.Tk()
root.title("QuantumForte")
window_width = 1260
window_height = 720
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
top_bar.pack_propagate(False)

sidebar = tk.Frame(main_content, bg="lightgray", width=60, relief="solid", bd=2)
sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)
top_bar.pack_propagate(False)

content_center = tk.Frame(main_content, bg="white", width=720, relief="solid", bd=2)
content_center.pack(side="left", fill="y", padx=(10, 0), pady=10)
top_bar.pack_propagate(False)

content_right = tk.Frame(main_content, bg="navy", width=480)
content_right.pack(side="left", fill="y")
top_bar.pack_propagate(False)


logo_label = tk.Label(top_bar, image=logo, bg="lightgray")
logo_label.pack(side="left", padx=10, pady=10)

title_label = tk.Label(top_bar, text="QuantumForte", font=("Impact", 60), bg="lightgray")
title_label.pack(side="left", padx=(10, 0))

search_frame = tk.Frame(top_bar, bg="lightgray")
search_frame.pack(side="right", anchor="n", padx=10, pady=10)

search_entry = tk.Entry(search_frame, font=("Arial", 15), bg="white")
search_entry.pack(side="right")

search_label = tk.Label(search_frame, image=search_icon, text="Suche:", compound="left", font=("Arial", 15, "bold"), bg="lightgray")
search_label.pack(side="right", padx=(0, 5))


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

for i in range(10):
    header_frame.columnconfigure(i, minsize=60)

tk.Label(header_frame, image=numer_icon, text="Nr.", compound="right", font=("Arial", 15, "bold"), bg="lightgray").grid(row=0, column=0, sticky="W")
tk.Label(header_frame, image=process_icon, text="Prozess", compound="right", font=("Arial", 15, "bold"), bg="lightgray").grid(row=0, column=1, columnspan=3, sticky="W")
tk.Label(header_frame, image=cpu_icon, text="CPU", compound="right", font=("Arial", 15, "bold"), bg="lightgray").grid(row=0, column=4, columnspan=2, sticky="E")
tk.Label(header_frame, image=ram_icon, text="RAM", compound="right", font=("Arial", 15, "bold"), bg="lightgray").grid(row=0, column=6, columnspan=2, sticky="E")
tk.Label(header_frame, image=ssd_icon, text="SSD", compound="right", font=("Arial", 15, "bold"), bg="lightgray").grid(row=0, column=8, columnspan=2, sticky="E")

stats_line = tk.Frame(content_center, bg="#000000", height=2)
stats_line.pack(side="top", fill="x")


summary_frame = tk.Frame(content_center, bg="lightgray")
summary_frame.pack(side="top", fill="x")

for i in range(10):
    summary_frame.columnconfigure(i, minsize=60)

tk.Label(summary_frame, text="Total", font=("Arial", 15), bg="lightgray").grid(row=0, column=1, columnspan=3, sticky="W")
tk.Label(summary_frame, text="0 %", font=("Arial", 15), bg="lightgray").grid(row=0, column=4, columnspan=2, sticky="E")
tk.Label(summary_frame, text="0 MB", font=("Arial", 15), bg="lightgray").grid(row=0, column=6, columnspan=2, sticky="E")
tk.Label(summary_frame, text="0 MB", font=("Arial", 15), bg="lightgray").grid(row=0, column=8, columnspan=2, sticky="E")

tk.Frame(content_center, bg="#000000", height=2).pack(side="top", fill="x")


root.mainloop()
