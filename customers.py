# """
# Customer Management Page (Performance Optimized with Pagination + Address)
# File: customers.py
# """

# import customtkinter as ctk
# from db import add_customer, get_all_customers, delete_customer, update_customer_remaining, update_customer
# import threading

# class Page(ctk.CTkFrame):
#     def __init__(self, parent, go_back_callback):
#         super().__init__(parent, fg_color="#f8f9fa")
#         self.go_back = go_back_callback
        
#         self.grid_rowconfigure(2, weight=1)
#         self.grid_columnconfigure(0, weight=1)
        
#         self.all_customers = []
#         self.filtered_customers = []
        
#         # Pagination
#         self.page_size = 15
#         self.current_page = 1
#         self.total_pages = 1
        
#         # Performance flags
#         self.is_loading = False
#         self.filter_timer = None
        
#         self.create_widgets()
#         self.load_customers_async()
    
#     def create_widgets(self):
#         """Create UI components"""
#         # Header
#         header = ctk.CTkFrame(self, fg_color="transparent")
#         header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
#         header.grid_columnconfigure(2, weight=1)
        
#         back_btn = ctk.CTkButton(
#             header, text="← Back", width=80, height=40,
#             command=self.go_back, fg_color="#666666", hover_color="#555555",
#             font=("Helvetica", 12, "bold")
#         )
#         back_btn.grid(row=0, column=0, padx=(0, 10))
        
#         title = ctk.CTkLabel(
#             header, text="👥 Customer Management",
#             font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
#         )
#         title.grid(row=0, column=1, sticky="w")
        
#         # Right side buttons
#         button_group = ctk.CTkFrame(header, fg_color="transparent")
#         button_group.grid(row=0, column=3, sticky="e")
        
#         refresh_btn = ctk.CTkButton(
#             button_group, text="🔄 Refresh", width=100, height=40,
#             command=self.load_customers_async, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 12, "bold")
#         )
#         refresh_btn.pack(side="left", padx=5)
        
#         # Search and Info bar
#         search_info_frame = ctk.CTkFrame(self, fg_color="transparent")
#         search_info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
#         search_info_frame.grid_columnconfigure(2, weight=1)
        
#         search_label = ctk.CTkLabel(search_info_frame, text="🔍 Search:", font=("Helvetica", 12, "bold"), text_color="#1f1f1f")
#         search_label.grid(row=0, column=0, padx=(0, 10))
        
#         self.search_entry = ctk.CTkEntry(search_info_frame, placeholder_text="Search by name, phone or address...", width=400, height=35, font=("Helvetica", 11))
#         self.search_entry.grid(row=0, column=1, padx=5)
#         self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
#         # Info text - moved to right
#         info_label = ctk.CTkLabel(
#             search_info_frame, text="ℹ️  Customers are automatically added during billing. You can edit or delete them below.",
#             font=("Helvetica", 11), text_color="#2563EB"
#         )
#         info_label.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
#         # Table frame - EXPANDED TO FULL HEIGHT
#         table_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
#         table_frame.grid_rowconfigure(1, weight=1)
#         table_frame.grid_columnconfigure(0, weight=1)
        
#         # Table header - Fixed width columns for proper alignment
#         header_frame = ctk.CTkFrame(table_frame, fg_color="#f0f0f0", corner_radius=8)
#         header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
#         header_frame.grid_columnconfigure(0, weight=1, minsize=140)
#         header_frame.grid_columnconfigure(1, weight=1, minsize=130)
#         header_frame.grid_columnconfigure(2, weight=2, minsize=200)
#         header_frame.grid_columnconfigure(3, weight=1, minsize=130)
#         header_frame.grid_columnconfigure(4, weight=1, minsize=90)
        
#         headers = ["Customer Name", "Phone Number", "Address", "Remaining Amount", "Actions"]
#         for i, h in enumerate(headers):
#             label = ctk.CTkLabel(
#                 header_frame, text=h, font=("Helvetica", 11, "bold"),
#                 text_color="#1f1f1f", anchor="w"
#             )
#             label.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
        
#         # Scrollable frame - takes full available space
#         self.scrollable_frame = ctk.CTkScrollableFrame(
#             table_frame, fg_color="transparent"
#         )
#         self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)
#         self.scrollable_frame._scrollbar.configure(width=12)
        
#         # Pagination frame - at bottom of table
#         pagination_container = ctk.CTkFrame(table_frame, fg_color="transparent")
#         pagination_container.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 10))
#         pagination_container.grid_columnconfigure(0, weight=1)
        
