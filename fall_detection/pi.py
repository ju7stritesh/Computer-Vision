import urllib
link = "http://10.0.0.127:8080" # Change this address to your settings
f = urllib.urlopen(link)
myfile = f.read()
print (myfile)
date = myfile.split(" ")
print (date)
