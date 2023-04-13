import pandas as pd
from FluxTube.src.core import get_conductivities

def test_sum_perd():
    for col in ["south", "north", "both"]:
        
        infile = f"results_{col}.txt"
        
        df = pd.read_csv(infile, index_col = 0)
        
        hs = df.alt.unique()
        
        df1 = df.loc[df["alt"] == hs[0]]
            
        hall, perd = get_conductivities(df1)
        

    
