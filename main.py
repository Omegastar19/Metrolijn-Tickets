import qrcode
import sys
from datetime import datetime
from fpdf import FPDF

class PDFGenerator:
    def save_ticket_information_as_pdf(self, age, ticket_type, price, num_zones=None, filename_prefix="ticket"):
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{filename_prefix}_{date_str}.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Ticket Information", ln=True, align="C")
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
        pdf.cell(200, 10, txt=f"Ticket Type: {ticket_type.capitalize()}", ln=True)
        if ticket_type == 'single':
            pdf.cell(200, 10, txt=f"Number of Zones: {num_zones}", ln=True)
        pdf.cell(200, 10, txt=f"The price of your {ticket_type} ticket is: {price:.2f} euro.", ln=True)
        pdf.cell(200, 10, txt="Ticket generated on: " + datetime.now().strftime("%Y-%m-%d"), ln=True)
        pdf.output(filename)

class QRCodeGenerator:
    def generate_qr_code(self, age, ticket_type, price, num_zones=None):
        qr_data = f"Age: {age}\nTicket Type: {ticket_type.capitalize()}\n"
        if ticket_type == 'single':
            qr_data += f"Number of Zones: {num_zones}\n"
        qr_data += f"The price of your {ticket_type} ticket is: {price:.2f} euro.\n"
        qr_data += "Ticket generated on: " + datetime.now().strftime("%Y-%m-%d")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"ticket_qr_code_{date_str}.png"

        qr_image.save(filename)
        return filename

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

    def generate_ticket_qr_code(self, age, ticket_type, price, num_zones=None):
        return self.qr_generator.generate_qr_code(age, ticket_type, price, num_zones)

    def generate_ticket_pdf(self, age, ticket_type, price, num_zones=None):
        self.pdf_generator.save_ticket_information_as_pdf(age, ticket_type, price, num_zones)

    def main(self):
        while True:
            try:
                age = int(input("Enter your age: "))
                ticket_type = input("Enter ticket type (single/daypass): ").lower()

                if ticket_type not in ['single', 'daypass']:
                    raise ValueError("Invalid ticket type. Please choose 'single' or 'daypass.'")

                num_zones = self.get_num_zones() if ticket_type == 'single' else 0

                price = self.calculate_ticket_price(age, ticket_type, num_zones)
                self.print_ticket_information(age, ticket_type, price, num_zones)

                generate_qr = input("Do you want to generate a QR code for this ticket? (yes/no): ")
                if generate_qr.lower() == 'yes':
                    qr_filename = self.generate_ticket_qr_code(age, ticket_type, price, num_zones)
                    print("QR code generated:", qr_filename)

                generate_pdf = input("Do you want to generate a PDF for this ticket? (yes/no): ")
                if generate_pdf.lower() == 'yes':
                    self.generate_ticket_pdf(age, ticket_type, price, num_zones)
                    print("PDF generated.")

                repeat = input("Do you want to calculate another ticket price? (yes/no): ")
                if repeat.lower() != 'yes':
                    sys.exit()

            except ValueError as e:
                print(f"Error: {e}. Please enter valid inputs.")

if __name__ == "__main__":
    ticket_calculator = TicketCalculator()
    ticket_calculator.main()
