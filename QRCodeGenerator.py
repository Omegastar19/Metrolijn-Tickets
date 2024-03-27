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
