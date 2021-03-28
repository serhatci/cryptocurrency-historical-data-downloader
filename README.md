<p align="center">
  <h1 align="center">Cryptocurrency Historical Data Downloader</h1>
  <p align="center">CoinbasePro | Kraken | Bitpanda | Exmo | Bitfinex</p>
  </p>
  <p align="center">
    <img src="https://img.shields.io/github/license/serhatci/cryptocurrency-historical-data-downloader" /></img>
   	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" /></img>
    <img src=https://img.shields.io/pypi/v/cryptoasset-data-downloader></img>
    <img src=https://www.codefactor.io/repository/github/serhatci/cryptocurrency-historical-data-downloader/badge/main /></img>  
</p>

![Application image](https://github.com/serhatci/cryptocurrency-historical-data-downloader/blob/main/application.jpg)

Historical data of crypto assets are demanded for different purposes such as investment analysis, academic research, etc. Though the data is most of the time publicly available, it is not always easy to reach it for the people who have less coding skills to connect API of crypto exchanges and download data by making several sequencing requests. Besides, crypto-exchanges mostly have different data formats that must be standardized. This application handles all these processes and stores all downloaded data in to csv files on your OS.

# Installation

Project is already uploaded in PyPI. You can download application by writing the code below in your terminal:

`pip install cryptoasset-data-downloader`

to execute the application, you should run below code:

`cryptoasset-data-downloader`

# Requirements

Application works in Python version 3.6 or higher! If you would like to run the script without installing from PyPI, you need to install below dependencies:

```
pip install arrow==0.16.0
pip install requests==2.22.0
pip install pandas==0.25.1
pip install PySimpleGUI==4.31.0
```

# Uml Diagram

![Application image](https://github.com/serhatci/cryptocurrency-historical-data-downloader/blob/main/uml-diagram.png)

# How to use

Application is pretty straightforward and easy to use. You just need to select a crypto-exchange from the list and provide the name & abbreviation of the crypto asset which you would like to download historical data. It is extremely important to use exactly the same crypto asset abbreviation supported by the selected crypto exchange. By clicking 'available coins?' button, you can learn which crypto assets are being currently supported by the selected crypto exchange.

You can also select a start and end date for your historical data. It should be noted that start date of your data will dependent on the selected crypto exchange's data providing capabilities.

Historical data can be downloaded with different resolutions such as minutes,hours,days,weeks and months. However, some crypto exchanges might have limited choices for historical data resolution. All downloaded historical data are saved in to cvs files on your OS.
