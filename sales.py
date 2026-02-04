# """
# Sales History Page with Calendar Date Picker
# File: sales.py
# """

# import customtkinter as ctk
# from db import get_all_sales, get_total_profit_loss
# from datetime import datetime
# import tkinter.ttk as ttk
# from tkcalendar import Calendar

# class Page(ctk.CTkFrame):
#     def __init__(self, parent, go_back_callback):
#         super().__init__(parent, fg_color="#f8f9fa")
#         self.go_back = go_back_callback

#         self.grid_rowconfigure(3, weight=1)
#         self.grid_columnconfigure(0, weight=1)

#         self.all_sales = []
#         self.filtered_sales = []
#         self.start_date = None
#         self.end_date = None

#         # Pagination
#         self.page_size = 25
#         self.current_page = 1
#         self.total_pages = 1

#         self.create_widgets()
#         self.load_sales()
    
#     def create_widgets(self):
#         """Create UI components"""
#         # Header
#         header = ctk.CTkFrame(self, fg_color="transparent")
#         header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
#         header.grid_columnconfigure(1, weight=1)
        
#         back_btn = ctk.CTkButton(
#             header, text="← Back", width=80, height=40,
#             command=self.go_back, fg_color="#666666", hover_color="#555555",
#             font=("Helvetica", 12, "bold")
#         )
#         back_btn.grid(row=0, column=0, padx=(0, 10))
        
#         title = ctk.CTkLabel(
#             header, text="💰 Sales History",
#             font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
#         )
#         title.grid(row=0, column=1, sticky="w")
        
#         refresh_btn = ctk.CTkButton(
#             header, text="🔄 Refresh", width=100, height=40,
#             command=self.load_sales, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 12, "bold")
#         )
#         refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
#         # Summary stats
#         stats_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        
#         total_profit = get_total_profit_loss()
#         profit_color = "#059669" if total_profit >= 0 else "#DC2626"
#         profit_icon = "📈" if total_profit >= 0 else "📉"
        
#         stat_label = ctk.CTkLabel(
#             stats_frame, text=f"{profit_icon} Total Profit/Loss: ₨{total_profit:.2f}",
#             font=("Helvetica", 15, "bold"), text_color=profit_color
#         )
#         stat_label.pack(padx=20, pady=15)
        
#         # ============= SEARCH & FILTER SECTION =============
#         filter_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         filter_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        
#         # Title for filter section
#         filter_title = ctk.CTkLabel(
#             filter_frame, text="🔍 Search & Filter",
#             font=("Helvetica", 13, "bold"), text_color="#1f1f1f"
#         )
#         filter_title.pack(anchor="w", padx=15, pady=(12, 10))
        
#         # Search by product/customer
#         search_label = ctk.CTkLabel(filter_frame, text="Product or Customer Name:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
#         search_label.pack(anchor="w", padx=15, pady=(5, 0))
        
#         self.search_entry = ctk.CTkEntry(
#             filter_frame, placeholder_text="Type product name or customer name...", 
#             width=400, height=35, font=("Helvetica", 11)
#         )
#         self.search_entry.pack(padx=15, pady=(0, 15), fill="x")
#         self.search_entry.bind("<KeyRelease>", lambda e: self.filter_sales())
        
#         # Date range section
#         date_label = ctk.CTkLabel(filter_frame, text="📅 Filter by Date Range:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
#         date_label.pack(anchor="w", padx=15, pady=(5, 10))
        
#         # Date picker buttons and display frame
#         date_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
#         date_frame.pack(padx=15, pady=(0, 15), fill="x")
        
#         # Start date section
#         start_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
#         start_frame.pack(side="left", padx=(0, 20))
        
#         start_label = ctk.CTkLabel(start_frame, text="From:", font=("Helvetica", 10, "bold"), text_color="#1f1f1f")
#         start_label.pack(anchor="w")
        
#         self.start_date_display = ctk.CTkLabel(
#             start_frame, text="Select Date", 
#             font=("Helvetica", 10), text_color="#2563EB"
#         )
#         self.start_date_display.pack(anchor="w", pady=(3, 8))
        
#         start_btn = ctk.CTkButton(
#             start_frame, text="📅 Pick Start Date", width=140, height=35,
#             command=self.pick_start_date, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 10, "bold")
#         )
#         start_btn.pack()
        
#         # End date section
#         end_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
#         end_frame.pack(side="left", padx=(0, 20))
        
#         end_label = ctk.CTkLabel(end_frame, text="To:", font=("Helvetica", 10, "bold"), text_color="#1f1f1f")
#         end_label.pack(anchor="w")
        
#         self.end_date_display = ctk.CTkLabel(
#             end_frame, text="Select Date", 
#             font=("Helvetica", 10), text_color="#2563EB"
#         )
#         self.end_date_display.pack(anchor="w", pady=(3, 8))
        
#         end_btn = ctk.CTkButton(
#             end_frame, text="📅 Pick End Date", width=140, height=35,
#             command=self.pick_end_date, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 10, "bold")
#         )
#         end_btn.pack()
        
#         # Clear filters button
#         clear_btn = ctk.CTkButton(
#             date_frame, text="🔄 Clear All Filters", width=140, height=35,
#             command=self.clear_filters, fg_color="#666666", hover_color="#555555",
#             font=("Helvetica", 10, "bold")
#         )
#         clear_btn.pack(side="left")
        
#         # ============= TABLE SECTION =============
#         # Table frame
#         table_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
#         table_frame.grid_rowconfigure(1, weight=1)
#         table_frame.grid_columnconfigure(0, weight=1)
        