#         self.pagination_label = ctk.CTkLabel(
#             pagination_container,
#             text="Page 1 of 1",
#             font=("Helvetica", 11, "bold"), text_color="#1f1f1f"
#         )
#         self.pagination_label.grid(row=0, column=0, sticky="w", padx=5)
        
#         self.pagination_btn_frame = ctk.CTkFrame(pagination_container, fg_color="transparent")
#         self.pagination_btn_frame.grid(row=0, column=1, sticky="e")
    
#     def load_customers_async(self):
#         """Load customers in background thread"""
#         if self.is_loading:
#             return
        
#         self.is_loading = True
#         threading.Thread(target=self._load_customers_thread, daemon=True).start()
    
#     def _load_customers_thread(self):
#         """Background thread for loading customers"""
#         try:
#             self.all_customers = get_all_customers()
#             self.after(0, self._update_ui_after_load)
#         except Exception as e:
#             print(f"✗ Error loading customers: {e}")
#             self.is_loading = False
    
#     def _update_ui_after_load(self):
#         """Update UI after loading customers"""
#         self.schedule_filter()
#         self.is_loading = False
    
#     def on_search_change(self, event):
#         """Handle search input with debouncing"""
#         self.schedule_filter()
    
#     def schedule_filter(self):
#         """Schedule filter with debouncing to avoid excessive updates"""
#         if self.filter_timer:
#             self.after_cancel(self.filter_timer)
#         self.filter_timer = self.after(150, self.filter_customers)
    
#     def filter_customers(self):
#         """Filter customers based on search - optimized"""
#         if self.is_loading:
#             return
        
#         search_text = self.search_entry.get().lower()
        
#         # Optimize filtering with list comprehension - search in name, phone, and address
#         filtered = [c for c in self.all_customers 
#                    if search_text in c[1].lower() or search_text in c[2].lower() or search_text in c[3].lower()]
        
#         self.filtered_customers = filtered
#         self.total_pages = max(1, (len(filtered) + self.page_size - 1) // self.page_size)
#         self.current_page = 1
#         self.display_page()
    
#     def display_page(self):
#         """Display only the current page - optimized rendering"""
#         # Clear previous widgets efficiently
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()
        
#         start_idx = (self.current_page - 1) * self.page_size
#         end_idx = start_idx + self.page_size
#         page_customers = self.filtered_customers[start_idx:end_idx]
        
#         if not page_customers:
#             empty_label = ctk.CTkLabel(
#                 self.scrollable_frame,
#                 text="No customers found." if self.filtered_customers else "No customers added yet.",
#                 text_color="#999999", font=("Helvetica", 12, "bold")
#             )
#             empty_label.pack(pady=30)
#         else:
#             # Batch create rows
#             for customer in page_customers:
#                 self._create_customer_row(customer)
        
#         self._update_pagination()
    
#     def _create_customer_row(self, customer):
#         """Create a single customer row with proper table alignment"""
#         cust_id, name, phone, address, remaining = customer
        
#         row_frame = ctk.CTkFrame(
#             self.scrollable_frame, fg_color="white", corner_radius=8
#         )
#         row_frame.pack(fill="x", padx=5, pady=4)
        
#         # Fixed width columns matching header exactly
#         row_frame.grid_columnconfigure(0, weight=1, minsize=140)
#         row_frame.grid_columnconfigure(1, weight=1, minsize=130)
#         row_frame.grid_columnconfigure(2, weight=2, minsize=200)
#         row_frame.grid_columnconfigure(3, weight=1, minsize=130)
#         row_frame.grid_columnconfigure(4, weight=1, minsize=90)
        
#         amount_color = "#DC2626" if remaining > 0 else "#059669"
        
#         # Truncate address if too long for display
#         display_address = address[:40] + "..." if len(address) > 40 else address
        
#         # Create labels with consistent spacing and alignment
#         ctk.CTkLabel(
#             row_frame, text=name, font=("Helvetica", 11, "bold"),
#             anchor="w", text_color="#1f1f1f"
#         ).grid(row=0, column=0, padx=12, pady=10, sticky="ew")
        
#         ctk.CTkLabel(
#             row_frame, text=phone, font=("Helvetica", 11, "bold"),
#             anchor="w", text_color="#1f1f1f"
#         ).grid(row=0, column=1, padx=12, pady=10, sticky="ew")
        
