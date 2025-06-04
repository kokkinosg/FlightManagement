    # Connect to the database. If there isn't one, it will create it. 
        print ("Connecting to the database...")
        dbConnection = sqlite3.connect("FlightManagementDB.db")
        cursor = dbConnection.cursor()
        print ("Connection successfull!")

        view = View()
        flightsModel = FlightsModel()
        dbSetUpModel = DBSetUpModel(dbConnection,cursor)
        controller = Controller(view, dbSetUpModel,flightsModel)
        controller.run()