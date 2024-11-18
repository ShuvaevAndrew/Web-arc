import curses
from presentation_layer import PresentationLayer
from business_logic import BusinessLogicLayer
from data_access_layer import DataAccessLayer

def main(stdscr):
    try:
        data_access = DataAccessLayer()
        data_access.connect()

        business_logic = BusinessLogicLayer(data_access)
        presentation = PresentationLayer(stdscr, business_logic)

        if presentation.authenticate():  
            presentation.display_tables()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    curses.wrapper(main)
