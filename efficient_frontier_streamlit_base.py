import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
import matplotlib.pyplot as plt

from efficient_frontier import *

returns_methods = ["means_returns"]
risk_methods = ["covariance"]

st.header("Efficient Frontier")
tickers = st.text_input('Please enter tickers here (seperated by comma):')
status_radio = st.radio('Please click Search when you are ready.', ('Entry', 'Search'))

today = dt.date.today()

before = today - dt.timedelta(days=700)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

df = pd.DataFrame()
find_frontier = False

if status_radio == "Search":

    df = yf.download(tickers, start_date, end_date)['Adj Close']
    st.dataframe(df)
    
    find_frontier = True


if find_frontier == True:
    
    ef = Efficient_Frontier(df, tickers)
    
    returns_method = st.selectbox("Select returns method", returns_methods)
    risk_measure = st.selectbox("Select risk method", risk_methods)
    num_portfolios_resp = st.number_input('Please enter number of simulations', min_value = 0, max_value = 1000000, step = 1)
    
    returns_method = df.pct_change().mean()
    risk_measure = df.pct_change().cov()
    num_portfolios = num_portfolios_resp
    rf = 0.0
    
    frontier_radio = st.radio('Please click Search when you are ready to run.', ('Entry', 'Search'))
    if frontier_radio == "Search":
        
        results_frame = ef.simulate_random_portfolios(num_portfolios, returns_method, risk_measure, rf, tickers)   
        
        portfolios = ef.find_portfolios(results_frame)
        
        fig = plt.figure()
        plt.scatter(results_frame['stdev'], results_frame['ret'], c = results_frame.sharpe, cmap = 'RdYlBu')
        
        plt.scatter(portfolios[0][1], portfolios[0][0], marker=(5,1,0),color='r',s=500)
        plt.scatter(portfolios[1][1], portfolios[1][0], marker=(5,1,0),color='g',s=500)
        plt.colorbar()
        plt.xlabel("standard deviation")
        plt.ylabel("return")
        st.pyplot(fig)
        
        st.write("maximum sharpe portfolio", portfolios[0])
        st.write("mininum variance portfolio", portfolios[1]) 

    
    
    