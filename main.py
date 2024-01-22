# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

from reporting import *
from intelligence import *
from monitoring import *

def main_menu():
    """This main menu function runs on start. It allows the user to select which module to run"""
    print()
    print("Welcome to the Main Menu!")
    options = "R - Access the PR module \nI - Access the MI module \nM - Access the RM module \nA - Print the About text \nQ - Quit the application"
    choice = None
    while choice!="Q":                              #Repeats until the user either quits or inputs a valid module letter
        print(options)
        choice = input("Enter your choice: ").upper()   #.upper() means the user can input either upper or lower case letters for the modules
        if choice == "R":
            reporting_menu()
        elif choice == "I":
            intelligence_menu()
        elif choice == "M":
            monitoring_menu()
        elif choice == "A":
            about()
        elif choice == "Q":
            quit()
        else:
            print("\nPlease only enter a valid choice: R, I, M, A, or Q.")
            print()   

def reporting_menu():
    """This reporting menu function runs when the user inputs R in the main menu. It allows the user to choose which reporting function to use on a pollutant and location of their choosing"""
    print()
    print("Welcome to the Reporting Menu!")
    pollutant = check_pollutant()
    print()    
    data, station = check_station()
    reportingOptions = "1 - Daily Average \n2 - Daily Median \n3 - Hour Average \n4 - Monthly Average \n5 - Peak Hour Date \n6 - Count Missing Data \n7 - Fill Missing Data \nM - Main Menu"
    choice = None
    while choice!="M":                      #Repeats until the user either returns to the main menu or inputs a valid function code
        print()
        print(reportingOptions)
        choice = input("Enter your choice: ").upper()
        if choice == "1":
            dailyAverages = daily_average(data, station, pollutant)
            print(dailyAverages)
        elif choice == "2":
            dailyMedians = daily_median(data, station, pollutant)
            print(dailyMedians)
        elif choice == "3":
            hourlyAverages = hourly_average(data, station, pollutant)
            print(hourlyAverages)
        elif choice == "4":
            monthlyAverages = monthly_average(data, station, pollutant)
            print(monthlyAverages)
        elif choice == "5":
            date = check_date()
            peakHourValue, peakHour = peak_hour_date(data, date, station, pollutant)
            print(str(peakHour), str(peakHourValue))
        elif choice == "6":
            count = count_missing_data(data, station, pollutant)
            print("There are " + str(count) + " No Datas")
        elif choice == "7":
            newData = new_data()
            newDataArray = fill_missing_data(data, newData, station, pollutant)
            print(newDataArray)
        elif choice == "M":
            print("Returning to Main Menu")
            break
        else:
            print("\nPlease only enter a valid choice: 1, 2, 3, 4, 5, 6, 7, or M.")
            print()
    main_menu()

def check_pollutant():
    """I added this function to check which pollutant the user would like to perform the reporting functions on"""
    pollutantOptions = "1 - no \n2 - pm10 \n3 - pm25"
    choice = None
    while (choice!="1") and (choice!="2") and (choice!="3"):
        print(pollutantOptions)
        choice = input("Which pollutant? ")
        if choice == "1":
            return("no")
        elif choice == "2":
            return("pm10")
        elif choice == "3":
            return("pm25")
        else:
            print("\nPlease only enter a valid choice: 1, 2, or 3.")
            print()

def check_station():
    """I added this function to check which monitoring station the user would like to perform the reporting functions on"""
    stationOptions = "H - Harrington \nM - Marylebone \nK - North Kensington"
    choice = None
    while (choice!="H") and (choice!="M") and (choice!="K"):
        print(stationOptions)
        choice = input("Which station? ").upper()
        if choice == "H":
            return("data/Pollution-London Harlington.csv", "Harrington")
        elif choice == "M":
            return("data/Pollution-London Marylebone Road.csv", "Marylebone")
        elif choice == "K":
            return("data/Pollution-London N Kensington.csv", "Kensington")
        else:
            print("\nPlease only enter a valid choice: H, M, or K.")
            print()

def check_date():
    """I added this function to check which date the user would like to perform the peak_hour_date function with"""
    print()
    year = month = day = None  
    valid = False
    while valid == False:                   #Ensures the user enters a valid year
        year = input("Enter the year: ")
        try:
            year = int(year)
            if year == 2021:
                valid = True
            else:
                print("Please enter a valid year")
        except:
            valid = False
    valid = False
    while valid == False:                   #Ensures the user enters a valid month
        month = input("Enter the month: ")
        try:
            month = int(month)
            if 0 <= month <= 9:
                valid = True
                month = "0" + str(month)
            elif 10 <= month <= 12:
                valid = True
            else:
                print("Please enter a valid month")
        except:
            valid = False
    valid = False
    while valid == False:                   #Ensures the user enters a valid day
        day = input("Enter the day: ")
        try:
            day = int(day)
            if 1 <= day <= 9:
                valid = True 
                day = "0" + str(day)
            elif 10 <= day <= 31:
                valid = True
            else:
                print("Please enter a valid day")
        except:
            valid = False
    date = str(year) + "-" + str(month) + "-" + str(day)
    return(date)

