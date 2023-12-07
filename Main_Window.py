# This is a sample Python script.
from  tkinter import *
from tkinter.ttk import Progressbar, Treeview, Style, Scrollbar
from tkinter import messagebox, filedialog
from  PIL import  Image, ImageTk
from datetime import *
import  time
import os
import cv2
import hand as htm
import multiprocessing
import threading

from openpyxl import Workbook
import csv


import snap7
from snap7.types import*
from snap7.util import*

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

import sqlite3
#================================================================
#=======================INIT SNAP7===============================
#================================================================
IP = '192.168.3.5'
RACK = 0
SLOT = 1
freq_ref =0.0
freq_out =0.0
volt_out=0.0
temp_1=0.0
humi_1=0.0
plc = snap7.client.Client()
is_on = True
textstatus = "Disconnected"
glb_status_connect = False
plcStatus_get = False
value_bar =0

frequency_ref =0.0
frequency_out =0.0
voltage_out =0.0
tempurature_1 =0.0
humidity_1= 0.0

freqout_min=0.0
freqout_max=0.0
avg_frequency =0.0
volt_min=0.0
volt_max=0.0
avg_volt =0.0
temp_min=0.0
temp_max=0.0
avg_temp = 0.0
humi_min=0.0
humi_max=0.0
avg_humi =0.0


count = 0
tree_data= None
my_data =[]

imgtk = None
lbl_Image = None

btn_Status_Enable = False
cap = None
# ================================================================
#====================Read Memory functions =======================
# Function read PLC
def ReadMemory(plc, byte, bit, datatype):
      result = plc.read_area(Areas['MK'],0,byte, datatype)
      if datatype == S7WLBit:
            return get_bool(result,0,1)
      elif datatype == S7WLByte or datatype == S7WLWord:
            return get_int(result,0)
      elif datatype == S7WLReal:
            return get_real(result,0)
      elif datatype == S7WLDWord:
            return get_dword(result,0)
      else:
            return None

# Function write PLC
def WriteMemory(plc,byte, bit, datatype, value):
      result = plc.read_area(Areas['MK'],0,byte, datatype)
      if datatype == S7WLBit:
          set_bool(result,0,bit, value)
      elif datatype == S7WLByte or datatype == S7WLWord:
          set_int(result,0, value)
      elif datatype == S7WLReal:
          set_real(result,0, value)
      elif datatype == S7WLDWord:
          set_dword(result,0, value)
      plc.write_area(Areas['MK'],0,byte,result)

