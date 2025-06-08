import pandas as pd


class BaseModel:

    # Define all attributes for all tables
    flightAttributes = ["flightID", "aircraftID", "pilotID", "fromDestinationID", "toDestinationID", "departTime", "arrivalTime", "passengerCount", "travelDistanceKM", "status"]
    pilotAttributes = [ "pilotID", "pilotName", "pilotSurname", "gender", "licenseNumber", "experienceYears", "aircraftID","currentLocationID"]
    airportAttributes = ["airportID", "airportName", "city", "country", "postCode"]
    aircraftAttributes = ["aircraftID", "model", "airline", "manufacturer", "capacity", "rangeKM", "currentLocationID"]

    # When this class is initialised it should received the already initialised dbConnection and cursor. 
    def __init__(self, dbConnection,cursor):
        self.dbConnection = dbConnection
        self.cursor = cursor

    # Method which retrieves a dataframe with the results of the querry. You specify the table to get the data from, the attribute and its value. 
    def retrieveTableDataByAttribute(self, tableName, attributeName, attributeValue):
        # Check if the attribute name is valid for a specified table
        if self._isValidAttribute(tableName, attributeName):
            # Construct and execute the select querry
            df = self._executeSelectQuerry(tableName, attributeName, attributeValue)
            return df
        else:
            return None 
        
    # Method to return all rows from a specified table
    def retrieveAllDataFromTable(self,tableName):
        # If the table is valid, i.e. exists in database, carry out the querry
        if self._isValidTable(tableName):
            querry = f"SELECT * FROM {tableName}"
            df = pd.read_sql_query(querry, self.dbConnection)
            return df
        else:
            print(f"{tableName} does not exist in the database.")
            return None 


    # Helper function which creates and executes a select querry by specifying the Table, the attribute from that table and the value of the attribute.      
    # It returns a dataframe with the results
    def _executeSelectQuerry(self, tableName,attributeName,attributeValue):
        try: 
            # Construct a parameterised querry to return all flights mathing the criterion
            querry = f'''SELECT * FROM {tableName} WHERE {attributeName} = ?'''

            # Get a dataframe with the results. 
            df = pd.read_sql_query(querry,self.dbConnection, params =(attributeValue,))

            # Return the data frame
            return df
        except Exception as e:
            print(f"Error encountered at _executeSelectQuerry : {e}")
            return None

    # Helper function which checks if the attribute name is valid for a specified table
    def _isValidAttribute(self, tableName, attributeName):

        # Create a dictionary of tableName: tableAttributes
        validAttributes = {
            "flights": self.flightAttributes,
            "pilot": self.pilotAttributes,
            "aircraft": self.aircraftAttributes,
            "airport": self.airportAttributes
        }
        # Get the appropriate list of attributes from the specified table. If the tableName is not in hte dictionary it will return an empty list.
        attributeList = validAttributes.get(tableName, [])

        # CHeck if the desired attribute is in the specified table
        if attributeName in attributeList:
            return True
        else:
            print (f"{attributeName} does not exist in {tableName} table.")
            return False
        
    # Check if a chosen table is valid
    def _isValidTable(self,tableName):
        validTableNames = ["flights", "pilot", "aircraft", "airport"]

        # If the tableName is in hte list of valid tables, return true else return false. 
        if tableName in validTableNames:
            return True
        else:
            return False

    
  