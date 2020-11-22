# Cryptocurrency Historical Data Downloader
A desktop application to download historical data of desired crypto assets by connecting several different crypto-exchanges' API.

Historical data of crypto assets are demanded for different purposes such as investment analysis, academic research, etc. Though the data is most of the time publicly available, it is not always easy to reach it for the people who have less coding skills to connect API of crypto exchanges and download data by making several sequencing requests. Besides, crypto-exchanges mostly have different data formats that must be standardized. This application handles all these processes and makes it easier for its users.

![Alt text](application.jpg?raw=true "Title")

# Installation
Project is already uploaded in PyPI. You can download application by writing the code below in your terminal:

`pip install cryptoasset-data-downloader`
  
to execute the application, you should run below code:
 
 `cryptoasset-data-downloader`
 
 Alternatively you can download **application** folder in your system. After that you must install below requirements;
 ```
 pip install arrow
 pip install request
 pip install pandas
 ```
 
 And then you can just run the **__main__.py** file in your terminal for the execution.
 
 # Requirements
 Application works in Python version 3.6 or higher!
