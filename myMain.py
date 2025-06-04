from DBSetUpModel import DBSetUpModel
from view import View

def main():
    # Create a DBOperations object which calls the constructor 
    db = DBSetUpModel()
    view = View()
    view.displayMenu()
    view.showMessage("User selected menu option " + str(view.getMenuSelection()))

    # Close connection
    db.close()

if __name__ == "__main__":
    main()
