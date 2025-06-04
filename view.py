class View:

    def __init__(self):
        # construct all objects and declare all variables
        pass
    
    # Public methods
    # Method to display the menu
    def displayMenu(self): 
        print("\n Menu:")
        print("**********")
        print(" 1. Create table FlightInfo")
        print(" 2. Insert data into FlightInfo")
        print(" 3. Select all data from FlightInfo")
        print(" 4. Search a flight")
        print(" 5. Update data some records")
        print(" 6. Delete data some records")
        print(" 7. Exit\n")
        pass

    # Method to get a user menu selection
    def getMenuSelection(self):
        try:
            userChoice = int(input("Please choose an option: "))
            if 1 <= userChoice <= 7:
                return userChoice
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                return -1
        except ValueError:
            print("Invalid input. Please enter a number.")
            return -1
        
    # Method to show any message
    def showMessage(self,message):
        print(str(message))
        pass


        