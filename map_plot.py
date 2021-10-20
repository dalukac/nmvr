from os import remove
from tkinter import YView
import matplotlib, time, threading
import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy.core.defchararray import split
from numpy.core.fromnumeric import size
from numpy.lib.npyio import genfromtxt
import pandas as pd
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors
plt.style.use('Solarize_Light2')

#cell definition and color assign
EMPTY_CELL = 0
OBSTACLE_CELL = 1
ROBOT_CELL = 2
GOAL_CELL = 3 
cmap= colors.ListedColormap(['purple','yellow','green','cyan'])
bounds = [EMPTY_CELL,OBSTACLE_CELL,ROBOT_CELL,GOAL_CELL]
norm = colors.BoundaryNorm(bounds,cmap.N)



file = "map.csv"
data = genfromtxt("map.csv", delimiter=",")
matplotlib.use("TkAgg")

def find_robot():
    result = np.where(data == 2)
    x=result[0]
    y=result[1]
    return [x,y]

def clearMap():
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 2:
                data[i][j]=0

def createObstacle(X,Y):
    valueX = int(X)
    valueY = int(Y)
    if data[valueX,valueY] == 2:
        data[X,Y] = 2
        print("cell occupied")
    else: 
        data[valueX,valueY] = 1
        print("obstacle created at: ", valueX,valueY)

def removeObstacle(X,Y):
    valueX = int(X)
    valueY = int(Y)
    if data[valueX,valueY] == 2:
        data[X,Y] = 2
        print("cell occupied")
    else: 
        data[valueX,valueY] = 0
        print("obstacle removed at: ", valueX,valueY)

def changeRobotPos(X,Y):
    lastX = find_robot()[0]
    lastY = find_robot()[1]
    clearMap()
    valueX = int(X)
    valueY = int(Y)
    if data[valueX,valueY] == 1:
        data[lastX,lastY] = 2
        print("cell occupied")
    else: 
        data[valueX,valueY] = 2
        print("robot moved to pos: ", valueX,valueY)
    
def fig_maker(data):
    fig, ax = plt.subplots()
    ax.imshow(data,cmap=cmap,norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth='1')
    ax.set_xticks(np.arange(0.5,30,1))
    ax.set_yticks(np.arange(0.5,30,1))
    plt.tick_params(axis='both',which='both',bottom='False',left='False',labelbottom='False',labelleft='False', labelsize=0, length = 0)
    fig.patch.set_facecolor('black')
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
    [sg.Button('spawn robot',size=(10,1)),sg.Button('Create',size=(10,1)),sg.Button('Remove',size=(10,1))],
    [sg.Text('X pos:'), sg.Input(key='XINPUT',size=(10,1)), sg.Text('Y pos:'),sg.Input(key='YINPUT',size=(10,1))],
    [sg.Button('U',size=(5,1)), sg.Button('D',size=(5,1)), sg.Button('L',size=(5,1)),sg.Button('R',size=(5,1))],
    [sg.Canvas(key='test_env')]
   
    ]


window = sg.Window(
    'matplotlib Test',
    layout,
    resizable = True,
    size=(800,600),
    auto_size_buttons=False,
    location=(100,100),
    finalize=True,
    element_justification='center',
    font="Verdana 18",
)

fig_agg = None
if fig_agg is not None:
            delete_fig_agg(fig_agg)
fig = fig_maker(data)
fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == 'spawn robot':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        if Xvalue == "" or Yvalue =="":
            Xvalue = 1
            Yvalue = 1
        else:
            Xvalue = values['XINPUT']
            Yvalue = values['YINPUT']

        changeRobotPos(Xvalue,Yvalue)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'U':
        changeRobotPos(find_robot()[0]-1,find_robot()[1])
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'D':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        changeRobotPos(find_robot()[0]+1,find_robot()[1])
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'L':
        changeRobotPos(find_robot()[0],find_robot()[1]-1)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'R':
        changeRobotPos(find_robot()[0],find_robot()[1]+1)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'Create':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        createObstacle(Xvalue,Yvalue)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'Remove':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        removeObstacle(Xvalue,Yvalue)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

window.close()

