from models.FlightsModel import FlightsModel

class View:

    def __init__(self, dbConnection, cursor):
        # construct all objects and declare all variables
        self.flightsModel = FlightsModel(dbConnection, cursor)
        pass
    
    # Public methods
    # Method to display the menu
    def displayMenu(self): 
        print("\n Menu:")
        print("**********")
        print(" 0. Create flights, airport, pilot and aircraft tables and populate them with sample data")
        print(" 1. View flight/airport/aircraft/pilot information based on criteria.")
        print(" 2. View all records in the selected table")
        print(" 3. Add a new record to any table")
        print(" 4. Delete record/s from any table")
        print(" 5. Update existing record/s from any table")
        print(" 6. TBD")
        print(" 7. TBD")
        print(" 8. Show specific pilot/pilots schedule")
        print(" 9. Exit\n") 
        pass

    # Method which is called when we want to see results from a search
    def showQuerryResults(self, df):
        # We must check if it is None fdirst because if it is and we check for empty first, it will throw an error.  
        if df is None:
            print("Something went wrong — no DataFrame was returned.")
        elif df.empty:
            print("Query succeeded, but returned no data.")
        else:
            print(df)
    

    # Method to get a user menu selection
    def getMenuSelection(self):
        try:
            userChoice = int(input("Please choose an option: "))
            if 0 <= userChoice <= 9:
                return userChoice
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
                return -1
        except ValueError:
            print("Invalid input. Please enter a number.")
            return -1
    
    def getUserInput(self, message):
        try:
            # Invoke the showMessage method to print the message
            self.showMessage(message)
            # Get the user input from a new line
            userChoice = input()
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


        