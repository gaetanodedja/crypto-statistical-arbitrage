# Binance Cryptocurrency Pair Trading Bot

## Project Overview
This project involves developing a cryptocurrency pair trading strategy for finding anomalies of the prices between assets. The bot fetches historical data for USDT pairs, checks for cointegrated pairs, calculates hedge ratios, and generates trading signals based on the Z-score of the price ratio between cointegrated pairs.

# Note: This project is still in the development phase.

## Strategy Explanation
Every movement of prices in time is a time series, and cryptocurrencies are no exception. Since all the crypto prices move together with Bitcoin and are identified with it, there is an opportunity to find cointegrated assets. The price relationship of two or more cointegrated series is linear.

The main idea is that if two assets are cointegrated, there may be specific times when, for different reasons, this relationship could change. This is the time when the bot tries to generate signals because the prices will likely revert to their historical mean. This mean reversion provides an opportunity to enter a trade and profit from the price correction.

## Project Structure
The project consists of :
- `pairtrading.ipynb`: The main Python Notebook script to build and test the strategy.
- `generatingsignals.py`: The Python bot script that gets the data from binance api and generates the signals when to open a position.

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.x
- ccxt
- numpy
- pandas
- statsmodels
- yfinance

You can install the required libraries using pip:
```bash
pip install ccxt numpy pandas statsmodels yfinance
