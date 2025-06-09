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
        # Check the table is valid and the attribue exists in that table
        if self._isValidTable(tableName) and self._isValidAttribute(tableName, attributeName):
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

    # Method to add data to a specified table. Params is a list containing a value for each table column. 
    def addRowToTable(self, tableName, params):
        # Check if the requested table is valid
        if self._isValidTable(tableName):
            # Get all columns names from the table 
            attributeNames = self.getTableAttributeNames(tableName) 

            # Check if enough parameters were provided 
            if len(attributeNames) == len(params):
                # Construct the querry with the helper function 
                querry = self._constructInsertQuerry(tableName,params,attributeNames)
                # Execute the querry 
                self._executeInsertQuerry(tableName, querry, params)
            else:
                print(f"{len(attributeNames)} values were expected but only {len(params)} values were provided")
        else:
            print(f"Table '{tableName}' is not valid.")

    # Method which deletes rows which match certain criteria.
    def deleteRowsFromTable(self, tableName, attributeName, attributeValue):
        # Check the table is valid and the attribue exists in that table
        if self._isValidTable(tableName) and self._isValidAttribute(tableName, attributeName):
            # Construct and execute the delete querry. If it returns true, return true here
            self._executeDeleteQuerry(tableName, attributeName, attributeValue)
        else:
            return None 

    # Method which updates a single attribute of a row obtained from a single search criterion.
    def updateRowsFromTable(self, tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue):
        # Check the table is valid and the attribue exists in that table
        if self._isValidTable(tableName) and self._isValidAttribute(tableName, setAttributeName) and self._isValidAttribute(tableName, whereAttributeName):
            # Construct and execute the delete querry. If it returns true, return true here
            self._executeUpdateQuerry(tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue)
        else:
            return None 

    # Function to get all column names / attributes from a table 
    def getTableAttributeNames(self, tableName):
        # This is a META querry which will return the schema of the table, from which i will only extract the attribute names. 
        querry = f"PRAGMA table_info({tableName})"
        # df contains the schema of the table 
        df = pd.read_sql_query(querry,self.dbConnection)
        # Extract the column names in a new array
        attributeNames = []
        for column in df['name']:
            attributeNames.append(column)
        return attributeNames
    
    # Function to get all column data types
    def getTableAttributeDataTypes(self, tableName):
        # This is a META querry which will return the schema of the table, from which i will only extract the attribute names. 
        querry = f"PRAGMA table_info({tableName})"
        # df contains the schema of the table 
        df = pd.read_sql_query(querry,self.dbConnection)
        # Extract the column data Types in a new array
        attributeDataTypes = []
        for column in df['type']:
            attributeDataTypes.append(column)
        return attributeDataTypes

    # Helper function to execute the update querry
    def _executeUpdateQuerry(self, tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue):
        # Construct the parameterised querry
        querry = f'''UPDATE {tableName} SET {setAttributeName} = ? WHERE {whereAttributeName} = ? '''

        try:
            self.cursor.execute(querry, (setAttributeValue,whereAttributeValue))
            self.dbConnection.commit()
             # Use rowcount to see if actually any records would be affected by the querry
            if self.cursor.rowcount == 0:
                print(f"No records found in '{tableName}' where {whereAttributeName} = {whereAttributeValue}. Nothing was updated.")
            else:
                print(f"Successfully updated {self.cursor.rowcount} record(s) in '{tableName}': set {setAttributeName} = {setAttributeValue} where {whereAttributeName} = {whereAttributeValue}.")
        except Exception as e:
            print(f"Error encountered at _executeUpdateQuery: {e}")
        
    # Gets the specified pilot schedules. If no pilot licences are specified, it shows all pilots.
    # The license Numbers is an array of licence numbers. 
    def getMultiplePilotsSchedule(self, licenseNumbers):

        querry = '''SELECT p.pilotID as "Pilot ID", p.pilotName AS Name, p.pilotSurname AS Surname, p.licenseNumber AS "Licence Number", dep.airportName AS "Current Location", arr.airportName AS "Flies to",
        f.departTime AS "Departure Time", f.arrivalTime AS "Arrival Time", a.airline 
        FROM pilot p
        LEFT JOIN flights f ON f.pilotID = p.pilotID
        LEFT JOIN aircraft a ON f.aircraftID = a.aircraftID
        LEFT JOIN airport dep ON f.toDestinationID = dep.airportID
        LEFT JOIN airport arr ON f.fromDestinationID = arr.airportID'''

        # If multiple licenseNumbers are provided, filter the results
        if len(licenseNumbers) > 0:
            # Loop over every license number in hte arraylist. If no numbers are provided this code will not run and instead it will show all pilot's schedule. 
            placeholders = ', '.join(['?'] * len(licenseNumbers))
            querry += f" WHERE p.licenseNumber IN ({placeholders})"
            querry += " ORDER BY p.licenseNumber"
            df = pd.read_sql_query(querry, self.dbConnection, params=licenseNumbers)
        else:
            # Conclude the querry by ordering by pilot license number
            querry += " ORDER BY p.licenseNumber "
            df = pd.read_sql_query(querry, self.dbConnection)
        
        return df

    # Helper function to construct the insertion querry. The params are the values correspodning to the attributeNames
    def _constructInsertQuerry(self, tableName, params, attributeNames):
            # Create the approapraite number of placeholders in a string like "?,?,?..."
            placeholders = ', '.join(['?'] * len(params))
            # Create the appropriate attributes name string
            attributeNamesString = ', '.join(attributeNames)
            # Construct the querry
            querry = f"INSERT INTO {tableName} ({attributeNamesString}) VALUES ({placeholders})"
            return querry
    
    # Helper function to execute the insertion querry 
    def _executeInsertQuerry(self,tableName, querry, params):
        # Execute querry
        try:
            # Remember, we are using parameterised querry, so execute has a second argument. 
            self.cursor.execute(querry, params)
            self.dbConnection.commit()
            print(f"Row added to '{tableName}' successfully.")
        except Exception as e:
            print(f"Error adding row to '{tableName}': {e}")

    # Helper function which creates and executes a delete querry by specifying the Table, the attribute from that table and the value of the attribute. 
    # It returns true if succesful     
    def _executeDeleteQuerry(self, tableName,attributeName,attributeValue):
        try: 
            # Construct a parameterised querry to return all flights mathing the criterion
            querry = f''' DELETE FROM {tableName} WHERE {attributeName} = ?'''
            # We need the cursor execute this querry.
            self.cursor.execute(querry, (attributeValue,))
            self.dbConnection.commit()

            # Use rowcount to see if actually any records would be affected by the querry
            if self.cursor.rowcount == 0:
                print(f"No records found in '{tableName}' where {attributeName} = {attributeValue}. Nothing was deleted.")
            else:
                print(f"Successfully deleted {self.cursor.rowcount} record(s) from '{tableName}' where {attributeName} = {attributeValue}.")
        except Exception as e:
            print(f"Error encountered at _executeDeleteQuery: {e}")

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

    
  