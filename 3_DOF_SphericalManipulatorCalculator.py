import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code

sg.theme('DarkBlack')

# Excel Read Code

EXCEL_FILE = 'Spherical Manipulator RRP Calculator Design Data.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

layout = [
    [sg.Push(), sg.Text('Spherical RRP MEXE CALCULATOR', font = ("Lucida Sans Unicode", 15)), sg.Push()],
    [sg.Text('Forward Kinematics Calculator', font = ("Lucida Sans", 12))],
    [sg.Text('Fill out the following fields:', font = ("Lucida Sans", 10)),
    sg.Push(), sg.Button('Start the Calculation', font = ("Lucida Sans Unicode", 15), size=(36,0), button_color=('white', 'gray')), sg.Push()],
    
    [sg.Text('a1 =', font = ("Lucida Sans", 10)),sg.InputText('0', key='a1', size=(20,10)),
    sg.Text('T1 =', font = ("Lucida Sans", 10)),sg.InputText('0', key='T1', size=(20,10)), sg.Push(),
    sg.Push(), sg.Button('Jacobian Matrix (J)', bind_return_key=True,disabled=True, font = ("Lucida Sans Unicode", 12), size=(15,0), button_color=('black', 'lightgray')),
    sg.Button('Det(J)', bind_return_key=True,disabled=True, font = ("Lucida Sans Unicode", 12), size=(14,0), button_color=('black', 'lightgray')),
    sg.Button('Inverse of J', bind_return_key=True,disabled=True, font = ("Lucida Sans Unicode", 12), size=(15,0), button_color=('black', 'lightgray')),
    sg.Button('Transpose of J', bind_return_key=True,disabled=True, font = ("Lucida Sans Unicode", 12), size=(15,0), button_color=('black', 'lightgray')), sg.Push()],

    [sg.Text('a2 =', font = ("Lucida Sans", 10)),sg.InputText('0', key='a2', size=(20,10)),
    sg.Text('T2 =', font = ("Lucida Sans", 10)),sg.InputText('0', key='T2', size=(20,10))],

    [sg.Text('a3 =', font = ("Lucida Sans", 10)),sg.InputText('0', key='a3', size=(20,10)),
    sg.Text('d3 =', font = ("Lucida Sans", 10)),sg.InputText('0', key='d3', size=(20,10)),
    sg.Push(), sg.Button('Inverse Kinematics', bind_return_key=True,disabled=True, font = ("Lucida Sans Unicode", 12), size=(35,0), button_color=('lightgray', 'gray')), sg.Push()],

    [sg.Button('Solve Forward Kinematics', bind_return_key=True,disabled=True, tooltip='Go to "Start the Calculation"!', font = ("Lucida Sans Unicode", 12), button_color=('black', 'white')), sg.Push(),
    sg.Push(), sg.Button('Path and Trajectory Planning', bind_return_key=True,disabled=True, font = ("Lucida Sans Unicode", 12), size=(40, 0), button_color=('lightgray', 'gray')), sg.Push()],
    
    [sg.Frame('Position Vector: ',[[
        sg.Text('X =', font = ("Lucida Sans", 10)),sg.InputText('0', key='X', size=(10,1)),
        sg.Text('Y =', font = ("Lucida Sans", 10)),sg.InputText('0', key='Y', size=(10,1)),
        sg.Text('Z =', font = ("Lucida Sans", 10)),sg.InputText('0', key='Z', size=(10,1))]])],

    [sg.Push(), sg.Frame('H0_3 Transformation Matrix = ', [[sg.Output(size=(60,12), key = '_output_')]]),
    sg.Push(), sg.Image('SphericalM1.gif', key='_IMAGE_'), sg.Push()],
    [sg.Submit(font = ("Lucida Sans", 10)), sg.Button('Reset', font = ("Lucida Sans", 10)), sg.Exit(font = ("Lucida Sans", 10))]]

window = sg.Window('Spherical-RRP Manipulator Forward Kinematics', layout, resizable=True)

# Variable Codes for disabling buttons

disable_FK = window['Solve Forward Kinematics']
disable_J = window['Jacobian Matrix (J)']
disable_D = window['Det(J)']
disable_IV = window['Inverse of J']
disable_TJ = window['Transpose of J']
disable_IK = window['Inverse Kinematics']
disable_PT = window['Path and Trajectory Planning']

