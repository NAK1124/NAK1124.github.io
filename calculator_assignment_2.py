"""
Mini-Project: Multi-Purpose Calculator
Author  : Alice Kim
Purpose : To demonstrate how constants, functions, and control flow work together in a Python program by creating a multi-purpose calculator.
"""

# ---------------------------- CONSTANTS -----------------------------
"""
These are constants. DO NOT TOUCH.
"""
MENU_TEXT = """
================ Multi-Base Calculator ================
[A]dd  [S]ubtract  [M]ultiply       [D]ivide
[C]onvert Base     [AS]CII_lookup   [Q]uit
--------------------------------------------------------
Choose an option: """
DIV_ZERO_MSG = "Cannot divide by zero!"
INVALID_MSG  = "Invalid selection. Try again!"

# ---------------------------- FUNCTIONS -----------------------------
def add(a: int, b: int) -> int:
    """Return the sum of a and b"""
    return a + b

# TODO: create functions for subtract, multiply, divide
def subtract(a: int, b: int) -> int:
    """Return the difference of two integers a and b."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Return the product of two integers a and b."""
    return a * b

def divide(a: int, b: int):
    """Divide a by b. Print error if dividing by zero."""
    if b == 0:
        print(DIV_ZERO_MSG)
        return None
    return a / b

def convert_base():
    """Prompt user for which base to convert,
    then display conversion"""
    # TODO: implement base conversion
    number = int(input("Please enter a decimal number you want to convert:"))
    common_base = input("Convert to (2=binary, 10=decimal, 16=hexadecimal):")
    
    if common_base == "2":
        print(bin(number))
    elif common_base == "10":
        print(number)
    elif common_base == "16":
        print(hex(number))
    else:
        print(INVALID_MSG)
    

def ascii_lookup():
    """Convert the characters to their ascii values"""
    # TODO: implement the ASCII Conversion
    letter = input("Enter a character:").strip()
    if len(letter) == 1:
        print(ord(letter))
    else:
        print(INVALID_MSG)

def main() -> None:
    """Main program loop. (Don't worry about while loop)
    Do not modify the structure! Just add the functions to where appropriate"""
    while True:
        choice = input(MENU_TEXT).strip().lower()
        if choice == 'q':
            print("Good-bye!")
            break
        
        elif choice == 'a':
        # TODO: ask for inputs and apply add function accordingly
        # … additional elif blocks …
        # TODO implement the other features depending on the user input
            a = int(input("Enter first number:"))
            b = int(input("Enter second number:"))
            print(add(a,b))
            
        elif choice == "s":
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
            print(subtract(a,b))
            
        elif choice == 'm':
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
            print(multiply(a,b))
            
        elif choice == 'd':
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
            print(divide(a,b))
                
        elif choice == 'c':
            convert_base()
            
        elif choice == 'as':
            ascii_lookup()        
            
        else:
            print(INVALID_MSG)


if __name__ == "__main__":
    main()
