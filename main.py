import sys

def calculate_ticket_price(age, ticket_type, num_zones):
    # Basis-prijs van tickets
    base_single_ticket_price = 2.50
    base_daypass_price = 12.00

    # Berekening van de prijs van een losse ticket
    if ticket_type == "single":
        if age < 3:
            return 0.00
        else:
            return min(base_single_ticket_price * num_zones, base_single_ticket_price * 4)
    # Berekening van de prijs van een dagkaart
    elif ticket_type == "daypass":
        if age >= 65:
            return 9.50
        elif age < 3:
            return 0.00  # Children under 3 travel for free
        elif age < 13:
            return 5.00
        else:
            return base_daypass_price
    else:
        raise ValueError("Invalid ticket type. Please choose 'single' or 'daypass.'")

def get_num_zones():
    try:
        num_zones = int(input("Enter the number of zones (1-4): "))
        if not (1 <= num_zones <= 4):
            print("Invalid number of zones. Please enter a number between 1 and 4.")
            return None
        return num_zones
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

def main():
    while True:
        try:
            age = int(input("Enter your age: "))
            ticket_type = input("Enter ticket type (single/daypass): ").lower()

            if ticket_type not in ['single', 'daypass']:
                raise ValueError("Invalid ticket type. Please choose 'single' or 'daypass.'")

            num_zones = get_num_zones() if ticket_type == 'single' else 0

            price = calculate_ticket_price(age, ticket_type, num_zones)
            print(f"Ticket Type: {ticket_type.capitalize()}")
            print(f"The price of your {ticket_type} ticket is: {price:.2f} euro.")

            repeat = input("Do you want to calculate another ticket price? (yes/no): ")
            if repeat.lower() != 'yes':
                sys.exit()

        except ValueError as e:
            print(f"Error: {e}. Please enter valid inputs.")

if __name__ == "__main__":
    main()
