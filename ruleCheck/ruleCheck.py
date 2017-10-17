import argparse as arg
import pandas as pd
import numpy as np
import xlwings as xw
import os
import shutil
import time


#parser = arg.ArgumentParser()
#parser.add_argument("-g", default="total", help="machine group")
#args = parser.parse_args()

smonth = "2017.09"
stable = "行为规范表"
sfolder = smonth + "月" + stable

fnamelist = "list.name.csv"
frulelist = "list.rule.csv"
frecord = smonth + ".record.csv"

fnamesave = smonth +".summary.name.csv"
frulesave = smonth +".summary.rule.csv"

aname = pd.read_csv(fnamelist, header=None, usecols=[0, 1, 2], index_col=0, names=['No', 'name', 'A'])
t = aname.index.duplicated()
aname['duplicated'] = t
print('\n--- Name List ---')
print(aname)
t = aname[aname['duplicated'] == True]
if not t.empty:
    print('--- Error ---')
    print(t)
    exit(0)

arule = pd.read_csv(frulelist, header=None, usecols=[0, 1, 2, 3], index_col=2, names=['group1', 'group2', 'rule', 'score'])
arule.group2.fillna(value='-', inplace=True)
arule['group3'] = arule.group1 + arule.group2
arule['total'] = 0
arule['Nos'] = 'a.'
t = arule.index.duplicated()
arule['duplicated'] = t
print('\n--- Rule List ---')
print(arule)
t = arule[arule['duplicated'] == True]
if not t.empty:
    print('--- Error ---')
    print(t)
    exit(0)

arecord = pd.read_csv(frecord, header=None, usecols=[0, 1, 2], names=['date', 'rule', 'No'])
print('\n--- Record List ---')
print(arecord)

t1 = arecord.values
t2 = []
#print(type(t1))
for i in t1:
    t3 = i[2].split('.')
    #print(type(t3))
    #print(t3)
    t3 = t3[1:]
    #print(t3)
    for j in t3:
        t2.append([j, i[1], i[0], 0])
        #print(t2)

t4 = np.array(t2)
#print(t4.dtype)
brecord = pd.DataFrame(t4, columns=['No', 'rule', 'date', '0'])
print('\n--- Record Detail List ---')
print(brecord)

flag = False
t1 = brecord.groupby(['No']).count()
#print(t1.index)
t2 = t1.index.values.astype(int)
t3 = aname.index.values
t4 = list(set(t2) - (set(t3)))
if t4:
    flag = True
    print('--- Error ---')
    print('--- invalid No ---')
    print(t4)
    for i in t4:
        print(brecord[brecord['No'].astype(int) == i])

t1 = brecord.groupby(['rule']).count()
t2 = t1.index.values
t3 = arule.index.values
t4 = list(set(t2) - (set(t3)))
if t4:
    flag = True
    print('--- Error ---')
    print('--- invalid rule ---')
    print(t4)
    for i in t4:
        print(brecord[brecord['rule'] == i])

t1 = brecord.groupby(['No', 'rule', 'date']).count()
t2 = t1[t1['0'] > 1]
if not t2.empty:
    flag = True
    print('--- Error ---')
    print('--- repeat record ---')
    print(t2)

if flag:
    exit(0)

t1 = arule.groupby(['group1']).count()
t2 = t1.index.values
for i in t2:
    aname[i] = 0

aname['total'] = 100
aname['comment'] = '差'

t1 = arule.groupby(['group3']).count()
t2 = t1.index.values
for i in t2:
    aname[i] = ''

#print(aname)

for iNo in aname.index:
    t1 = brecord[brecord.No.astype(int) == iNo]
    tx = t1.groupby('rule').count().index.values
    for iRule in tx:
        t2 = t1[t1.rule == iRule]
        t3 = t2.date.values
        t4 = arule[arule.index == iRule]
        tgroup1 = t4['group1'].values[0]
        tgroup3 = t4['group3'].values[0]
        tscore = t4['score'].values[0]
        t5 = aname[aname.index == iNo]
        tnoA = t5['A'].values[0]
        #print(tgroup1, tgroup3, tscore, tnoA, iNo, iRule)
        i = 1
        if(tscore < 0 and tnoA == 'A'):
            i = 2
        i1 = 0
        s1 = ''
        for i2 in t3:
            i1 = i1 + tscore*i
            s1 = s1 + i2 + ' '
        #print(i1, s1)

        aname.loc[iNo, tgroup1] = aname.loc[iNo, tgroup1] + i1
        aname.loc[iNo, 'total'] = aname.loc[iNo, 'total'] + i1
        aname.loc[iNo, tgroup3] = aname.loc[iNo, tgroup3] + iRule + '(' + s1 + ') '
        arule.loc[iRule, 'total'] = arule.loc[iRule, 'total'] + 1
        ss = str(iNo)
        arule.loc[iRule, 'Nos'] = arule.loc[iRule, 'Nos'] + ss + '.'

t1 = aname['total'].values
t2 = []
for i1 in t1:
    if i1 >= 90:
        i2 = 'A(优)'
    elif i1 >= 85:
        i2 = 'B(良)'
    elif i1 >= 80:
        i2 = 'C(中)'
    else:
        i2 = 'D(差)'
    t2.append(i2)

aname['comment'] = t2

print(aname)
print(arule)

aname.to_csv(fnamesave)
arule.to_csv(frulesave)

shutil.rmtree(sfolder, ignore_errors=True)
os.mkdir(sfolder)

for iNo in aname.index:
    s1 = '{:02d}'.format(iNo)
    t1 = sfolder + "(" + s1 + ").xlsx"
    t2 = sfolder + r"/" + t1
    t3 = r"规范表模板/小白.xlsx"
    shutil.copyfile(t3, t2)

    wb = xw.Book(t2)
    app = xw.apps.active


    sheet1 = wb.sheets['Sheet1']
    sheet1.range('B5').value = sfolder
    sheet1.range('B6').value = 'No.' + s1
    sheet1.range('D7').value = aname.loc[iNo, 'name']
    sheet1.range('F7').value = aname.loc[iNo, 'total']
    sheet1.range('H7').value = aname.loc[iNo, 'comment']
    tx = arule.groupby('group3').count().index.values
    i = 8
    for j in tx:
        k = 'D' + str(i)
        sheet1.range(k).value = aname.loc[iNo, j]
        i = i + 1

    wb.save()
    #wb.close()

    xw.App.quit(app)
    #time.sleep(1)

    i = 0
    while(True):
        i = i + 1
        appx = xw.apps
        k = True
        for j in appx:
            if( j == app):
                k = False
        if(k):
            s2 = '{:9d}'.format(i)
            print("--- ", s1, " ---", s2, app, "  ", xw.apps.count, xw.apps)
            break
