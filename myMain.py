from DBOperations import DBOperations

def main():
    # Create a DBOperations object which calls the constructor 
    db = DBOperations()

    # Close connection
    db.close()

if __name__ == "__main__":
    main()
