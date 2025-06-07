import sqlite3
import pandas as pd

class FlightsModel:

    # All possible attributes of this list which are accessible outside of this class. 
    possibleAttributes = ["flightID", "aircraftID", "pilotID", "fromDestinationID", "toDestinationID", "departTime", "arrivalTime", "passengerCount", "travelDistanceKM", "status"]

    # When this class is initialised it should received the already initialised dbConnection and cursor. 
    def __init__(self, dbConnection,cursor):
        self.dbConnection = dbConnection
        self.cursor = cursor
    
    # Method to retrieve all flights which match certain search criteria.
    def retrieveFlightByAttribute(self, flightsAttribute, flightsAttributeValue):
        
        print("Retrieving all flights where " + flightsAttribute + " is " + str(flightsAttributeValue))
        
        # Check if the input parameter to this method matches one of the possible attributes of the fligths table. 
        if flightsAttribute in FlightsModel.possibleAttributes:
            # Construct the querry from input 
            querry = '''SELECT * FROM flights WHERE ''' + str(flightsAttribute) + " = " + str(flightsAttributeValue)

            df = pd.read_sql_query(querry, self.dbConnection)
            return df
        else:
             print("Uknown attribute")
    
    # Method which retrieves all available flight records
    def showAllFlights(self):
        querry = '''SELECT * FROM flights'''
        df = pd.read_sql_query(querry, self.dbConnection)
        return df
    
    # Method to update a single flight details 
    def updateFlightDetails(self, selectedFlightsAttribute, existingFlightsAttributeValue, newValue):
        
        #Invoke the function which retrieves flights by attribute
        df = self.retrieveFlightByAttribute(selectedFlightsAttribute, existingFlightsAttributeValue)

        # Check if df is empty
        if df == None:
            print("No flights matching the details provided")
        else:
            query = f"UPDATE flights SET {selectedFlightsAttribute} = ? WHERE {selectedFlightsAttribute} = ?"
            self.cursor.execute(query, (newValue, existingFlightsAttributeValue))
            self.dbConnection.commit()
            print("Flight details updated successfully.")



    




    