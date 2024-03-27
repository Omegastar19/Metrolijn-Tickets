class TicketCalculator:
    def __init__(self):
        self.base_single_ticket_price = 2.50
        self.base_daypass_price = 12.00
        self.qr_generator = QRCodeGenerator()
        self.pdf_generator = PDFGenerator()

    def calculate_ticket_price(self, age, ticket_type, num_zones):
        if ticket_type == "single":
            if age < 3:
                return 0.00
            else:
                return min(self.base_single_ticket_price * num_zones, self.base_single_ticket_price * 4)
        elif ticket_type == "daypass":
            if age >= 65:
                return 9.50
            elif age < 3:
                return 0.00
            elif age < 13:
                return 5.00
            else:
                return self.base_daypass_price
        else:
            raise ValueError("Invalid ticket type. Please choose 'single' or 'daypass.'")

    def get_num_zones(self):
        try:
            num_zones = int(input("Enter the number of zones (1-4): "))
            if not (1 <= num_zones <= 4):
                print("Invalid number of zones. Please enter a number between 1 and 4.")
                return None
            return num_zones
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return None

    def print_ticket_information(self, age, ticket_type, price, num_zones=None):
        print(f"Age: {age}")
        print(f"Ticket Type: {ticket_type.capitalize()}")
        if ticket_type == 'single':
            print(f"Number of Zones: {num_zones}")
        print(f"The price of your {ticket_type} ticket is: {price:.2f} euro.")
        print("Ticket generated on:", datetime.now().strftime("%Y-%m-%d"))