#         # Table header
#         header_frame = ctk.CTkFrame(table_frame, fg_color="#f0f0f0", corner_radius=8)
#         header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
#         header_frame.grid_columnconfigure(0, weight=2)
#         header_frame.grid_columnconfigure(1, weight=2)
#         header_frame.grid_columnconfigure(2, weight=1)
#         header_frame.grid_columnconfigure(3, weight=2)
#         header_frame.grid_columnconfigure(4, weight=2)
#         header_frame.grid_columnconfigure(5, weight=2)
        
#         headers = ["Product", "Customer", "Qty", "Selling Price", "Profit/Loss", "Date"]
#         for i, h in enumerate(headers):
#             label = ctk.CTkLabel(
#                 header_frame, text=h, font=("Helvetica", 12, "bold"),
#                 text_color="#1f1f1f", anchor="w"
#             )
#             label.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
        
#         # Scrollable frame
#         self.scrollable_frame = ctk.CTkScrollableFrame(
#             table_frame, fg_color="transparent"
#         )
#         self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
#         self.grid_rowconfigure(2, weight=0)
#         self.grid_rowconfigure(3, weight=1)
    
#     def pick_start_date(self):
#         """Open calendar for start date selection"""
#         self.open_calendar("start")
    
#     def pick_end_date(self):
#         """Open calendar for end date selection"""
#         self.open_calendar("end")
    
#     def open_calendar(self, date_type):
#         """Open calendar dialog"""
#         # Create top-level window for calendar
#         cal_window = ctk.CTkToplevel(self)
#         cal_window.title("📅 Select Date")
#         cal_window.geometry("400x450")
#         cal_window.resizable(False, False)
        
#         # Make window stay on top
#         cal_window.attributes('-topmost', True)
#         cal_window.lift()
#         cal_window.focus()
        
#         # Center window on screen
#         cal_window.update_idletasks()
        
#         # Create frame for calendar
#         cal_frame = ctk.CTkFrame(cal_window, fg_color="white", corner_radius=10)
#         cal_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
#         # Title label
#         title = ctk.CTkLabel(
#             cal_frame, 
#             text=f"Select {'Start' if date_type == 'start' else 'End'} Date",
#             font=("Helvetica", 13, "bold"), text_color="#1f1f1f"
#         )
#         title.pack(pady=(10, 5))
        
#         # Create embedded calendar using tkcalendar
#         try:
#             # Get current date or previously selected date
#             if date_type == "start" and self.start_date:
#                 current_date = self.start_date
#             elif date_type == "end" and self.end_date:
#                 current_date = self.end_date
#             else:
#                 current_date = datetime.now()
            
#             # Create calendar
#             cal = Calendar(
#                 cal_frame,
#                 font=("Helvetica", 10),
#                 selectmode='day',
#                 cursor="hand2",
#                 year=current_date.year,
#                 month=current_date.month,
#                 day=current_date.day,
#                 background="#2563EB",
#                 foreground="white",
#                 normalforeground="#1f1f1f",
#                 weekendforeground="#DC2626",
#                 headersforeground="#ffffff",
#                 headersbackground="#1E40AF",
#                 selectforeground="#ffffff",
#                 selectbackground="#059669"
#             )
#             cal.pack(fill="both", expand=True, padx=10, pady=10)
            
#             # Buttons frame
#             button_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
#             button_frame.pack(fill="x", padx=10, pady=(10, 10))
            
#             # Select button
#             def select_date():
#                 selected_date = cal.selection_get()
#                 if selected_date:
#                     if date_type == "start":
#                         self.start_date = selected_date
#                         self.start_date_display.configure(text=selected_date.strftime("%d-%m-%Y"))
#                     else:
#                         self.end_date = selected_date
#                         self.end_date_display.configure(text=selected_date.strftime("%d-%m-%Y"))
                    
#                     self.filter_sales()
#                     cal_window.destroy()
            
#             select_btn = ctk.CTkButton(
#                 button_frame, text="✓ Select Date", height=35,
#                 command=select_date, fg_color="#059669", hover_color="#047857",
#                 font=("Helvetica", 11, "bold")
#             )
#             select_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
#             # Cancel button
#             cancel_btn = ctk.CTkButton(
#                 button_frame, text="✕ Cancel", height=35,
#                 command=cal_window.destroy, fg_color="#DC2626", hover_color="#B91C1C",
#                 font=("Helvetica", 11, "bold")
#             )
#             cancel_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
#         except Exception as e:
#             error_label = ctk.CTkLabel(
#                 cal_frame,
#                 text=f"Calendar Error:\n{str(e)}\n\nPlease use manual date entry\nFormat: DD-MM-YYYY",
#                 font=("Helvetica", 10), text_color="#DC2626"
#             )
#             error_label.pack(pady=20)



#     def load_sales(self):
#         """Load and display sales"""
#         self.all_sales = get_all_sales()
#         self.filter_sales()

#     def filter_sales(self):
#         """Filter sales based on search and date range"""
#         search_text = self.search_entry.get().lower()

#         filtered = self.all_sales

#         # Filter by search text
#         if search_text:
#             filtered = [s for s in filtered if search_text in (s[0].lower() or "") or search_text in (s[5].lower() or "")]

#         # Filter by date range
#         try:
#             if self.start_date or self.end_date:
#                 filtered_by_date = []
#                 for sale in filtered:
#                     sale_date_str = sale[6]  # date is at index 6
#                     if sale_date_str:
#                         sale_date = datetime.strptime(sale_date_str, "%Y-%m-%d %H:%M:%S").date()
#                         include = True
#                         if self.start_date and sale_date < self.start_date:
#                             include = False
#                         if self.end_date and sale_date > self.end_date:
#                             include = False
#                         if include:
#                             filtered_by_date.append(sale)
#                 filtered = filtered_by_date
#         except Exception as e:
#             print(f"Date filtering error: {e}")

