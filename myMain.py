import sqlite3
import pandas as pd
from models.DBSetUpModel import DBSetUpModel
from view.view import View
from Controller.Controller import Controller
from models.BaseModel import BaseModel

def main():
        
    # Connect to the database. If there isn't one, it will create it. 
    print ("Connecting to the database...")
    dbConnection = sqlite3.connect("FlightManagementDB.db")
    cursor = dbConnection.cursor()
    print ("Connection successfull!")

    # Instantiate all models, view and controller
    view = View()
    dbSetUpModel = DBSetUpModel(dbConnection,cursor)
    baseModel = BaseModel(dbConnection,cursor)
    controller = Controller(view, dbSetUpModel, baseModel)

    # Run the logic defined in the controller. 
    controller.run()

if __name__ == "__main__":
    main()
