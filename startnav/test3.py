import time
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.npyio import genfromtxt
from math import cos, pi, pow, atan2, sqrt, dist, sin, floor
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors
from scipy.spatial.distance import cityblock

from rclpy import get_global_executor
#plt.style.use('Solarize_Light2')
# 

r_theta = 0

#cell definition and color assign
cmap= colors.ListedColormap(['white','gray','red','green','teal'])
bounds = [-0.5,0.5,1.5,2.5,3.5,4.5]
norm = colors.BoundaryNorm(bounds,cmap.N)

#load map
file = "map2.csv"
data = genfromtxt("/home/nmvr/dev_ws/src/startnav/startnav/map2.csv", delimiter=",")
matplotlib.use("TkAgg")

#create/destroy robot/goal/obstacles
#=========================================

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
            elif data[i][j] == 3:
                data[i][j]=3

def wipeMap():
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 2 or data[i][j] == 4 or data[i][j] == 3:
                data[i][j]=0


def changeRobotPos(X,Y):
    lastX = find_robot()[0]
    lastY = find_robot()[1]
    clearMap()
    valueX = int(X)
    valueY = int(Y)
    text = valueX,valueY
    window['-R-'].Update(text)
    if data[valueX,valueY] == 1:
        data[lastX,lastY] = 2
        print("cell occupied")
    else: 
        data[valueX,valueY] = 2
        data[lastX,lastY] = 4
        print("robot moved to pos: ", valueX,valueY)
    
    
def setGoal(X,Y):
    lastX = find_robot()[0]
    lastY = find_robot()[1]
    valueX = int(X)
    valueY = int(Y)
    if data[valueX,valueY] == 2:
        data[lastX,lastY] = 2
        print("cannot set goal, robot already here")
    elif data[valueX,valueY] == 1:
        data[valueX,valueY]== 1
        print("can't place goal on obstacle")
    else: 
        data[valueX,valueY] = 3
        print("goal set to: ", valueX,valueY)
        cityblock_dist()
        linear_vel()
        steering_angle()

def removeGoal():
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 3:
                data[i][j]=0

def find_goal():
    result = np.where(data == 3)
    x=result[0]
    y=result[1]
    return [x,y]

#variables for G2G and odometry
#==================================

def cityblock_dist():
    city = cityblock( [find_goal()[0], find_goal()[1]], [find_robot()[0], find_robot()[1]])
    text = city
    window['-G-'].Update(text)
    return city


def linear_vel(constant=1.5):
    velocity = constant * cityblock_dist()
    text = velocity
    window['-V-'].Update(text)
    return velocity

def steering_angle():
    ang =  atan2(find_goal()[1] - find_robot()[1], find_goal()[0] - find_robot()[0])
    angle = round((ang * 180))/pi
    if angle<0:
        angle +=360
    window['-A-'].Update(angle)
    return angle

def angular_velocity(constant=6):
    a_vel = constant * (steering_angle() - r_theta)
    return a_vel

# Pangle to movement
# ================================= 

def steerAng():
    steerX, steerY = 0, 0
    angle_to_check = steering_angle()
    if angle_to_check > 202.5 and angle_to_check <247.5 or angle_to_check == 225:
        steerX = -1
        steerY = -1
    elif angle_to_check < 337.5 and angle_to_check > 292.5 or angle_to_check == 315:
        steerX = 1
        steerY = -1
    elif angle_to_check >112.5 and angle_to_check <157.5 or angle_to_check == 135:
        steerX = -1
        steerY = 1
    elif angle_to_check < 67.5 and angle_to_check > 22.5 or angle_to_check == 45: 
        steerX = 1
        steerY = 1
    elif angle_to_check > 157.5 and angle_to_check < 202.5: 
        steerX = -1
        steerY = 0
    elif angle_to_check <22.5 and angle_to_check >0: #or angle_to_check<=360 and angle_to_check>337.5:
        steerX = 1
        steerY = 0
    elif angle_to_check < 360 and angle_to_check >337: #or angle_to_check<=360 and angle_to_check>337.5:
        steerX = 1
        steerY = 0
    elif angle_to_check <292.5 and angle_to_check>247.5:
        steerX = 0
        steerY = -1
    elif angle_to_check > 67.5 and angle_to_check < 112.5 :
        steerX = 0
        steerY = 1
    return steerX, steerY

#calculate odometry
#==========================

def odometry():
    global r_theta

    sample = 0.1                           
    wheels = 0.05                        

    l_vel = linear_vel()
    a_vel = angular_velocity()

    dr = (l_vel + (0.5 * wheels * a_vel)) * sample
    dl = (l_vel - (0.5 * wheels * a_vel)) * sample

    fi = (dr - dl) / wheels
    d_center = (dl + dr) / 2
    r_theta = r_theta + fi

    new_r_pos_x = find_robot()[0] + (d_center*cos(r_theta))
    new_r_pos_y = find_robot()[1] + (d_center*sin(r_theta))

    window['-NX-'].Update(new_r_pos_x)
    window['-NY-'].Update(new_r_pos_y)
    window['-TH-'].Update(r_theta)