#         self.filtered_sales = filtered
#         self.total_pages = max(1, (len(filtered) + self.page_size - 1) // self.page_size)
#         self.current_page = 1
#         self.display_page()

#     def display_page(self):
#         """Render only the current page of sales"""
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()

#         start_idx = (self.current_page - 1) * self.page_size
#         end_idx = start_idx + self.page_size
#         page_sales = self.filtered_sales[start_idx:end_idx]

#         if not page_sales:
#             empty_label = ctk.CTkLabel(
#                 self.scrollable_frame,
#                 text="No sales found." if self.filtered_sales else "No sales recorded yet.",
#                 text_color="#999999", font=("Helvetica", 12, "bold")
#             )
#             empty_label.pack(pady=30)
#             return

#         for sale in page_sales:
#             product_name, qty, pp, sp, profit_loss, customer, date = sale

#             row_frame = ctk.CTkFrame(
#                 self.scrollable_frame, fg_color="white", corner_radius=8
#             )
#             row_frame.pack(fill="x", padx=5, pady=4)
#             row_frame.grid_columnconfigure(0, weight=2)
#             row_frame.grid_columnconfigure(1, weight=2)
#             row_frame.grid_columnconfigure(2, weight=1)
#             row_frame.grid_columnconfigure(3, weight=2)
#             row_frame.grid_columnconfigure(4, weight=2)
#             row_frame.grid_columnconfigure(5, weight=2)

#             profit_color = "#059669" if profit_loss >= 0 else "#DC2626"
#             date_str = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d %b %y") if date else "N/A"
#             customer_name = customer if customer else "Walk-in"

#             ctk.CTkLabel(row_frame, text=product_name, font=("Helvetica", 11, "bold"), anchor="w", text_color="#1f1f1f").grid(row=0, column=0, padx=12, pady=10, sticky="ew")
#             ctk.CTkLabel(row_frame, text=customer_name, font=("Helvetica", 11, "bold"), anchor="w", text_color="#1f1f1f").grid(row=0, column=1, padx=12, pady=10, sticky="ew")
#             ctk.CTkLabel(row_frame, text=str(qty), font=("Helvetica", 11, "bold"), anchor="w", text_color="#1f1f1f").grid(row=0, column=2, padx=12, pady=10, sticky="ew")
#             ctk.CTkLabel(row_frame, text=f"₨{sp:.2f}", font=("Helvetica", 11, "bold"), anchor="w", text_color="#1f1f1f").grid(row=0, column=3, padx=12, pady=10, sticky="ew")
#             ctk.CTkLabel(row_frame, text=f"₨{profit_loss:.2f}", font=("Helvetica", 11, "bold"), text_color=profit_color, anchor="w").grid(row=0, column=4, padx=12, pady=10, sticky="ew")
#             ctk.CTkLabel(row_frame, text=date_str, font=("Helvetica", 11, "bold"), anchor="w", text_color="#1f1f1f").grid(row=0, column=5, padx=12, pady=10, sticky="ew")

#         # Pagination controls
#         if hasattr(self, 'pagination_frame'):
#             self.pagination_frame.destroy()

#         self.pagination_frame = ctk.CTkFrame(self, fg_color="transparent")
#         self.pagination_frame.grid(row=4, column=0, pady=(0, 20))

#         prev_btn = ctk.CTkButton(self.pagination_frame, text="← Previous", width=120, command=self.prev_page, fg_color="#2563EB")
#         prev_btn.pack(side="left", padx=5)
#         page_label = ctk.CTkLabel(self.pagination_frame, text=f"Page {self.current_page} of {self.total_pages}", font=("Helvetica", 12, "bold"))
#         page_label.pack(side="left", padx=10)
#         next_btn = ctk.CTkButton(self.pagination_frame, text="Next →", width=120, command=self.next_page, fg_color="#2563EB")
#         next_btn.pack(side="left", padx=5)

#     def next_page(self):
#         if self.current_page < self.total_pages:
#             self.current_page += 1
#             self.display_page()

#     def prev_page(self):
#         if self.current_page > 1:
#             self.current_page -= 1
#             self.display_page()
    
#     def clear_filters(self):
#         """Clear all filters"""
#         self.search_entry.delete(0, "end")
#         self.start_date = None
#         self.end_date = None
#         self.start_date_display.configure(text="Select Date")
#         self.end_date_display.configure(text="Select Date")
#         self.filter_sales()






# """
# Sales History Page with Calendar Date Picker - Optimized Layout
# File: sales.py
# """

# import customtkinter as ctk
# from db import get_all_sales, get_total_profit_loss
# from datetime import datetime
# import tkinter.ttk as ttk
# from tkcalendar import Calendar

# class Page(ctk.CTkFrame):
#     def __init__(self, parent, go_back_callback):
#         super().__init__(parent, fg_color="#f8f9fa")
#         self.go_back = go_back_callback

#         self.grid_rowconfigure(3, weight=1)
#         self.grid_columnconfigure(0, weight=1)

#         self.all_sales = []
#         self.filtered_sales = []
#         self.start_date = None
#         self.end_date = None

#         # Pagination
#         self.page_size = 20
#         self.current_page = 1
#         self.total_pages = 1

#         self.create_widgets()
#         self.load_sales()
    
