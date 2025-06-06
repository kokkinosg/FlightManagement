import pandas as pd

class PilotModel:

    possibleAttributes = ["pilotID", "pilotName", "pilotSurname", "gender", "licenseNumber",
                "experienceYears", "aircraftID", "currentLocationID"]

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def getAllPilotsSchedule(self):

        querry = '''SELECT p.pilotName AS Name, p.pilotSurname AS Surname, p.licenseNumber AS "Licence Number", dep.airportName AS "Current Location", arr.airportName AS "Flies to",
        f.departTime AS "Departure Time", f.arrivalTime AS "Arrival Time", a.airline 
        FROM aircraft a, airport dep, airport arr, flights f, pilot p
        WHERE f.aircraftID =  a.aircraftID AND f.pilotID = p.pilotID AND f.toDestinationID= dep.airportID AND f.fromDestinationID = arr.airportID ORDER BY p.licenseNumber
        '''

        df = pd.read_sql_query(querry,self.dbConnection)
        return df
    
    def getAPilotsSchedule(self, licenseNumber):
        querry = '''SELECT p.pilotName AS Name, p.pilotSurname AS Surname, p.licenseNumber AS "Licence Number", dep.airportName AS "Current Location", arr.airportName AS "Flies to",
        f.departTime AS "Departure Time", f.arrivalTime AS "Arrival Time", a.airline 
        FROM aircraft a, airport dep, airport arr, flights f, pilot p
        WHERE f.aircraftID =  a.aircraftID AND f.pilotID = p.pilotID AND f.toDestinationID= dep.airportID AND f.fromDestinationID = arr.airportID ORDER BY p.licenseNumber AND p.liceseNumber = ''' + str(licenseNumber)

        df = pd.read_sql_query(querry)
        return df
    
    