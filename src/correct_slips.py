import numpy as np
from utils import smooth

def find_index(diff, ts = 0.5):
    for i, v in enumerate(diff):
        if (v > ts) or (v < - ts):
            return i

def correct_slip(vls, ts = 1):
    
    avg = vls.rolling(
        window = 3, 
        center = True
        ).mean()

    diff = np.diff(vls - avg)
    
    index = find_index(diff, ts = ts)
    
    cycle = vls[index] - vls[index + 1]
    vls[index + 1:] += cycle
    return vls


def correct_and_smooth(
        vls, 
        threshold = 1, 
        pts = 10, 
        window = 2
        ):
    vls =  correct_slip(vls, ts = threshold)
    return smooth(vls, pts = pts, window = 2)


