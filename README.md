# ML-Firewall
Machine learning based fire wall

BurpSuit has been used to create the log files and any web crawler can be used to scan through the site.

I have used Acunetix Web vulnerability scanner and used BurpSuit as a proxy to intercept the requests.
The log file contains Base64 encoded raw requests that gets decoded and made into a csv using the log parser.(It uses Python 2.7)

The csv file is trained using PyCaret. I have used 2 models, Kmeans and Logistic Regression.
