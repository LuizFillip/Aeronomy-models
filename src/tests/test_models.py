import pandas as pd
from RayleighTaylor.core import timerange_msise

def test_plot(start):
    import matplotlib.pyplot as plt
    infile = "database/MSIS/msis_300_saa.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df1 = timerange_msise(start)

    df1["Tn"].plot(label = "msise")
    df["T"].plot(label = "pyglow")
    
    plt.legend()