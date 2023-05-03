# Description: This script uses the Prophet library to forecast the price of Ethereum.
import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
import plotly.io as pio
import json
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import warnings

warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format

# Get data from Yahoo Finance
today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'
eth_df = yf.download('ETH-USD',start_date, today)

# Reset index so we can have Date as a column
eth_df.reset_index(inplace=True)

# Rename columns to fit Prophet
df = eth_df[["Date", "Open"]]
new_names = {
    "Date": "ds", 
    "Open": "y",
}
df.rename(columns=new_names, inplace=True)

# Visalize data using the Plotly library
x = df["ds"]
y = df["y"]

# Create figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=x, y=y))

# Set title
fig.update_layout(
    title_text="Time series plot of Ethereum Open Price",
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=True),
        type="date",
    )
)
#fig.show()
#pio.write_html(fig, file='ethereum_open_price_plot.html', auto_open=True)

# Create and fit model
m = Prophet(
    seasonality_mode="multiplicative" 
)
m.fit(df)

#Future dataframe
future = m.make_future_dataframe(periods = 365)
future.tail()

#Predictions
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

#Forecast for tomorrow
next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
forecast[forecast['ds'] == next_day]['yhat'].item()

#Plotting the forecast
plot_plotly(m, forecast)

forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json('static/forecast.json', orient='records', date_format='iso')