# ML-Firewall
Machine learning based fire wall

BurpSuit has been used to create the log files and any web crawler can be used to scan through the site.

I have used Acunetix Web vulnerability scanner and used BurpSuit as a proxy to intercept the requests.
The log file contains Base64 encoded raw requests that gets decoded and made into a csv using the log parser.(It uses Python 2.7)

The csv file is trained using PyCaret. I have used 2 models, Kmeans and Logistic Regression.

Keep the log files and code in the same folder I have seperated them for better organizing.

I have given a small data set to see if things are working on your machine and fix things before you take a larger data set to work on.
