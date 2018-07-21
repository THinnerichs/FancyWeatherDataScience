import csv
import geocoder

import matplotlib.pyplot as plt
import numpy as np
import datetime


# How to display the trend of some data
def analyse(city, criteria_list, min_year = 2000, max_year = 2018):
    if city == "" or criteria_list == []:
        return {}

    years = range(min_year, max_year, 1)
    months = range(1, 13)

    trend_dict= {}

    for year in years:
        for month in months:
            with open(file="./data/{}-{}.csv".format(str(year), str(month)), mode='r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                header_row = ""
                for row in reader:
                    if "1-name" in row:
                        header_row = row
                    elif city in row:
                        for i in range(len(row)):
                            if header_row[i] in criteria_list:
                                try:
                                    trend_dict[(year,month,header_row[i])] = int(row[i])
                                except ValueError:
                                    pass
    return trend_dict

def criteria_over_time(criteria_list, city_list, temp_dict, min_year = 2000, max_year = 2018):
    years = range(min_year, max_year, 1)
    months = range(1, 13)

    city_criteria_dict = {}
    for criteria in criteria_list:
        for city in city_list:

            temp_list = [-1]*len(years)*len(months)
            for year in years:
                for month in months:
                    try:
                        temp_list[(year-2000)*12+month-1] = temp_dict[(year, month, criteria)]
                    except KeyError:
                        index = (year-2000)*12+month-1
                        if index >0:
                            temp_list[index] = temp_list[index-1]
            city_criteria_dict[(city, criteria)] = temp_list
    return city_criteria_dict

def analyse_FAOSTAT():
    complete_dict = {}

    with open(file ="FAOSTAT_data_7-21-2018.csv", mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter= ',')
        first = True
        header_row = ""
        for row in reader:
            if first:
                header_row = row
                first = False
                for i in range(len(header_row)):
                    complete_dict[header_row[i]] = []
            else:
                for i in range(len(header_row)):
                    complete_dict[header_row[i]].append(row[i])

    plt.plot(complete_dict["Year"],[int(x) for x in complete_dict["Value"]])
    plt.grid()
    plt.ylabel("Production Quantity in tonnes")
    plt.xlabel("Year")
    plt.show()


def geo():
    city_list = []

    with open(file="./data/2000-1.csv", mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter= ',')
        for row in reader:
            if len(row)>=5 and row[2] != "1-name" and row[2].strip != "":
                try:
                    print("City:", row[2])
                    lat = int(row[3])/100.0
                    lon = int(row[4])/100.0

                    g = geocoder.google([lat, lon], method='reverse')
                    if g.country_long in ['India']:
                        city_list.append(row[2])
                except ValueError:
                    pass
    print("City list:", city_list)


def main():


    city_list = ['GUWAHATI', 'CHERRAPUNJI', 'DALTONGANJ', 'JAGDALPUR', 'CHENNAI MINAMBAKKAM', 'BANGALORE']
    #['BILMA', 'MALAKAL', 'WAU', 'JUBA', 'GORE', 'ADDIS ABABA', 'METEHARA']

    years = range(2000, 2018, 1)
    months = range(1, 13)

    for city in city_list:
        x = np.array([year+month/12.0 for year in years for month in months])
        criteria_list = ["4.21-liquid precipitation amount (mm)"]#"4.8-mean air temperature (0.1 C)", "6.13-number of days with precipitation amount >= 1,0 mm", "6.1-number of days with Tmax >= 25,0 C (summer days)", "5.25-monthly precipitation amount (mm)" , "4.22-quintile, 0 less than any value in the last 30 years, ..., 6 greater than any value in the last 30 years"]#
        # , "6.2-number of days with Tmax >= 30,0 C (hot days)", "6.5-number of days with Tmax >= 35,0 C","6.6-number of days with Tmax >= 40,0 C"]
        #, , ]
        #, "4.23-number of days measured >= 1 mm", "4.13-mean maximum air temperature (0.1 C)",
        y_list = []

        temp_dict = analyse(city=city, criteria_list=criteria_list)

        for criteria in criteria_list:
            y_list.append((np.array(criteria_over_time([criteria], city_list, temp_dict)[(city, criteria)]), criteria))

        for y in y_list:
            plt.plot(x,y[0],'r')
            plt.xlabel(city)
            plt.ylabel(y[1])
            plt.grid()
            plt.show()



    """
    #get amount of set data
    name_list = []
    with open(file="./data/2000-1.csv", mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter= ',')
        for row in reader:
            if len(row)>=2 and row[2] != "1-name" and row[2].strip != "":
                length = len(analyse(city= row[2]))
                print("City:", row[2], "Amount data:", length)
                name_list.append((row[2], length))
    """


if __name__ == '__main__':
    main()