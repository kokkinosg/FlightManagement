import sqlite3

# This class is for creating the tables and populating them with sample data. 
class DBSetUpModel:

    # Constructor
    # Class attributes are created here.
    # Upon instantiation of this class, it connects to the database and creates the tables if they do not already exist. 
    def __init__(self, dbConnection, cursor ):
        try:
            self.dbConnection = dbConnection
            self.cur = cursor
        except Exception as e:
            print("Error during initialisation of DBSetUpModel: ", e)

    def createAllTables(self):
        try:
            print("Creating tables...")
            self._create_table(self._create_flights_table_querry())
            self._create_table(self._create_airport_table_querry())
            self._create_table(self._create_aircraft_table_querry())
            self._create_table(self._create_pilot_table_querry())

            print("Tables created successfully!")
        except Exception as e:
            print("Error in creating all tables: " + str(e))
    
    def addAllSampleData(self):
        try:
            print("Adding sample data to the database...")

            self._add_sample_data_to_table(self._create_raw_aircraft_data_querries())
            print ("Sample aircraft data added successfully.")

            self._add_sample_data_to_table(self._create_raw_flight_data_querries())
            print ("Sample flight data added successfully.")

            self._add_sample_data_to_table(self._create_raw_pilot_data_querries())
            print ("Sample pilot data added successfully.")

            self._add_sample_data_to_table(self._create_raw_airport_data_querries())
            print ("Sample airport data added successfully.")

            print("All sample data added succesfully!")
        except Exception as e:
            print("Error in populating all tables with sample data: " + str(e))


    # Close connection to the database
    def close(self):
        try: 
            self.dbConnection.close()
            print("Connection closed succesffully!")
        except Exception as e:
            print("Error whilst attempting to close the connection: " + e)

    # Private methods
    # This method creates all the necessary tables if they do not exist. It is called in the constructor. 
    def _create_table(self, sqlQuerry):
        # Pass the table creation SQL querries to the cursor and execute them. 
        self.cur.execute(sqlQuerry)
        # Commit the change
        self.dbConnection.commit()
        pass

    # SQL querry to create the flights table
    def _create_flights_table_querry(self):
        sqlQuerry = '''CREATE TABLE IF NOT EXISTS flights (
            flightID INTEGER PRIMARY KEY AUTOINCREMENT,
            aircraftID INTEGER NOT NULL,
            pilotID INTEGER NOT NULL,
            fromDestinationID INTEGER NOT NULL,
            toDestinationID INTEGER NOT NULL,
            departTime DATETIME NOT NULL,
            arrivalTime DATETIME NOT NULL,
            passengerCount INTEGER NOT NULL,
            travelDistanceKM FLOAT NOT NULL CHECK (travelDistanceKM>0),
            status TEXT CHECK(status IN ('As planned', 'Delayed', 'Cancelled')),
            FOREIGN KEY (aircraftID) REFERENCES aircraft(aircraftID),
            FOREIGN KEY (pilotID) REFERENCES pilot(pilotID),
            FOREIGN KEY (fromDestinationID) REFERENCES airport(airportID),
            FOREIGN KEY (toDestinationID) REFERENCES airport(airportID)
            );'''
        return sqlQuerry
    
    # SQL querry to create the airport table
    def _create_airport_table_querry(self):
        sqlQuerry = '''CREATE TABLE IF NOT EXISTS airport (
            airportID INTEGER PRIMARY KEY AUTOINCREMENT,
            airportName TEXT NOT NULL,
            city TEXT,
            country TEXT,
            postCode TEXT NOT NULL
            );'''
        return sqlQuerry
    
    # SQL querry to create the pilot table
    def _create_pilot_table_querry(self):
        sqlQuerry = '''CREATE TABLE IF NOT EXISTS pilot (
            pilotID INTEGER PRIMARY KEY AUTOINCREMENT,
            pilotName TEXT NOT NULL,
            pilotSurname TEXT NOT NULL,
            gender TEXT CHECK (gender IN ('Male', 'Female')),
            licenseNumber TEXT UNIQUE NOT NULL,
            experienceYears INTEGER,
            aircraftID INTEGER NOT NULL,
            currentLocationID INTEGER NOT NULL,
            FOREIGN KEY (aircraftID) REFERENCES aircraft(aircraftID),
            FOREIGN KEY (currentLocationID) REFERENCES airport(airportID)
            );'''
        return sqlQuerry
    
    # SQL querry to create the aircraft table
    def _create_aircraft_table_querry(self):
        sqlQuerry ='''CREATE TABLE IF NOT EXISTS aircraft (
            aircraftID INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            airline TEXT NOT NULL,
            manufacturer TEXT,
            capacity INTEGER CHECK (capacity > 0),
            rangeKM FLOAT CHECK (rangeKM > 0),
            currentLocationID INTEGER NOT NULL,
            FOREIGN KEY (currentLocationID) REFERENCES airport(airportID)
            );'''
        return sqlQuerry
    
    # Add sample data to each table
    def _add_sample_data_to_table(self, querriesArray):
        for querry in querriesArray:
                self.cur.execute(querry)
        self.dbConnection.commit()
        pass

    # SQL querries to insert raw data
    def _create_raw_flight_data_querries(self):
        sqlQuerries = [
            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (1, 1, 1, 101, 102, '2025-06-01 08:30:00', '2025-06-01 10:45:00', 120, 950.5, 'As planned');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (2, 2, 2, 102, 103, '2025-06-02 14:00:00', '2025-06-02 16:20:00', 95, 780.0, 'Delayed');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (3, 3, 1, 101, 104, '2025-06-03 09:00:00', '2025-06-03 12:30:00', 135, 1120.2, 'As planned');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (4, 4, 3, 103, 105, '2025-06-04 06:15:00', '2025-06-04 08:00:00', 85, 620.4, 'Cancelled');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (5, 2, 4, 104, 101, '2025-06-05 18:45:00', '2025-06-05 21:10:00', 100, 860.0, 'Delayed');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (6, 5, 5, 105, 101, '2025-06-06 07:00:00', '2025-06-06 09:15:00', 110, 970.3, 'As planned');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (7, 1, 2, 101, 103, '2025-06-07 13:30:00', '2025-06-07 15:50:00', 88, 890.0, 'Delayed');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (8, 2, 3, 102, 104, '2025-06-08 10:00:00', '2025-06-08 12:25:00', 140, 990.8, 'Cancelled');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (9, 3, 4, 103, 105, '2025-06-09 16:00:00', '2025-06-09 18:30:00', 160, 1025.1, 'As planned');''',

            '''INSERT OR IGNORE INTO flights (
                flightID, aircraftID, pilotID, fromDestinationID, toDestinationID,
                departTime, arrivalTime, passengerCount, travelDistanceKM, status
            ) VALUES
            (10, 4, 5, 104, 102, '2025-06-10 19:45:00', '2025-06-10 22:10:00', 105, 865.7, 'Delayed');''',
        ]
        return sqlQuerries
    
    def _create_raw_pilot_data_querries(self):
        sqlQuerries = [
            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (1, 'John', 'Smith', 'Male', 'LIC1234', 12, 1, 101);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (2, 'Maria', 'Lopez', 'Female', 'LIC2345', 9, 2, 102);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (3, 'Ahmed', 'Khan', 'Male', 'LIC3456', 15, 4, 103);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (4, 'Elena', 'Rossi', 'Female', 'LIC4567', 7, 2, 104);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (5, 'Rudolph', 'Rednose', 'Male', 'LIC4583', 8, 4, 105);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (6, 'Alice', 'Johnson', 'Female', 'LIC5678', 10, 1, 102);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (7, 'Bob', 'Lee', 'Male', 'LIC6789', 6, 2, 103);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (8, 'Clara', 'Chen', 'Female', 'LIC7890', 14, 3, 104);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (9, 'David', 'Singh', 'Male', 'LIC8901', 5, 4, 105);''',

            '''INSERT OR IGNORE INTO pilot (
                pilotID, pilotName, pilotSurname, gender, licenseNumber,
                experienceYears, aircraftID, currentLocationID
            ) VALUES
            (10, 'Eva', 'Martinez', 'Female', 'LIC9012', 11, 5, 101);'''
        ]
        return sqlQuerries
    
    def _create_raw_aircraft_data_querries(self):
        sqlQuerries = [
            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (1, 'A320', 'British Airways', 'Airbus', 180, 6100.0, 101);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (2, '737 MAX', 'Ryanair', 'Boeing', 200, 6500.0, 102);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (3, 'A330', 'Lufthansa', 'Airbus', 250, 11750.0, 104);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (4, '787 Dreamliner', 'Alitalia', 'Boeing', 296, 13620.0, 103);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (5, '888 Dreamliner', 'Cyprus Airwats', 'Boeing', 296, 19620.0, 105);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (6, 'B737-800', 'EasyJet', 'Boeing', 186, 5430.0, 102);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (7, 'A350', 'Qatar Airways', 'Airbus', 283, 15000.0, 103);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (8, 'E190', 'KLM', 'Embraer', 100, 4500.0, 104);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (9, 'CRJ900', 'Lufthansa', 'Bombardier', 90, 2900.0, 105);''',

            '''INSERT OR IGNORE INTO aircraft (
                aircraftID, model, airline, manufacturer,
                capacity, rangeKM, currentLocationID
            ) VALUES
            (10, 'A380', 'Emirates', 'Airbus', 517, 15200.0, 101);'''
        ]
        return sqlQuerries
    
    def _create_raw_airport_data_querries(self):
        sqlQuerries = [
            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (101, 'Heathrow Airport', 'London', 'UK', 'TW6 1EW');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (102, 'Charles de Gaulle Airport', 'Paris', 'France', '95700');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (103, 'Frankfurt Airport', 'Frankfurt', 'Germany', '60547');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (104, 'Madrid Barajas Airport', 'Madrid', 'Spain', '28042');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (105, 'Leonardo da Vinci Airport', 'Rome', 'Italy', '00054');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (106, 'Schiphol Airport', 'Amsterdam', 'Netherlands', '1118 CP');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (107, 'Zurich Airport', 'Zurich', 'Switzerland', '8058');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (108, 'Barcelona El Prat Airport', 'Barcelona', 'Spain', '08820');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (109, 'Vienna International Airport', 'Vienna', 'Austria', '1300');''',

            '''INSERT OR IGNORE INTO airport (
                airportID, airportName, city, country, postCode
            ) VALUES
            (110, 'Dublin Airport', 'Dublin', 'Ireland', 'K67');'''
        ]
        return sqlQuerries
    