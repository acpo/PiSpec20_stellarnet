#Stellarnet initialization functions
#
import json
import requests
import numpy as np

def stellarnet_init():
    device=[]
    c1=0
    c2=0
    c3=0
    c4=0
    IntTime=0
    data=[]
    dark=[]
    incident=[]
    x = []
    y = []
    deviceurl = 'http://localhost:5000/spectrometers'

        
# GET SPECTROMETER DEVICE NUMBER        
    device_r = requests.get(deviceurl)
    device_full = device_r.json()
    device = device_full['device_ids']
# GET SPECTROMETER CONFIGURATION
    configurl = deviceurl+'/'+device[0]+'/config'
    config_r = requests.get(configurl)
    config_full = config_r.json()
    c1 = config_full['coeffs'][0]
    c2 = config_full['coeffs'][1]
    c3 = config_full['coeffs'][2]
    c4 = config_full['coeffs'][3]

    IntTime = 50
    Averages = 1
    headers = {
            'Content-Type': 'application/json',
    }
    conf = '{"int_time":'+str(IntTime)+',"x_timing":3,"x_smooth":0,"scans_to_avg":'+str(Averages)+'}'
    requests.put(configurl, headers=headers, data=conf)
    
    IntTime = config_full['int_time']
    Averages = config_full['scans_to_avg']
        
# GET INITIAL SPECTRUM AND SETUP VARIABLES
    spectrumurl = deviceurl+'/'+device[0]+'/spectrum'
    spec_r = requests.get(spectrumurl)
    spec_fulldata = spec_r.json()
    data = spec_fulldata['data']
    data = np.array(data, dtype=float)
    pixels = len(data)
    for i in range(pixels):
        x.append(i)
    x = np.array(x)
    x = np.around(((c4*((x^3)/8))+(c2*((x^2)/4))+(c1*x/2)+c3), decimals=2)   #calibrate x to wavelength
    xmin = np.around(min(x), decimals=2)
    xmax = np.around(max(x), decimals=2)
    ymin = np.around(min(data), decimals=2)
    ymax = np.around(max(data), decimals=2)

# incident and dark loaded with ones to prevent math error if no data taken
    incident = np.ones_like(data)
    dark = np.ones_like(data)

    return spectrumurl, configurl, data, x, incident, dark, IntTime, Averages, xmin, xmax, ymin, ymax
