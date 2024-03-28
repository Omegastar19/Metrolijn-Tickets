import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class TicketPricingApp:
    def __init__(self, master):
        self.master = master
        master.title("Ticket Pricing Calculator")

        self.label_age = tk.Label(master, text="Enter your age:")
        self.label_age.pack()

        self.entry_age = tk.Entry(master)
        self.entry_age.pack()

        self.label_ticket_type = tk.Label(master, text="Enter ticket type (single/daypass):")
        self.label_ticket_type.pack()

        self.entry_ticket_type = tk.Entry(master)
        self.entry_ticket_type.pack()

        self.label_zones = tk.Label(master, text="Enter the number of zones (1-4):")
        self.label_zones.pack()

        self.entry_zones = tk.Entry(master)
        self.entry_zones.pack()

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

    def calculate(self):
        try:
            age = int(self.entry_age.get())
            ticket_type = self.entry_ticket_type.get().lower()

            if ticket_type not in ['single', 'daypass']:
                raise ValueError("Invalid ticket type. Please choose 'single' or 'daypass'.")

            num_zones = int(self.entry_zones.get()) if ticket_type == 'single' else 0

            price = calculate_ticket_price(age, ticket_type, num_zones)
            self.show_result(age, ticket_type, price, num_zones)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_result(self, age, ticket_type, price, num_zones=None):
        result_text = f"Age: {age}\nTicket Type: {ticket_type.capitalize()}\n"
        if ticket_type == 'single':
            result_text += f"Number of Zones: {num_zones}\n"
        result_text += f"The price of your {ticket_type} ticket is: {price:.2f} euro."
        messagebox.showinfo("Ticket Information", result_text)
        self.master.quit()

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