#     def create_widgets(self):
#         """Create UI components"""
#         # Header
#         header = ctk.CTkFrame(self, fg_color="transparent")
#         header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
#         header.grid_columnconfigure(1, weight=1)
        
#         back_btn = ctk.CTkButton(
#             header, text="← Back", width=80, height=40,
#             command=self.go_back, fg_color="#666666", hover_color="#555555",
#             font=("Helvetica", 12, "bold")
#         )
#         back_btn.grid(row=0, column=0, padx=(0, 10))
        
#         title = ctk.CTkLabel(
#             header, text="💰 Sales History",
#             font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
#         )
#         title.grid(row=0, column=1, sticky="w")
        
#         refresh_btn = ctk.CTkButton(
#             header, text="🔄 Refresh", width=100, height=40,
#             command=self.load_sales, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 12, "bold")
#         )
#         refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
#         # Summary stats
#         stats_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        
#         total_profit = get_total_profit_loss()
#         profit_color = "#059669" if total_profit >= 0 else "#DC2626"
#         profit_icon = "📈" if total_profit >= 0 else "📉"
        
#         stat_label = ctk.CTkLabel(
#             stats_frame, text=f"{profit_icon} Total Profit/Loss: ₨{total_profit:.2f}",
#             font=("Helvetica", 15, "bold"), text_color=profit_color
#         )
#         stat_label.pack(padx=20, pady=15)
        
#         # ============= SEARCH & FILTER SECTION - COMPACT ROW =============
#         filter_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         filter_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        
#         # Search section (left side)
#         search_container = ctk.CTkFrame(filter_frame, fg_color="transparent")
#         search_container.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
#         search_label = ctk.CTkLabel(
#             search_container, text="🔍 Search:", 
#             font=("Helvetica", 11, "bold"), text_color="#1f1f1f"
#         )
#         search_label.pack(anchor="w", pady=(0, 5))
        
#         self.search_entry = ctk.CTkEntry(
#             search_container, placeholder_text="Product or customer name...", 
#             height=35, font=("Helvetica", 11)
#         )
#         self.search_entry.pack(fill="x", pady=(0, 10))
#         self.search_entry.bind("<KeyRelease>", lambda e: self.filter_sales())
        
#         # Date range section (right side)
#         date_container = ctk.CTkFrame(filter_frame, fg_color="transparent")
#         date_container.pack(side="right", padx=15, pady=12)
        
#         date_label = ctk.CTkLabel(
#             date_container, text="📅 Filter by Date:", 
#             font=("Helvetica", 11, "bold"), text_color="#1f1f1f"
#         )
#         date_label.pack(anchor="w", pady=(0, 5))
        
#         # Date buttons row
#         date_buttons_frame = ctk.CTkFrame(date_container, fg_color="transparent")
#         date_buttons_frame.pack(fill="x")
        
#         start_btn = ctk.CTkButton(
#             date_buttons_frame, text="From:", width=70, height=32,
#             command=self.pick_start_date, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 10, "bold")
#         )
#         start_btn.pack(side="left", padx=2)
        
#         self.start_date_display = ctk.CTkLabel(
#             date_buttons_frame, text="Select", 
#             font=("Helvetica", 10), text_color="#1f1f1f",
#             width=80
#         )
#         self.start_date_display.pack(side="left", padx=2)
        
#         end_btn = ctk.CTkButton(
#             date_buttons_frame, text="To:", width=70, height=32,
#             command=self.pick_end_date, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 10, "bold")
#         )
#         end_btn.pack(side="left", padx=2)
        
#         self.end_date_display = ctk.CTkLabel(
#             date_buttons_frame, text="Select", 
#             font=("Helvetica", 10), text_color="#1f1f1f",
#             width=80
#         )
#         self.end_date_display.pack(side="left", padx=2)
        
#         clear_btn = ctk.CTkButton(
#             date_buttons_frame, text="🔄", width=32, height=32,
#             command=self.clear_filters, fg_color="#666666", hover_color="#555555",
#             font=("Helvetica", 10, "bold")
#         )
#         clear_btn.pack(side="left", padx=2)
        
#         # ============= TABLE SECTION - FULL HEIGHT =============
#         # Table frame
#         table_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
#         table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
#         table_frame.grid_rowconfigure(1, weight=1)
#         table_frame.grid_columnconfigure(0, weight=1)
        
#         # Table header - Fixed width columns
#         header_frame = ctk.CTkFrame(table_frame, fg_color="#f0f0f0", corner_radius=8)
#         header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
#         header_frame.grid_columnconfigure(0, weight=1, minsize=120)
#         header_frame.grid_columnconfigure(1, weight=1, minsize=120)
#         header_frame.grid_columnconfigure(2, weight=1, minsize=110)
#         header_frame.grid_columnconfigure(3, weight=1, minsize=110)
#         header_frame.grid_columnconfigure(4, weight=1, minsize=100)
#         header_frame.grid_columnconfigure(5, weight=1, minsize=100)
#         header_frame.grid_columnconfigure(6, weight=1, minsize=130)
        
#         headers = ["Product", "Customer", "Phone", "Qty", "Unit Price", "Profit/Loss", "Date"]
#         for i, h in enumerate(headers):
#             label = ctk.CTkLabel(
#                 header_frame, text=h, font=("Helvetica", 11, "bold"),
#                 text_color="#1f1f1f", anchor="w"
#             )
#             label.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
        
#         # Scrollable frame
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
    
#     def pick_start_date(self):
#         """Open calendar for start date selection"""
#         self.open_calendar("start")
    
#     def pick_end_date(self):
#         """Open calendar for end date selection"""
#         self.open_calendar("end")
    
