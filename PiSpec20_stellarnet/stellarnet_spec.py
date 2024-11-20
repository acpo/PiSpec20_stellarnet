import stellarnet_init_mod

import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

from sys import version_info
if version_info.major == 2:
    # use Python 2.7 style
    import Tkinter as tk
    import ttk
elif version_info.major == 3:
    # use Python 3.x style
    import tkinter as tk
    from tkinter import ttk

import json
import requests

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)

def popupmsg(msg):  # warning popup boxes
    popup = tk.Tk()
    popup.wm_title("!")
    popup.geometry('300x200-100+200')
    label = ttk.Label(popup, text=msg, font=NORM_FONT, wraplength = 250)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

class Spec(tk.Tk):
    def __init__(self, ax, *args, **kwargs):
        global spectrumurl, configurl, data, x, incident, dark, IntTime, Averages, xmin, xmax, ymin, ymax, AbMode
        global monitorindex, monitor, monitorwave
        spectrumurl, configurl, data, x, incident, dark, IntTime, Averages, xmin, xmax, ymin, ymax = stellarnet_init_mod.stellarnet_init()

        # set initial values in text boxes and spectrum window
        IntTime = 50    # 50 ms sets text in entry box to match value in _init_mod
        Averages = 1    # sets text to match value from _init_mod
        AbMode = 0      # initial mode is raw intensity
        self.ax = ax
        self.spectrumurl = spectrumurl
        self.x = x
        # xmin = 420     #for Spec20 type operation with LED, 420 nm is a useful minimum
        # xmax = 900     #for Spec20 type operation with LED, 900 nm is a useful maximum
        self.xmin = xmin    #if line above is commented out, the spectrometer determines min and max
        self.xmax = xmax
        self.ymin = ymin    #initial value supplied by _init module
        self.ymax = ymax    #initial value supplied by _init module
        self.data = data
        self.line = Line2D(self.x, self.data)
        self.ax.add_line(self.line)
        self.ax.set_ylim(ymin*0.8, ymax*1.1)
        self.ax.set_xlim(self.xmin, self.xmax)
        monitorwave = np.median(x)  #set monitor wavelength to middle of hardware range

        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default="clienticon.ico")  set window icon
        tk.Tk.wm_title(self, "StellarNet Spectrometer Control")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="Spectrometer on a Pi", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side='left', anchor=tk.N)
        labelint = tk.Label(self.frame1, text='Integration Time (ms)', relief='ridge')    
        labelint.pack(side='top', pady=2)
        labelavg = tk.Label(self.frame1, text='# of spectra to average', relief='ridge', width='17', wraplength='100')
        labelavg.pack(side='top', pady=1)
        labelxmin = tk.Label(self.frame1, text='Minimum wavelength', relief='ridge')
        labelxmin.pack(side='top', pady=2)
        labelxmax = tk.Label(self.frame1, text='Maximum wavelength', relief='ridge')
        labelxmax.pack(side='top', pady=2)
        self.button_dark = tk.Button(self.frame1, text='Measure Dark', background='light grey')
        self.button_dark.pack(side='top', pady=2)
        self.button_dark.bind('<ButtonRelease-1>', self.getdark)
        self.buttonAbMode = tk.Button(self.frame1, text='Absorbance Mode (off)', background = 'light grey')
        self.buttonAbMode.pack(side='top', pady=1)
        self.buttonAbMode.bind('<ButtonRelease-1>', self.AbMode)

        monitorindex = np.searchsorted(x, monitorwave, side='left')
        monitor = np.round(self.data[monitorindex], decimals=3)
        self.text = self.ax.text(0.9, 0.9, monitor, transform=ax.transAxes, fontsize=14)
        self.ax.axvline(x=monitorwave, lw=2, color='blue', alpha  = 0.5)
        
        self.labelmonitor = tk.Label(self.frame1, text='Wavelength to monitor (nm)', font=LARGE_FONT)
        self.labelmonitor.pack(side='top')
        self.entrymonitor = tk.Entry(self.frame1, width='7')
        self.entrymonitor.pack(side='top', pady=1, anchor=tk.N)
        self.entrymonitor.insert(0, x[monitorindex])
        self.entrymonitor.bind('<Return>', self.entrymonitor_return)
        self.labelmonitor2 = tk.Label(self.frame1, text="press <Enter> to set new wavelength")
        self.labelmonitor2.pack(side='top')
        self.button_reset_y = tk.Button(self.frame1, text='Reset Y axis scale', background='light blue')
        self.button_reset_y.pack(side='top', pady=10)
        self.button_reset_y.bind('<ButtonRelease-1>', self.reset_y)
        
        self.frame2 = tk.Frame(self)
        self.frame2.pack(side='left', anchor=tk.N)
        self.entryint = tk.Entry(self.frame2, width='6')
        self.entryint.pack(side='top', pady=1, anchor=tk.N)
        self.entryint.insert(0, IntTime)
        self.entryint.bind('<Return>', self.EntryInt_return)
        self.entryavg = tk.Entry(self.frame2, width='4')
        self.entryavg.pack(side='top', pady=5)
        self.entryavg.insert(0, Averages)
        self.entryavg.bind('<Return>', self.EntryAvg_return)
        self.entryxmin = tk.Entry(self.frame2, width='7')
        self.entryxmin.pack(side='top', pady=2)
        self.entryxmin.insert(0, xmin)
        self.entryxmin.bind('<Return>', self.Entryxmin_return)
        self.entryxmax = tk.Entry(self.frame2, width='7')
        self.entryxmax.pack(side='top', pady=2)
        self.entryxmax.insert(0, xmax)
        self.entryxmax.bind('<Return>', self.Entryxmax_return)
        self.button_incident = tk.Button(self.frame2, text='Measure 100% T', background='light grey') 
        self.button_incident.pack(side='top', pady=2)
        self.button_incident.bind('<ButtonRelease-1>', self.getincident)
        
        button_quit = ttk.Button(self, text='Quit')
        button_quit.pack(side='right', anchor=tk.N)
        button_quit.bind('<ButtonRelease-1>', self.ButtonQuit)

        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Counts')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def update(self, data):
        global AbMode
        spec_r = requests.get(spectrumurl)
        spec_fulldata = spec_r.json()
        self.data = spec_fulldata['data']

        if AbMode == 1:
            self.data = np.array(self.data, dtype=float)
            self.data = np.log10((incident-dark)/(self.data-dark))
            self.line.set_data(self.x, self.data)
            monitor = np.round(self.data[monitorindex], decimals=3)
            self.text.set_text(monitor)
            return self.line,

        else:
            #self.ax.set_ylim(min(self.data)*0.9, max(self.data)*1.1)
            #y-axis handled by reset button 
            self.line.set_data(self.x, self.data)
            monitor = np.round(self.data[monitorindex], decimals=3)
            self.text.set_text(monitor)