#         ctk.CTkLabel(
#             row_frame, text=display_address, font=("Helvetica", 11, "bold"),
#             anchor="w", text_color="#666666"
#         ).grid(row=0, column=2, padx=12, pady=10, sticky="ew")
        
#         ctk.CTkLabel(
#             row_frame, text=f"₨{remaining:.2f}", font=("Helvetica", 11, "bold"),
#             text_color=amount_color, anchor="w"
#         ).grid(row=0, column=3, padx=12, pady=10, sticky="ew")
        
#         # Action buttons
#         action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
#         action_frame.grid(row=0, column=4, padx=8, pady=10, sticky="ew")
        
#         edit_btn = ctk.CTkButton(
#             action_frame, text="✎", width=32, height=32,
#             font=("Helvetica", 12, "bold"), fg_color="#9333EA", hover_color="#7E22CE",
#             command=lambda cid=cust_id, cn=name, cp=phone, ca=address: self.edit_customer(cid, cn, cp, ca)
#         )
#         edit_btn.pack(side="left", padx=1)
        
#         update_btn = ctk.CTkButton(
#             action_frame, text="💳", width=32, height=32,
#             font=("Helvetica", 12, "bold"), fg_color="#2563EB", hover_color="#1E40AF",
#             command=lambda cid=cust_id, cn=name, cp=phone: self.update_payment(cid, cn, cp)
#         )
#         update_btn.pack(side="left", padx=1)
        
#         del_btn = ctk.CTkButton(
#             action_frame, text="✕", width=32, height=32,
#             font=("Helvetica", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C",
#             command=lambda cid=cust_id: self.delete_cust(cid)
#         )
#         del_btn.pack(side="left", padx=1)
    
#     def _update_pagination(self):
#         """Update pagination controls - optimized"""
#         # Clear previous buttons
#         for widget in self.pagination_btn_frame.winfo_children():
#             widget.destroy()
        
#         # Update label
#         self.pagination_label.configure(
#             text=f"Page {self.current_page} of {self.total_pages}"
#         )
        
#         # Create navigation buttons
#         prev_btn = ctk.CTkButton(
#             self.pagination_btn_frame, text="← Previous", width=110,
#             command=self.prev_page, fg_color="#2563EB", font=("Helvetica", 11, "bold")
#         )
#         prev_btn.pack(side="left", padx=3)
        
#         next_btn = ctk.CTkButton(
#             self.pagination_btn_frame, text="Next →", width=110,
#             command=self.next_page, fg_color="#2563EB", font=("Helvetica", 11, "bold")
#         )
#         next_btn.pack(side="left", padx=3)
    
#     def next_page(self):
#         """Go to next page"""
#         if self.current_page < self.total_pages:
#             self.current_page += 1
#             self.display_page()
    
#     def prev_page(self):
#         """Go to previous page"""
#         if self.current_page > 1:
#             self.current_page -= 1
#             self.display_page()
    
#     def edit_customer(self, customer_id, name, phone, address):
#         """Edit customer details including address"""
#         # Edit name
#         new_name = self.show_input(f"Edit Customer Name (Current: {name}):", "")
#         if new_name is None:
#             return
#         new_name = new_name if new_name else name
        
#         # Edit phone
#         new_phone = self.show_input(f"Edit Phone (Current: {phone}):", "")
#         if new_phone is None:
#             return
#         new_phone = new_phone if new_phone else phone
        
#         # Edit address
#         new_address = self.show_input(f"Edit Address (Current: {address}):", "")
#         if new_address is None:
#             return
#         new_address = new_address if new_address else address
        
#         success, msg = update_customer(customer_id, name=new_name, phone=new_phone, address=new_address)
#         if success:
#             self.show_message(msg, "✓")
#             self.load_customers_async()
#         else:
#             self.show_message(msg, "⚠")
    
#     def update_payment(self, customer_id, name, phone):
#         """Update customer payment"""
#         amount_str = self.show_input(f"Payment Amount (₨) for {name}:", "")
#         if not amount_str:
#             return
        
#         try:
#             amount = float(amount_str)
#             success, msg = update_customer_remaining(name, phone, -amount)
#             if success:
#                 self.show_message(f"Payment recorded: ₨{amount}", "✓")
#                 self.load_customers_async()
#             else:
#                 self.show_message(msg, "⚠")
#         except ValueError:
#             self.show_message("Invalid amount", "⚠")
    
