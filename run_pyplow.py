import numpy as np
from pyglow.pyglow import Point
from datetime import datetime, date, timedelta
import pandas as pd


def get_neutrals(dn, lat = -3.73, lon = -38.522):
   
    heights = np.arange(100, 605, 1)

    Ne = []
    for alt in heights:
        point = Point(dn, lat, lon, alt)
        point.run_msis()
        Ne.append(point.ne)

    return pd.DataFrame({"Ne": Ne, "date": dn}, index = heights)

def get_winds(dn, lat = -3.73, lon = -38.522):

    zon_wind = []
    mer_wind = []

    heights = np.arange(100, 601, 1)
    
    for alt in heights:
        point = Point(dn, lat, lon, alt)

        point.run_hwm14()
        #print("Running...", alt)
        zon_wind.append(point.u)
        mer_wind.append(point.v) 

    df = pd.DataFrame({"zon": zon_wind, 
                       "mer": mer_wind, 
                       "date": dn}, 
                       index = heights)

    return df


day = 1
month = 1
year = 2014

path = "venv/density/"

def run_for_all_night(function, date):
    out_dat = []
    year, month, day = date.year, date.month, date.day
    for hour in np.arange(19, 23, 1):
        for minute in np.arange(0, 60, 10):
            dn = datetime(year, month, day, hour, minute)
            out_dat.append(function(dn))
    return pd.concat(out_dat)





def float_to_time(tt):
    args = str(tt).split(".")
    hour = int(args[0])
    minute = int(float("0." + args[1])*60)
    return hour, minute

import datetime

def get_wind_by_time(site, year = 2014, alt = 250):

    dates = pd.date_range(str(year) + "-1-1 18:00", 
                          str(year) + "-12-31 00:00", 
                           freq = "10min")

    data = {
            "zon": [], 
            "mer": [], 
            "time": []
            }

    coords = {"car": (-7.38, -36.528), 
              "for": (-3.73, -38.522), 
              "saa": (-2.53, -44.296)}

    lat, lon = coords[site]

    for dn in dates:
    
        point = Point(dn, lat, lon, alt)

        point.run_hwm14()
        data["zon"].append(point.u)
        data["mer"].append(point.v) 
        data["time"].append(dn)

    df = pd.DataFrame(data)

    df.to_csv(site + '_' + str(alt) + '_' + str(year) + '.txt')
    
    return df

df = get_wind_by_time(site = "saa", year = 2013, alt = 500)


print(df)


