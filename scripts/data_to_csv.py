import re
import csv


with open('info.txt') as file:#opens the input file contains raw data
    x = file.read()#read the input file
    content = re.split('\n', x)#split by using newline 
    example=csv.writer(open('emp.csv', 'w'), delimiter=',')#creates emp.csv file in write mode
    example.writerow(['Id', 'Name', 'Date of joining', 'Education', 'Location'])#writes headers of csv
    id=1
    for i in content:
        if i is '':
            break
        else:
            name = re.findall('NAME : (.*?)\,', i)[0]
            doj = re.findall('DOJ : (.*?)\,', i)[0]
            edu = re.findall('EDU : (.*?)\,', i)[0]
            loc = re.findall('LOC : (.*)', i)[0]
            example.writerow([id, name, doj, edu, loc])#writes info to rows
            id+=1
