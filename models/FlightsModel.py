import sqlite3
import pandas as pd

class FlightsModel:

    # All possible attributes of this list which are accessible outside of this class. 
    possibleAttributes = ["flightID", "aircraftID", "pilotID", "fromDestinationID", "toDestinationID", "departTime", "arrivalTime", "passengerCount", "travelDistanceKM", "status"]

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection
    
    def retrieveFlightByAttribute(self, flightsAttribute, flightsAttributeValue):
        
        print("Retrieving all flights where " + flightsAttribute + " is " + str(flightsAttributeValue))
        
        # Check if the input parameter to this method matches one of the possible attributes of the fligths table. 
        if flightsAttribute in FlightsModel.possibleAttributes:
            # Construct the querry from input 
            querry = '''SELECT * FROM flights WHERE ''' + str(flightsAttribute) + " = " + str(flightsAttributeValue)

            df = pd.read_sql_query(querry, self.dbConnection)
            if df.empty:
                print("No flights exist in database where " + str(flightsAttribute) + " = " + str(flightsAttributeValue))
            else:
                print()
                print(df)
                print()
        else:
             print("Uknown attribute")

    