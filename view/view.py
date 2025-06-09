

class View:

    def __init__(self):
        pass
    
    # Public methods
    # Method to display the menu
    def displayMenu(self): 
        print("\n Menu:")
        print("**********")
        print(" Main Functions\n")

        print(" 0. Create flights, airport, pilot and aircraft tables and populate them with sample data")
        print(" 1. View flight/airport/aircraft/pilot information based on criteria")
        print(" 2. View all records in the selected table - E.g. View all flights")
        print(" 3. Add a new record to any table - E.g. Add a new flight")
        print(" 4. Delete record/s from any table - E.g. Delete a flight")
        print(" 5. Update existing record/s from any table - E.g. Assign a pilot to a flight\n")
        print("**********")
        print(" Frequently used functions\n")
        print(" 6. Show specific pilot/pilots schedule")
        print(" 7. Add a new flight")
        print(" 8. View flights by criteria")
        print(" 9. Update flight information") 
        print(" 10. Assign pilot to flight")
        print(" 11. View destination (airport) information")
        print(" 12. Update destination (airport) information")
        print(" 13. Total Number of Passengers Flown by Each Aircraft") 
        print(" 14. Number of Flights Assigned to Each Pilot")
        print(" 15. Number of Flights to Each Destination Airport")
        print(" 16. Average Travel Distance per Pilot")
        print(" 17. Exit\n") 
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
            if 0 <= userChoice <= 17:
                return userChoice
            else:
                print("Invalid choice. Please enter a number between 0 and 17.")
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



        