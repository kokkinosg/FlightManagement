import sqlite3
import pandas as pd
from models.DBSetUpModel import DBSetUpModel
from view.view import View
from models.FlightsModel import FlightsModel
from Controller.Controller import Controller
from models.PilotModel import PilotModel

def main():
        
    # Connect to the database. If there isn't one, it will create it. 
    print ("Connecting to the database...")
    dbConnection = sqlite3.connect("FlightManagementDB.db")
    cursor = dbConnection.cursor()
    print ("Connection successfull!")

    view = View(dbConnection, cursor)
    flightsModel = FlightsModel(dbConnection, cursor)
    pilotModel = PilotModel(dbConnection)
    dbSetUpModel = DBSetUpModel(dbConnection,cursor)
    controller = Controller(view, dbSetUpModel,flightsModel, pilotModel)

    print("Creating the required tables for testing...")
    dbSetUpModel.createAllTables()
    print("Populate the required tables for testing...")
    dbSetUpModel.addAllSampleData()

    controller.run()

if __name__ == "__main__":
    main()
