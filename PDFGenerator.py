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
