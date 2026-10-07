import tkinter as tk
from constants import CITIES

window = tk.Tk()

city = tk.StringVar(value = ">")

def villes(choix):
    print(choix, CITIES[choix])

menu = tk.OptionMenu(window, city, *CITIES.keys(), command=villes)
menu.pack()

window.mainloop()