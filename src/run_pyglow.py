import numpy as np
from pyglow.pyglow import Point
from datetime import datetime, date, timedelta
import pandas as pd
import datetime as dt

coords = {"car": (-7.38, -36.528),  # Cariri
          "for": (-3.73, -38.522),  # Fortaleza
          "saa": (-2.53, -44.296),  # São Luis
          "boa": (2.8, -60.7),      # Boa Vista
          "ccb": (-9.5, -54.8),     # Cachimbo
          "cgg": (-20.5, 45.7)}     # Campo Grande

def get_winds(dn, site):
    lat, lon = coords[site] 
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


def float_to_time(tt):
    args = str(tt).split(".")
    hour = int(args[0])
    minute = int(float("0." + args[1])*60)
    return hour, minute


def get_wind_by_time(site, year = 2014, alt = 250):
    

    dates = pd.date_range("2012-1-1 18:00", 
                          "2016-12-31 00:00", 
                           freq = "10min")

    data = {
            "zon": [], 
            "mer": [], 
            "time": []
            }
    
    lat, lon = coords[site]

    for dn in dates:
    
        point = Point(dn, lat, lon, alt)

        point.run_hwm14()
        data["zon"].append(point.u)
        data["mer"].append(point.v) 
        data["time"].append(dn)

    df = pd.DataFrame(data)
    
    df = df.set_index("time")

    df.to_csv(site + '_250_2012_2016.txt', 
              index = True)
    
    return df

#df = get_wind_by_time(site = "car", year = 2013, alt = 500)



def get_density_by_height(dn, site = "saa", 
                hmin = 200, 
                hmax = 500, step = 1):
    
    lat, lon = coords[site]

    heights = np.arange(hmin, hmax + step, step)

    Ne = []
    for alt in heights:
        point = Point(dn, lat, lon, alt)

        point.run_iri()
        Ne.append(point.ne)

    return pd.DataFrame({"Ne": Ne, 
                         "alt": heights}, 
                          index = [dn] * len(heights))
def run_year_density():
    
    dates = pd.date_range("2013-1-1 21:00", 
                         "2013-12-31 21:00", 
                        freq = "1D")
        
    out = []

    for dn in dates:
        print("process...", dn)
        out.append(get_density_by_height(dn))

    df = pd.concat(out)
        
    df.to_csv("SAA_2013.txt", index = True)

    print(df)
    

def run_grid_wind():
    dates = [dt.datetime(2013, 1, 1, 21, 0), 
            dt.datetime(2013, 1, 2, 0, 0), 
            dt.datetime(2013, 1, 2, 3, 0), 
            dt.datetime(2013, 1, 2, 6, 0)] 
    data = {
            "zon": [], 
            "mer": [], 
            "time": [],
            "lat": [], 
            "lon": []
            }
    
    
    for dn in dates:
        for lat in np.arange(-20, 0, 0.5):
            for lon in np.arange(-80, -30, 0.5):
                point = Point(dn, lat, lon, 250)
                point.run_hwm14()
                data["time"].append(dn)
                data["lat"].append(lat)
                data["lon"].append(lon)
                data["zon"].append(point.u)
                data["mer"].append(point.v) 
                
                
    df = pd.DataFrame(data)

    df.to_csv("grid_winds_20130101.txt", index = True)



