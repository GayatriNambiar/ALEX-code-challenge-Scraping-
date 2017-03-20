from bs4 import BeautifulSoup
import requests
import csv
import urllib
import pandas as pd

url ="http://www.nyit.edu/academics/courses"
data = requests.get(url)

soup = BeautifulSoup(data.content, "lxml")
##print(soup)
l =[]



div = soup.find('div' , {'class': 'table-wrap MEDdata'})
#print(div)

table = div.find('table', {'id':'course_catalog_table'})


for row in table.findAll("a"):
        l.append(row.text)

links = []

for i in l[::2]:
    #print(i)
    link  = "http://www.nyit.edu/academics/courses/?cs="+i+"&cal=PROF"
    links.append(link)
    


Allinfo=[]
name = []
title = []
credits = []
school=[]
description=[]
coursedescription=[]
prereq_classroomhrs=[]


for i in links:
    new = requests.get(i)
    soup_new = BeautifulSoup(new.content.decode(encoding='UTF-8'), "lxml")
    tb = soup_new.find("table", {"id":"course_catalog_table"})
    
    for j in tb.findAll("td"):
       Allinfo.append(j.text)
#print(Allinfo)
for i in Allinfo[::5]:
		name.append(i)
#print(name)
for i in Allinfo[1::5]:
		title.append(i)
for i in Allinfo[2::5]:
		credits.append(i)
for i in Allinfo[3::5]:
		school.append(i)
for i in Allinfo[4::5]:
		description.append(i)
for i in description:
    		i = i.strip()
		coursedescription.append(i.split('\t')[0])
		try:
			prereq_classroomhrs.append(i.split('\t')[-1])
		except:
			pass
		   	
    
df=pd.DataFrame()
df=pd.DataFrame(name, columns=['Course ID'])
df1=pd.DataFrame()
df1=pd.DataFrame(title, columns=['Course Title'])
df2=pd.DataFrame()
df2=pd.DataFrame(credits, columns=['Course Credits'])
df3=pd.DataFrame()
df3=pd.DataFrame(school, columns=['School Name'])
df4=pd.DataFrame()
df4=pd.DataFrame(coursedescription, columns=['Course Description'])
df5=pd.DataFrame()
df5=pd.DataFrame(prereq_classroomhrs, columns=['Course Pre-requisists & class room hours'])

df6=pd.DataFrame()
df6=pd.concat([df,df1,df2,df3,df4,df5], axis=1)

df6.to_csv(r'nyit_med_CoursesData.csv', header='True', index= 'False', encoding = 'utf-8')



