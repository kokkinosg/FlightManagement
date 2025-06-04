import sqlite3
import pandas as pd
from models.DBSetUpModel import DBSetUpModel
from view.view import View
from models.FlightsModel import FlightsModel
from Controller.Controller import Controller

def main():

    try:
        # Connect to the database. If there isn't one, it will create it. 
        print ("Connecting to the database...")
        dbConnection = sqlite3.connect("FlightManagementDB.db")
        cursor = dbConnection.cursor()
        print ("Connection successfull!")

        view = View()
        flightsModel = FlightsModel()
        dbSetUpModel = dbSetUpModel()
        controller = Controller(view, dbSetUpModel,flightsModel)
        controller.run()



    except Exception as e:
        print("Error during initialisation of DBOperations: ", e)

    





    # # Create a DBOperations object which calls the constructor 
    # db = DBSetUpModel()
    # view = View()
    # view.displayMenu()
    # view.showMessage("User selected menu option " + str(view.getMenuSelection()))

    # # Close connection
    # db.close()

if __name__ == "__main__":
    main()
