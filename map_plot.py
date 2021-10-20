import matplotlib
import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy.lib.npyio import genfromtxt
import pandas as pd
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors

_VARS = {'window': False,'fig_agg':False,'pltFig':False}

EMPTY_CELL = 0
OBSTACLE_CELL = 1
ROBOT_CELL = 2
GOAL_CELL = 3 
cmap= colors.ListedColormap(['purple','yellow','green','cyan'])
bounds = [EMPTY_CELL,OBSTACLE_CELL,ROBOT_CELL,GOAL_CELL]
norm = colors.BoundaryNorm(bounds,cmap.N)

plt.style.use('Solarize_Light2')

file = "map.csv"
data = genfromtxt("map.csv", delimiter=",")
matplotlib.use("TkAgg")

def changeRobotPos(X,Y):
    valueX = int(X)
    valueY = int(Y)
    print(valueX,valueY)
    data[valueX,valueY] = 2
    
def fig_maker(data):
    fig, ax = plt.subplots()
    ax.imshow(data,cmap=cmap,norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth='1')
    ax.set_xticks(np.arange(0.5,30,1))
    ax.set_yticks(np.arange(0.5,30,1))
    plt.tick_params(axis='both',which='both',bottom='False',left='False',labelbottom='False',labelleft='False', labelsize=0, length = 0)
    fig.set_size_inches((8.5,11),forward='False')
    return fig

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both',expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')
    

sg.theme('black')

layout = [
    [sg.Text('robot_map')],
    [sg.Button('create robot',size=(10,1))],
    [sg.Input(key='XINPUT',size=(10,1))],[sg.Input(key='YINPUT',size=(10,1))],
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



fig_agg = None

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == 'create robot':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        changeRobotPos(Xvalue,Yvalue)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)
        window.refresh()


window.close()

