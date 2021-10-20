import matplotlib
import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy.lib.npyio import genfromtxt
import pandas as pd
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

_VARS = {'window': False,'fig_agg': False,'pltFig':False}

plt.style.use('Solarize_Light2')

file = "map.csv"
data = genfromtxt("map.csv", delimiter=",")
matplotlib.use("TkAgg")

fig, ax = plt.subplots()
ax.imshow(data)
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth='1')
ax.set_xticks(np.arange(0.5,30,1))
ax.set_yticks(np.arange(0.5,30,1))
plt.tick_params(axis='both',which='both',bottom='False',left='False',labelbottom='False',labelleft='False', labelsize=0, length = 0)
fig.set_size_inches((8.5,11),forward='False')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both',expand=1)
    return figure_canvas_agg

sg.theme('black')

layout = [
    [sg.Text('robot_map')],
    [sg.Button('ok',size=(5,1))],
    [sg.Input(key='-INPUT-')],
    [sg.Canvas(key='test_env')]
   
    ]


window = sg.Window(
    'matplotlib Test',
    layout,
    resizable = True,
    size=(500,500),
    auto_size_buttons=False,
    location=(100,100),
    finalize=True,
    element_justification='center',
    font="Verdana 18",
)

draw_figure(window['test_env'].TKCanvas,fig)


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break


window.close()