def new_data():
    """I added this function to check which date value the user would like to use instead of 'No data' in the new_data function"""
    print()
    valid = False
    while valid == False:
        newData = input("Enter the new value: ")
        try:
            newData = float(newData)
            return(newData)
        except:
            valid = False
            print("Please ensure the input is a number")
    


def intelligence_menu():
    """This intelligence menu function runs when the user inputs I in the main menu. It allows the user to choose which intelligence function to use on the marylebone map"""
    print("Welcome to the Intelligence Menu!")
    intelligenceOptions = "1 - Find Red Pixels \n2 - Find Cyan Pixels \n3 - Detect Connected Components \n4 - Detect Connected Components Sorted \nM - Main Menu"
    choice = None
    while choice!="M":              #Repeats until the user either returns to the main menu or inputs a valid function code
        print()
        print(intelligenceOptions)
        choice = input("Enter your choice: ").upper()
        if choice == "1":
            find_red_pixels('data/map.png')
        elif choice == "2":
            find_cyan_pixels('data/map.png')
        elif choice == "3":
            IMG = check_image()
            detect_connected_components(IMG)
        elif choice == "4":
            IMG = check_image()
            MARK = detect_connected_components(IMG)
            detect_connected_components_sorted(MARK)
        elif choice == "M":
            print("Returning to Main Menu")
            break
        else:
            print("\nPlease only enter a valid choice: 1, 2, 3, 4, or M.")
    main_menu()


def check_image():
    IMGoptions = "1 - map-red-pixels.jpg \n2 - map-cyan-pixels.jpg"
    choice = None
    while choice != "1" and choice != "2":                      #Repeats until the user either returns to the main menu or inputs a valid function code
        print()
        print(IMGoptions)
        choice = input("Enter your choice: ").upper()
        if choice == "1":
            return("data/map-red-pixels.jpg")
        elif choice == "2":
            return("data/map-cyan-pixels.jpg")
        else:
            print("Please only enter a vlid choice: 1 or 2")



def monitoring_menu():
    """This monitoring menu function runs when the user inputs M in the main menu. It allows the user to choose which monitoring function to use on the API"""
    monitoringOptions = "1 - Get Today's Data \n2 - Check Site Code \n3 - Check Species Code \n4 - Display Pollutant Information \n5 - Average of Previous x Values \n6 - Get Highest AirQualityIndex \n7 - Get Highest Average and Median\nM - Main Menu"
    choice = None
    while choice!="M":                      #Repeats until the user either returns to the main menu or inputs a valid function code
        print()
        print(monitoringOptions)
        choice = input("Enter your choice: ").upper()
        if choice == "1":
            siteCode = get_site_code()
            speciesCode = get_species_code()
            liveData = get_today_data(siteCode, speciesCode)
            print(liveData)
        elif choice == "2":
            groupName = get_group_name()
            codeToSearch = get_site_code()
            print(rm_search_site_codes(groupName, codeToSearch))
        elif choice == "3":
            codeToSearch = get_species_code()
            print(rm_search_species_codes(codeToSearch))
        elif choice == "4":
            print()
            siteCode = get_species_code()
            print(rm_print_spieces_info(siteCode))
        elif choice == "5":
            siteCode = get_site_code()
            speciesCode = get_species_code() 
            numValues = get_number_of_values()
            valid, average = rm_return_average(numValues,siteCode,speciesCode)
            if valid:
                print("The average of the last " + str(numValues) + " values is " + str(average))
            else:
                print(average)
        elif choice == "6":
            siteCode = get_site_code()
            print(rm_return_highest_pollutant(siteCode))
        elif choice == "7":
            siteCode = get_site_code()
            returned =  return_highest_average_and_median(siteCode)
            print(returned)
        elif choice == "M":
            print("Returning to Main Menu")
            break
        else:
            print("\nPlease only enter a valid choice: 1, 2, 3, 4, 5, or M.")
    main_menu()

def get_number_of_values():
    valid = False
    while valid == False:
        numOfValues = input("How many values would you like to include? ")
        try:
            numOfValues = int(numOfValues)
            return(numOfValues)
        except:
            print("Please ensure you enter an integer value")
    get_number_of_values()

def get_site_code():
    """I added this function to check the site code to be used for API requests"""
    print()
    choice = input("Enter the site code you wish to use: ")
    return(choice)
    
def get_species_code():
    """I added this function to check the species code to be used for API requests"""
    print()
    choice = input("Enter the species code you wish to use: ")
    return(choice)

def get_group_name():
    """I added this function to check the group name to be used for API requests"""
    print()
    choice = input("Enter the group name you wish to use: ")
    return(choice)


def about():
    """This about function runs when the user inputs A in the main menu. It deisplays the module code and my candidate number"""
    moduleCode = "ECM1400"
    candidateNumber = "242303"
    print("\nModule Code: " + moduleCode + ". Candidate Number: " + candidateNumber)
    main_menu()



def quit():
    """This quit function runs when the user inputs Q in the main menu. It ends the program"""
    print("\nThank you for using this program")
    exit()


if __name__ == '__main__':
    main_menu()