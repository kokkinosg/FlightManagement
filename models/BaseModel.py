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

    # Method which retrieves a dataframe with the results of the query. You specify the table to get the data from, the attribute and its value. 
    def retrieveTableDataByAttribute(self, tableName, attributeName, attributeValue):
        # Check the table is valid and the attribue exists in that table
        if self._isValidTable(tableName) and self._isValidAttribute(tableName, attributeName):
            # Construct and execute the select query
            df = self._executeSelectQuery(tableName, attributeName, attributeValue)
            return df
        else:
            return None 
        
    # Method to return all rows from a specified table
    def retrieveAllDataFromTable(self,tableName):
        # If the table is valid, i.e. exists in database, carry out the query
        if self._isValidTable(tableName):
            query = f"SELECT * FROM {tableName}"
            df = pd.read_sql_query(query, self.dbConnection)
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
                # Construct the query with the helper function 
                query = self._constructInsertQuery(tableName,params,attributeNames)
                # Execute the query 
                self._executeInsertQuery(tableName, query, params)
            else:
                print(f"{len(attributeNames)} values were expected but only {len(params)} values were provided")
        else:
            print(f"Table '{tableName}' is not valid.")

    # Method which deletes rows which match certain criteria.
    def deleteRowsFromTable(self, tableName, attributeName, attributeValue):
        # Check the table is valid and the attribue exists in that table
        if self._isValidTable(tableName) and self._isValidAttribute(tableName, attributeName):
            # Construct and execute the delete query. If it returns true, return true here
            self._executeDeleteQuery(tableName, attributeName, attributeValue)
        else:
            return None 

    # Method which updates a single attribute of a row obtained from a single search criterion.
    def updateRowsFromTable(self, tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue):
        # Check the table is valid and the attribue exists in that table
        if self._isValidTable(tableName) and self._isValidAttribute(tableName, setAttributeName) and self._isValidAttribute(tableName, whereAttributeName):
            # Construct and execute the delete query. If it returns true, return true here
            self._executeUpdateQuery(tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue)
        else:
            return None 

    # Function to get all column names / attributes from a table 
    def getTableAttributeNames(self, tableName):
        # This is a META query which will return the schema of the table, from which i will only extract the attribute names. 
        query = f"PRAGMA table_info({tableName})"
        # df contains the schema of the table 
        df = pd.read_sql_query(query,self.dbConnection)
        # Extract the column names in a new array
        attributeNames = []
        for column in df['name']:
            attributeNames.append(column)
        return attributeNames
    
    # Function to get all column data types
    def getTableAttributeDataTypes(self, tableName):
        # This is a META query which will return the schema of the table, from which i will only extract the attribute names. 
        query = f"PRAGMA table_info({tableName})"
        # df contains the schema of the table 
        df = pd.read_sql_query(query,self.dbConnection)
        # Extract the column data Types in a new array
        attributeDataTypes = []
        for column in df['type']:
            attributeDataTypes.append(column)
        return attributeDataTypes

    # Method to change the pilotID assigned to a flight to a different one which exists in the pilot table. 
    def assignPilotToFlight(self, oldPilotID, newPilotID):
        # Specify the table and attribute to be updated. 
        tableName = "flights"
        attributeName = "pilotID"

        # Get all available pilotIDs from tge pilot table
        availablePilotIDs = self._getAllAttributeValues("pilot", "pilotID")

        # Only update the pilot id of a flight, if the pilotID also exists in the pilot table 
        if newPilotID in availablePilotIDs:
            # Invoke the updateRowsFromTable function to execute the update to pilot
            self.updateRowsFromTable(tableName,attributeName,newPilotID,attributeName, oldPilotID)
        else:
            print(f"{newPilotID} does not correspond to a recorded Pilot in the Pilot table")
   
    # Helper function to extract all values in a specified column/attribute
    def _getAllAttributeValues(self, tableName, attributeName):
        try:
            # Construct a simple select query to get all values in a specified column
            query = f"SELECT {attributeName} FROM {tableName}"
            # Get the results from the query to a dataframe
            df = pd.read_sql_query(query, self.dbConnection)
            # extract all the values to a list
            column_values = df[attributeName].tolist()
            return column_values
        except Exception as e:
            print(f"Error at getAllAttributeValues: {e}")

    # Helper function to execute the update query
    def _executeUpdateQuery(self, tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue):
        # Construct the parameterised query
        query = f'''UPDATE {tableName} SET {setAttributeName} = ? WHERE {whereAttributeName} = ? '''

        try:
            self.cursor.execute(query, (setAttributeValue,whereAttributeValue))
            self.dbConnection.commit()
             # Use rowcount to see if actually any records would be affected by the query
            if self.cursor.rowcount == 0:
                print(f"No records found in '{tableName}' where {whereAttributeName} = {whereAttributeValue}. Nothing was updated.")
            else:
                print(f"Successfully updated {self.cursor.rowcount} record(s) in '{tableName}': set {setAttributeName} = {setAttributeValue} where {whereAttributeName} = {whereAttributeValue}.")
        except Exception as e:
            print(f"Error encountered at _executeUpdateQuery: {e}")
        
    # Gets the specified pilot schedules. If no pilot licences are specified, it shows all pilots.
    # The license Numbers is an array of licence numbers. 
    def getMultiplePilotsSchedule(self, licenseNumbers):

        query = '''SELECT p.pilotID as "Pilot ID", p.pilotName AS Name, p.pilotSurname AS Surname, p.licenseNumber AS "Licence Number", dep.airportName AS "Current Location", arr.airportName AS "Flies to",
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
            query += f" WHERE p.licenseNumber IN ({placeholders})"
            query += " ORDER BY p.licenseNumber"
            df = pd.read_sql_query(query, self.dbConnection, params=licenseNumbers)
        else:
            # Conclude the query by ordering by pilot license number
            query += " ORDER BY p.licenseNumber "
            df = pd.read_sql_query(query, self.dbConnection)
        
        return df

    # Helper function to construct the insertion query. The params are the values correspodning to the attributeNames
    def _constructInsertQuery(self, tableName, params, attributeNames):
            # Create the approapraite number of placeholders in a string like "?,?,?..."
            placeholders = ', '.join(['?'] * len(params))
            # Create the appropriate attributes name string
            attributeNamesString = ', '.join(attributeNames)
            # Construct the query
            query = f"INSERT INTO {tableName} ({attributeNamesString}) VALUES ({placeholders})"
            return query
    
    # Helper function to execute the insertion query 
    def _executeInsertQuery(self,tableName, query, params):
        # Execute query
        try:
            # Remember, we are using parameterised query, so execute has a second argument. 
            self.cursor.execute(query, params)
            self.dbConnection.commit()
            print(f"Row added to '{tableName}' successfully.")
        except Exception as e:
            print(f"Error adding row to '{tableName}': {e}")

    # Helper function which creates and executes a delete query by specifying the Table, the attribute from that table and the value of the attribute. 
    # It returns true if succesful     
    def _executeDeleteQuery(self, tableName,attributeName,attributeValue):
        try: 
            # Construct a parameterised query to return all flights mathing the criterion
            query = f''' DELETE FROM {tableName} WHERE {attributeName} = ?'''
            # We need the cursor execute this query.
            self.cursor.execute(query, (attributeValue,))
            self.dbConnection.commit()

            # Use rowcount to see if actually any records would be affected by the query
            if self.cursor.rowcount == 0:
                print(f"No records found in '{tableName}' where {attributeName} = {attributeValue}. Nothing was deleted.")
            else:
                print(f"Successfully deleted {self.cursor.rowcount} record(s) from '{tableName}' where {attributeName} = {attributeValue}.")
        except Exception as e:
            print(f"Error encountered at _executeDeleteQuery: {e}")

    # Helper function which creates and executes a select query by specifying the Table, the attribute from that table and the value of the attribute.      
    # It returns a dataframe with the results
    def _executeSelectQuery(self, tableName,attributeName,attributeValue):
        try: 
            # Construct a parameterised query to return all flights mathing the criterion
            query = f'''SELECT * FROM {tableName} WHERE {attributeName} = ?'''

            # Get a dataframe with the results. 
            df = pd.read_sql_query(query,self.dbConnection, params =(attributeValue,))

            # Return the data frame
            return df
        except Exception as e:
            print(f"Error encountered at _executeSelectQuery : {e}")
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

    # Methods with specific queries 

    # Method to return the total number of passengers flown by a specific aircraft 
    def getTotalPassengerPerAircract(self):
        try: 
            query = '''SELECT a.model AS AircraftModel, a.airline, SUM(f.passengerCount) AS TotalPassengers
                    FROM flights f
                    JOIN aircraft a ON f.aircraftID = a.aircraftID
                    GROUP BY f.aircraftID;'''
            df = pd.read_sql_query(query,self.dbConnection)
            return df
        except Exception as e:
            print(f"Error encountered at getTotalPassengerPerAircract : {e}")
            return None

    # Method to return the number of Flights to each destination airport
    def getNumFlightsPerDestAirport(self):
        try:
            query = '''SELECT a.airportName AS Destination, COUNT(f.flightID) AS TotalFlights
            FROM flights f
            JOIN airport a ON f.toDestinationID = a.airportID
            GROUP BY f.toDestinationID;'''
            df = pd.read_sql_query(query,self.dbConnection)
            return df
        except Exception as e:
            print(f"Error encountered at getNumFlightsPerDestAirport : {e}")
            return None
        
    # Method to return the number of flights assigned to each pilot
    def getNumFlightsPerPilot(self):
        try:
            # Concatenate the name 
            query = '''SELECT p.pilotName || ' ' || p.pilotSurname AS Pilot, COUNT(f.flightID) AS TotalFlights
            FROM flights f 
            JOIN pilot p ON f.pilotID = p.pilotID
            GROUP BY f.pilotID;'''
            df = pd.read_sql_query(query,self.dbConnection)
            return df
        except Exception as e:
            print(f"Error encountered at getNumFlightsPerPilot : {e}")
            return None
        
    # Method to return the average travel distance per pilot
    def getAvgDistancePerPilot(self):
        try:
            # Calculates the average travel distance of all flights flown by each pilot, groups the results by pilot and displays their full name with concatenation.
            query = '''SELECT p.pilotName || ' ' || p.pilotSurname AS Pilot, ROUND(AVG(f.travelDistanceKM), 2) AS AvgDistanceKM
            FROM flights f
            JOIN pilot p ON f.pilotID = p.pilotID
            GROUP BY f.pilotID;'''
            df = pd.read_sql_query(query,self.dbConnection)
            return df
        except Exception as e:
            print(f"Error encountered at getNumFlightsPerPilot : {e}")
            return None
