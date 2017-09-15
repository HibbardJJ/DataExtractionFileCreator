# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:54:01 2017

@author: Joshua Hibbard
"""

import csv
import re
import os

date = input('What is the date of the experiment? Format: MMDDYY') 
start_time=input('What is the starting time of the experiment? Please use the format HH MM SS MSS and separate each entry with a space.')


start_time_list=start_time.split()
hours=start_time_list[0]
minutes=start_time_list[1]
seconds=start_time_list[2]
milliseconds=start_time_list[3]
thermal_image_time_list=[]
"""Delineates the columns in the gas exchange data with the desired values."""
time_stamp_column=2
lower_before_thermo_column=26
lower_after_thermo_column=27
upper_before_thermo_column=28
upper_after_thermo_column=29
xout2_column=22




for filename in os.listdir('TempImages'):
    regex=re.compile(r'\d+')
    time_stamp=regex.findall(filename)
    del(time_stamp[0:4])
    'Parse the list according to time signatures'
    image_hours=time_stamp[0]
    image_minutes=time_stamp[1]
    image_seconds=time_stamp[2]
    image_milliseconds=time_stamp[3]
    'Calculate the actual time of the first image.'
    image_true_hours=float(hours) + float(image_hours)
    image_true_minutes=float(minutes) + float(image_minutes)
    image_true_seconds=float(seconds) + float(image_seconds)
    image_true_milliseconds=float(milliseconds) + float(image_milliseconds)
    'Convert the true image time into minutes elapsed since midnight.'
    final_image_time = image_true_hours*60 + image_true_minutes + image_true_seconds/60 + image_true_milliseconds/60000
    'Add the final image time to the thermal image list'
    thermal_image_time_list.append(final_image_time)

thermal_image_index = 0


with open(date + '.csv', 'r') as gas_exchange_data, open('DataExtraction.csv','w') as outputfile:
    data = csv.reader(gas_exchange_data, delimiter = ',', quotechar = '\n')
    #writer = csv.writer(outputfile , delimiter=',')
    while True:
        ged_row = next(data)
        time_stamp=float(ged_row[time_stamp_column])
        if time_stamp <= thermal_image_time_list[thermal_image_index] + 0.3 and time_stamp >= thermal_image_time_list[thermal_image_index] - 0.3:
            
            lbt=float(ged_row[lower_before_thermo_column])
            lat=float(ged_row[lower_after_thermo_column])
            ubt=float(ged_row[upper_before_thermo_column])
            uat=float(ged_row[upper_after_thermo_column])
            xout2=float(ged_row[xout2_column])
        
        
            outputfile.write(str(time_stamp))
            outputfile.write(',')
            outputfile.write('Kmatrixfile')
            outputfile.write(',')
            outputfile.write(str(lbt))
            outputfile.write(',')
            outputfile.write(str(lat))
            outputfile.write(',')
            outputfile.write(str(ubt))
            outputfile.write(',')
            outputfile.write(str(uat))
            outputfile.write(',')
            outputfile.write(str(xout2))
            outputfile.write('\n')
        
            thermal_image_index+=1        
        
        
        #writer.writerow([time_stamp,'Kmatrixfile',lbt,lat,ubt,uat,xout2])
        