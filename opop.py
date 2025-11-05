def read_float(prompt):
    """Read a float from user input and return it."""
    return float(input(prompt))


def c_to_f(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def f_to_c(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def do_c_to_f():
    """Handle conversion from Celsius to Fahrenheit."""
    c = read_float("Celsius: ")
    result = c_to_f(c)
    print("Fahrenheit:", result)


def do_f_to_c():
    """Handle conversion from Fahrenheit to Celsius."""
    f = read_float("Fahrenheit: ")
    result = f_to_c(f)
    print("Celsius:", result)


def menu_loop():
    """Display menu options and route user choices."""
    choice = ""
    while choice != "3":
        print("1) C to F  2) F to C  3) Quit")
        choice = input("Choose: ")

        if choice == "1":
            do_c_to_f()
        elif choice == "2":
            do_f_to_c()
        elif choice == "3":
            print("Goodbye")
        else:
            print("Invalid")

def main():
    menu_loop()


if __name__ == "__main__":
    main()