#     def open_calendar(self, date_type):
#         """Open calendar dialog"""
#         # Create top-level window for calendar
#         cal_window = ctk.CTkToplevel(self)
#         cal_window.title("📅 Select Date")
#         cal_window.geometry("400x450")
#         cal_window.resizable(False, False)
        
#         # Make window stay on top
#         cal_window.attributes('-topmost', True)
#         cal_window.lift()
#         cal_window.focus()
        
#         # Center window on screen
#         cal_window.update_idletasks()
        
#         # Create frame for calendar
#         cal_frame = ctk.CTkFrame(cal_window, fg_color="white", corner_radius=10)
#         cal_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
#         # Title label
#         title = ctk.CTkLabel(
#             cal_frame, 
#             text=f"Select {'Start' if date_type == 'start' else 'End'} Date",
#             font=("Helvetica", 13, "bold"), text_color="#1f1f1f"
#         )
#         title.pack(pady=(10, 5))
        
#         # Create embedded calendar using tkcalendar
#         try:
#             # Get current date or previously selected date
#             if date_type == "start" and self.start_date:
#                 current_date = self.start_date
#             elif date_type == "end" and self.end_date:
#                 current_date = self.end_date
#             else:
#                 current_date = datetime.now()
            
#             # Create calendar
#             cal = Calendar(
#                 cal_frame,
#                 font=("Helvetica", 10),
#                 selectmode='day',
#                 cursor="hand2",
#                 year=current_date.year,
#                 month=current_date.month,
#                 day=current_date.day,
#                 background="#2563EB",
#                 foreground="white",
#                 normalforeground="#1f1f1f",
#                 weekendforeground="#DC2626",
#                 headersforeground="#ffffff",
#                 headersbackground="#1E40AF",
#                 selectforeground="#ffffff",
#                 selectbackground="#059669"
#             )
#             cal.pack(fill="both", expand=True, padx=10, pady=10)
            
#             # Buttons frame
#             button_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
#             button_frame.pack(fill="x", padx=10, pady=(10, 10))
            
#             # Select button
#             def select_date():
#                 selected_date = cal.selection_get()
#                 if selected_date:
#                     if date_type == "start":
#                         self.start_date = selected_date
#                         self.start_date_display.configure(text=selected_date.strftime("%d-%m-%Y"))
#                     else:
#                         self.end_date = selected_date
#                         self.end_date_display.configure(text=selected_date.strftime("%d-%m-%Y"))
                    
#                     self.filter_sales()
#                     cal_window.destroy()
            
#             select_btn = ctk.CTkButton(
#                 button_frame, text="✓ Select Date", height=35,
#                 command=select_date, fg_color="#059669", hover_color="#047857",
#                 font=("Helvetica", 11, "bold")
#             )
#             select_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
#             # Cancel button
#             cancel_btn = ctk.CTkButton(
#                 button_frame, text="✕ Cancel", height=35,
#                 command=cal_window.destroy, fg_color="#DC2626", hover_color="#B91C1C",
#                 font=("Helvetica", 11, "bold")
#             )
#             cancel_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
#         except Exception as e:
#             error_label = ctk.CTkLabel(
#                 cal_frame,
#                 text=f"Calendar Error:\n{str(e)}\n\nPlease use manual date entry\nFormat: DD-MM-YYYY",
#                 font=("Helvetica", 10), text_color="#DC2626"
#             )
#             error_label.pack(pady=20)

#     def load_sales(self):
#         """Load and display sales"""
#         self.all_sales = get_all_sales()
#         self.filter_sales()

#     def filter_sales(self):
#         """Filter sales based on search and date range"""
#         search_text = self.search_entry.get().lower()

#         filtered = self.all_sales

#         # Filter by search text
#         if search_text:
#             filtered = [s for s in filtered if search_text in (s[0].lower() or "") or search_text in (s[5].lower() or "")]

#         # Filter by date range
#         try:
#             if self.start_date or self.end_date:
#                 filtered_by_date = []
#                 for sale in filtered:
#                     sale_date_str = sale[6]  # date is at index 6
#                     if sale_date_str:
#                         sale_date = datetime.strptime(sale_date_str, "%Y-%m-%d %H:%M:%S").date()
#                         include = True
#                         if self.start_date and sale_date < self.start_date:
#                             include = False
#                         if self.end_date and sale_date > self.end_date:
#                             include = False
#                         if include:
#                             filtered_by_date.append(sale)
#                 filtered = filtered_by_date
#         except Exception as e:
#             print(f"Date filtering error: {e}")

#         self.filtered_sales = filtered
#         self.total_pages = max(1, (len(filtered) + self.page_size - 1) // self.page_size)
#         self.current_page = 1
#         self.display_page()

#     def display_page(self):
#         """Render only the current page of sales"""
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()

#         start_idx = (self.current_page - 1) * self.page_size
#         end_idx = start_idx + self.page_size
#         page_sales = self.filtered_sales[start_idx:end_idx]

#         if not page_sales:
#             empty_label = ctk.CTkLabel(
#                 self.scrollable_frame,
#                 text="No sales found." if self.filtered_sales else "No sales recorded yet.",
#                 text_color="#999999", font=("Helvetica", 12, "bold")
#             )
#             empty_label.pack(pady=30)
#             self._update_pagination()
#             return

#         for sale in page_sales:
#             product_name, qty, pp, sp, profit_loss, customer, phone, date = sale

#             row_frame = ctk.CTkFrame(
#                 self.scrollable_frame, fg_color="white", corner_radius=8
#             )
#             row_frame.pack(fill="x", padx=5, pady=4)
            
