
# Project Summary

I joined a quant competition recently and have 3months access to the financial database of Refinitiv. Before my access right expires, I want to utilize this data and address some of the problems I met recently.

This project is an exercise to apply package of dash and plotly to visualize data in dashboard in Python. Historical data and tick data for Henry Hub gas price is collected from Refinitiv API using SQL query.

Historical data is available from 2016-11-01 to 2018-10-31, while tick history is available from 2018-10-01 to 2018-12-31.


### Data collection 

* Historical Data (daily): NGc1 and CLc1 collected and saved as Jason file.
* 3 months tick data of NGc1 is collected: each SQL query collect roughly 5 business days of tick data and saved as json file for future use, saved all tick data is impossible because of the volume of data and the computer will run out of memory.

### Dashboard

After collecting those data, I started to build components of the dashboard.

* 1. The first part is basically a comparison chart of gas and oil price. Historically, oil and gas has strong correlation. This graph plots gas price and 13% of oil price together. A date selector is incorporated to choose the period of data
* 2. The second part is calculation of monthly mean, median, max of gas price for the date selected in the selector.
* 3. The thrid part is to compute monthly min, max and median for the tick data. Because of the large volume of data, we can't load the entire month of tick data, so for min and max, we need to load tick data of 5 days and compute their respectively min and max. We then find the monthly min and max. 

For the median is more trickier, what have used is a binning method. Since I know the minimum and maximum of price and length of the data after the first iteration, I separate the interval between minimum and maximum into equally-spaced bins, i.e if the price is between 3-4, I can separate this interval into 10 bins, each of length 0.1. I then go through each data point and which bin this data point belong to. After this second iteration, then I would know the which bin the median belongs to, so the precision of the median is essentially the width of the bin.


* 4. The fourth part is plot of daily price movement and traded volume using tick data. The problem I currently have for this part is that there it is very slow to plot the new graph, beacause tick data for one day has huge volume and at the back end, it takes a long time to load the json file.


