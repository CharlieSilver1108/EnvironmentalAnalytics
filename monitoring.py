# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import requests
import datetime
import numpy as np
import re

def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()



def get_today_data(siteCode, speciesCode):
    """This returns all the data values of a chosen pollutant and site from today"""
    data = get_live_data_from_api(siteCode, speciesCode)        #uses the function provided to receive the json

    dict = data["RawAQData"]                                    #ensures that 'dict' is the dictionary of the data values
    dict = dict["Data"]

    values = []
    for entry in dict:                                          #for each value that exists in today's dictionary, adds it to an array with the time
        date = entry["@MeasurementDataGMT"]
        time = date[11:]
        value = entry["@Value"]
        toAppend = time + ": " + value
        values.append(toAppend)
    
    return(values)                                              #returns the list



def rm_search_site_codes(*args, **kwargs):
    """This checks whether a site code exists in London and returns the result"""
    groupName = args[0]
    siteCodeToCheck = args[1]
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName={group_name}/Json"
    
    url = endpoint.format(
        group_name = groupName
    )

    result = requests.get(url)
    data = result.json()

    dict = data["Sites"]
    dict = dict["Site"]                                         #ensures that 'dict' is the dictionary of the sites

    for site in dict:                                           #linear search through the dictionary to see if the site code exists
        if site["@SiteCode"] == siteCodeToCheck:
            return("Valid Code for " + site["@SiteName"])       #if the code exists in the dictionary then the site name is returned
    return("Invalid Site Code")                                 #if the code is not in the dictionary then the previous return statement will not be executed and instead 'Invalid Site Code' is returned


def rm_search_species_codes(*args,**kwargs):
    """This returns of the codes of the commmonly monitored species"""
    speciesCodeToCheck = args[0]
    url = "https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json"
    result = requests.get(url)
    data = result.json()

    dict = data["AirQualitySpecies"]
    dict = dict["Species"]                                              #ensures that 'dict' is the dictionary of the sites

    for species in dict:                                                #linear search through the dictionary to see if the site code exists
        if species["@SpeciesCode"] == speciesCodeToCheck:
            return("Valid code for " + species["@SpeciesName"])         #if the code exists in the dictionary then the speices name is returned
    return("Invalid Species Code")                                      #if the code is not in the dictionary then the previous return statement will not be executed and instead 'Invalid Site Code' is returned



def rm_print_spieces_info(*args,**kwargs):
    """Returns information about whichever species the user chooses"""
    speciesCode = args[0]
    
    speciesCodeFormatCheck = re.findall("[A-Z]+[1-9]?", speciesCode)                #RegEx check to ensure that the spieces code is of the correct format  
    if not speciesCodeFormatCheck:
        return("Your species code is not of a valid format")

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/Species/SpeciesCode={speciesCode}/Json"

    url = endpoint.format(speciesCode = speciesCode)

    result = requests.get(url)
    result = result.json()

    try:                                                                            #if the code exists then compiles all the data about the pollutant
        dict = result["AirQualitySpecies"]
        dict = dict["Species"]
        speciesName = dict["@SpeciesName"]
        description = dict["@Description"]
        healthEffect = dict["@HealthEffect"]
        link = dict["@Link"]
        to_print = ("Species Name: " + speciesName + "\nDescription: " + description + "\nHealth Effect: " + healthEffect + "\nLink: " + link)
    except:
        to_print = ("Invalid Species Code")                                         #if the code does not exist then returns that it is invalid

    return(to_print)

    

