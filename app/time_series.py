import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def analyze_trends(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    result = seasonal_decompose(df['Close'], model='additive')
    result.plot()
    plt.tight_layout()
    plt.savefig("app/trend_plot.png")