#===========================================================
#====================Class Dashboard========================
class Dashboard:      
    def __init__(self, window):
        self.window = window
        self.window.title('System Management Dashboard')
        self.window.geometry('1366x768')
        #self.window.state('zoomed')
        self.window.resizable(0,0)
        self.window.config(background='#eff5f6')
        # window Icon
        icon = PhotoImage(file='images\\pic-icon.png')
        self.window.iconphoto(True, icon)
        
        # ========================================================
        # ======================header========================
        # ========================================================
        self.header = Frame(self.window, bg='#009df4')
        self.header.place(x=300, y=0, width=1070, height=60)

        self.header_text = Label(self.window, text='ENERGY MONITORING', font=("", 18, "bold"), fg='#ff0000', bg='#009df4')
        self.header_text.place(x=700, y=15)

        # ========================================================
        # ======================sidebar========================
        # ========================================================
        self.sidebar = Frame(self.window, bg='#CCFFCC')
        self.sidebar.place(x=0, y=0, width=300, height=760)
        
        # ======TIMe AND DATE===========
        self.clock_Image = Image.open('images\\time.png')
        photo = ImageTk.PhotoImage(self.clock_Image)
        self.date_time_image = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.date_time_image.image = photo
        self.date_time_image.place(x=88, y=20)

        self.date_time = Label(self.window, bg='#CCFFCC')
        self.date_time.place(x=115, y=15)
        self.show_time()

        # Logo
        self.logoImage = Image.open('images\\hyy.png')
        photo = ImageTk.PhotoImage(self.logoImage)
        self.logo = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.logo.image = photo
        self.logo.place(x=70, y=80)

        # Name of brand person
        self.brandName = Label(self.sidebar, text='Trieu a Tai', bg='#CCFFCC', font=("", 15, "bold"))
        self.brandName.place(x=85, y=200)

        # Dashboard
        self.DashboardImage = Image.open('images\\dashboard-icon.png')
        photo = ImageTk.PhotoImage(self.DashboardImage)
        self.Dashboard = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.Dashboard.image = photo
        self.Dashboard.place(x=35, y=289)

        self.Dashboard_text = Button(self.sidebar, text='Dashboard', bg='#CCFFCC', font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#CCFFCC', command= self.Home_page)
        self.Dashboard_text.place(x=80, y=287)

        # Manage
        self.ManageImage = Image.open('images\\manage-icon.png')
        photo = ImageTk.PhotoImage(self.ManageImage)
        self.Manage = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.Manage.image = photo
        self.Manage.place(x=35, y=340)

        self.Manage_text = Button(self.sidebar, text='Manage', bg='#CCFFCC', font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#CCFFCC', command=self.Manage_page)
        self.Manage_text.place(x=80, y=345)

        # Settings
        self.settingsImage = Image.open('images\\settings-icon.png')
        photo = ImageTk.PhotoImage(self.settingsImage)
        self.settings = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.settings.image = photo
        self.settings.place(x=35, y=402)

        self.settings_text = Button(self.sidebar, text='Settings', bg='#CCFFCC', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#CCFFCC', command= self.Setting_page)
        self.settings_text.place(x=80, y=402)
        
        def Switch_Cam():
            global btn_Status_Enable
      
            if btn_Status_Enable :
                btn_Status_Enable = False
            else:
                btn_Status_Enable = True
        
        # Camera
        self.settingsImage = Image.open('images\\camera.png')
        photo = ImageTk.PhotoImage(self.settingsImage)
        self.settings = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.settings.image = photo
        self.settings.place(x=35, y=452)

        self.settings_text = Button(self.sidebar, text='Camera', bg='#CCFFCC', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#CCFFCC', command= self.Camera_page)
        self.settings_text.place(x=80, y=452)

        # Exit
        self.exitImage = Image.open('images\\exit-icon.png')
        photo = ImageTk.PhotoImage(self.exitImage)
        self.exit = Label(self.sidebar, image=photo, bg='#CCFFCC')
        self.exit.image = photo
        self.exit.place(x=25, y=502)

        self.exit_text = Button(self.sidebar, text='Exit', bg='#CCFFCC', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#CCFFCC', command= self.exit_app)
        self.exit_text.place(x=80, y=512)
        
        # Connect PLC
        self.plcConnect = Label(self.sidebar, text='PLC CONNECT', bg='#CCFFCC', font=("", 15, "bold"))
        self.plcConnect.place(x=25, y=560)
        #================================================================  
        def Switch():
            global is_on
      
            if is_on :
                self.sw_button.config(text = "DISCONNECT",bg ='#FF0000',fg='#FFFF00' )
                is_on = False
                if plcStatus_get:
                    self.textstatus = "Connected"
                    self.plcStatus.config(text = "Connected")
                else:
                    self.textstatus = "Disconnected"
                    self.plcStatus.config(text = "Disconnected")
            else:
                
                self.sw_button.config(text = "CONNECT" ,  bg ='#C0C0C0')
                is_on = True
                self.textstatus = "Disconnected"
                self.plcStatus.config(text = "Disconnected")
                self.totalPeople_text.config(text= frequency_ref)
                self.people_who_left.config(text = frequency_out)
                self.Earning_figure.config(text= voltage_out)
                
        self.sw_button = Button(self.sidebar, text= 'CONNECT',bd =0, width= 15, height= 2,command=Switch)
        self.sw_button.pack(pady = 5)
        self.sw_button.place(x=25, y=600)
        
        self.plcStatus = Label(self.sidebar, text=textstatus, bg='#CCFFCC', font=("", 15, "bold"))
        self.plcStatus.place(x=145, y=605)
              
        #================================================================
        self.bar = Progressbar(self.sidebar, orient= HORIZONTAL, length=250)
        self.bar.pack(pady = 10)
        self.bar.place(x=25, y= 650)

        # ========================================================
        # ======================body==============================
        # ========================================================
        self.heading = Label(self.window, text='Dashboard', font=("", 13, "bold"), fg='#0064d3', bg='#eff5f6')
        self.heading.place(x=325, y=70)
        
        #================================================================
        #=======================Frame Main===============================
        self.Camera_page()
        self.Manage_page()
        self.Setting_page()
        self.Home_page()
        self.Insert_Data()
        #================================================================
        self.ReadPLCData()
       
    # =================================================================
    def Home_page(self):
        self.mainFrame = Frame(self.window, bg='#808080')
        self.mainFrame.place(x=300, y= 60, width= 1070, height= 700)
        
        # =========Body Frame 1=====
        self.bodyFrame1 = Frame(self.mainFrame, bg='#ffffff')
        self.bodyFrame1.place(x=15, y=10, width=1040, height=350)
        
        self.graph_frame1 =Frame(self.bodyFrame1, bg = '#0000EE')
        self.graph_frame1.place(x=10, y=10, width = 500, height= 320)
        
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master= self.graph_frame1)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        
        def update_plot():
            data = random.randint(0, 100)  # Replace with your real-time data source
            ax.clear()
            ax.plot([1, 2, 3], [data, data + 10, data - 5])  # Example data
            ax.set_title("Real-Time Plot")
            canvas.draw()
            self.graph_frame1.after(1000, update_plot)  # Update every 1000 milliseconds (1 second)
            
        update_plot()

        # =========Body Frame 2=====
        self.bodyFrame2 = Frame(self.mainFrame, bg='#009aa5')
        self.bodyFrame2.place(x=15, y=390, width=310, height=220)
        
        # =========Body Frame 3=====
        self.bodyFrame3 = Frame(self.mainFrame, bg='#e21f26')
        self.bodyFrame3.place(x=380, y=390, width=310, height=220)
        
        # =========Body Frame 4=====
        self.bodyFrame4 = Frame(self.mainFrame, bg='#ffcb1f')
        self.bodyFrame4.place(x=745, y=390, width=310, height=220)
                
                # =========Body Frame 5=====
        self.bodyFrame5 = Frame(self.mainFrame, bg='#ffcb1f')
        self.bodyFrame5.place(x=600, y=80, width=410, height=220)  
        
        # Graph
        '''self.graphImage = Image.open('images\\graph.png')
        photo = ImageTk.PhotoImage(self.graphImage)
        self.graph = Label(self.bodyFrame1, image=photo, bg='#ffffff')
        self.graph.image = photo
        self.graph.place(x=40, y=70)'''
        
        # Tempurature and Humidity data
        self.EarningImage = Image.open('images\\thermometer_32.png')
        photo = ImageTk.PhotoImage(self.EarningImage)
        self.temp_humi = Label(self.bodyFrame5, image=photo, bg='#ffcb1f')
        self.temp_humi.image = photo
        self.temp_humi.place(x=260, y=5)

        self.temp1_text = Label(self.bodyFrame5, text='Tempurature and Humidity', bg='#ffcb1f', font=("", 13, "bold"))
        self.temp1_text.place(x=5, y=5)

        self.temp1_value1 = Label(self.bodyFrame5, text= tempurature_1, bg='#ffcb1f', fg='#0000FF', font=("", 45, "bold"))
        self.temp1_value1.place(x=100, y=50)
        self.temp1_unit = Label(self.bodyFrame5, text= "°C", bg='#ffcb1f', fg='#0000FF', font=("", 45, "bold"))
        self.temp1_unit.place(x=330, y=50)
        
        self.humi_value1 = Label(self.bodyFrame5, text= humidity_1, bg='#ffcb1f',fg='#0000FF', font=("", 45, "bold"))
        self.humi_value1.place(x=100, y=130)
        self.humi_unit = Label(self.bodyFrame5, text= "%", bg='#ffcb1f',fg='#0000FF', font=("", 45, "bold"))
        self.humi_unit.place(x=330, y=130)
        
         # Frequency reference
        #================================================================
        self.totalPeopleImage = Image.open('images\\frequency_64.png')
        photo = ImageTk.PhotoImage(self.totalPeopleImage)
        self.totalPeople = Label(self.bodyFrame2, image=photo, bg='#009aa5')
        self.totalPeople.image = photo
        self.totalPeople.place(x=230, y=5)

        self.totalPeople_text = Label(self.bodyFrame2, text= freq_ref, bg='#009aa5',fg='#0000FF' , font=("", 45, "bold"))
        self.totalPeople_text.place(x=60, y=100)

        self.total_people = Label(self.bodyFrame2, text='Frequency reference', bg='#009aa5' ,fg='#FFFFFF',  font=("", 13, "bold"))
        self.total_people.place(x=5, y=5)
        
        self.ref_hz_text = Label(self.bodyFrame2, text= "(Hz)",bg='#009aa5',fg='#0000FF' , font=("", 25, "bold"))
        self.ref_hz_text.place(x=220, y=115)

        # Frequency oputput
        self.people_who_leftImage = Image.open('images\\frequency_64.png')
        photo = ImageTk.PhotoImage(self.people_who_leftImage)
        self.people_who_left = Label(self.bodyFrame3, image=photo, bg='#e21f26')
        self.people_who_left.image = photo
        self.people_who_left.place(x=230, y=5)

        self.people_who_left_text = Label(self.bodyFrame3, text='Frequency Output', bg='#e21f26', fg='#FFFFFF', font=("", 13, "bold"))
        self.people_who_left_text.place(x=5, y=5)

        self.people_who_left = Label(self.bodyFrame3, text=freq_out, bg='#e21f26',fg='#0000FF', font=("", 45, "bold"))
        self.people_who_left.place(x=60, y=100)
        
        self.out_hz_text = Label(self.bodyFrame3, text= "(Hz)",bg='#e21f26', fg='#0000FF' , font=("", 25, "bold"))
        self.out_hz_text.place(x=220, y=115)

        # Volatge output
        self.EarningImage = Image.open('images\\voltage_64.png')
        photo = ImageTk.PhotoImage(self.EarningImage)
        self.Earning = Label(self.bodyFrame4, image=photo, bg='#ffcb1f')
        self.Earning.image = photo
        self.Earning.place(x=230, y=5)

        self.Earning_text = Label(self.bodyFrame4, text='Voltage Output', bg='#ffcb1f', font=("", 13, "bold"))
        self.Earning_text.place(x=5, y=5)

        self.Earning_figure = Label(self.bodyFrame4, text= voltage_out, bg='#ffcb1f',fg='#0000FF', font=("", 45, "bold"))
        self.Earning_figure.place(x=60, y=100)
        
        self.out_voltage_text = Label(self.bodyFrame4, text= "(V)",bg='#ffcb1f', fg='#0000FF' , font=("", 25, "bold"))
        self.out_voltage_text.place(x=220, y=115)
        
    #================================================================    
    def Manage_page(self):
        global temp_min, temp_max, avg_temp
        global humi_min, humi_max, avg_humi
        global volt_min, volt_max, avg_volt
        global freqout_min, freqout_max, avg_frequency
        
        self.Mana_Frame = Frame(self.window, bg='#888888')
        self.Mana_Frame.place(x=300, y= 60, width= 1070, height= 700)
        
        self.mana_fram1 = Frame(self.Mana_Frame, bg='#00FF99')
        self.mana_fram1.place(x=0,y=0, width=1070, height= 120)
        
        # Frequency output min
        self.freq_out_min_text = Label(self.mana_fram1, text = 'Frequency min',bg='#00FF99', font=("", 13, "bold") )
        self.freq_out_min_text.place(x=10, y = 20)   
        self.freq_out_min = Label(self.mana_fram1, text = freqout_min,bg='#FFFFFF', font=("", 25, "bold"), anchor='c' )
        self.freq_out_min.place(x=150, y = 10, width= 120)
        
        # Frequency output max
        self.freq_out_max_text = Label(self.mana_fram1, text = 'Frequency max',bg='#00FF99', font=("", 13, "bold") )
        self.freq_out_max_text.place(x=10, y = 75) 
        self.freq_out_max = Label(self.mana_fram1, text = freqout_max,bg='#FFFFFF', font=("", 25, "bold"), anchor= 'c' )
        self.freq_out_max.place(x=150, y = 65,width = 120, )
        
        # voltage min
        self.volt_min_text = Label(self.mana_fram1, text = 'Voltage min',bg='#00FF99', font=("", 13, "bold") )
        self.volt_min_text.place(x=280, y = 20)   
        self.volt_min = Label(self.mana_fram1, text = volt_min,bg='#FFFFFF', font=("", 25, "bold"), anchor='c' )
        self.volt_min.place(x=390, y = 10, width= 120)
        
        # voltage max
        self.volt_max_text = Label(self.mana_fram1, text = 'Voltage max',bg='#00FF99', font=("", 13, "bold") )
        self.volt_max_text.place(x=280, y = 75) 
        self.volt_max = Label(self.mana_fram1, text = volt_max,bg='#FFFFFF', font=("", 25, "bold"), anchor= 'c' )
        self.volt_max.place(x=390, y = 65,width = 120, )

        # temp min
        self.temp_min_text = Label(self.mana_fram1, text = 'Tempurature min',bg='#00FF99', font=("", 13, "bold") )
        self.temp_min_text.place(x=520, y = 20)   
        self.temp_min = Label(self.mana_fram1, text = temp_min,bg='#FFFFFF', font=("", 25, "bold"), anchor='c' )
        self.temp_min.place(x=670, y = 10, width= 120)
        
        # temp max
        self.temp_max_text = Label(self.mana_fram1, text = 'Tempurature max',bg='#00FF99', font=("", 13, "bold") )
        self.temp_max_text.place(x=520, y = 75) 
        self.temp_max = Label(self.mana_fram1, text = temp_max,bg='#FFFFFF', font=("", 25, "bold"), anchor= 'c' )
        self.temp_max.place(x=670, y = 65,width = 120, )
          
        # humi min
        self.temp_min_text = Label(self.mana_fram1, text = 'Humidity min',bg='#00FF99', font=("", 13, "bold") )
        self.temp_min_text.place(x=800, y = 20)   
        self.temp_min = Label(self.mana_fram1, text = humi_min,bg='#FFFFFF', font=("", 25, "bold"), anchor='c' )
        self.temp_min.place(x=930, y = 10, width= 120)
        
        # humi max
        
        self.temp_max_text = Label(self.mana_fram1, text = 'Humidity max',bg='#00FF99', font=("", 13, "bold") )
        self.temp_max_text.place(x=800, y = 75) 
        self.temp_max = Label(self.mana_fram1, text = humi_max,bg='#FFFFFF', font=("", 25, "bold"), anchor= 'c' )
        self.temp_max.place(x=930, y = 65,width = 120, )
        
        
        
        self.mana_frame2 = Frame(self.Mana_Frame, bg='#CCCC99')
        self.mana_frame2.place(x=0, y= 120, width=1070, height=500)
        
        tree_scroll = Scrollbar(self.mana_frame2)
        tree_scroll.place(relx= 0.934, rely=0.128, width=42, height= 432)
        tree_scroll.pack(side= RIGHT, fill= Y)
        #tree_scroll.pack(side= RIGHT)
        def data_update(rows):
            global my_data
            my_data = rows
            table_data.delete(*table_data.get_children())
            for i in rows:
                table_data.insert('','end',values=i)
        self.btn_refresh = Button(self.Mana_Frame, text= 'REFRESH', bg='#FFFFCC', command= data_update)
        self.btn_refresh.place(x=20, y= 640, width= 120, height= 40)
        # 
        def export_excel():
            if len(my_data)<1:
                messagebox.showinfo("Error", "No data to export")
                return False

            fln = filedialog.asksaveasfilename(initialdir= os.getcwd(), title="Save CSV",
                                               filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
            with open(fln, mode='w') as myfile:
                exp_writer = csv.writer(myfile, delimiter =',')
                for i in my_data:
                    exp_writer.writerow(i)
            messagebox.showinfo("Data Export Success")
        
        self.btn_excel = Button(self.Mana_Frame, text= 'EXCEL', bg='#FFFFCC', command= export_excel)
        self.btn_excel.place(x=200, y= 640, width= 120, height= 40)
        
        
        self.avg_frequency_text = Label(self.Mana_Frame, text = 'Frequency Average', bg='#888888', font=("", 13, "bold") )
        self.avg_frequency_text.place(x=360, y = 630)
        self.avg_frequency = Label(self.Mana_Frame, text = avg_frequency, bg='#FFFFFF', font=("", 13, "bold") )
        self.avg_frequency.place(x=540, y = 625, width =100, height= 30)
        
        self.avg_volt_text = Label(self.Mana_Frame, text = 'Voltage Average', bg='#888888', font=("", 13, "bold") )
        self.avg_volt_text.place(x=360, y = 665)
        self.avg_volt = Label(self.Mana_Frame, text = avg_volt, bg='#FFFFFF', font=("", 13, "bold") )
        self.avg_volt.place(x=540, y = 665, width =100, height= 30)
        
        self.avg_temp_text = Label(self.Mana_Frame, text = 'Tempurature Average', bg='#888888', font=("", 13, "bold") )
        self.avg_temp_text.place(x=690, y = 630)
        self.avg_temp = Label(self.Mana_Frame, text = avg_temp, bg='#FFFFFF', font=("", 13, "bold") )
        self.avg_temp.place(x=890, y = 625, width =100, height= 30)
        
        self.avg_humi_text = Label(self.Mana_Frame, text = 'Humidity Average', bg='#888888', font=("", 13, "bold") )
        self.avg_humi_text.place(x=690, y = 665)
        self.avg_humi = Label(self.Mana_Frame, text = avg_humi, bg='#FFFFFF', font=("", 13, "bold"))
        self.avg_humi.place(x=890, y = 665, width =100, height= 30)
        
        #self.btn_excel.pack()
        
        # Table
        table_data = Treeview(self.mana_frame2, height=500, columns=('Id', 'Freq_Ref', 'Freq_Out','Volt_out', 'Temp_1', 'Humi_1'), 
                              show= 'headings', yscrollcommand= tree_scroll.set, selectmode='browse')
        table_data.place(x=0, y= 120)
        table_data.column('Id', width= 100, anchor='c')
        table_data.column('Freq_Ref', width= 190, anchor='c')
        table_data.column('Freq_Out', width= 190, anchor='c')
        table_data.column('Volt_out', width= 190, anchor='c')
        table_data.column('Temp_1', width= 190, anchor='c')
        table_data.column('Humi_1', width= 190, anchor='c')
        
        table_data.heading('Id', text= 'ID')
        table_data.heading('Freq_Ref', text= 'Frequency Reference')
        table_data.heading('Freq_Out', text= 'Frequency Output')
        table_data.heading('Volt_out', text= 'Volage Output')
        table_data.heading('Temp_1', text= 'Tempurature 1')
        table_data.heading('Humi_1', text= 'Humidity 1')
        
        table_data.tag_configure("gray", background="lightgray")
        table_data.tag_configure("normal",  background="white")

        my_tag ='normal'
        s = Style()
        s.configure(table_data)
        s.theme_use('alt')
        
        table_data.pack()
        tree_scroll.config(command= table_data.yview)
        
        # Create dadabase connection
        conn = sqlite3.connect('Database\IoT_Dashboard.db')
        
        # Create a cursor instance
        c = conn.cursor()
        c.execute("SELECT * FROM Data_Table")
        records = c.fetchall()
        
        #data_update(records)
        
        # Add our data to the screen
        global count
        count = 0
        i= 0
        
        my_data = records
        for ro in records:
            if(my_tag =='gray'):
                my_tag = 'normal'
            else:
                my_tag = 'gray'
            if ro[0]%2  ==0:
                table_data.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]), tags= ("gray"),)   
            else:
                table_data.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]), tags= ("normal"),)
            i = i+ 1
        
        #================================================================

        #================================================================
        def find_min_in_column(column_id):
            items = table_data.get_children()
            values_in_column = [table_data.item(item, "values")[column_id] for item in items]
            min_value = min(values_in_column)
            return min_value
        
        def find_max_in_column(column_id):
            items = table_data.get_children()
            values_in_column = [table_data.item(item, "values")[column_id] for item in items]
            max_value = max(values_in_column)
            return max_value
        
        def getAvg(column_id):
            val =0
            for row in table_data.get_children():
                val = val + float(table_data.item(row, "values")[column_id])
                
            avg_value = "{:.2f}".format(val/len(table_data.get_children()))
            return avg_value
        
        def saveExcel():
            workbook = Workbook()
            sheet = workbook.active
            
            headers = [column["text"] for column in table_data["columns"]]
            sheet.append(headers)
            for item in table_data.get_children():
                row_data = [table_data.item(item, "values")[i] for i in range(len(headers))]
                sheet.append(row_data)
            workbook.save("DataPLC.xlsx")
        
        freqout_min = find_min_in_column(2)
        freqout_max = find_max_in_column(2)
        avg_frequency = getAvg(2)
        
        volt_min = find_min_in_column(3)
        volt_max = find_max_in_column(3)
        avg_volt = getAvg(3)
        
        temp_min = find_min_in_column(4)
        temp_max = find_max_in_column(4)
        avg_temp = getAvg(4)
        
        humi_min = find_min_in_column(5)
        humi_max = find_max_in_column(5)
        avg_humi = getAvg(5) 
    #================================================================
    def Setting_page(self):
        self.Setting_Frame = Frame(self.window, bg='#999999')
        self.Setting_Frame.place(x=300, y= 60, width= 1070, height= 700)  
        
        self.setting_frame1 =Frame(self.Setting_Frame, bg = '#0000EE')
        self.setting_frame1.place(x=10, y=10, width = 500, height= 350)
        
        self.setting_frame2 =Frame(self.Setting_Frame, bg = '#0000EE')
        self.setting_frame2.place(x=550, y=10, width = 500, height= 350)
        
        self.setting_frame3 =Frame(self.Setting_Frame, bg = '#0000EE')
        self.setting_frame3.place(x=10, y=370, width = 1040, height= 320)
        
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master= self.setting_frame1)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        
        def update_plot():
            data = random.randint(0, 100)  # Replace with your real-time data source
            ax.clear()
            ax.plot([1, 2, 3], [data, data + 10, data - 5])  # Example data
            ax.set_title("Real-Time Plot")
            canvas.draw()
            self.setting_frame1.after(1000, update_plot)  # Update every 1000 milliseconds (1 second)
            
        update_plot()
    #================================================================  
    
    def Camera_page(self):
        global imgtk
        global lbl_Image, btn_Status_Enable, cap
        self.Camera_Frame = Frame(self.window, bg='#999999')
        self.Camera_Frame.place(x=300, y= 60, width= 1070, height= 700) 
        
        self.frame_cam = Frame(self.Camera_Frame, bg='#0000EE')
        self.frame_cam.place(x= 20, y= 10, width= 600, height= 400)
        
        lbl_Image = Label(self.frame_cam, width=600, height=400)
        lbl_Image.pack()

        
        def Switch():
            global btn_Status_Enable
      
            if btn_Status_Enable :
                btn_Status_Enable = False
            else:
                btn_Status_Enable = True
                
            
        cap = cv2.VideoCapture(0)
        cv2image = None
        if not cap.isOpened():
            messagebox('Cannot open camera')
            exit()
            
            
        def show_frames():
            global cv2image
            cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = img)
            lbl_Image.imgtk = imgtk
            lbl_Image.configure(image=imgtk)
            lbl_Image.after(20, show_frames)

        def key_pressed(event):
            take_pic()

        i = 0
        def take_pic():
            global i
            cv2.imwrite(f"pics/{i}.jpg", cv2image)
            i += 1
        #show_frames()
        
        thread = threading.Thread(target=show_frames)
        thread.start()
        self.btn_Cam = Button(self.Camera_Frame, text= 'Enable Camera', command= key_pressed)
        self.btn_Cam.place( x= 100, y= 430, width= 120, height= 30)
        

        
     #================================================================               
    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%Y/%m/%d')
        set_text = f" {self.time} \n {self.date}"
        self.date_time.configure(text = set_text, font=("",13,"bold"), bd=0, bg='#CCFFCC',fg= "black")
        self.date_time.after(100, self.show_time)
    #================================================================
    #======================FUNCTION CONNECT PLC======================
    #================================================================ 
    def ReadPLCData(self):
        global plcStatus_get
        global frequency_ref 
        global frequency_out 
        global voltage_out 
        global tempurature_1 
        global  humidity_1 
        if not is_on:
            plc = snap7.client.Client()
            plc.connect(IP,RACK,SLOT)
            state = plc.get_cpu_state()
            plcStatus_get = plc.get_connected()
            if plcStatus_get:
                self.startBar()
                glb_status_connect = True
                freq_ref = ReadMemory(plc,42,0,S7WLWord)
                freq_out = ReadMemory(plc,44,0,S7WLReal)
                volt_out = ReadMemory(plc, 48,0,S7WLReal)
                temp_1 = ReadMemory(plc, 52,0, S7WLReal)
                humi_1 = ReadMemory(plc, 56,0, S7WLReal)
                #print(f'Frequency reference: {freq_ref}')
                #print(f'Frequency reference: {freq_out}')
                frequency_ref =freq_ref/100
                frequency_out = freq_out/100
                voltage_out = volt_out/10
                tempurature_1 = "{:.2f}".format(temp_1)
                humidity_1 = "{:.2f}".format(humi_1)
                
                self.totalPeople_text.config(text= frequency_ref)
                self.people_who_left.config(text = frequency_out)
                self.Earning_figure.config(text= voltage_out)
                self.temp1_value1.config(text= tempurature_1)
                self.humi_value1.config(text= humidity_1)
                
                self.textstatus = "Connected"
                self.plcStatus.config(text = "Connected")
            else:
                glb_status_connect = False
                self.textstatus = "Disconnected"
                self.plcStatus.config(text = "Disconnected")

        else:
            plc = snap7.client.Client()
            plc.disconnect()
            glb_status_connect = False
            value_bar =0
            self.bar["value"]=0
            plcStatus_get = plc.get_connected()
            if not plcStatus_get:
                pass
        
        print(f'Button Connect: {is_on}')
        print(f'Bool connect PLC: {plcStatus_get}')
        #self.graphs()
        self.window.after(200, self.ReadPLCData)
        #================================================================
    def my_function_Local_Glb(self):
        pass
        #================================================================
    def Insert_Data(self): 
        try:    
            #self.ReadPLCData()
            connection = sqlite3.connect('Database\IoT_Dashboard.db')
            cur = connection.cursor()
            cmd1 = """INSERT INTO Data_Table
                                (frequency_ref, frequency_out, voltage_out, tempurature_1, humidity_1) 
                                VALUES(?,?,?,?,?);"""
            data_tuple =(frequency_ref, frequency_out, voltage_out, tempurature_1, humidity_1)  
            if voltage_out !=0:    
                cur.execute(cmd1,data_tuple)
                        
            connection.commit()
            connection.close()
            print('Insert succeeded')
        except sqlite3.Error as error:
                print("Failed to insert Python variable into sqlite table", error)
        finally:
            if connection:
                connection.close()
                
            self.window.after(5000, self.Insert_Data)

    '''def getMin(val_data):
        val = val_data.item("1")["values"][3]
        for row in val_data.get_children():
            if val > val_data.item(row[3]):
                val = val_data.item(row[3])
        print(val)
        return temp_min'''
    #===============================================================
    def startBar(self):
        task = 10
        value_bar =0
        print(glb_status_connect)
        if not glb_status_connect:
            while(value_bar<task):
                self.bar['value']+=10
                value_bar+=1  
        else:
            self.bar['value']=0
            
    def exit_app(self):
        self.window.destroy()
        exit()
    
    #================================================================
    def graphs():
         value_temp1 = np._FloatValue(tempurature_1)   
         plt.hist(value_temp1, 50)
         plt.show()
    
#================================================================
#================================================================
#================================================================        
def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()
    
def opencv_function():
    
    global btn_Status_Enable
    cap = cv2.VideoCapture(0)  # Capture video from the default camera (you can change the source)
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("OpenCV Window", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #win()
    tkinter_process = multiprocessing.Process(target=win)
    #opencv_process = multiprocessing.Process(target=opencv_function)
    
    # Start both processes
    tkinter_process.start()
    #opencv_process.start()   
    
    
    # Wait for both processes to finish
    tkinter_process.join()
    #opencv_process.join()