# https://geo-python.github.io/site/notebooks/L7/advanced-plotting.html

import pandas as pd
import matplotlib.pyplot as plt
fp = r"data/029740.txt"

data = pd.read_csv("pollution.csv", parse_dates=['date'], index_col='date')
