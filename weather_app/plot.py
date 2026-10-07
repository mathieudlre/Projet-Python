from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Plot Matplotlib
# ----------------------------------------------------------------------

def create_plot(dates, temperatures_min, temperatures_max):
    """Crée et retourne une Figure Matplotlib avec les courbes de températures min et max sur les dates fournies."""
    figure = Figure(figsize = (3.8, 3.2))
    axes = figure.add_subplot(111)

    ######################################

    # TODO
    # axes.plot(...)
    #courbe max
    axes.plot(temperatures_max, color="red", marker="o")
    #courbe min
    axes.plot(temperatures_min,color='blue', marker="o")



    ######################################

    # Améliore la lisibilité
    axes.set_xticks(range(len(dates)))
    axes.set_xticklabels([d[5:] for d in dates], rotation = 45)
    figure.tight_layout()

    return figure