def rm_return_average(*args,**kwargs):
    """Returns the average of the last x values for whichever species and site the user chooses"""
    valid = False
    
    numOfValues = args[0]
    numOfDays = (numOfValues // 24) + 1                                                 #floor division to calculate the number of days required to be requested from the API
    
    siteCode = args[1]
    speciesCode = args[2]

    siteCodeFormatCheck = re.findall("[A-Z]+[1-9]?", siteCode)                          #RegEx check to ensure that the site and spieces codes are of the correct format
    speciesCodeFormatCheck = re.findall("[A-Z]+[1-9]?", speciesCode)

    if not (siteCodeFormatCheck and speciesCodeFormatCheck):
        return(valid, "Your site code or species code is not of a valid format")

    endDate = datetime.date.today()
    startDate = endDate - datetime.timedelta(days=numOfDays)

    data = get_live_data_from_api(siteCode,speciesCode,startDate,endDate)

    values = []
    dict = data["RawAQData"]
    dict = dict["Data"]
    for entry in dict:
        try:
            value = float(entry["@Value"])                      #for each value in the returned data, attempt to append a float, if not possible, then append 'No data'
        except:
            value = "No data"
        values.append(value)
    
    values = values[-numOfValues:]                              #takes the final x values specified by the user
    
    try:
        average = np.nanmean(values)                            #if there were data values from the API then the mean is calculated
        valid = True
    except:
        average = "Error calculating average. There may not be any data"    #if the data was entirely 'No Data' then an error message is returned
    return(valid, average)



def rm_return_highest_pollutant(*args, **kwargs):
    """Returns which pollutant has the worst AirQualityIndex for whichever site the user chooses"""
    siteCode = args[0]
    siteCodeFormatCheck = re.findall("[A-Z]+[1-9]?", siteCode)
    if not siteCodeFormatCheck:
        return("Your site code is not of a valid format")                                           #RegEx check to ensure that the site and spieces codes are of the correct format

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Hourly/MonitoringIndex/SiteCode={site_code}/Json"
   
    url = endpoint.format(
        site_code = siteCode,
    )

    result = requests.get(url)
    result = result.json()

    try:                                                                                 #if the site code is valid then the dictionary exists
        dict = result["HourlyAirQualityIndex"]
        dict = dict["LocalAuthority"]
        dict = dict["Site"]
        dict = dict["species"]

        speciesArray = []
        maxValue = 1

        for species in dict:                                                            #for each species, checks if it is the new max or if it is the same as the current max
            airQualityIndex = species["@AirQualityIndex"]                               #if it's the new max, the list is deleted and the current max updated
            try:                                                                        #if it's equal to the max, it's added to the list
                airQualityIndex = int(airQualityIndex)                                  #if it's less than the max, continues
                speciesName = species["@SpeciesName"] 
                if airQualityIndex > maxValue:
                    speciesArray = [speciesName]
                    maxValue = airQualityIndex
                elif airQualityIndex == maxValue:
                    speciesArray.append(speciesName)
            except:
                continue

        if len(speciesArray) > 0:
            to_return = ", ".join(speciesArray)
            to_return = to_return + (" have the worst AirQualityIndex of " + str(maxValue))
        else:
            to_return = "No Data"                                                   #if there is a speices with a max value then it is returned, if not then 'No Data' is returned
    except:
        to_return = "Invalid Site Code"

    return(to_return)



def return_highest_average_and_median(*args, **kwargs):
    """Returns which pollutant has the highest average and which has the highest median for today for whichever site the user chooses"""
    siteCode = args[0]
    
    siteCodeFormatCheck = re.findall("[A-Z]+[1-9]?", siteCode)                #RegEx check to ensure that the spieces code is of the correct format  
    if not siteCodeFormatCheck:
        return("Your site code is not of a valid format")

    startDate = datetime.date.today()
    endDate = startDate + datetime.timedelta(days=1)

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json"

    url = endpoint.format(
        site_code = siteCode,
        start_date = startDate,
        end_date = endDate
    )

    values = []
    maxAverage = 0
    maxMedian = 0
    valid = False

    try:                                                                            #if the code exists then compiles all the data about the pollutant
        result = requests.get(url)
        data = result.json()

        dict = data["AirQualityData"]
        dict = dict["Data"]

        currentSpecies = dict[1]["@SpeciesCode"]

        for entry in dict:
            if entry["@SpeciesCode"] == currentSpecies:
                #add value to current array
                value = entry["@Value"]
                if value != "":
                    value = float(value)
                    values.append(value)
            else:
                #calculate mean and median
                if len(values) > 0:
                    currentAverage = np.nanmean(values)
                    currentMedian = np.nanmedian(values)
                    valid = True
                    if currentAverage > maxAverage:
                        maxAverage = currentAverage
                        maxAverageName = currentSpecies
                    if currentMedian > maxMedian:
                        maxMedian = currentMedian
                        maxMedianName = currentSpecies
                currentSpecies = entry["@SpeciesCode"]
                values = []

        if valid:
            maxAverage = round(maxAverage, 2)
            maxMedian = round(maxMedian, 2)
            to_print = "The pollutant with the highest average of " + str(maxAverage) + " was " + maxAverageName + ". The pollutant with the highest median of " + str(maxMedian) + " was " + maxMedianName
            return(to_print)
        else:
            return("No Data")

    except:
        return("Invalid Site Code")                                         #if the code does not exist then returns that it is invalid
