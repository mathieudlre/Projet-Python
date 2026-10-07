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
# Écrans
# ----------------------------------------------------------------------

def draw_welcome_screen(window, canvas):
    """Écran 1 : Icône de la météo, température actuelle, températures min et max du jour."""
    global weather_icon
    icon_path = "assets/icons/sunny.png"
    weather_icon = PhotoImage(file=icon_path)
    weather_icon = weather_icon.subsample(2, 2)
    
    erase_screen(canvas)
    
    temperature, code, t_min, t_max = 19.7, 0, 18.0, 27.4

    canvas.create_image(
        200, 200,
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

    button = tk.Button(
        window,
        text="Prévisions 7 jours",
        command=lambda: draw_forecast(window, canvas)
    )

    canvas.create_window(
        200, 430,
        window=button,
        tags="ecran"
    )


def draw_forecast(window, canvas):
    """Écran 2 : graphique des températures sur 7 jours"""

    erase_screen(canvas)
    
    dates, t_mins, t_maxs = (
        ['2026-10-05', '2026-10-06', '2026-10-07', '2026-10-08', '2026-10-09', '2026-10-10', '2026-10-11'], 
        [18.5, 18.2, 18.0, 12.6, 9.0, 11.0, 13.3], 
        [27.0, 27.2, 21.5, 17.6, 19.0, 21.0, 20.0]
    )

    # Titre et période (avec le tag "ecran")
    canvas.create_text(
        WIDTH // 2, 35,
        text="Prévisions sur 7 jours ",
        font=("Helvetica", 16, "bold"), fill="white",
        tags="ecran"
    )
    canvas.create_text(
        WIDTH // 2, 60,
        text=f"Du {dates[0]} au {dates[-1]}",
        font=("Helvetica", 10), fill="white",
        tags="ecran"
    )

    # Graphique Matplotlib
    fig = create_plot(dates, t_mins, t_maxs)
    chart_canvas = FigureCanvasTkAgg(fig, master=window)
    chart_widget = chart_canvas.get_tk_widget()
    canvas.create_window(WIDTH // 2, 230, window=chart_widget, tags="ecran")

    # Navigation (Boutons bas)
    def aller_accueil():
        chart_widget.destroy()
        btn_accueil.destroy()
        btn_prev.destroy()
        btn_next.destroy()
        draw_welcome_screen(window, canvas)
        villes(window, canvas)

    btn_prev = tk.Button(window, text="◄", width=4)
    btn_accueil = tk.Button(window, text="Accueil", command=aller_accueil)
    btn_next = tk.Button(window, text="►", width=4)

    canvas.create_window(WIDTH // 2 - 80, 420, window=btn_prev, tags="ecran")
    canvas.create_window(WIDTH // 2, 420, window=btn_accueil, tags="ecran")
    canvas.create_window(WIDTH // 2 + 80, 420, window=btn_next, tags="ecran")


def villes(window, canvas):

    def on_city_change(nom):
        canvas.itemconfig("ville", text=nom + " ▾")
        print(nom, CITIES[nom])

    liste = tk.Menu(window, tearoff=0)
    for nom in CITIES:
        liste.add_command(label=nom, command=lambda n=nom: on_city_change(n))

    # Ajout des deux tags ("ecran" et "ville") pour qu'il soit effacé au changement d'écran
    canvas.create_text(
        WIDTH // 2, 60, 
        text="Bordeaux ▾",
        font=("Helvetica", 24, "bold"), 
        fill="white", 
        tags=("ecran", "ville")
    )

    def ouvrir(event):
        liste.tk_popup(event.x_root, event.y_root)

    canvas.tag_bind("ville", "<Button-1>", ouvrir)