#self.ax.canvas.blit()      the blit approach isn't working   
            return self.line,
    
    def ButtonQuit(root, event):
            root.destroy()
            exit()

    def getdark(self, event):
        global dark
        spec_r = requests.get(spectrumurl)
        spec_fulldata = spec_r.json()
        darkj = spec_fulldata['data']
        dark = np.array(darkj, dtype=float)
        self.button_dark.configure(background = 'light green')
        
    def getincident(self, event):
        global incident
        spec_r = requests.get(spectrumurl)
        spec_fulldata = spec_r.json()
        incidentj = spec_fulldata['data']
        incident = np.array(incidentj, dtype=float)
        self.button_incident.configure(background = 'light green')
        
        # SET CONFIGURATION
    def setconfig(self,configurl):
        global IntTime, Averages
        headers = {
            'Content-Type': 'application/json',
        }
        conf = '{"int_time":'+str(IntTime)+',"x_timing":3,"x_smooth":0,"scans_to_avg":'+str(Averages)+'}'
        requests.put(configurl, headers=headers, data=conf)

        # read back new configuration from spectrometer to verify new settings
        config_r = requests.get(configurl)
        config_full = config_r.json()
        IntTime = config_full['int_time']
        Averages = config_full['scans_to_avg']
        self.entryint.delete(0, 5)
        self.entryint.insert(0,IntTime)  #set text in integration time box
        self.entryavg.delete(0, 5)
        self.entryavg.insert(0,Averages)  #set text in averages box

    def EntryInt_return(self, event):
        global IntTime
        IntTimeTemp = self.entryint.get()
        if IntTimeTemp.isdigit() == True:
            if int(IntTimeTemp) > 65000:
                msg = "The integration time must be 65000 ms or smaller.  You tried " +(IntTimeTemp)
                self.setconfig(configurl)
                popupmsg(msg)
            elif int(IntTimeTemp) < 1:
                msg = "The integration time must be 1 ms or greater.  You tried " +(IntTimeTemp)
                self.setconfig(configurl)
                popupmsg(msg)
            else:
                IntTime = int(float(IntTimeTemp))
                self.setconfig(configurl)
        else:
            msg = "Integration time must be an integer between 1 and 65000 ms.  You tried " +str(IntTimeTemp)
            self.setconfig(configurl)
            popupmsg(msg)

    def EntryAvg_return(self, event):
        global Averages
        Averages = self.entryavg.get()
        if Averages.isdigit() == True:           
            Averages = int(float(Averages))
            self.setconfig(configurl)
        else:
            msg = "Averages must be an integer.  You tried " + str(Averages) + ".  Setting value to 1."
            Averages = 1
            self.setconfig(configurl)
            popupmsg(msg)

    def Entryxmax_return(self,event):
        global xmax
        xmaxtemp = self.entryxmax.get()
        try:
            float(xmaxtemp)
            xmaxtemp = float(self.entryxmax.get())
            if xmaxtemp > xmin:
                xmax = xmaxtemp
                self.entryxmax.delete(0, 'end')
                self.entryxmax.insert(0, xmax)  #set text in box
                self.ax.set_xlim(xmin,xmax)
            else:
                msg = "Maximum wavelength must be larger than minimum wavelength.  You entered " + str(xmaxtemp) + " nm."
                self.entryxmax.delete(0, 'end')
                self.entryxmax.insert(0, xmax)  #set text in box
                popupmsg(msg)
        except:
            self.entryxmax.delete(0, 'end')
            self.entryxmax.insert(0, xmax)  #set text in box to unchanged value

    def Entryxmin_return(self, event):
        global xmin
        xmintemp = self.entryxmin.get()
        try:
            float(xmintemp)
            xmintemp = float(self.entryxmin.get())
            if xmintemp < xmax:
                xmin = xmintemp
                self.entryxmin.delete(0, 'end')
                self.entryxmin.insert(0, xmin)  #set text in box
                self.ax.set_xlim(xmin,xmax)
            else:
                msg = "Minimum wavelength must be smaller than maximum wavelength.  You entered " + str(xmintemp) + " nm."
                self.entryxmin.delete(0, 'end')
                self.entryxmin.insert(0, xmin)  #set text in box
                popupmsg(msg)
        except:
            self.entryxmin.delete(0, 'end')
            self.entryxmin.insert(0, xmin)  #set text in box to unchanged value

    def AbMode(self, event):
        global AbMode
        if AbMode == 1:
            AbMode = 0
            ax.set_ylabel('Counts')
            self.buttonAbMode.configure(text='Absorbance Mode (off)', background = 'light grey')
            self.reset_y(self)
        else:
            AbMode = 1
            ax.set_ylabel('Absorbance')
            ax.set_ylim(-0.1,1.2)
            self.buttonAbMode.configure(text='Absorbance Mode (on)', background = 'light green')

    def reset_y(self, event):
        if AbMode == 0:
            spec_r = requests.get(spectrumurl)
            spec_fulldata = spec_r.json()
            data = spec_fulldata['data']
            ymin = min(data)
            ymax = max(data)
            ax.set_ylim(ymin * 0.9, ymax * 1.1)
        else:
            pass

    def entrymonitor_return(self, event):
        global monitorwave, monitorindex, x
        monitorwavetemp = self.entrymonitor.get()
        try:
            float(monitorwavetemp)
            monitorwavetemp = float(self.entrymonitor.get())
            if xmin < monitorwavetemp < xmax:
                monitorwave = monitorwavetemp                
                monitorindex = np.searchsorted(x, monitorwave, side='left')
                monitorwave = np.around(x[monitorindex], decimals=2)
                self.entrymonitor.delete(0, 'end')
                self.entrymonitor.insert(0,monitorwave)
                self.ax.lines.pop(-1)
                self.ax.axvline(x=monitorwave, lw=2, color='blue', alpha  = 0.5)
            else:
                msg = "Monitored wavelength must be within the detected range.  Range is " + str(xmin) + " to " + str(xmax) + " nm."
                self.entrymonitor.delete(0, 'end')
                self.entrymonitor.insert(0, monitorwave)
                popupmsg(msg)
        except:
            self.entrymonitor.delete(0, 'end')
            self.entrymonitor.insert(0, monitorwave)

fig, ax = plt.subplots()
spec = Spec(ax)

# animate
ani = animation.FuncAnimation(fig, spec.update, interval=10, blit=False)
spec.mainloop()
