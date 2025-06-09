import sqlite3

class Controller:

    # Create objects of all models and the view.
    def __init__(self,view, dBSetUpModel, BaseModel): 
        self.view = view
        self.baseModel = BaseModel
        self.dBSetUpModel = dBSetUpModel

    def run(self):
        while True:

            #  Display the menu
            self.view.displayMenu()
            # Get the user choice
            choice  = self.view.getMenuSelection()

            if choice == 0:
                self._option0()
                pass
            elif choice == 1:
                self._option1()
                pass
            elif choice == 2:
                self._option2()
                pass
            elif choice == 3:
                self._option3()
            elif choice == 4:
                self._option4()
            elif choice == 5:
                self._option5()
            elif choice == 6:
                self._option6()
            elif choice == 7:
                self._option7()
            elif choice == 8:
                self._option8()
            elif choice == 9:
                self._option9()
            elif choice == 10:
                self._option10()
            elif choice == 11:
                self._option11()
            elif choice == 12:
                self._option12()
            elif choice == 13:
                self._option13()
            elif choice == 14:
                self._option14()
            elif choice == 15:
                self._option15()
            elif choice == 16:
                self._option16()
                pass
            elif choice == 17:
                self.dBSetUpModel.closeConnection()
                break
            else:
                self.view.showMessage("Invalid selection. Try again...")
    
   
    # Local methods
    # Create flights, airport, pilot and aircraft tables and populate them with sample data.
    def _option0(self):
        self.view.showMessage("Creating the required tables for testing...")
        self.dBSetUpModel.createAllTables()
        self.view.showMessage("Populating the required tables for testing with sample data...")
        self.dBSetUpModel.addAllSampleData()
        self.view.getUserInput("\nPress any button to continue...")

    # View flight/airport/aircraft/pilot information based on criteria.
    def _option1(self):
        # Get the table from the user.
        table = self.view.getUserInput("Please type the table contianing the required data\n")
        self.view.showMessage(f"These are the table: {table} columns/attributes\n")
        # Show all possible attributes for that table 
        self.view.showMessage(self.baseModel.getTableAttributeNames(table))
        # Get the attribute from the user. 
        attribute = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        attributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        df = self.baseModel.retrieveTableDataByAttribute(table,attribute,attributeValue)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")
    
    # View all records in the selected table - E.g. View all flights
    def _option2(self):
        # Get the table from the user.
        table = self.view.getUserInput("Please type the table contianing the required data\n")
        # Get all rows from the table
        df = self.baseModel.retrieveAllDataFromTable(table)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

    # Add a new record to any table - E.g. Add a new flight
    def _option3(self):
        # Get the table from the user.
        tableName = self.view.getUserInput("Please type the table containing the required data\n")
        # Get the attribute names for that table 
        attributeNames = self.baseModel.getTableAttributeNames(tableName)
        # Get the attribute data types from that table 
        attributeDataTypes = self.baseModel.getTableAttributeDataTypes(tableName)
        # Show the required attributes and their data types to the user. 
        self.view.showMessage(f"To add a row to the {tableName} please provide the below attributes")
        # Initialise an empty params list to contain the params 
        params = []
        # Initiate a counter 
        counter = 0 
        # Request as many user inputs as there are attributes 
        for attribute in attributeNames:
            # Get the data type of this attribute 
            attributeType = attributeDataTypes[counter]
            # Get the user input
            param = self.view.getUserInput(f"Please provide an input of type {attributeType}  for {attribute}")
            # Add the parameter to the list
            params.append(param)
            counter += 1
        
        self.baseModel.addRowToTable(tableName,params)
        self.view.getUserInput("\nPress any button to continue...")
    
    # Delete record/s from any table - E.g. Delete a flight
    def _option4(self):
        # Get the table from the user.
        table = self.view.getUserInput("Please type the table containing the data to be deleted\n")
        self.view.showMessage(f"These are the table: {table} columns/attributes\n")
        # Show all possible attributes for that table 
        self.view.showMessage(self.baseModel.getTableAttributeNames(table))
        
        # Get the attribute from the user. 
        attribute = self.view.getUserInput(" Please choose one of the above attributes to narrow down the search \n")

        # Get the attribute value from the user. 
        attributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")

        # Display warning 
        self.view.showMessage(f"You are about to delete all records from {table} where {attribute} = {attributeValue}")

        # Ask for confirmation 
        if self._continueProcess():
            self.baseModel.deleteRowsFromTable(table,attribute,attributeValue)
            self.view.getUserInput("\nPress any button to continue...")
        else:
            self.view.getUserInput("\nPress any button to continue...")
        
    # Update existing record/s from any table - E.g. Assign a pilot to a flight
    def _option5(self):
        # Get the table from the user.
        tableName = self.view.getUserInput("Please type the table containing the data to be deleted\n")
        # Show all possible attributes for that table 
        self.view.showMessage(f"These are the table: {tableName} columns/attributes\n")
        self.view.showMessage(self.baseModel.getTableAttributeNames(tableName))
        # Get the attribute from the user. 
        whereAttributeName = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        whereAttributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        # Get the attribute from the user. 
        setAttributeName = self.view.getUserInput(" Please type the attribute whose value will be updated\n")
        # Get the attribute value from the user. 
        setAttributeValue = self.view.getUserInput("Please type the new value for the attribute\n")

        # Display warning 
        self.view.showMessage(f"You are about to update {setAttributeName} = {setAttributeValue} of all rows in {tableName} where {whereAttributeName} = {whereAttributeValue}")

        # Ask for confirmation 
        if self._continueProcess():
            self.baseModel.updateRowsFromTable(tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue)
            self.view.getUserInput("\nPress any button to continue...")
        else:
            self.view.getUserInput("\nPress any button to continue...")

    # Show specific pilot/pilots schedule
    def _option6(self):
        # Array to contain all license numbers 
        lisenceNumbers = []

        # Get the first license number 
        lisenceNumber = self.view.getUserInput("Please type the first pilot's license number or press enter to display all pilots' schedule\n")

        # Get additional license Numbers until the user presses enter which will provide an empty string
        while lisenceNumber != "":
            lisenceNumbers.append(lisenceNumber)
            lisenceNumber = self.view.getUserInput("Please type in another pilot's license number or press enter to diplay specified pilots' schedule\n")

        df = self.baseModel.getMultiplePilotsSchedule(lisenceNumbers)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

    # Add a new flight
    def _option7(self):
        # Specify the fligts table
        tableName = "flights"
        # Get the attribute names for that table 
        attributeNames = self.baseModel.getTableAttributeNames(tableName)
        # Get the attribute data types from that table 
        attributeDataTypes = self.baseModel.getTableAttributeDataTypes(tableName)
        # Show the required attributes and their data types to the user. 
        self.view.showMessage(f"To add a row to the {tableName} please provide the below attributes")
        # Initialise an empty params list to contain the params 
        params = []
        # Initiate a counter 
        counter = 0 
        # Request as many user inputs as there are attributes 
        for attribute in attributeNames:
            # Get the data type of this attribute 
            attributeType = attributeDataTypes[counter]
            # Get the user input
            param = self.view.getUserInput(f"Please provide an input of type {attributeType}  for {attribute}")
            # Add the parameter to the list
            params.append(param)
            counter += 1
        
        self.baseModel.addRowToTable(tableName,params)
        self.view.getUserInput("\nPress any button to continue...")

    # View flights by criteria
    def _option8(self):
         # Get the table from the user.
        table = "flights"
        self.view.showMessage(f"These are the table: {table} columns/attributes\n")
        # Show all possible attributes for that table 
        self.view.showMessage(self.baseModel.getTableAttributeNames(table))
        # Get the attribute from the user. 
        attribute = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        attributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        df = self.baseModel.retrieveTableDataByAttribute(table,attribute,attributeValue)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

    # Update flight information
    def _option9(self):
        # Get the table from the user.
        tableName = "flights"
        # Show all possible attributes for that table 
        self.view.showMessage(f"These are the table: {tableName} columns/attributes\n")
        self.view.showMessage(self.baseModel.getTableAttributeNames(tableName))
        # Get the attribute from the user. 
        whereAttributeName = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        whereAttributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        # Get the attribute from the user. 
        setAttributeName = self.view.getUserInput(" Please type the attribute whose value will be updated\n")
        # Get the attribute value from the user. 
        setAttributeValue = self.view.getUserInput("Please type the new value for the attribute\n")

        # Display warning 
        self.view.showMessage(f"You are about to update {setAttributeName} = {setAttributeValue} of all rows in {tableName} where {whereAttributeName} = {whereAttributeValue}")

        # Ask for confirmation 
        if self._continueProcess():
            self.baseModel.updateRowsFromTable(tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue)
            self.view.getUserInput("\nPress any button to continue...")
        else:
            self.view.getUserInput("\nPress any button to continue...")

    # Assign pilot to flight
    def _option10(self):
        
        # Get the old pilot ID 
        oldPilotID = self.view.getUserInput(" Please specify the pilotID which will be replaced for a specific flight\n")
        # Get the attribute value from the user. 
        newPilotID = self.view.getUserInput("Please specify the new pilotID for that flight\n")
    
        # Display warning 
        self.view.showMessage(f"You are about to update the pilotID of a flight from {oldPilotID} to {newPilotID}")

        # Ask for confirmation 
        if self._continueProcess():
            self.baseModel.assignPilotToFlight(oldPilotID,newPilotID)
            self.view.getUserInput("\nPress any button to continue...")
        else:
            self.view.getUserInput("\nPress any button to continue...")

    # View destination (airport) information
    def _option11(self):
         # Get the table from the user.
        table = "airport"
        self.view.showMessage(f"These are the table: {table} columns/attributes\n")
        # Show all possible attributes for that table 
        self.view.showMessage(self.baseModel.getTableAttributeNames(table))
        # Get the attribute from the user. 
        attribute = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        attributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        df = self.baseModel.retrieveTableDataByAttribute(table,attribute,attributeValue)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

    # Update destination (airport) information
    def _option12(self):
        tableName = "airport"
        # Show all possible attributes for that table 
        self.view.showMessage(f"These are the table: {tableName} columns/attributes\n")
        self.view.showMessage(self.baseModel.getTableAttributeNames(tableName))
        # Get the attribute from the user. 
        whereAttributeName = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        whereAttributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        # Get the attribute from the user. 
        setAttributeName = self.view.getUserInput(" Please type the attribute whose value will be updated\n")
        # Get the attribute value from the user. 
        setAttributeValue = self.view.getUserInput("Please type the new value for the attribute\n")

        # Display warning 
        self.view.showMessage(f"You are about to update {setAttributeName} = {setAttributeValue} of all rows in {tableName} where {whereAttributeName} = {whereAttributeValue}")

        # Ask for confirmation 
        if self._continueProcess():
            self.baseModel.updateRowsFromTable(tableName, setAttributeName, setAttributeValue, whereAttributeName, whereAttributeValue)
            self.view.getUserInput("\nPress any button to continue...")
        else:
            self.view.getUserInput("\nPress any button to continue...")

    # Total Number of Passengers Flown by Each Aircraft"
    def _option13(self):
        df = self.baseModel.getTotalPassengerPerAircract()
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")
   
    # Number of Flights Assigned to Each Pilot
    def _option14(self):
        df = self.baseModel.getNumFlightsPerPilot()
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

    # Number of Flights to Each Destination Airport
    def _option15(self):
        df = self.baseModel.getNumFlightsPerDestAirport()
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

    # Average Travel Distance per Pilot
    def _option16(self):
        df = self.baseModel.getAvgDistancePerPilot()
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")
    
    # Boolean check to see if the process will continue  
    def _continueProcess(self):
        # Keep a loop going until the user presses the correct button
        while True:
            # Get the user choice
            userChoice = self.view.getUserInput("Continue with the process? \nType 1 to continue, 2 to stop.")
            if (userChoice == "1"):
                print(" Confirmed process")
                return True
            elif (userChoice == "2"):
                print(" Process cancelled")
                return False
            else:
                print("Invalid input. Please enter 1 to continue or 2 to stop.")

        

        











            


