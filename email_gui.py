import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from main import EmailGenerator  # Import your existing class


class EmailGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mantel Email Generator")
        self.root.geometry("1200x800")

        # Initialize backend components
        self.email_generator = EmailGenerator()

        # Store current ticket info
        self.current_ticket_id = None
        self.current_language = 'en'

        # Create GUI components
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        # Ticket ID Section
        self.ticket_frame = ttk.LabelFrame(self.root, text="Ticket Information", padding=10)
        self.ticket_label = ttk.Label(self.ticket_frame, text="Ticket ID:")
        self.ticket_entry = ttk.Entry(self.ticket_frame, width=20)
        self.fetch_button = ttk.Button(
            self.ticket_frame,
            text="Fetch Ticket",
            command=self.fetch_ticket_data
        )

        # Customer Email Display
        self.customer_frame = ttk.LabelFrame(self.root, text="Customer Email Content", padding=10)
        self.customer_text = scrolledtext.ScrolledText(
            self.customer_frame,
            wrap=tk.WORD,
            height=10,
            state='disabled'
        )

        # Employee Notes Input
        self.notes_frame = ttk.LabelFrame(self.root, text="Employee Notes", padding=10)
        self.notes_text = scrolledtext.ScrolledText(
            self.notes_frame,
            wrap=tk.WORD,
            height=8
        )

        # Generate Button
        self.generate_button = ttk.Button(
            self.root,
            text="Generate Email",
            command=self.generate_email_response
        )

        # Output Display
        self.output_frame = ttk.LabelFrame(self.root, text="Generated Email", padding=10)
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            wrap=tk.WORD,
            height=15,
            state='disabled'
        )

    def setup_layout(self):
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Ticket frame
        self.ticket_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        self.ticket_label.pack(side='left')
        self.ticket_entry.pack(side='left', padx=5)
        self.fetch_button.pack(side='left', padx=5)

        # Customer email frame
        self.customer_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        self.customer_text.pack(fill='both', expand=True)

        # Employee notes frame
        self.notes_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        self.notes_text.pack(fill='both', expand=True)

        # Generate button
        self.generate_button.grid(row=3, column=0, sticky='e', padx=10, pady=5)

        # Output frame
        self.output_frame.grid(row=4, column=0, sticky='nsew', padx=10, pady=5)
        self.output_text.pack(fill='both', expand=True)

    def fetch_ticket_data(self):
        ticket_id = self.ticket_entry.get().strip()
        if not ticket_id:
            messagebox.showwarning("Input Error", "Please enter a valid Ticket ID")
            return

        try:
            # Get customer content from backend
            customer_content = self.email_generator.get_customer_content(ticket_id)
            if not customer_content:
                messagebox.showerror("Error", "Failed to fetch ticket data")
                return

            # Update customer display
            self.customer_text.config(state='normal')
            self.customer_text.delete('1.0', tk.END)
            self.customer_text.insert(tk.END, customer_content)
            self.customer_text.config(state='disabled')

            # Detect language
            self.current_language = self.email_generator.detect_language(customer_content)
            self.current_ticket_id = ticket_id

            messagebox.showinfo(
                "Success",
                f"Loaded Ticket {ticket_id}\nDetected language: {self.current_language.upper()}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch ticket: {str(e)}")

    def generate_email_response(self):
        if not self.current_ticket_id:
            messagebox.showwarning("Error", "No ticket loaded. Please fetch a ticket first.")
            return

        # Get employee notes
        employee_notes = self.notes_text.get('1.0', tk.END).strip()
        if not employee_notes:
            messagebox.showwarning("Input Error", "Please enter employee notes")
            return

        try:
            # Get customer content from display
            self.customer_text.config(state='normal')
            customer_content = self.customer_text.get('1.0', tk.END)
            self.customer_text.config(state='disabled')

            # Generate email
            generated_email = self.email_generator.generate_email(
                customer_content,
                employee_notes,
                self.current_language
            )

            # Display output
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, generated_email)
            self.output_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Generation Error", f"Failed to generate email: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailGeneratorApp(root)
    root.mainloop()