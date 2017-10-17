import argparse as arg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parser = arg.ArgumentParser()
parser.add_argument("-g", default="total", help="machine group")
args = parser.parse_args()

#plt.figure(figsize=(15, 30))
#ax1 = plt.subplot(311)
#ax2 = plt.subplot(312)

left = 0.1
width = 0.8
spare = 0.1
height = 0.2
bottom1 = 0.1
bottom2 = bottom1 + height + spare
bottom3 = bottom2 + height + spare

ax1 = plt.axes([left, bottom1, width, height])
ax2 = plt.axes([left, bottom2, width, height])
ax3 = plt.axes([left, bottom3, width, height])

#fserver = "1.csv"
fserver = "vboxstat.csv"
fuser = "vboxuser.csv"
flic = "rtdslichistory.csv"

# --- machines ---
a = pd.read_csv(fserver, header=None, usecols=[0,1,2,3])
b = a[(a[1] == args.g)]
c1 = b.iloc[:,0]
c2 = b.iloc[:,[2,3]]
arr = c1.values

c2.columns = ['total machines', 'active machines']
c2.index = pd.to_datetime(arr)
#c2.index = arr

print(type(c2.index))

print(a.head(5))
print(b.head(5))
print(c1[:5])
print(c2[:5])

#plt.sca(ax1)
c2.plot(title='vCloud / Machines', grid=True, ax=ax3, sharex=False)

# --- users ---
ua = pd.read_csv(fuser, header=None, usecols=[0,2,3], index_col=0, parse_dates=True, names=['', 'total users', 'active users'])
print(type(ua.index))
print(ua.head(5))
ua.plot(title='vCloud / Users', grid=True, ax=ax2, sharex=False)

# --- licences ---
la = pd.read_csv(flic, header=None, usecols=[0,1,2], index_col=0, parse_dates=True, names=['', 'total licences', 'active licences'])
print(type(la.index))
print(la.head(5))
la.plot(title='vCloud / Licences', grid=True, ax=ax1, sharex=False)


plt.show()


if __name__ == "__main__":
    print(args.g)
