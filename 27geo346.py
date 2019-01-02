"""
Description: This program reads an input csv file with name and lat,long of weather stations, calls openweathermap API to retrieve data
        and writes to an ouput csv file. 

Author: Rikitaro Suzuki
Date: 12/14/18

"""
import requests
import sys
import time
import csv


def weatherStationGetter():
    """Function reads an input csv file with name and lat,long of weather stations, calls openweathermap API to retrieve data
        and writes to an ouput csv file. 
    """
    #API KEY = 0e16583042dcdf9bb5561b5d406540ce
    #A lambda function that returns a URL to call the weather station of interest using latitude and longitude.
    weather = lambda lat,lon :"http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&APPID=0e16583042dcdf9bb5561b5d406540ce".format(lat, lon)
    #uses the requests library to get information and converts json information to a dictionary.
    stationJSON = lambda lat,lon: requests.get(weather(lat,lon)).json()
    #reads input file with station names and their lat longs. fileReader returns 3 lists
    stationName,lat,lon = fileReader('Weather-Stations.csv',"Station_Na","Latitude__","Longitude_")

    #Fieldnames for the output csv.
    stationList = [["Name","Longitude","Latitude","Temperature","Pressure","Humidity","Wind","Clouds","Rain", "Snow"]]
    for i in range(len(stationName)):
        #gets the information from API converted from json to dictionary.
        station = stationJSON(lat[i],lon[i])
        print("Station Data: \n{0}\n\n".format(station))
        #prepares the row for an individual station. "NA" will be changed if information is available.
        stat = [stationName[i],lat[i],lon[i],"NA","NA","NA","NA","NA","NA","NA"]
        #iterates through the dictionary. 
        for key,value in station.items():
            if key == "main":
                stat[3] = station[key]['temp'] - 273 #temperature is measured in kelvin. Converts to celcius.
                stat[4] = station[key]['pressure']
                stat[5] = station[key]['humidity']
            elif key == "wind":
                stat[6] = station[key]['speed']
            elif key == "clouds":
                stat[7] = station[key]['all']
            elif key == "rain":
                if "3h" in station[key]:
                    stat[8] = station[key]['3h']
                else:
                    stat[8] = station[key]['1h']
            elif key == "snow":
                if "3h" in station[key]:
                    stat[8] = station[key]['3h']
                else:
                    stat[8] = station[key]['1h']
        print("Data Taken: \n{0}\n\n".format(stat))
        #API limits number of calls.
        time.sleep(5)
        #appends row
        stationList.append(stat)
    #after all weather station data is found, writes 
    fileWriter('WeatherStationData2.7.csv',stationList)
    print("Done!")

def fileReader(FilePathCSV,stationNameField,latitudeNameField,longitudeNameField):
    """Reads a csv file. returns 3 lists: Station Names, Latitudes, Longitudes
        Keywords:
            FilePathCSV -- File Path to csv
            stationNameField -- Field Name for name of weather stations
            latitudeNameField -- Field Name for weather stations latitude
            longitudeNameField -- Field name for weather stations longitude
    """
    stationName = []
    lat = []
    lon = []
    with open(FilePathCSV, 'rb') as csvfile:
        stationsLatLong = csv.reader(csvfile,delimiter=",")
        fieldNames = stationsLatLong.next()
        stationNameIndex = fieldNames.index(stationNameField)
        latIndex = fieldNames.index(latitudeNameField)
        lonIndex = fieldNames.index(longitudeNameField)
        for row in stationsLatLong:
            stationName.append(row[stationNameIndex])
            lat.append(row[latIndex])
            lon.append(row[lonIndex])
     
    return (stationName,lat,lon)

def fileWriter(fileName,stationList):
    """Takes a 2D array and desired output file name to produce a CSV file
        Keywords:
            fileName -- Desired file name for the output CSV file.
            stationList -- 2D array with station names. 
    """
    with open(fileName,"wb") as f:
        writer = csv.writer(f)
        writer.writerows(stationList)


weatherStationGetter()