#     def delete_cust(self, customer_id):
#         """Delete a customer"""
#         success, msg = delete_customer(customer_id)
#         if success:
#             self.show_message(msg, "✓")
#             self.load_customers_async()
#         else:
#             self.show_message(msg, "⚠")
    
#     def show_input(self, prompt, title):
#         """Show input dialog"""
#         dialog = ctk.CTkInputDialog(text=prompt, title=title)
#         return dialog.get_input()
    
#     def show_message(self, msg, icon):
#         """Show message dialog"""
#         dialog = ctk.CTkInputDialog(text=f"{msg}", title="Info")
#         dialog.get_input()





"""
Customer Management Page (Performance Optimized with Pagination + Address)
File: customers.py
"""

import customtkinter as ctk
from db import add_customer, get_all_customers, delete_customer, update_customer_remaining, update_customer
import threading

class Page(ctk.CTkFrame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, fg_color="#f8f9fa")
        self.go_back = go_back_callback
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.all_customers = []
        self.filtered_customers = []
        
        # Pagination
        self.page_size = 15
        self.current_page = 1
        self.total_pages = 1
        
        # Performance flags
        self.is_loading = False
        self.filter_timer = None
        
        self.create_widgets()
        self.load_customers_async()
    
    def create_widgets(self):
        """Create UI components"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_columnconfigure(2, weight=1)
        
        back_btn = ctk.CTkButton(
            header, text="← Back", width=80, height=40,
            command=self.go_back, fg_color="#666666", hover_color="#555555",
            font=("Helvetica", 12, "bold")
        )
        back_btn.grid(row=0, column=0, padx=(0, 10))
        
        title = ctk.CTkLabel(
            header, text="👥 Customer Management",
            font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
        )
        title.grid(row=0, column=1, sticky="w")
        
        # Right side buttons
        button_group = ctk.CTkFrame(header, fg_color="transparent")
        button_group.grid(row=0, column=3, sticky="e")
        
        add_btn = ctk.CTkButton(
            button_group, text="+ Add Customer", width=130, height=40,
            command=self.add_new_customer, fg_color="#059669", hover_color="#047857",
            font=("Helvetica", 12, "bold")
        )
        add_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            button_group, text="🔄 Refresh", width=100, height=40,
            command=self.load_customers_async, fg_color="#2563EB", hover_color="#1E40AF",
            font=("Helvetica", 12, "bold")
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Search and Info bar
        search_info_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        search_info_frame.grid_columnconfigure(2, weight=1)
        
        search_label = ctk.CTkLabel(search_info_frame, text="🔍 Search:", font=("Helvetica", 12, "bold"), text_color="#1f1f1f")
        search_label.grid(row=0, column=0, padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(search_info_frame, placeholder_text="Search by name, phone or address...", width=400, height=35, font=("Helvetica", 11))
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Info text - moved to right
        info_label = ctk.CTkLabel(
            search_info_frame, text="ℹ️  Customers are automatically added during billing. You can edit or delete them below.",
            font=("Helvetica", 11), text_color="#2563EB"
        )
        info_label.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
        # Table frame - EXPANDED TO FULL HEIGHT
        table_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Table header - Fixed width columns for proper alignment
        header_frame = ctk.CTkFrame(table_frame, fg_color="#f0f0f0", corner_radius=8)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header_frame.grid_columnconfigure(0, weight=1, minsize=140)
        header_frame.grid_columnconfigure(1, weight=1, minsize=130)
        header_frame.grid_columnconfigure(2, weight=2, minsize=200)
        header_frame.grid_columnconfigure(3, weight=1, minsize=130)
        header_frame.grid_columnconfigure(4, weight=1, minsize=90)
        
        headers = ["Customer Name", "Phone Number", "Address", "Remaining Amount", "Actions"]
        for i, h in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, text=h, font=("Helvetica", 11, "bold"),
                text_color="#1f1f1f", anchor="w"
            )
            label.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
        
        # Scrollable frame - takes full available space
        self.scrollable_frame = ctk.CTkScrollableFrame(
            table_frame, fg_color="transparent"
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame._scrollbar.configure(width=12)
        
        # Pagination frame - at bottom of table
        pagination_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        pagination_container.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 10))
        pagination_container.grid_columnconfigure(0, weight=1)
        
        self.pagination_label = ctk.CTkLabel(
            pagination_container,
            text="Page 1 of 1",
            font=("Helvetica", 11, "bold"), text_color="#1f1f1f"
        )
        self.pagination_label.grid(row=0, column=0, sticky="w", padx=5)
        
        self.pagination_btn_frame = ctk.CTkFrame(pagination_container, fg_color="transparent")
        self.pagination_btn_frame.grid(row=0, column=1, sticky="e")
    
    def load_customers_async(self):
        """Load customers in background thread"""
        if self.is_loading:
            return
        
        self.is_loading = True
        threading.Thread(target=self._load_customers_thread, daemon=True).start()
    
    def _load_customers_thread(self):
        """Background thread for loading customers"""
        try:
            self.all_customers = get_all_customers()
            self.after(0, self._update_ui_after_load)
        except Exception as e:
            print(f"✗ Error loading customers: {e}")
            self.is_loading = False
    
    def _update_ui_after_load(self):
        """Update UI after loading customers"""
        self.schedule_filter()
        self.is_loading = False
    
    def on_search_change(self, event):
        """Handle search input with debouncing"""
        self.schedule_filter()
    
    def schedule_filter(self):
        """Schedule filter with debouncing to avoid excessive updates"""
        if self.filter_timer:
            self.after_cancel(self.filter_timer)
        self.filter_timer = self.after(150, self.filter_customers)
    
    def filter_customers(self):
        """Filter customers based on search - optimized"""
        if self.is_loading:
            return
        
        search_text = self.search_entry.get().lower()
        
        # Optimize filtering with list comprehension - search in name, phone, and address
        filtered = [c for c in self.all_customers 
                   if search_text in c[1].lower() or search_text in c[2].lower() or search_text in c[3].lower()]
        
        self.filtered_customers = filtered
        self.total_pages = max(1, (len(filtered) + self.page_size - 1) // self.page_size)
        self.current_page = 1
        self.display_page()
    
    def display_page(self):
        """Display only the current page - optimized rendering"""
        # Clear previous widgets efficiently
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        page_customers = self.filtered_customers[start_idx:end_idx]
        
        if not page_customers:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No customers found." if self.filtered_customers else "No customers added yet.",
                text_color="#999999", font=("Helvetica", 12, "bold")
            )
            empty_label.pack(pady=30)
        else:
            # Batch create rows
            for customer in page_customers:
                self._create_customer_row(customer)
        
        self._update_pagination()
    
    def _create_customer_row(self, customer):
        """Create a single customer row with proper table alignment"""
        cust_id, name, phone, address, remaining = customer
        
        row_frame = ctk.CTkFrame(
            self.scrollable_frame, fg_color="white", corner_radius=8
        )
        row_frame.pack(fill="x", padx=5, pady=4)
        
        # Fixed width columns matching header exactly
        row_frame.grid_columnconfigure(0, weight=1, minsize=140)
        row_frame.grid_columnconfigure(1, weight=1, minsize=130)
        row_frame.grid_columnconfigure(2, weight=2, minsize=200)
        row_frame.grid_columnconfigure(3, weight=1, minsize=130)
        row_frame.grid_columnconfigure(4, weight=1, minsize=90)
        
        amount_color = "#DC2626" if remaining > 0 else "#059669"
        
        # Truncate address if too long for display
        display_address = address[:40] + "..." if len(address) > 40 else address
        
        # Create labels with consistent spacing and alignment
        ctk.CTkLabel(
            row_frame, text=name, font=("Helvetica", 11, "bold"),
            anchor="w", text_color="#1f1f1f"
        ).grid(row=0, column=0, padx=12, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            row_frame, text=phone, font=("Helvetica", 11, "bold"),
            anchor="w", text_color="#1f1f1f"
        ).grid(row=0, column=1, padx=12, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            row_frame, text=display_address, font=("Helvetica", 11, "bold"),
            anchor="w", text_color="#666666"
        ).grid(row=0, column=2, padx=12, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            row_frame, text=f"₨{remaining:.2f}", font=("Helvetica", 11, "bold"),
            text_color=amount_color, anchor="w"
        ).grid(row=0, column=3, padx=12, pady=10, sticky="ew")
        
        # Action buttons
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.grid(row=0, column=4, padx=8, pady=10, sticky="ew")
        
        edit_btn = ctk.CTkButton(
            action_frame, text="✎", width=32, height=32,
            font=("Helvetica", 12, "bold"), fg_color="#9333EA", hover_color="#7E22CE",
            command=lambda cid=cust_id, cn=name, cp=phone, ca=address: self.edit_customer(cid, cn, cp, ca)
        )
        edit_btn.pack(side="left", padx=1)
        
        update_btn = ctk.CTkButton(
            action_frame, text="💳", width=32, height=32,
            font=("Helvetica", 12, "bold"), fg_color="#2563EB", hover_color="#1E40AF",
            command=lambda cid=cust_id, cn=name, cp=phone: self.update_payment(cid, cn, cp)
        )
        update_btn.pack(side="left", padx=1)
        
        del_btn = ctk.CTkButton(
            action_frame, text="✕", width=32, height=32,
            font=("Helvetica", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C",
            command=lambda cid=cust_id: self.delete_cust(cid)
        )
        del_btn.pack(side="left", padx=1)
    
    def _update_pagination(self):
        """Update pagination controls - optimized"""
        # Clear previous buttons
        for widget in self.pagination_btn_frame.winfo_children():
            widget.destroy()
        
        # Update label
        self.pagination_label.configure(
            text=f"Page {self.current_page} of {self.total_pages}"
        )
        
        # Create navigation buttons
        prev_btn = ctk.CTkButton(
            self.pagination_btn_frame, text="← Previous", width=110,
            command=self.prev_page, fg_color="#2563EB", font=("Helvetica", 11, "bold")
        )
        prev_btn.pack(side="left", padx=3)
        
        next_btn = ctk.CTkButton(
            self.pagination_btn_frame, text="Next →", width=110,
            command=self.next_page, fg_color="#2563EB", font=("Helvetica", 11, "bold")
        )
        next_btn.pack(side="left", padx=3)
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_page()
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_page()
    
    def add_new_customer(self):
        """Add a new customer"""
        # Get customer name
        name = self.show_input("Enter Customer Name:", "")
        if not name or not name.strip():
            self.show_message("Customer name cannot be empty", "⚠")
            return
        
        # Get phone number
        phone = self.show_input(f"Enter Phone Number for {name}:", "")
        if not phone or not phone.strip():
            self.show_message("Phone number cannot be empty", "⚠")
            return
        
        # Get address (optional)
        address = self.show_input(f"Enter Address for {name} (Optional):", "")
        address = address if address else ""
        
        # Add customer to database
        success, msg = add_customer(name.strip(), phone.strip(), address.strip())
        if success:
            self.show_message(f"Customer '{name}' added successfully!", "✓")
            self.load_customers_async()
        else:
            self.show_message(msg, "⚠")
    
    def edit_customer(self, customer_id, name, phone, address):
        """Edit customer details including address"""
        # Edit name
        new_name = self.show_input(f"Edit Customer Name (Current: {name}):", "")
        if new_name is None:
            return
        new_name = new_name if new_name else name
        
        # Edit phone
        new_phone = self.show_input(f"Edit Phone (Current: {phone}):", "")
        if new_phone is None:
            return
        new_phone = new_phone if new_phone else phone
        
        # Edit address
        new_address = self.show_input(f"Edit Address (Current: {address}):", "")
        if new_address is None:
            return
        new_address = new_address if new_address else address
        
        success, msg = update_customer(customer_id, name=new_name, phone=new_phone, address=new_address)
        if success:
            self.show_message(msg, "✓")
            self.load_customers_async()
        else:
            self.show_message(msg, "⚠")
    
    def update_payment(self, customer_id, name, phone):
        """Update customer payment"""
        amount_str = self.show_input(f"Payment Amount (₨) for {name}:", "")
        if not amount_str:
            return
        
        try:
            amount = float(amount_str)
            success, msg = update_customer_remaining(name, phone, -amount)
            if success:
                self.show_message(f"Payment recorded: ₨{amount}", "✓")
                self.load_customers_async()
            else:
                self.show_message(msg, "⚠")
        except ValueError:
            self.show_message("Invalid amount", "⚠")
    
    def delete_cust(self, customer_id):
        """Delete a customer"""
        success, msg = delete_customer(customer_id)
        if success:
            self.show_message(msg, "✓")
            self.load_customers_async()
        else:
            self.show_message(msg, "⚠")
    
    def show_input(self, prompt, title):
        """Show input dialog"""
        dialog = ctk.CTkInputDialog(text=prompt, title=title)
        return dialog.get_input()
    
    def show_message(self, msg, icon):
        """Show message dialog"""
        dialog = ctk.CTkInputDialog(text=f"{msg}", title="Info")
        dialog.get_input()