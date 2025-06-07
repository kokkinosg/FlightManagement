import pandas as pd

class PilotModel:

    possibleAttributes = ["pilotID", "pilotName", "pilotSurname", "gender", "licenseNumber",
                "experienceYears", "aircraftID", "currentLocationID"]

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    # def getAllPilotsSchedule(self):

    #     querry = '''SELECT p.pilotName AS Name, p.pilotSurname AS Surname, p.licenseNumber AS "Licence Number", dep.airportName AS "Current Location", arr.airportName AS "Flies to",
    #     f.departTime AS "Departure Time", f.arrivalTime AS "Arrival Time", a.airline 
    #     FROM aircraft a, airport dep, airport arr, flights f, pilot p
    #     WHERE f.aircraftID =  a.aircraftID AND f.pilotID = p.pilotID AND f.toDestinationID= dep.airportID AND f.fromDestinationID = arr.airportID ORDER BY p.licenseNumber
    #     '''

    #     df = pd.read_sql_query(querry,self.dbConnection)
    #     return df
    
    # Gets the specified pilot schedules. The license Numbers is an array of licence numbers. 
    def getMultiplePilotsSchedule(self, licenseNumbers):

        querry = '''SELECT p.pilotName AS Name, p.pilotSurname AS Surname, p.licenseNumber AS "Licence Number", dep.airportName AS "Current Location", arr.airportName AS "Flies to",
        f.departTime AS "Departure Time", f.arrivalTime AS "Arrival Time", a.airline 
        FROM pilot p
        LEFT JOIN flights f ON f.pilotID = p.pilotID
        LEFT JOIN aircraft a ON f.aircraftID = a.aircraftID
        LEFT JOIN airport dep ON f.toDestinationID = dep.airportID
        LEFT JOIN airport arr ON f.fromDestinationID = arr.airportID'''

        # If multiple licenseNumbers are provided, filter the results
        if len(licenseNumbers) > 0:
            # Loop over every license number in hte arraylist. If no numbers are provided this code will not run. 
            placeholders = ', '.join(['?'] * len(licenseNumbers))
            querry += f" WHERE p.licenseNumber IN ({placeholders})"
            querry += " ORDER BY p.licenseNumber"
            df = pd.read_sql_query(querry, self.dbConnection, params=licenseNumbers)
        else:
            # Conclude the querry by ordering by pilot license number
            querry = querry + " ORDER BY p.licenseNumber "
            df = pd.read_sql_query(querry, self.dbConnection)
        
        return df
    
    