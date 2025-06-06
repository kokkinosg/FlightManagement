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
                # Assign pilot to flight
                pass
            elif choice == 6:
                # View destination  information
                pass
            elif choice == 7:
                self._option7()
            elif choice == 8:
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
    
    def _option7(self):
        df = self.pilotModel.getAllPilotsSchedule()
        self.view.showQuerryResults(df)
        self.view.getUserInput(("\nPress any button to continue..."))







            


