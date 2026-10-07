import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date

from constants import *
from weather import *
from weather_queries import *
from plot import *

# ----------------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------------
# Ville actuelle
city = "Paris"
# city = "Bordeaux"

# ImageTk : ces variables globales permettent d'éviter que le garbage collector ne les efface
image_background = None
weather_icon = None

# ----------------------------------------------------------------------
# Canvas
# ----------------------------------------------------------------------

def load_background(canvas):
    """Charge "assets/blue_sky.jpg", la redimensionne et la place sur le canvas."""
    global image_background
    image = Image.open("assets/blue_sky.jpg").convert("RGBA")
    image = image.resize((WIDTH, HEIGHT))
    image_background = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image_background, anchor="nw")


def erase_screen(canvas):
    """Supprime tout ce qui a le tag 'ecran'."""
    canvas.delete("ecran")


# ----------------------------------------------------------------------
# Ecrans
# ----------------------------------------------------------------------

def draw_welcome_screen(window, canvas):
    """Écran 1 : Icône de la météo, température actuelle, températures min et max du jour."""
    global weather_icon
    icon_path = "assets/icons/sunny.png"
    weather_icon = PhotoImage(file=icon_path)
    weather_icon = weather_icon.subsample(2, 2)
    erase_screen(canvas)
    temperature, code, t_min, t_max = 19.7, 0, 18.0, 27.4
s
    canvas.create_image(
        200,
        200,
        image=weather_icon,
        tags="ecran"
    )


    canvas.create_text(
        200, 300,
        text=f"{temperature} °C",
        font=("Helvetica", 30, "bold"),
        fill="white",
        tags="ecran"
    )

    canvas.create_text(
        250, 350,
        text=f"Max : {t_max} °C",
        font=("Arial", 11, "bold"),
        fill="white",
        tags="ecran"
    )

    canvas.create_text(
        150, 350,
        text=f"Min : {t_min} °C",
        font=("Arial", 11, "bold"),
        fill="white",
        tags="ecran"
    )

    # ...

def draw_forecast(window, canvas):
    """Écran 2 : graphique des températures sur 7 jours"""

    erase_screen(canvas)
    # start_day = ...
    dates, t_mins, t_maxs = [], [], [] # TODO

    button = tk.Button(window, text="Prévisions 7 jours", command=lambda: """à
    compléter ...""")
    canvas.create_window(x, y, window=button, tags="ecran")

    # ...

def choix_villes(choix):
    print(choix, CITIES[choix])

def villes(window, canvas):

    def on_city_change(nom):
        canvas.itemconfig("ville", text=nom + " ▾")
        print(nom, CITIES[nom])

    liste = tk.Menu(window, tearoff=0)
    for nom in CITIES:
        liste.add_command(label=nom, command=lambda n=nom: on_city_change(n))

    canvas.create_text(WIDTH // 2, 60, text="Bordeaux ▾",
                       font=("Helvetica", 24, "bold"), fill="white", tags="ville")

    def ouvrir(event):
        liste.tk_popup(event.x_root, event.y_root)

    canvas.tag_bind("ville", "<Button-1>", ouvrir)