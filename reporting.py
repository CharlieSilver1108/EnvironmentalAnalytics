# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import csv
import numpy as np

def calc_pollutant_value(pollutantName):
    """Returns the column number for the pollutant the user has chosen"""
    if pollutantName == "no":
        pollutantColumn = 2
    elif pollutantName == "pm10":
        pollutantColumn = 3
    elif pollutantName == "pm25":
        pollutantColumn = 4
    return(pollutantColumn)

def daily_average(data, monitoring_station, pollutant):
    """Returns a list with the daily averages (365 values) for a particular pollutant and monitoring station"""
    pollutantColumn = calc_pollutant_value(pollutant)
    dailyAverage = []
    fulldailyAverages = []
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)        #skip first line (column headings)   
        j = 1     
        for row in csv_reader:
            if row[pollutantColumn] != "No data":
                dailyAverage.append(float(row[pollutantColumn]))
            j += 1
            if j == 25:
                try:
                    average = np.average(dailyAverage)
                except:
                    average = "No Data"
                fulldailyAverages.append(average)
                dailyAverage = []
                j = 1
    return(fulldailyAverages)
        

def daily_median(data, monitoring_station, pollutant):
    """Returns a list with the daily median (365 values) for a particular pollutant and monitoring station"""
    pollutantColumn = calc_pollutant_value(pollutant)
    dailyMedian = []
    fulldailyMedians = []
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)        #skip first line (column headings)   
        j = 1     
        for row in csv_reader:
            if row[pollutantColumn] != "No data":
                dailyMedian.append(float(row[pollutantColumn]))
            j += 1
            if j == 25:
                try:
                    median = np.median(dailyMedian)
                except:
                    median = "No Data"
                fulldailyMedians.append(median)
                dailyMedian = []
                j = 1
    return(fulldailyMedians)


def hourly_average(data, monitoring_station, pollutant):
    """Returns a list with the hourly averages (24 values) for a particular pollutant and monitoring station"""
    pollutantColumn = calc_pollutant_value(pollutant)
    hourlyAverage = np.empty((24,365))
    fullhourlyAverage = []
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)                                        #skips first line (column headings)
        hour = 0
        day = 0
        for row in csv_reader:
            if row[pollutantColumn] != "No data":
                hourlyAverage[hour,day] = (float(row[pollutantColumn]))
            hour += 1
            if hour == 24:
                hour = 0
                day += 1
        for i in range (0,23):
            try:
                average = np.nanmean(hourlyAverage[i])          #nanmean ignores values that are NotANumber
            except:
                average = "No Data"
            fullhourlyAverage.append(average)
    return(fullhourlyAverage)


def monthly_average(data, monitoring_station, pollutant):
    """Returns a list with the monthly averages (12 values) for a particular pollutant and monitoring station"""
    pollutantColumn = calc_pollutant_value(pollutant)
    monthlyAverage = []
    fullmonthlyAverages = []
    previousMonth = "1"
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)                                        #skips first line (column headings)
        for row in csv_reader:
            currentMonth = str(row[0])
            currentMonth = currentMonth[6]                      #gets the month of the current row
            if currentMonth != previousMonth:                   #checks if the data is for a new month, if it is then it calculates the average and stores it in another list
                previousMonth = currentMonth
                try:
                    average = np.nanmean(monthlyAverage)
                except:
                    average = "No Data"
                fullmonthlyAverages.append(average)
                monthlyAverage = []
            elif row[pollutantColumn] != "No data":
                monthlyAverage.append(float(row[pollutantColumn]))
        try:                                                    #calculates the average for december since it is not included in the for loop
            average = np.nanmean(monthlyAverage)
        except:
            average = "No Data"
        fullmonthlyAverages.append(average)
    return(fullmonthlyAverages)
            

def peak_hour_date(data, date, monitoring_station, pollutant):
    """For a given date (eg 2021-01-01) returns the hour of the day with the highest pollution level and its corresponding value (eg (12:00, 14.8))"""
    pollutantColumn = calc_pollutant_value(pollutant)
    peakHourValue = 0
    peakHour = None
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)                                        #skips first line (column headings)
        for row in csv_reader:
            valid = False
            if row[0] == date:                                  #if the date of the row is the date the user enterred, then checks if the value is greater than the current max
                pollutantValue = row[pollutantColumn]
                try:
                    pollutantValue = float(pollutantValue)
                    valid = True
                except:
                    valid = False
                if valid:
                    if pollutantValue > peakHourValue:
                        peakHourValue = pollutantValue
                        peakHour = row[1]
    return(peakHourValue, peakHour)


def count_missing_data(data,  monitoring_station, pollutant):
    """For a given monitoring station and pollutant, returns the number of 'No data' entries are there in the data"""
    pollutantColumn = calc_pollutant_value(pollutant)
    count = 0
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)                                    #skips first line (column headings)
        for row in csv_reader:
            if row[pollutantColumn] == "No data":
                count += 1                                  #adds 1 to the count if the value is 'No data'
    return(count)


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    """For a given monitoring station and pollutant, returns a copy of the data with the missing values 'No data' replaced by the value in the parameter new value"""
    pollutantColumn = calc_pollutant_value(pollutant)
    newDataArray = []
    with open(data) as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)                                    #skips first line (column headings)
        for row in csv_reader:
            if row[pollutantColumn] == "No data":           #if the value is 'No data', then new_value is added to the list. Otherwise, the actual value is added
                newDataArray.append(str(new_value))
            else:
                newDataArray.append(row[pollutantColumn])
    return(newDataArray)