#func to plot map
#==========================
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

#helper func for pysimplegui to plot 
#=======================================
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both',expand=1)
    return figure_canvas_agg

#delete existing figure
#==========================
def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')


#gui layout
#==========================
sg.theme('black')


col1 = [[sg.Button('spawn robot',size=(10,1)),sg.Button('clear',size = (10,1)),sg.Button('G2G',size=(10,1))],
    [sg.Text('X pos:'), sg.Input(key='XINPUT',size=(10,1)), sg.Text('Y pos:'),sg.Input(key='YINPUT',size=(10,1))],
    [sg.Button('U',size=(5,1)), sg.Button('D',size=(5,1)), sg.Button('L',size=(5,1)),sg.Button('R',size=(5,1))],
    [sg.Button('Set goal',size = (10,1)), sg.Button('remove goal',size = (10,1))],
    [sg.Text("Robot Pos:", justification='c', font='Mambo 20'),sg.Text("X Y", justification='c', font='Mambo 20', key='-R-')],
    [sg.Text("Distance goal:", justification='c', font='Mambo 20'),sg.Text("dist", justification='c', font='Mambo 20', key='-G-')],
    [sg.Text("Velocity:", justification='c', font='Mambo 20'),sg.Text("vel", justification='c', font='Mambo 20', key='-V-')],
    [sg.Text("Angular Velocity:", justification='c', font='Mambo 20'),sg.Text("vel", justification='c', font='Mambo 20', key='-AV-')],
    [sg.Text("Steer Angle:", justification='c', font='Mambo 20'),sg.Text("ang", justification='c', font='Mambo 20', key='-A-')],
    [sg.Text("Steer x:", justification='c', font='Mambo 20'),sg.Text("Steer x", justification='c', font='Mambo 20', key='-SX-'),sg.Text("Steer y:", justification='c', font='Mambo 20'),sg.Text("Steer y", justification='c', font='Mambo 20', key='-SY-')],
    [sg.Text("Odometry", justification='c', font='Mambo 20')],
    [sg.Text("New X position:", justification='c', font='Mambo 20'),sg.Text("new X", justification='c', font='Mambo 20', key='-NX-')],
    [sg.Text("New Y position:", justification='c', font='Mambo 20'),sg.Text("new Y", justification='c', font='Mambo 20', key='-NY-')],
    [sg.Text("Theta:", justification='c', font='Mambo 20'),sg.Text("theta", justification='c', font='Mambo 20', key='-TH-')]]
col2 = [[sg.Canvas(key='test_env')] ]

layout = [
   [sg.Column(col1, element_justification = 'l'), sg.Column(col2, element_justification = 'c')]
]


window = sg.Window(
    'robot navigation',
    layout,
    resizable = True,
    size=(800,600),
    auto_size_buttons=False,
    location=(100,100),
    finalize=True,
    element_justification='center',
    font="Verdana 18",
)

#first time plot
#==========================
fig_agg = None
if fig_agg is not None:
            delete_fig_agg(fig_agg)
fig = fig_maker(data)
fig_agg = draw_figure(window['test_env'].TKCanvas,fig)


#event listener for gui
#==========================
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
        text = Xvalue,Yvalue
        window['-R-'].Update(text)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'Set goal':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        setGoal(Xvalue,Yvalue)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)
    
    if event == 'remove goal':
        removeGoal()
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'clear':
        wipeMap()
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'G2G':
        angular_velocity()

        while  find_goal()[0] != find_robot()[0] or find_goal()[1] != find_robot()[1]:
            goX, goY = steerAng()
            window['-SX-'].Update(goX)
            window['-SY-'].Update(goY)
            try:
                text = angular_velocity()
                odometry()
            except ValueError:
                break
            changeRobotPos(find_robot()[0]+ goX, find_robot()[1] + goY)
            
            window['-AV-'].Update(text)
            if fig_agg is not None:
                delete_fig_agg(fig_agg)
            fig = fig_maker(data)
            fig_agg = draw_figure(window['test_env'].TKCanvas,fig)


#Movement
#===============================

    if event == 'U':
        changeRobotPos(find_robot()[0]-1,find_robot()[1])    
        cityblock_dist()
        linear_vel()
        steerAng() 
        print(steering_angle())
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'D':
        Xvalue = values['XINPUT']
        Yvalue = values['YINPUT']
        changeRobotPos(find_robot()[0]+1,find_robot()[1])
        cityblock_dist()
        linear_vel()
        steerAng()
        print(steering_angle())
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'L':
        changeRobotPos(find_robot()[0],find_robot()[1]-1)
        cityblock_dist()
        linear_vel()
        steerAng()
        print(steering_angle())
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    if event == 'R':
        changeRobotPos(find_robot()[0],find_robot()[1]+1)
        cityblock_dist()
        linear_vel()
        steerAng()
        print(steering_angle())
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig = fig_maker(data)
        fig_agg = draw_figure(window['test_env'].TKCanvas,fig)

    

        

window.close()

