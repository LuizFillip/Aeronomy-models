from .iri import (point_iri, 
                  altrange_iri, 
                  ne_from_latitude, 
                  timeseries_iri)
from .msis import altrange_msis, timerange_msis, point_msis
from .core import altrange_models, point_models
from .hwm import load_hwm
import settings as s

s.config_labels()