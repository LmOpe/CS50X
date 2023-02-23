# TODO
# Main Function
def main():
    # Get user input and checks for correct input
    while True:
        try:
            height = int(input("Height: "))
            if height in range(1, 9):
                break
        except:
            print("That is invalid, type number between 1 and 8 both inclusive!")
    # Calls the print_block function
    print_block(height)


# Defines the print_block function
def print_block(height):
    # Prints each row
    for i in range(height):
        # Prints left white space
        for j in range(height - i - 1):
            print(" ", end="")
        # Prints left pyramids
        for n in range(i+1):
            print("#", end="")
        # Prints space between adjacent pyramids
        print("  ", end="")
        # Prints right pyramids
        for n in range(i+1):
            print("#", end="")
        # Jump to a new line
        print()


# Calls main function
main()
