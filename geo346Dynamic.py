import requests
import sys
import time
import csv


def weatherStationGetter(inCSV,outCSV, stationNameField,latitudeNameField,longitudeNameField):
    """
    Function gets weather station data from the Open Weather API. File takes in a CSV file where station name, 
    latitude and longitude field names are specififed. 
    Returned is a CSV file with weather data from the stations with the following field names:
        - "Name","Longitude","Latitude","Temperature","Pressure","Humidity","Wind","Clouds","Rain", "Snow"
    Keywords:
        inCSV              -- the csv file to read station name, latitude and longitude field names.
        outCSV             -- the csv file to write final output to.
        stationNameField   -- The field name for the name of the station from inCSV.
        LatitudeNameField  -- The field name for the latitude from inCSV.
        LongitudeNameField -- The field name for the longitude from inCSV.
    
    """
    #Getting lists of the stationName, latitude and longitude
    stationName,lat,lon = fileReader(inCSV,stationNameField,latitudeNameField,longitudeNameField)
    #CSV header Names and the final list to write output csv file. 
    stationList = [["Name","Longitude","Latitude","Temperature","Pressure","Humidity","Wind","Clouds","Rain", "Snow"]]
    for i in range(len(stationName)):
        station = APICaller(lat[i],lon[i]) #gets weather data as JSON/dict
        print("Station Data: \n{0}\n\n".format(station))
        stat = [stationName[i],lat[i],lon[i],"NA","NA","NA","NA","NA","NA","NA"] #prepares the row   
        for key,value in station.items():
            if key == "main":
                stat[3] = station[key]['temp'] - 273
                stat[4] = station[key]['pressure']
                stat[5] = station[key]['humidity']
            elif key == "wind":
                stat[6] = station[key]['speed']
            elif key == "clouds":
                stat[7] = station[key]['all']
            elif key == "rain":
                if "3h" in station[key]:
                    stat[8] = str(station[key]['3h']) + "3h"
                else:
                    stat[8] = str(station[key]['1h']) + "1h"
            elif key == "snow":
                if "3h" in station[key]:
                    stat[8] = str(station[key]['3h']) + "3h"
                else:
                    stat[8] = str(station[key]['1h']) + "1h"

        print("Data Taken: \n{0}\n\n".format(stat))
        time.sleep(5) #makes sure not to call API too quickly.
        stationList.append(stat) #appends finished row

    fileWriter(outCSV,stationList) #writes the final output
    print("Done!")

def fileReader(inCSV,stationNameField,latitudeNameField,longitudeNameField):
    """Reads a csv file. returns 3 lists: Station Names, Latitudes, Longitudes
        Keywords:
            inCSV -- File Path to csv
            stationNameField -- Field Name for name of weather stations
            latitudeNameField -- Field Name for weather stations latitude
            longitudeNameField -- Field name for weather stations longitude
    """
    stationName = []
    lat = []
    lon = []
    with open(inCSV, 'rb') as csvfile:
        stationsLatLong = csv.reader(csvfile,delimiter=",")
        fieldNames = stationsLatLong.next() #gets the field names of the CSV file
        stationNameIndex = fieldNames.index(stationNameField)
        latIndex = fieldNames.index(latitudeNameField)
        lonIndex = fieldNames.index(longitudeNameField)
        for row in stationsLatLong:
            stationName.append(row[stationNameIndex])
            lat.append(row[latIndex])
            lon.append(row[lonIndex])

    return (stationName,lat,lon)

def fileWriter(outCSV,stationList):
    """Writes a csv file.
        Keywords:
            outCSV -- Name of csv
            stationList -- The 2D list used to create the CSV
    """
    with open(outCSV,"wb") as f:
        writer = csv.writer(f)
        writer.writerows(stationList)

def APICaller(lat, lon):
    """Calls the Open Weather API for weather station data using the latitude and longitude location.
       Returns a JSON file for weather data. 
    """
    #The URL link to call when getting data from Open Weather Map
    #API KEY = 0e16583042dcdf9bb5561b5d406540ce
    weather = lambda lat,lon :"http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&APPID=0e16583042dcdf9bb5561b5d406540ce".format(lat, lon)
    stationJSON = lambda lat,lon: requests.get(weather(lat,lon)).json()
    return stationJSON(lat,lon)


weatherStationGetter('Weather-Stations.csv','WeatherStationData2.7.csv',"Station_Na","Latitude__","Longitude_")

