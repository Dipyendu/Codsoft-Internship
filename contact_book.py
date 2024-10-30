import customtkinter as ctk
from tkinter import messagebox, ttk, Text, END
import sqlite3

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Contact Book")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Initialize database
        self.init_db()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI components
        self.create_widgets()
    
    def init_db(self):
        """Initialize the SQLite database and contacts table."""
        self.conn = sqlite3.connect("contacts.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT
            )
        """)
        self.conn.commit()
    
    def create_widgets(self):
        """Create and layout all GUI components."""
        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title Label
        title_label = ctk.CTkLabel(main_frame, text="Contact Book", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="n")
        
        # Upper Frame for Add/Search
        upper_frame = ctk.CTkFrame(main_frame)
        upper_frame.grid(row=1, column=0, sticky="nsew")
        upper_frame.grid_columnconfigure(0, weight=1)
        upper_frame.grid_columnconfigure(1, weight=1)
        upper_frame.grid_columnconfigure(2, weight=1)
        
        # Add Contact Button
        add_button = ctk.CTkButton(upper_frame, text="Add Contact", command=self.open_add_contact_window)
        add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Search Entry
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(upper_frame, placeholder_text="Search by Name or Phone", textvariable=self.search_var)
        search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Search Button
        search_button = ctk.CTkButton(upper_frame, text="Search", command=self.search_contacts)
        search_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Treeview Frame
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.grid(row=0, column=1, sticky="ns")
        
        # Treeview for Contact List
        self.contact_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
        self.contact_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll.config(command=self.contact_tree.yview)
        
        # Define columns
        self.contact_tree['columns'] = ("Name", "Phone", "Email", "Address")
        self.contact_tree.column("#0", width=0, stretch=False)  # Hidden ID column
        self.contact_tree.column("Name", anchor="w", width=200)
        self.contact_tree.column("Phone", anchor="center", width=120)
        self.contact_tree.column("Email", anchor="w", width=200)
        self.contact_tree.column("Address", anchor="w", width=200)
        
        # Define headings
        self.contact_tree.heading("#0", text="", anchor="w")
        self.contact_tree.heading("Name", text="Name", anchor="w")
        self.contact_tree.heading("Phone", text="Phone", anchor="center")
        self.contact_tree.heading("Email", text="Email", anchor="w")
        self.contact_tree.heading("Address", text="Address", anchor="w")
        
        # Bind double-click event to edit contact
        self.contact_tree.bind("<Double-1>", self.on_double_click)
        
        # Populate the treeview with all contacts
        self.load_contacts()
        
        # Lower Frame for Update/Delete
        lower_frame = ctk.CTkFrame(main_frame)
        lower_frame.grid(row=3, column=0, pady=10, sticky="ew")
        lower_frame.grid_columnconfigure(0, weight=1)
        lower_frame.grid_columnconfigure(1, weight=1)
        
        # Update Contact Button
        update_button = ctk.CTkButton(lower_frame, text="Update Contact", command=self.open_update_contact_window)
        update_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Delete Contact Button
        delete_button = ctk.CTkButton(lower_frame, text="Delete Contact", command=self.delete_contact)
        delete_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    def load_contacts(self, contacts=None):
        """Load contacts into the treeview. If contacts is None, load all from DB."""
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        if contacts is None:
            self.cursor.execute("SELECT * FROM contacts")
            contacts = self.cursor.fetchall()
        
        for contact in contacts:
            self.contact_tree.insert(parent='', index='end', iid=contact[0], text='', 
                                     values=(contact[1], contact[2], contact[3], contact[4]))
    
    def open_add_contact_window(self):
        """Open a new window to add a contact."""
        add_window = ctk.CTkToplevel(self)
        add_window.title("Add New Contact")
        add_window.geometry("400x400")
        add_window.resizable(False, False)
        
        # Add Frame without padding in constructor
        add_frame = ctk.CTkFrame(add_window)
        add_frame.pack(fill="both", expand=True, padx=20, pady=20)  # Apply padding here
        add_frame.grid_columnconfigure(1, weight=1)
        
        # Name
        name_label = ctk.CTkLabel(add_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter name")
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Phone
        phone_label = ctk.CTkLabel(add_frame, text="Phone Number:")
        phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        phone_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter phone number")
        phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Email
        email_label = ctk.CTkLabel(add_frame, text="Email:")
        email_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        email_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter email address")
        email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Address
        address_label = ctk.CTkLabel(add_frame, text="Address:")
        address_label.grid(row=3, column=0, padx=10, pady=10, sticky="ne")
        
        # Using standard tkinter Text widget as CTkTextbox does not exist
        address_text = Text(add_frame, width=30, height=5, font=("Arial", 12))
        address_text.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # Add Button
        add_contact_button = ctk.CTkButton(add_frame, text="Add Contact", command=lambda: self.add_contact(
            add_window, name_entry.get(), phone_entry.get(), email_entry.get(), address_text.get("1.0", END).strip()
        ))
        add_contact_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    def add_contact(self, window, name, phone, email, address):
        """Add a new contact to the database."""
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone Number are required.")
            return
        try:
            self.cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                                (name, phone, email, address))
            self.conn.commit()
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            window.destroy()
            self.load_contacts()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def search_contacts(self):
        """Search contacts by name or phone number."""
        query = self.search_var.get().strip()
        if not query:
            self.load_contacts()
            return
        try:
            self.cursor.execute("""
                SELECT * FROM contacts 
                WHERE name LIKE ? OR phone LIKE ?
            """, (f'%{query}%', f'%{query}%'))
            results = self.cursor.fetchall()
            self.load_contacts(results)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def on_double_click(self, event):
        """Handle double-click event to update contact."""
        self.open_update_contact_window()
    
    def open_update_contact_window(self):
        """Open a window to update the selected contact."""
        selected = self.contact_tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")
            return
        
        # Fetch contact details
        self.cursor.execute("SELECT * FROM contacts WHERE id=?", (selected,))
        contact = self.cursor.fetchone()
        if not contact:
            messagebox.showerror("Error", "Selected contact not found.")
            return
        
        # Update Window
        update_window = ctk.CTkToplevel(self)
        update_window.title("Update Contact")
        update_window.geometry("400x400")
        update_window.resizable(False, False)
        
        # Update Frame without padding in constructor
        update_frame = ctk.CTkFrame(update_window)
        update_frame.pack(fill="both", expand=True, padx=20, pady=20)  # Apply padding here
        update_frame.grid_columnconfigure(1, weight=1)
        
        # Name
        name_label = ctk.CTkLabel(update_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = ctk.CTkEntry(update_frame, placeholder_text="Enter name")
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        name_entry.insert(0, contact[1])
        
        # Phone
        phone_label = ctk.CTkLabel(update_frame, text="Phone Number:")
        phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        phone_entry = ctk.CTkEntry(update_frame, placeholder_text="Enter phone number")
        phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        phone_entry.insert(0, contact[2])
        
        # Email
        email_label = ctk.CTkLabel(update_frame, text="Email:")
        email_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        email_entry = ctk.CTkEntry(update_frame, placeholder_text="Enter email address")
        email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        email_entry.insert(0, contact[3])
        
        # Address
        address_label = ctk.CTkLabel(update_frame, text="Address:")
        address_label.grid(row=3, column=0, padx=10, pady=10, sticky="ne")
        
        # Using standard tkinter Text widget as CTkTextbox does not exist
        address_text = Text(update_frame, width=30, height=5, font=("Arial", 12))
        address_text.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        address_text.insert("1.0", contact[4])
        
        # Update Button
        update_contact_button = ctk.CTkButton(update_frame, text="Update Contact", command=lambda: self.update_contact(
            selected, name_entry.get(), phone_entry.get(), email_entry.get(), address_text.get("1.0", END).strip(), update_window
        ))
        update_contact_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    def update_contact(self, contact_id, name, phone, email, address, window):
        """Update the contact details in the database."""
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone Number are required.")
            return
        try:
            self.cursor.execute("""
                UPDATE contacts
                SET name = ?, phone = ?, email = ?, address = ?
                WHERE id = ?
            """, (name, phone, email, address, contact_id))
            self.conn.commit()
            messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
            window.destroy()
            self.load_contacts()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def delete_contact(self):
        """Delete the selected contact."""
        selected = self.contact_tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")
            return
        
        # Fetch contact details
        self.cursor.execute("SELECT name FROM contacts WHERE id=?", (selected,))
        contact = self.cursor.fetchone()
        if not contact:
            messagebox.showerror("Error", "Selected contact not found.")
            return
        
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete contact '{contact[0]}'?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM contacts WHERE id=?", (selected,))
                self.conn.commit()
                messagebox.showinfo("Success", f"Contact '{contact[0]}' deleted successfully!")
                self.load_contacts()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def on_closing(self):
        """Handle application closing."""
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = ContactBookApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