while True:
    event,values = window.read(200)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    window.Element('_IMAGE_').UpdateAnimation('SphericalM1.gif',  time_between_frames=50)

    if event == 'Reset' :

        window['a1'].update(0)
        window['a2'].update(0)
        window['a3'].update(0)
        window['T1'].update(0)
        window['T2'].update(0)
        window['d3'].update(0)
        window['X'].update(0)
        window['Y'].update(0)
        window['Z'].update(0)

        disable_FK.update(disabled=True)
        disable_J.update(disabled=True)
        disable_D.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)
        disable_IK.update(disabled=True)
        disable_PT.update(disabled=True)

        window['_output_'].update('')

    if event == 'Start the Calculation' :
        disable_FK.update(disabled=False)

    if event == 'Solve Forward Kinematics' :
        
        # Forward Kinematic Codes
      
        # link lengths in cm
        a1 = float(values['a1'])
        a2 = float(values['a2'])
        a3 = float(values['a3'])

        # Joint Variable (Thetas in degrees & dinstance in cm)
        T1 = float(values['T1'])
        T2 = float(values['T2'])
        d3 = float(values['d3'])

        T1 = (T1/180.0)*np.pi  # Theta 1 in radian
        T2 = (T2/180.0)*np.pi  # Theta 2 in radian

        DHPT = [
            [T1,(90.0/180.0)*np.pi, 0, a1],
            [T2+(90.0/180.0)*np.pi, (90.0/180.0)*np.pi, a2, 0],
            [0, 0, 0, a3+d3],
            ]

        # D-H Notation Formula for HTM
        i = 0
        H0_1 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1],
            ]

        i = 1
        H1_2 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1],
            ]

        i = 2
        H2_3 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1],
            ]

        # Transformation Matrices from base to end-effector
        #print("HO_1 = ")
        #print(np.matrix(H0_1))
        #print("H1_2 = ")
        #print(np.matrix(H1_2))
        #print("H2_3 = ")
        #print(np.matrix(H2_3))

        # Dot Product of H0_3 = HO_1*H1_2*H2_3
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        # Transformation Matrix of the Manipulator
        print("H0_3 = ")
        print(np.matrix(H0_3))

        # Position Vector X Y Z

        X0_3 = H0_3[0,3]
        print("X = ", X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ", Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ", Z0_3)
        
        # Disabler program 
        disable_J.update(disabled=False)
        disable_IK.update(disabled=False)
        disable_PT.update(disabled=False)
        disable_D.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)

        # XYZ OUTPUT TO INPUT UPDATER
        window['X'].update(X0_3)
        window['Y'].update(Y0_3)
        window['Z'].update(Z0_3)

    if event == 'Jacobian Matrix (J)' :
        
        # Defining the equations

        IM = [[1,0,0],[0,1,0],[0,0,1]]
        i = [[0],[0],[1]]
        d0_3 = H0_3[0:3,3:]

        # Row 1 - 3 column 1
        J1a = (np.dot(IM,i))

        # Cross product of Row 1 - 3 column 1

        J1 = [
            [(J1a[1,0]*d0_3[2,0])-(J1a[2,0]*d0_3[1,0])],
            [(J1a[2,0]*d0_3[0,0])-(J1a[0,0]*d0_3[2,0])],
            [(J1a[0,0]*d0_3[1,0])-(J1a[1,0]*d0_3[0,0])]
            ]

        # Row 1 - 3 column 2
        R0_1a = np.dot(H0_1,1)
        R0_1b = R0_1a[0:3, 0:3]
        d0_1 = R0_1a[0:3,3:]
        J2a = (np.dot(R0_1b,i))
        J2b = (np.subtract(d0_3,d0_1))

        # Cross product of Row 1 - 3 column 2

        J2 = [
            [(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
            [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
            [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]
            ]

        # Row 1 - 3 column 3
        R0_2 = H0_2[0:3,0:3]
        J3 = (np.dot(R0_2,i))
        J3a = [[0], [0], [0]]

        # Jacobian Matrix
        JM1 = np.concatenate((J1, J2, J3), 1)
        JM2 = np.concatenate((J1a, J2a, J3a), 1)
        Jacobian = np.concatenate((JM1, JM2), 0)
        sg.popup('J =', Jacobian)

        # Disabler program 
        disable_J.update(disabled=True)
        disable_D.update(disabled=False)
        disable_IV.update(disabled=False)
        disable_TJ.update(disabled=False)

    if event == 'Det(J)' :
        DJ = np.linalg.det(JM1)
        #print("D(J) = ", DJ)
        sg.popup('D(J) = ', "%.4f" % DJ)

        if DJ == -0.0E-20 <= 0 <= 0.0E-20 :
            disable_IV.update(disabled=True)
            sg.popup('Warning: This is Non-Invertible')
    
    if event == 'Inverse of J' :
        IJ = np.linalg.inv(JM1)
        sg.popup('I(J) = ', IJ)

    if event == 'Transpose of J' :
        TJ = np.transpose(JM1)
        sg.popup('T(J) = ', TJ)

    if event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data Saved!')

window.close()