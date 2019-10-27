from datetime import datetime


def main():
    show_current_time()


def show_current_time():
    """
    Displays the current date and time.
    """
    current_datetime = datetime.now()
    print("Current Date and Time:", current_datetime.strftime(
          "%Y-%m-%d %H:%M:%S"))


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