#             # Fixed width columns matching header exactly
#             row_frame.grid_columnconfigure(0, weight=1, minsize=120)
#             row_frame.grid_columnconfigure(1, weight=1, minsize=120)
#             row_frame.grid_columnconfigure(2, weight=1, minsize=110)
#             row_frame.grid_columnconfigure(3, weight=1, minsize=110)
#             row_frame.grid_columnconfigure(4, weight=1, minsize=100)
#             row_frame.grid_columnconfigure(5, weight=1, minsize=130)
#             row_frame.grid_columnconfigure(6, weight=1, minsize=130)

#             profit_color = "#059669" if profit_loss >= 0 else "#DC2626"
#             date_str = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d %b %y") if date else "N/A"
#             customer_name = customer if customer else "Walk-in"
#             customer_phone = phone if phone else "N/A"

#             # Create labels with consistent spacing and alignment
#             ctk.CTkLabel(
#                 row_frame, text=product_name, font=("Helvetica", 11, "bold"),
#                 anchor="w", text_color="#1f1f1f"
#             ).grid(row=0, column=0, padx=12, pady=10, sticky="ew")
            
#             ctk.CTkLabel(
#                 row_frame, text=customer_name, font=("Helvetica", 11, "bold"),
#                 anchor="w", text_color="#1f1f1f"
#             ).grid(row=0, column=1, padx=12, pady=10, sticky="ew")
            
#             ctk.CTkLabel(
#                 row_frame, text=customer_phone, font=("Helvetica", 11, "bold"),
#                 anchor="w", text_color="#666666"
#             ).grid(row=0, column=2, padx=12, pady=10, sticky="ew")
            
#             ctk.CTkLabel(
#                 row_frame, text=str(qty), font=("Helvetica", 11, "bold"),
#                 anchor="w", text_color="#1f1f1f"
#             ).grid(row=0, column=3, padx=12, pady=10, sticky="ew")
            
#             ctk.CTkLabel(
#                 row_frame, text=f"₨{sp:.2f}", font=("Helvetica", 11, "bold"),
#                 anchor="w", text_color="#1f1f1f"
#             ).grid(row=0, column=4, padx=12, pady=10, sticky="ew")
            
#             ctk.CTkLabel(
#                 row_frame, text=f"₨{profit_loss:.2f}", font=("Helvetica", 11, "bold"),
#                 text_color=profit_color, anchor="w"
#             ).grid(row=0, column=5, padx=12, pady=10, sticky="ew")
            
#             ctk.CTkLabel(
#                 row_frame, text=date_str, font=("Helvetica", 11, "bold"),
#                 anchor="w", text_color="#1f1f1f"
#             ).grid(row=0, column=6, padx=12, pady=10, sticky="ew")

#         self._update_pagination()

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
#         if self.current_page < self.total_pages:
#             self.current_page += 1
#             self.display_page()

#     def prev_page(self):
#         if self.current_page > 1:
#             self.current_page -= 1
#             self.display_page()
    
#     def clear_filters(self):
#         """Clear all filters"""
#         self.search_entry.delete(0, "end")
#         self.start_date = None
#         self.end_date = None
#         self.start_date_display.configure(text="Select")
#         self.end_date_display.configure(text="Select")
#         self.filter_sales()



"""
Sales History Page with Calendar Date Picker - Optimized Layout
File: sales.py - FIXED VERSION
"""

import customtkinter as ctk
from db import get_all_sales, get_total_profit_loss
from datetime import datetime
import tkinter.ttk as ttk
from tkcalendar import Calendar

