import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import datetime


print("Loading the application kusumakar")
yfinance_symbols = {
    "S&P 500": "^GSPC",
    "NASDAQ Composite": "^IXIC",
    "Dow Jones Industrial Average": "^DJI",
    "Russell 2000": "^RUT",
    "FTSE 100": "^FTSE",
    "DAX (Germany)": "^GDAXI",
    "CAC 40 (France)": "^FCHI",
    "Nikkei 225 (Japan)": "^N225",
    "Shanghai Composite": "000001.SS",
    "Hang Seng Index": "^HSI",
    
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "USDCAD=X",
    "USD/CHF": "USDCHF=X",

    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil WTI": "CL=F",
    "Crude Oil Brent": "BZ=F",
    "Natural Gas": "NG=F",
    "Copper": "HG=F",

    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Dogecoin": "DOGE-USD",
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD",

    "SPDR S&P 500 ETF": "SPY",
    "Invesco QQQ Trust": "QQQ",
    "Vanguard Total Stock Market ETF": "VTI",
    "ARK Innovation ETF": "ARKK",
    "iShares Russell 2000 ETF": "IWM",

    "U.S. 10-Year Treasury Yield": "^TNX",
    "U.S. 30-Year Treasury Yield": "^TYX",
    "U.S. 5-Year Treasury Yield": "^FVX",
    "U.S. 2-Year Treasury Yield": "^IRX",

    "Vanguard 500 Index Fund": "VFINX",
    "Fidelity Contrafund": "FCNTX",
    "American Funds Growth Fund": "AGTHX",

    "S&P 500 Futures": "ES=F",
    "Nasdaq 100 Futures": "NQ=F",
    "Dow Jones Futures": "YM=F",
    "Gold Futures": "GC=F",
    "Crude Oil Futures": "CL=F",

    "Reliance Industries (India)": "RELIANCE.NS",
    "Tata Motors (India)": "TATAMOTORS.NS",
    "Infosys (India)": "INFY.NS",
    "BP (UK)": "BP.L",
    "Rolls-Royce (UK)": "RR.L",
    "Volkswagen (Germany)": "VOW.DE",
    "Siemens (Germany)": "SIE.DE"
}



# Function to fetch stock data
def get_stock_data(symbol,name, start="2024-01-01", end="2025-02-11"):
    from datetime import timedelta
    start=(datetime.datetime.now()-timedelta(days=300)).strftime("%Y-%m-%d")
    end=(datetime.datetime.now()+timedelta(days=10)).strftime("%Y-%m-%d")
    df = yf.download(symbol, start=start, end=end)

    # Flatten MultiIndex columns (if applicable)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df['Name']=[name]*len(df)
    df.dropna(inplace=True)  # Remove missing values
    
    return df

# Function to calculate indicators
def calculate_indicators(df):
    if 'Close' not in df.columns:
        raise ValueError("No 'Close' column found. Check data source.")

    df['SMA_50'] = df['Close'].rolling(window=50).mean()  
    df['SMA_200'] = df['Close'].rolling(window=200).mean()  

    # RSI Calculation
    rsi_indicator = ta.momentum.RSIIndicator(df['Close'], window=14)
    df['RSI'] = rsi_indicator.rsi()  

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['BB_Upper'] = bb.bollinger_hband()  
    df['BB_Lower'] = bb.bollinger_lband()  

    return df

# Function to generate buy/sell signals and trend
def generate_signals_and_trend(df):
    buy_signals = []
    sell_signals = []
    trends = []

    for i in range(len(df)):
        buy_signal = np.nan
        sell_signal = np.nan
        trend = np.nan

        # Determine trend based on SMA crossovers
        if df['SMA_50'].iloc[i] > df['SMA_200'].iloc[i]:
            trend = "Uptrend"  # Bullish (SMA 50 is above SMA 200)
        elif df['SMA_50'].iloc[i] < df['SMA_200'].iloc[i]:
            trend = "Downtrend"  # Bearish (SMA 50 is below SMA 200)

        # Golden Cross: 50-period SMA above 200-period SMA (Uptrend)
        if (
            df['SMA_50'].iloc[i] > df['SMA_200'].iloc[i] and  # SMA 50 > SMA 200
            df['RSI'].iloc[i] < 30 and  # RSI below 30 (oversold)
            df['Close'].iloc[i] <= df['BB_Lower'].iloc[i] * 1.02  # Price touches or below lower Bollinger Band
        ):
            buy_signal = df['Close'].iloc[i]  # Generate Buy Signal

        # Death Cross: 50-period SMA below 200-period SMA (Downtrend)
        elif (
            df['SMA_50'].iloc[i] < df['SMA_200'].iloc[i] and  # SMA 50 < SMA 200
            df['RSI'].iloc[i] > 70 and  # RSI above 70 (overbought)
            df['Close'].iloc[i] >= df['BB_Upper'].iloc[i] * 0.98  # Price touches or above upper Bollinger Band
        ):
            sell_signal = df['Close'].iloc[i]  # Generate Sell Signal

        buy_signals.append(buy_signal)
        sell_signals.append(sell_signal)
        trends.append(trend)

    df['Buy_Signal'] = buy_signals
    df['Sell_Signal'] = sell_signals
    df['Trend'] = trends  # Add the Trend column
    df=df.reset_index()
   
    df['Date']=pd.to_datetime(df['Date'])
    df['Month']=df['Date'].dt.month
    df['Year']=df['Date'].dt.year
    return df

# Function to plot results

def get_signal(df):
	
  d=datetime.datetime.now().strftime("%Y-%m-%d")
  df=df[df.Date==d]
  buy=df[(df.RSI<=30) & (df.Trend=='Uptrend') & (df.Month==2) & (df.Year==2025)]
    
  sell = df[(df.RSI>=50) & (df.Trend=='Downtrend') & (df.Month==2) & (df.Year==2025)]

  print("-------   BUY  ---------")
  buy= str(buy.Name.unique())
  print("----------SELL -- ")
  sell = str(sell.Name.unique())
  return "BUY ---- "+buy+ "   SELL---- "+sell
def get_buysell(df):
  d=datetime.datetime.now().strftime("%Y-%m-%d")
  k=df[df.Date==d]
  sell=str(k[~(k['Sell_Signal'].isna())]['Name'].unique())
  buy=str(k[~(k['Buy_Signal'].isna())]['Name'].unique())
  return "CURRENT STATUS SELL--->>>>>"+sell+" BUY---->>>>"+buy
	

print("Getting data from yfinance")
stocks=[]
for name,symbol in yfinance_symbols.items():
	          df = get_stock_data(symbol,name)  # Changed interval to 4 hours
	          df = calculate_indicators(df)
	          df = generate_signals_and_trend(df)
	          stocks.append(df)

final=pd.concat(stocks)
output=get_signal(final)
signals = get_buysell(final)
st.subheader(output)
st.subheader(signals)
				
		


