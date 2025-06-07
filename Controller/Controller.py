import sqlite3

class Controller:

    # Connect to the database 
    def __init__(self,view, dBSetUpModel, flightsModel, pilotModel): #, airportModel, pilotModel, aircraftModel):
        self.view = view
        self.dBSetUpModel = dBSetUpModel
        self.flightsModel = flightsModel
        # self.airportModel = airportModel
        self.pilotModel = pilotModel
        # self.aircraftModel = aircraftModel

    def run(self):
        while True:

            #  Display the menu
            self.view.displayMenu()
            # Get the user choice
            choice  = self.view.getMenuSelection()

            if choice == 1:
                # Create flight tables
                pass
            elif choice == 2:
                # Add flight
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
    def _option3(self):
        self.view.showAllAttributes("flights")
        flightsAttribute = self.view.getUserInput("Please type in the appropriate attribute to initiate search\n")
        flightsAttributeValue = self.view.getUserInput("Please type in the value for the attribute\n")
        df = self.flightsModel.retrieveFlightByAttribute(flightsAttribute, flightsAttributeValue)
        self.view.showQuerryResults(df)
        self.view.getUserInput("\nPress any button to continue...")
    
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
        selectedFlightsAttribute = self.view.getUserInput("Please type in the appropriate attribute whose values will be modified it\n")
        existingFlightsAttributeValue = self.view.getUserInput("Please type in the value of the attribute to be updated \n")
        newValue = self.view.getUserInput("Please type in the new value")
        # Execute the update
        self.flightsModel.updateFlightDetails(selectedFlightsAttribute,existingFlightsAttributeValue,newValue)
        self.view.getUserInput("\nPress any button to continue...")
        











            