class Page(ctk.CTkFrame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, fg_color="#f8f9fa")
        self.go_back = go_back_callback

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.all_sales = []
        self.filtered_sales = []
        self.start_date = None
        self.end_date = None

        # Pagination
        self.page_size = 20
        self.current_page = 1
        self.total_pages = 1

        self.create_widgets()
        self.load_sales()
    
    def create_widgets(self):
        """Create UI components"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_columnconfigure(1, weight=1)
        
        back_btn = ctk.CTkButton(
            header, text="← Back", width=80, height=40,
            command=self.go_back, fg_color="#666666", hover_color="#555555",
            font=("Helvetica", 12, "bold")
        )
        back_btn.grid(row=0, column=0, padx=(0, 10))
        
        title = ctk.CTkLabel(
            header, text="💰 Sales History",
            font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
        )
        title.grid(row=0, column=1, sticky="w")
        
        refresh_btn = ctk.CTkButton(
            header, text="🔄 Refresh", width=100, height=40,
            command=self.load_sales, fg_color="#2563EB", hover_color="#1E40AF",
            font=("Helvetica", 12, "bold")
        )
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Summary stats
        stats_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        total_profit = get_total_profit_loss()
        profit_color = "#059669" if total_profit >= 0 else "#DC2626"
        profit_icon = "📈" if total_profit >= 0 else "📉"
        
        stat_label = ctk.CTkLabel(
            stats_frame, text=f"{profit_icon} Total Profit/Loss: ₨{total_profit:.2f}",
            font=("Helvetica", 15, "bold"), text_color=profit_color
        )
        stat_label.pack(padx=20, pady=15)
        
        # ============= SEARCH & FILTER SECTION - COMPACT ROW =============
        filter_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        filter_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # Search section (left side)
        search_container = ctk.CTkFrame(filter_frame, fg_color="transparent")
        search_container.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
        search_label = ctk.CTkLabel(
            search_container, text="🔍 Search:", 
            font=("Helvetica", 11, "bold"), text_color="#1f1f1f"
        )
        search_label.pack(anchor="w", pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_container, placeholder_text="Product or customer name...", 
            height=35, font=("Helvetica", 11)
        )
        self.search_entry.pack(fill="x", pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_sales())
        
        # Date range section (right side)
        date_container = ctk.CTkFrame(filter_frame, fg_color="transparent")
        date_container.pack(side="right", padx=15, pady=12)
        
        date_label = ctk.CTkLabel(
            date_container, text="📅 Filter by Date:", 
            font=("Helvetica", 11, "bold"), text_color="#1f1f1f"
        )
        date_label.pack(anchor="w", pady=(0, 5))
        
        # Date buttons row
        date_buttons_frame = ctk.CTkFrame(date_container, fg_color="transparent")
        date_buttons_frame.pack(fill="x")
        
        start_btn = ctk.CTkButton(
            date_buttons_frame, text="From:", width=70, height=32,
            command=self.pick_start_date, fg_color="#2563EB", hover_color="#1E40AF",
            font=("Helvetica", 10, "bold")
        )
        start_btn.pack(side="left", padx=2)
        
        self.start_date_display = ctk.CTkLabel(
            date_buttons_frame, text="Select", 
            font=("Helvetica", 10), text_color="#1f1f1f",
            width=80
        )
        self.start_date_display.pack(side="left", padx=2)
        
        end_btn = ctk.CTkButton(
            date_buttons_frame, text="To:", width=70, height=32,
            command=self.pick_end_date, fg_color="#2563EB", hover_color="#1E40AF",
            font=("Helvetica", 10, "bold")
        )
        end_btn.pack(side="left", padx=2)
        
        self.end_date_display = ctk.CTkLabel(
            date_buttons_frame, text="Select", 
            font=("Helvetica", 10), text_color="#1f1f1f",
            width=80
        )
        self.end_date_display.pack(side="left", padx=2)
        
        clear_btn = ctk.CTkButton(
            date_buttons_frame, text="🔄", width=32, height=32,
            command=self.clear_filters, fg_color="#666666", hover_color="#555555",
            font=("Helvetica", 10, "bold")
        )
        clear_btn.pack(side="left", padx=2)
        
        # ============= TABLE SECTION - FULL HEIGHT =============
        # Table frame
        table_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Table header - Fixed width columns
        header_frame = ctk.CTkFrame(table_frame, fg_color="#f0f0f0", corner_radius=8)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header_frame.grid_columnconfigure(0, weight=1, minsize=120)
        header_frame.grid_columnconfigure(1, weight=1, minsize=120)
        header_frame.grid_columnconfigure(2, weight=1, minsize=110)
        header_frame.grid_columnconfigure(3, weight=1, minsize=110)
        header_frame.grid_columnconfigure(4, weight=1, minsize=100)
        header_frame.grid_columnconfigure(5, weight=1, minsize=100)
        header_frame.grid_columnconfigure(6, weight=1, minsize=130)
        
        headers = ["Product", "Customer", "Phone", "Qty", "Unit Price", "Profit/Loss", "Date"]
        for i, h in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, text=h, font=("Helvetica", 11, "bold"),
                text_color="#1f1f1f", anchor="w"
            )
            label.grid(row=0, column=i, padx=12, pady=10, sticky="ew")
        
        # Scrollable frame
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
    
    def parse_sale_date(self, date_str):
        """Parse sale date from various formats"""
        if not date_str:
            return None
        
        date_str = str(date_str).strip()
        
        # Try standard datetime format first
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # If it's a number (Unix timestamp), convert it
        try:
            timestamp = float(date_str)
            return datetime.fromtimestamp(timestamp).date()
        except (ValueError, OSError):
            pass
        
        # Last resort - return None if can't parse
        print(f"⚠️  Could not parse date: {date_str}")
        return None
    
    def pick_start_date(self):
        """Open calendar for start date selection"""
        self.open_calendar("start")
    
    def pick_end_date(self):
        """Open calendar for end date selection"""
        self.open_calendar("end")
    
    def open_calendar(self, date_type):
        """Open calendar dialog"""
        # Create top-level window for calendar
        cal_window = ctk.CTkToplevel(self)
        cal_window.title("📅 Select Date")
        cal_window.geometry("400x450")
        cal_window.resizable(False, False)
        
        # Make window stay on top
        cal_window.attributes('-topmost', True)
        cal_window.lift()
        cal_window.focus()
        
        # Center window on screen
        cal_window.update_idletasks()
        
        # Create frame for calendar
        cal_frame = ctk.CTkFrame(cal_window, fg_color="white", corner_radius=10)
        cal_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title label
        title = ctk.CTkLabel(
            cal_frame, 
            text=f"Select {'Start' if date_type == 'start' else 'End'} Date",
            font=("Helvetica", 13, "bold"), text_color="#1f1f1f"
        )
        title.pack(pady=(10, 5))
        
        # Create embedded calendar using tkcalendar
        try:
            # Get current date or previously selected date
            if date_type == "start" and self.start_date:
                current_date = self.start_date
            elif date_type == "end" and self.end_date:
                current_date = self.end_date
            else:
                current_date = datetime.now()
            
            # Create calendar
            cal = Calendar(
                cal_frame,
                font=("Helvetica", 10),
                selectmode='day',
                cursor="hand2",
                year=current_date.year,
                month=current_date.month,
                day=current_date.day,
                background="#2563EB",
                foreground="white",
                normalforeground="#1f1f1f",
                weekendforeground="#DC2626",
                headersforeground="#ffffff",
                headersbackground="#1E40AF",
                selectforeground="#ffffff",
                selectbackground="#059669"
            )
            cal.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Buttons frame
            button_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
            button_frame.pack(fill="x", padx=10, pady=(10, 10))
            
            # Select button
            def select_date():
                selected_date = cal.selection_get()
                if selected_date:
                    if date_type == "start":
                        self.start_date = selected_date
                        self.start_date_display.configure(text=selected_date.strftime("%d-%m-%Y"))
                    else:
                        self.end_date = selected_date
                        self.end_date_display.configure(text=selected_date.strftime("%d-%m-%Y"))
                    
                    self.filter_sales()
                    cal_window.destroy()
            
            select_btn = ctk.CTkButton(
                button_frame, text="✓ Select Date", height=35,
                command=select_date, fg_color="#059669", hover_color="#047857",
                font=("Helvetica", 11, "bold")
            )
            select_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Cancel button
            cancel_btn = ctk.CTkButton(
                button_frame, text="✕ Cancel", height=35,
                command=cal_window.destroy, fg_color="#DC2626", hover_color="#B91C1C",
                font=("Helvetica", 11, "bold")
            )
            cancel_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        except Exception as e:
            error_label = ctk.CTkLabel(
                cal_frame,
                text=f"Calendar Error:\n{str(e)}\n\nPlease use manual date entry\nFormat: DD-MM-YYYY",
                font=("Helvetica", 10), text_color="#DC2626"
            )
            error_label.pack(pady=20)

    def load_sales(self):
        """Load and display sales"""
        self.all_sales = get_all_sales()
        self.filter_sales()

    def filter_sales(self):
        """Filter sales based on search and date range"""
        search_text = self.search_entry.get().lower()

        filtered = self.all_sales

        # Filter by search text
        if search_text:
            filtered = [s for s in filtered if search_text in (s[0].lower() or "") or search_text in (s[5].lower() or "")]

        # Filter by date range
        if self.start_date or self.end_date:
            filtered_by_date = []
            for sale in filtered:
                sale_date_str = sale[7]  # date is at index 7 (after adding customer_phone)
                sale_date = self.parse_sale_date(sale_date_str)
                
                if sale_date:
                    include = True
                    if self.start_date and sale_date < self.start_date:
                        include = False
                    if self.end_date and sale_date > self.end_date:
                        include = False
                    if include:
                        filtered_by_date.append(sale)
            filtered = filtered_by_date

        self.filtered_sales = filtered
        self.total_pages = max(1, (len(filtered) + self.page_size - 1) // self.page_size)
        self.current_page = 1
        self.display_page()

    def display_page(self):
        """Render only the current page of sales"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        start_idx = (self.current_page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        page_sales = self.filtered_sales[start_idx:end_idx]

        if not page_sales:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No sales found." if self.filtered_sales else "No sales recorded yet.",
                text_color="#999999", font=("Helvetica", 12, "bold")
            )
            empty_label.pack(pady=30)
            self._update_pagination()
            return

        for sale in page_sales:
            product_name, qty, pp, sp, profit_loss, customer, phone, date = sale

            row_frame = ctk.CTkFrame(
                self.scrollable_frame, fg_color="white", corner_radius=8
            )
            row_frame.pack(fill="x", padx=5, pady=4)
            
            # Fixed width columns matching header exactly
            row_frame.grid_columnconfigure(0, weight=1, minsize=120)
            row_frame.grid_columnconfigure(1, weight=1, minsize=120)
            row_frame.grid_columnconfigure(2, weight=1, minsize=110)
            row_frame.grid_columnconfigure(3, weight=1, minsize=110)
            row_frame.grid_columnconfigure(4, weight=1, minsize=100)
            row_frame.grid_columnconfigure(5, weight=1, minsize=130)
            row_frame.grid_columnconfigure(6, weight=1, minsize=130)

            profit_color = "#059669" if profit_loss >= 0 else "#DC2626"
            
            # Parse and format date
            parsed_date = self.parse_sale_date(date)
            date_str = parsed_date.strftime("%d %b %y") if parsed_date else "N/A"
            
            customer_name = customer if customer else "Walk-in"
            customer_phone = phone if phone else "N/A"

            # Create labels with consistent spacing and alignment
            ctk.CTkLabel(
                row_frame, text=product_name, font=("Helvetica", 11, "bold"),
                anchor="w", text_color="#1f1f1f"
            ).grid(row=0, column=0, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                row_frame, text=customer_name, font=("Helvetica", 11, "bold"),
                anchor="w", text_color="#1f1f1f"
            ).grid(row=0, column=1, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                row_frame, text=customer_phone, font=("Helvetica", 11, "bold"),
                anchor="w", text_color="#666666"
            ).grid(row=0, column=2, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                row_frame, text=str(qty), font=("Helvetica", 11, "bold"),
                anchor="w", text_color="#1f1f1f"
            ).grid(row=0, column=3, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                row_frame, text=f"₨{sp:.2f}", font=("Helvetica", 11, "bold"),
                anchor="w", text_color="#1f1f1f"
            ).grid(row=0, column=4, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                row_frame, text=f"₨{profit_loss:.2f}", font=("Helvetica", 11, "bold"),
                text_color=profit_color, anchor="w"
            ).grid(row=0, column=5, padx=12, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                row_frame, text=date_str, font=("Helvetica", 11, "bold"),
                anchor="w", text_color="#1f1f1f"
            ).grid(row=0, column=6, padx=12, pady=10, sticky="ew")

        self._update_pagination()

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
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_page()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_page()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_entry.delete(0, "end")
        self.start_date = None
        self.end_date = None
        self.start_date_display.configure(text="Select")
        self.end_date_display.configure(text="Select")
        self.filter_sales()