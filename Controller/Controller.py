import sqlite3

class Controller:

    # Create objects of all models and the view.
    def __init__(self,view, dBSetUpModel, flightsModel, pilotModel, BaseModel): #, airportModel, pilotModel, aircraftModel):
        self.view = view
        self.baseModel = BaseModel
        self.dBSetUpModel = dBSetUpModel
        # self.flightsModel = flightsModel
        # self.airportModel = airportModel
        # self.pilotModel = pilotModel
        # self.aircraftModel = aircraftModel

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
                # View destination  information
                pass
            elif choice == 7:
                pass
            elif choice == 8:
                self._option8()
            elif choice == 9:
                #Close connection and exit
                break
            else:
                self.view.showMessage("Invalid selection. Try again...")
    
   
    # Local methods
    def _option0(self):
        self.view.showMessage("Creating the required tables for testing...")
        self.dBSetUpModel.createAllTables()
        self.view.showMessage("Populating the required tables for testing with sample data...")
        self.dBSetUpModel.addAllSampleData()

    def _option1(self):
        # Get the table from the user.
        table = self.view.getUserInput("Please type the table contianing the required data\n")
        # Get the attribute from the user. 
        attribute = self.view.getUserInput(" Please type the attribute which will narrow the search\n")
        # Get the attribute value from the user. 
        attributeValue = self.view.getUserInput("Please type the value of the selected attribute\n")
        df = self.baseModel.retrieveTableDataByAttribute(table,attribute,attributeValue)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")
    
    def _option2(self):
        # Get the table from the user.
        table = self.view.getUserInput("Please type the table contianing the required data\n")
        # Get all rows from the table
        df = self.baseModel.retrieveAllDataFromTable(table)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")

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
    
    def _option4(self):
        df = self.flightsModel.showAllFlights()
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")
    
    def _option8(self):
        # Array to contain all license numbers 
        lisenceNumbers = []

        # Get the first license number 
        lisenceNumber = self.view.getUserInput("Please type in the pilot's license number or press enter to display results\n")

        # Get additional license Numbers until the user presses enter which will provide an empty string
        while lisenceNumber != "":
            lisenceNumbers.append(lisenceNumber)
            lisenceNumber = self.view.getUserInput("Please type in the pilot's license number or press enter to display results\n")


        df = self.pilotModel.getMultiplePilotsSchedule(lisenceNumbers)
        self.view.showQuerryResults(df)

    def _option5(self):
        # Show all attributes for flights table
        self.view.showAllAttributes("flights")

        # Get the required inputs from hte user
        selectedFlightsAttribute = self.view.getUserInput("Please type in the appropriate attribute whose values will be modified it \n")
        existingFlightsAttributeValue = self.view.getUserInput("Please type in the value of the attribute to be updated \n")
        newValue = self.view.getUserInput("Please type in the new value\n")

        print(f"Warning: You are about to update all rows where {selectedFlightsAttribute} = {existingFlightsAttributeValue}")
        print(f"If you wish to update a different attribute from the selection, record the ID of that record and search again")

        # Confirm that the user wants to continue. If not simply do nothing.
        if self._continueProcess():
            # Execute the update
            self.flightsModel.updateFlightDetails(selectedFlightsAttribute,existingFlightsAttributeValue,newValue)
            self.view.getUserInput("\nPress any button to continue...")
        else:
            return

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

        

        











            


