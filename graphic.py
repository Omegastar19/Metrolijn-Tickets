import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import qrcode

class PDFGenerator:
    def __init__(self):
        pass

    def save_ticket_information_as_pdf(self, age, ticket_type, price, num_zones=None, filename_prefix="ticket"):
        # Automatically generate PDF without user input
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
        messagebox.showinfo("PDF Generated", f"PDF generated: {filename}")

class QRCodeGenerator:
    def __init__(self):
        pass

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
        print("QR code generated:", filename)

class TicketPricingApp:
    def __init__(self, master):
        self.master = master
        master.title("Ticket Pricing Calculator")
        # Set window size
        width = 400
        height = 300

        # Get screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calculate x and y coordinates for the Tk root window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        # Set the geometry string
        master.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        self.label_age = tk.Label(master, text="Enter your age:")
        self.label_age.pack()

        self.entry_age = tk.Entry(master)
        self.entry_age.pack()

        self.label_zones = tk.Label(master, text="Enter the number of zones (1-4):")
        self.label_zones.pack()

        self.entry_zones = tk.Entry(master)
        self.entry_zones.pack()

        self.ticket_type = tk.StringVar()
        self.ticket_type.set("single")

        self.single_radio = tk.Radiobutton(master, text="Single", variable=self.ticket_type, value="single")
        self.single_radio.pack()

        self.daypass_radio = tk.Radiobutton(master, text="Daypass", variable=self.ticket_type, value="daypass")
        self.daypass_radio.pack()

        self.generate_pdf_var = tk.IntVar(value=0)
        self.generate_pdf_checkbox = tk.Checkbutton(master, text="Generate PDF", variable=self.generate_pdf_var)
        self.generate_pdf_checkbox.pack()

        self.generate_qr_var = tk.IntVar(value=0)
        self.generate_qr_checkbox = tk.Checkbutton(master, text="Generate QR Code", variable=self.generate_qr_var)
        self.generate_qr_checkbox.pack()

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.pdf_generator = PDFGenerator()  # Create an instance of PDFGenerator
        self.qr_code_generator = QRCodeGenerator()

    def calculate(self):
        try:
            age = int(self.entry_age.get())
            ticket_type = self.ticket_type.get()
            num_zones = int(self.entry_zones.get()) if ticket_type == 'single' else 0

            price = calculate_ticket_price(age, ticket_type, num_zones)
            self.show_result(age, ticket_type, price, num_zones)

            # Check if PDF generation is requested
            if self.generate_pdf_var.get() == 1:
                self.generate_pdf(age, ticket_type, price, num_zones)

            if self.generate_qr_var.get() == 1:
                self.qr_code_generator.generate_qr_code(age, ticket_type, price, num_zones)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_result(self, age, ticket_type, price, num_zones=None):
        result_text = f"Age: {age}\nTicket Type: {ticket_type.capitalize()}\n"
        if ticket_type == 'single':
            result_text += f"Number of Zones: {num_zones}\n"
        result_text += f"The price of your {ticket_type} ticket is: {price:.2f} euro."
        messagebox.showinfo("Ticket Information", result_text)
        self.master.quit()

    def generate_pdf(self, age, ticket_type, price, num_zones=None):
        self.pdf_generator.save_ticket_information_as_pdf(age, ticket_type, price, num_zones)

def calculate_ticket_price(age, ticket_type, num_zones):
    base_single_ticket_price = 2.50
    base_daypass_price = 12.00

    if ticket_type == "single":
        if age < 3:
            return 0.00
        else:
            return min(base_single_ticket_price * num_zones, base_single_ticket_price * 4)
    elif ticket_type == "daypass":
        if age >= 65:
            return 9.50
        elif age < 3:
            return 0.00
        elif age < 13:
            return 5.00
        else:
            return base_daypass_price
    else:
        raise ValueError("Invalid ticket type. Please choose 'single' or 'daypass'.")

def main():
    root = tk.Tk()
    app = TicketPricingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
