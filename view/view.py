from models.FlightsModel import FlightsModel

class View:

    def __init__(self, dbConnection):
        # construct all objects and declare all variables
        self.flightsModel = FlightsModel(dbConnection)
        pass
    
    # Public methods
    # Method to display the menu
    def displayMenu(self): 
        print("\n Menu:")
        print("**********")
        print(" 1. Create table FlightInfo")
        print(" 2. Insert data into FlightInfo")
        print(" 3. Search for a flight")
        print(" 4. Show all flights")
        print(" 5. Update data some records")
        print(" 6. Delete data some records")
        print(" 7. Show all pilots' schedule")
        print(" 8. Exit\n") 
        pass

    # Method which is called when we want to see results from a search
    def showQuerryResults(self, df):
        if df.empty:
            print("No data were retrieved")
        else:
            print(df)
    

    # Method to get a user menu selection
    def getMenuSelection(self):
        try:
            userChoice = int(input("Please choose an option: "))
            if 1 <= userChoice <= 8:
                return userChoice
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
                return -1
        except ValueError:
            print("Invalid input. Please enter a number.")
            return -1
    
    def getUserInput(self, message):
        try:
            userChoice = input(message)
            return userChoice
        except Exception as e:
            print("Error whilst getting user input: " + str(e))
            pass
        
    # Method to show any message
    def showMessage(self,message):
        print(str(message))
        pass

    # Method to show all possible attributes for a table 
    def showAllAttributes(self, table):

        print("Please type one of the following search criteria followed by a value\n")

        if table == "flights":
            print(self.flightsModel.possibleAttributes)
        elif table == "airport":
            # to be implemented
            pass
        elif table == "pilot":
            # to be implemented
            pass
        elif table == "aircraft":
            # to be implemented
            pass
        else:
            print("Table does not exist")
            pass


        