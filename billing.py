# """
# Billing / Cash Memo Page with PDF Generation (Searchable Products)
# File: billing.py
# """

# import customtkinter as ctk
# from db import (
#     get_all_products, get_all_customers, add_sale, update_inventory_quantity, 
#     update_customer_remaining, add_customer, get_product_by_name
# )
# from reportlab.lib.pagesizes import letter, A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
# from reportlab.lib import colors
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
# import os
# from datetime import datetime

# class SearchableComboBox(ctk.CTkFrame):
#     """Custom searchable combo box widget"""
#     def __init__(self, master, all_products, **kwargs):
#         super().__init__(master, fg_color="transparent")
        
#         self.all_products = all_products
#         self.filtered_products = all_products
#         self.selected_product = None
#         self.on_select_callback = kwargs.get('command', None)
        
#         # Entry field for search
#         self.search_entry = ctk.CTkEntry(
#             self, placeholder_text="Search product...",
#             height=35, font=("Helvetica", 11)
#         )
#         self.search_entry.pack(fill="x", pady=(0, 5))
#         self.search_entry.bind("<KeyRelease>", self.on_search_change)
#         self.search_entry.bind("<Up>", self.on_up_key)
#         self.search_entry.bind("<Down>", self.on_down_key)
#         self.search_entry.bind("<Return>", self.on_return_key)
        
#         # Dropdown listbox frame
#         self.listbox_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=6)
#         self.listbox_frame.pack(fill="both", expand=True)
#         self.listbox_frame.pack_propagate(False)
        
#         # Scrollable listbox
#         self.listbox = ctk.CTkScrollableFrame(
#             self.listbox_frame, fg_color="white"
#         )
#         self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
#         self.listbox.grid_columnconfigure(0, weight=1)
        
#         self.listbox_buttons = []
#         self.selected_index = -1
        
#         self.populate_listbox()
    
#     def on_search_change(self, event=None):
#         """Filter products as user types"""
#         search_text = self.search_entry.get().lower()
        
#         if search_text == "":
#             self.filtered_products = self.all_products
#         else:
#             self.filtered_products = [
#                 p for p in self.all_products
#                 if search_text in p[1].lower()  # p[1] is product name
#             ]
        
#         self.selected_index = -1
#         self.populate_listbox()
    
#     def populate_listbox(self):
#         """Populate listbox with filtered products"""
#         # Clear existing buttons
#         for btn in self.listbox_buttons:
#             btn.destroy()
#         self.listbox_buttons = []
        
#         if not self.filtered_products:
#             no_result = ctk.CTkLabel(
#                 self.listbox, text="No products found",
#                 text_color="#999999", font=("Helvetica", 11)
#             )
#             no_result.pack(pady=20)
#             return
        
#         # Create button for each product
#         for idx, product in enumerate(self.filtered_products):
#             prod_id, name, category, qty, pp, sp = product
            
#             # Button text with product info
#             btn_text = f"{name} - ₨{sp:.2f} (Qty: {qty})"
            
#             btn = ctk.CTkButton(
#                 self.listbox,
#                 text=btn_text,
#                 text_color="#1f1f1f",
#                 fg_color="transparent",
#                 hover_color="#E5E7EB",
#                 anchor="w",
#                 font=("Helvetica", 11),
#                 command=lambda p=product, i=idx: self.select_product(p, i)
#             )
#             btn.grid(row=idx, column=0, sticky="ew", padx=0, pady=3)
#             self.listbox_buttons.append(btn)
    
#     def select_product(self, product, index):
#         """Select a product from the list"""
#         self.selected_product = product
#         self.selected_index = index
#         self.search_entry.delete(0, "end")
#         self.search_entry.insert(0, product[1])  # Set entry to product name
        
#         # Call callback if provided
#         if self.on_select_callback:
#             self.on_select_callback(product)
        
#         # Reset filtered list
#         self.filtered_products = self.all_products
#         self.populate_listbox()
    
#     def on_up_key(self, event):
#         """Handle up arrow key"""
#         if self.selected_index > 0:
#             self.selected_index -= 1
#             self.select_product(self.filtered_products[self.selected_index], self.selected_index)
    
#     def on_down_key(self, event):
#         """Handle down arrow key"""
#         if self.selected_index < len(self.filtered_products) - 1:
#             self.selected_index += 1
#             self.select_product(self.filtered_products[self.selected_index], self.selected_index)
    
#     def on_return_key(self, event):
#         """Handle Enter key"""
#         if self.selected_index >= 0 and self.selected_index < len(self.filtered_products):
#             self.select_product(self.filtered_products[self.selected_index], self.selected_index)
    
#     def get(self):
#         """Get selected product"""
#         return self.selected_product


# class Page(ctk.CTkFrame):
#     def __init__(self, parent, go_back_callback):
#         super().__init__(parent, fg_color="#f8f9fa")
#         self.go_back = go_back_callback
        
#         self.grid_rowconfigure(1, weight=1)
#         self.grid_columnconfigure(0, weight=1)
        
#         self.bill_items = []
#         self.total_amount = 0.0
#         self.bill_completed = False
#         self.last_bill_data = None
        
#         self.create_widgets()
    
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
#             header, text="🧾 Billing / Cash Memo",
#             font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
#         )
#         title.grid(row=0, column=1, sticky="w")
        
#         # Main container with 3 sections: Input, Bill Items, Summary
#         container = ctk.CTkFrame(self, fg_color="transparent")
#         container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
#         container.grid_columnconfigure(0, weight=1)
#         container.grid_columnconfigure(1, weight=1)
#         container.grid_columnconfigure(2, weight=1)
#         container.grid_rowconfigure(0, weight=1)
        
#         # ===== LEFT PANEL - ADD ITEMS INPUT =====
#         left_panel = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
#         left_panel.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
#         section_label = ctk.CTkLabel(
#             left_panel, text="📦 Add Items",
#             font=("Helvetica", 14, "bold"), text_color="#1f1f1f"
#         )
#         section_label.pack(padx=15, pady=(15, 10))
        
#         # Product selection with search
#         ctk.CTkLabel(left_panel, text="Product:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f").pack(anchor="w", padx=15, pady=(8, 2))
        
#         # Searchable combo box
#         all_products = get_all_products() or []
#         self.product_combo = SearchableComboBox(
#             left_panel,
#             all_products,
#             command=self.on_product_selected
#         )
#         self.product_combo.pack(padx=15, pady=(0, 8), fill="x", ipady=3)
        
#         # Quantity
#         ctk.CTkLabel(left_panel, text="Quantity:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f").pack(anchor="w", padx=15, pady=(8, 2))
#         self.qty_entry = ctk.CTkEntry(left_panel, placeholder_text="Enter quantity", height=35, font=("Helvetica", 11))
#         self.qty_entry.pack(padx=15, pady=(0, 10), fill="x")
        
#         # Add button
#         add_item_btn = ctk.CTkButton(
#             left_panel, text="+ Add to Bill", height=40,
#             command=self.add_item_to_bill, fg_color="#059669", hover_color="#047857",
#             font=("Helvetica", 12, "bold")
#         )
#         add_item_btn.pack(padx=15, pady=(0, 15), fill="x")
        
#         # ===== MIDDLE PANEL - BILL ITEMS DISPLAY =====
#         middle_panel = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
#         middle_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
#         middle_panel.grid_rowconfigure(1, weight=1)
        
#         bill_items_label = ctk.CTkLabel(
#             middle_panel, text="📋 Bill Items",
#             font=("Helvetica", 14, "bold"), text_color="#1f1f1f"
#         )
#         bill_items_label.pack(padx=15, pady=(15, 10), anchor="w")
        
#         self.bill_frame = ctk.CTkScrollableFrame(middle_panel, fg_color="transparent")
#         self.bill_frame.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        
#         # ===== RIGHT PANEL - SUMMARY & CUSTOMER =====
#         right_panel = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
#         right_panel.grid(row=0, column=2, sticky="nsew")
#         right_panel.grid_rowconfigure(2, weight=1)
        
#         summary_label = ctk.CTkLabel(
#             right_panel, text="💵 Summary",
#             font=("Helvetica", 14, "bold"), text_color="#1f1f1f"
#         )
#         summary_label.pack(padx=15, pady=(15, 15))
        
#         # Total display
#         self.total_label = ctk.CTkLabel(
#             right_panel, text="Total: ₨0.00",
#             font=("Helvetica", 20, "bold"), text_color="#2563EB"
#         )
#         self.total_label.pack(padx=15, pady=(0, 20))
        
#         # Customer section
#         customer_title = ctk.CTkLabel(right_panel, text="Customer:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
#         customer_title.pack(anchor="w", padx=15, pady=(10, 5))
        
#         self.customer_name_entry = ctk.CTkEntry(right_panel, placeholder_text="Name", height=32, font=("Helvetica", 10))
#         self.customer_name_entry.pack(padx=15, pady=(0, 5), fill="x")
        
#         self.customer_phone_entry = ctk.CTkEntry(right_panel, placeholder_text="Phone", height=32, font=("Helvetica", 10))
#         self.customer_phone_entry.pack(padx=15, pady=(0, 12), fill="x")
        
#         # Payment section
#         payment_title = ctk.CTkLabel(right_panel, text="Amount Paid (₨):", font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
#         payment_title.pack(anchor="w", padx=15, pady=(8, 5))
        
#         self.payment_entry = ctk.CTkEntry(right_panel, placeholder_text="Full by default", height=32, font=("Helvetica", 10))
#         self.payment_entry.pack(padx=15, pady=(0, 15), fill="x")
        
#         # Action buttons - Compact
#         checkout_btn = ctk.CTkButton(
#             right_panel, text="✓ Checkout", height=38,
#             command=self.checkout, fg_color="#059669", hover_color="#047857",
#             font=("Helvetica", 11, "bold")
#         )
#         checkout_btn.pack(padx=15, fill="x", pady=(0, 8))
        
#         self.pdf_btn = ctk.CTkButton(
#             right_panel, text="📄 PDF Bill", height=38,
#             command=self.generate_pdf, fg_color="#2563EB", hover_color="#1E40AF",
#             font=("Helvetica", 11, "bold"),
#             state="disabled"
#         )
#         self.pdf_btn.pack(padx=15, fill="x", pady=(0, 8))
        
#         clear_btn = ctk.CTkButton(
#             right_panel, text="🔄 Clear", height=38,
#             command=self.clear_bill, fg_color="#DC2626", hover_color="#B91C1C",
#             font=("Helvetica", 11, "bold")
#         )
#         clear_btn.pack(padx=15, fill="x", pady=(0, 15))
    
#     def on_product_selected(self, product):
#         """Callback when product is selected from searchable combo"""
#         # This callback is optional - product is already selected in combo
#         pass
    
#     def add_item_to_bill(self):
#         """Add item to bill"""
#         product = self.product_combo.get()
#         qty_str = self.qty_entry.get()
        
#         if not product:
#             self.show_message("Please select a product", "⚠")
#             return
        
#         if not qty_str or not qty_str.isdigit():
#             self.show_message("Enter valid quantity", "⚠")
#             return
        
#         prod_id, name, category, available_qty, pp, sp = product
#         qty = int(qty_str)
        
#         if qty > available_qty:
#             self.show_message(f"Only {available_qty} items available", "⚠")
#             return
        
#         # Add to bill
#         item = {
#             "name": name,
#             "qty": qty,
#             "pp": pp,
#             "sp": sp,
#             "total": sp * qty
#         }
#         self.bill_items.append(item)
        
#         self.qty_entry.delete(0, "end")
#         self.update_bill_display()
    
#     def update_bill_display(self):
#         """Update bill items display"""
#         for widget in self.bill_frame.winfo_children():
#             widget.destroy()
        
#         self.total_amount = 0
        
#         for idx, item in enumerate(self.bill_items):
#             self.total_amount += item["total"]
            
#             item_frame = ctk.CTkFrame(self.bill_frame, fg_color="#f0f0f0", corner_radius=6)
#             item_frame.pack(fill="x", pady=5)
            
#             info_text = f"{item['name']} x{item['qty']} @ ₨{item['sp']:.2f} = ₨{item['total']:.2f}"
#             info_label = ctk.CTkLabel(item_frame, text=info_text, font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
#             info_label.pack(side="left", padx=10, pady=8)
            
#             remove_btn = ctk.CTkButton(
#                 item_frame, text="✕", width=30, height=30,
#                 font=("Helvetica", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C",
#                 command=lambda i=idx: self.remove_item(i)
#             )
#             remove_btn.pack(side="right", padx=5, pady=5)
        
#         self.total_label.configure(text=f"Total: ₨{self.total_amount:.2f}")
    
#     def remove_item(self, idx):
#         """Remove item from bill"""
#         if 0 <= idx < len(self.bill_items):
#             self.bill_items.pop(idx)
#             self.update_bill_display()
    
#     def checkout(self):
#         """Process checkout"""
#         if not self.bill_items:
#             self.show_message("Bill is empty", "⚠")
#             return
        
#         # Get customer info
#         customer_name = self.customer_name_entry.get().strip()
#         customer_phone = self.customer_phone_entry.get().strip()
        
#         # Get payment amount
#         payment_str = self.payment_entry.get()
#         payment = self.total_amount
#         if payment_str:
#             try:
#                 payment = float(payment_str)
#             except ValueError:
#                 self.show_message("Invalid payment amount", "⚠")
#                 return
        
#         # Auto-create customer if name and phone provided
#         if customer_name and customer_phone:
#             customers = get_all_customers()
#             customer_exists = any(c[1] == customer_name and c[2] == customer_phone for c in customers)
            
#             if not customer_exists:
#                 # Auto-create customer with initial balance
#                 remaining = self.total_amount - payment
#                 add_customer(customer_name, customer_phone)
#                 if remaining > 0:
#                     update_customer_remaining(customer_name, customer_phone, remaining)
#             else:
#                 # Update existing customer balance
#                 if payment < self.total_amount:
#                     remaining = self.total_amount - payment
#                     update_customer_remaining(customer_name, customer_phone, remaining)
        
#         # Store bill data for PDF generation
#         self.last_bill_data = {
#             "items": [item.copy() for item in self.bill_items],
#             "total": self.total_amount,
#             "customer_name": customer_name if customer_name else "Walk-in Customer",
#             "customer_phone": customer_phone if customer_phone else "N/A",
#             "payment": payment,
#             "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
#         }
        
#         # Process each item
#         for item in self.bill_items:
#             # Update inventory
#             update_inventory_quantity(item["name"], -item["qty"])
            
#             # Record sale
#             add_sale(
#                 item["name"], item["qty"], item["pp"], item["sp"],
#                 customer_name if customer_name else None,
#                 customer_phone if customer_phone else None,
#                 payment
#             )
        
#         self.bill_completed = True
#         self.pdf_btn.configure(state="normal")  # Enable PDF button
#         self.show_message(f"✓ Bill completed!\n\nTotal: ₨{self.total_amount:.2f}\nPaid: ₨{payment:.2f}\n\nClick 'Generate PDF Bill' to print", "✓")
    
#     def generate_pdf(self):
#         """Generate professional PDF bill"""
#         if not self.last_bill_data:
#             self.show_message("No completed bill to print", "⚠")
#             return
        
#         try:
#             # Create output directory if it doesn't exist
#             if not os.path.exists("bills"):
#                 os.makedirs("bills")
            
#             # Generate filename with timestamp
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"bills/Bill_{timestamp}.pdf"
            
#             # Create PDF
#             pdf = SimpleDocTemplate(
#                 filename,
#                 pagesize=A4,
#                 rightMargin=0.5*inch,
#                 leftMargin=0.5*inch,
#                 topMargin=0.5*inch,
#                 bottomMargin=0.5*inch
#             )
            
#             elements = []
#             styles = getSampleStyleSheet()
            
#             # Title
#             title_style = ParagraphStyle(
#                 'CustomTitle',
#                 parent=styles['Heading1'],
#                 fontSize=22,
#                 textColor=colors.HexColor("#2563EB"),
#                 spaceAfter=12,
#                 alignment=TA_CENTER,
#                 fontName='Helvetica-Bold'
#             )
#             title = Paragraph("INVOICE / BILL", title_style)
#             elements.append(title)
            
#             # Shop info and date
#             header_style = ParagraphStyle(
#                 'Header',
#                 parent=styles['Normal'],
#                 fontSize=10,
#                 alignment=TA_CENTER,
#                 textColor=colors.grey,
#                 fontName='Helvetica'
#             )
#             shop_info = Paragraph(
#                 f"<b>Professional Shop Management System</b><br/>Date: {self.last_bill_data['date']}",
#                 header_style
#             )
#             elements.append(shop_info)
#             elements.append(Spacer(1, 0.25*inch))
            
#             # Customer info section
#             customer_style = ParagraphStyle(
#                 'CustomerInfo',
#                 parent=styles['Normal'],
#                 fontSize=10,
#                 textColor=colors.HexColor("#1f1f1f"),
#                 fontName='Helvetica'
#             )
#             customer_text = f"""
#             <b>Customer Information:</b><br/>
#             Name: {self.last_bill_data['customer_name']}<br/>
#             Phone: {self.last_bill_data['customer_phone']}
#             """
#             customer_info = Paragraph(customer_text, customer_style)
#             elements.append(customer_info)
#             elements.append(Spacer(1, 0.2*inch))
            
#             # Bill items table
#             bill_data = [["Sr.", "Product Name", "Quantity", "Unit Price", "Amount"]]
            
#             sr_no = 1
#             for item in self.last_bill_data['items']:
#                 bill_data.append([
#                     str(sr_no),
#                     item['name'],
#                     str(item['qty']),
#                     f"₨{item['sp']:.2f}",
#                     f"₨{item['total']:.2f}"
#                 ])
#                 sr_no += 1
            
#             # Create table with professional styling
#             table = Table(bill_data, colWidths=[0.6*inch, 2.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
#             table.setStyle(TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563EB")),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('FONTSIZE', (0, 0), (-1, 0), 11),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#D1D5DB")),
#                 ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#                 ('FONTSIZE', (0, 1), (-1, -1), 10),
#                 ('TOPPADDING', (0, 1), (-1, -1), 10),
#                 ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
#                 ('ALIGN', (0, 1), (2, -1), 'CENTER'),
#                 ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
#                 ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
#             ]))
            
#             elements.append(table)
#             elements.append(Spacer(1, 0.25*inch))
            
#             # Summary section
#             summary_data = [
#                 ["Subtotal:", f"₨{self.last_bill_data['total']:.2f}"],
#                 ["Amount Paid:", f"₨{self.last_bill_data['payment']:.2f}"],
#                 ["Balance Due:", f"₨{max(0, self.last_bill_data['total'] - self.last_bill_data['payment']):.2f}"]
#             ]
            
#             summary_table = Table(summary_data, colWidths=[4.2*inch, 1.6*inch])
#             summary_table.setStyle(TableStyle([
#                 ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
#                 ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
#                 ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
#                 ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
#                 ('FONTSIZE', (0, 0), (1, -1), 10),
#                 ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#                 ('TOPPADDING', (0, 0), (-1, -1), 8),
#             ]))
            
#             elements.append(summary_table)
#             elements.append(Spacer(1, 0.3*inch))
            
#             # Thank you message
#             footer_style = ParagraphStyle(
#                 'Footer',
#                 parent=styles['Normal'],
#                 fontSize=10,
#                 alignment=TA_CENTER,
#                 textColor=colors.grey,
#                 fontName='Helvetica-Oblique'
#             )
#             footer = Paragraph("Thank you for your business! We appreciate your patronage.", footer_style)
#             elements.append(footer)
            
#             # Build PDF
#             pdf.build(elements)
            
#             self.show_message(f"✓ PDF Generated!\n\nSaved as: {filename}", "✓")
            
#             # Optional: Open the PDF automatically
#             try:
#                 if os.name == 'nt':  # Windows
#                     os.startfile(filename)
#                 elif os.name == 'posix':  # Mac/Linux
#                     os.system(f'open "{filename}"')
#             except Exception:
#                 pass  # Silent fail if auto-open doesn't work
            
#         except Exception as e:
#             self.show_message(f"Error generating PDF: {str(e)}", "⚠")
    
#     def clear_bill(self):
#         """Clear all items from bill"""
#         self.bill_items = []
#         self.total_amount = 0
#         self.qty_entry.delete(0, "end")
#         self.payment_entry.delete(0, "end")
#         self.customer_name_entry.delete(0, "end")
#         self.customer_phone_entry.delete(0, "end")
#         self.bill_completed = False
#         self.pdf_btn.configure(state="disabled")
#         self.update_bill_display()
    
#     def show_message(self, msg, icon):
#         """Show message dialog"""
#         dialog = ctk.CTkInputDialog(text=f"{msg}", title="Bill Status")
#         dialog.get_input()



"""
Billing / Cash Memo Page with PDF Generation (Searchable Products)
File: billing.py
"""

import customtkinter as ctk
from db import (
    get_all_products, get_all_customers, add_sale, update_inventory_quantity, 
    update_customer_remaining, add_customer, get_product_by_name
)
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime

class SearchableComboBox(ctk.CTkFrame):
    """Custom searchable combo box widget - Performance Optimized"""
    def __init__(self, master, all_products, **kwargs):
        super().__init__(master, fg_color="transparent")
        
        self.all_products = all_products
        # Pre-create lowercase index for faster searching
        self.product_name_lower = {i: p[1].lower() for i, p in enumerate(all_products)}
        self.filtered_products = list(range(len(all_products)))  # Store indices instead of full objects
        self.selected_product = None
        self.on_select_callback = kwargs.get('command', None)
        
        # Entry field for search
        self.search_entry = ctk.CTkEntry(
            self, placeholder_text="Search product...",
            height=35, font=("Helvetica", 11)
        )
        self.search_entry.pack(fill="x", pady=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        self.search_entry.bind("<Up>", self.on_up_key)
        self.search_entry.bind("<Down>", self.on_down_key)
        self.search_entry.bind("<Return>", self.on_return_key)
        
        # Dropdown listbox frame - Fixed height for performance
        self.listbox_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=6, height=200)
        self.listbox_frame.pack(fill="both", expand=True)
        self.listbox_frame.pack_propagate(False)
        
        # Scrollable listbox
        self.listbox = ctk.CTkScrollableFrame(
            self.listbox_frame, fg_color="white"
        )
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.listbox.grid_columnconfigure(0, weight=1)
        self.listbox._scrollbar.configure(width=10)
        
        self.listbox_buttons = []
        self.selected_index = -1
        self.search_timer = None
        self.MAX_DISPLAY = 50  # Limit displayed items for performance
        
        self.populate_listbox()
    
    def on_search_change(self, event=None):
        """Filter products as user types - with debouncing"""
        if self.search_timer:
            self.after_cancel(self.search_timer)
        
        # Debounce: only update after 50ms of no typing
        self.search_timer = self.after(50, self._perform_search)
    
    def _perform_search(self):
        """Actually perform the search - separated for debouncing"""
        search_text = self.search_entry.get().lower()
        
        if search_text == "":
            self.filtered_products = list(range(len(self.all_products)))
        else:
            # Only search product names (pre-lowercased)
            self.filtered_products = [
                i for i in range(len(self.all_products))
                if search_text in self.product_name_lower[i]
            ]
        
        self.selected_index = -1
        self.populate_listbox()
    
    def populate_listbox(self):
        """Populate listbox with filtered products - Optimized"""
        # Clear existing buttons efficiently
        for btn in self.listbox_buttons:
            btn.destroy()
        self.listbox_buttons = []
        
        if not self.filtered_products:
            no_result = ctk.CTkLabel(
                self.listbox, text="No products found",
                text_color="#999999", font=("Helvetica", 11)
            )
            no_result.pack(pady=20)
            return
        
        # Limit displayed items for performance
        display_count = min(len(self.filtered_products), self.MAX_DISPLAY)
        
        # Create buttons only for visible items
        for display_idx in range(display_count):
            product_idx = self.filtered_products[display_idx]
            product = self.all_products[product_idx]
            prod_id, name, category, qty, pp, sp = product
            
            # Button text with product info
            btn_text = f"{name} - ₨{sp:.2f} (Qty: {qty})"
            
            btn = ctk.CTkButton(
                self.listbox,
                text=btn_text,
                text_color="#1f1f1f",
                fg_color="transparent",
                hover_color="#E5E7EB",
                anchor="w",
                font=("Helvetica", 11),
                command=lambda p=product, i=display_idx: self.select_product(p, i)
            )
            btn.grid(row=display_idx, column=0, sticky="ew", padx=0, pady=2)
            self.listbox_buttons.append(btn)
        
        # Show more results indicator if truncated
        if len(self.filtered_products) > self.MAX_DISPLAY:
            more_label = ctk.CTkLabel(
                self.listbox,
                text=f"... and {len(self.filtered_products) - self.MAX_DISPLAY} more results",
                text_color="#999999", font=("Helvetica", 10)
            )
            more_label.grid(row=display_count, column=0, sticky="ew", padx=0, pady=5)
    
    def select_product(self, product, index):
        """Select a product from the list"""
        self.selected_product = product
        self.selected_index = index
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, product[1])  # Set entry to product name
        
        # Call callback if provided
        if self.on_select_callback:
            self.on_select_callback(product)
        
        # Reset filtered list
        self.filtered_products = list(range(len(self.all_products)))
        self.populate_listbox()
    
    def on_up_key(self, event):
        """Handle up arrow key"""
        if self.selected_index > 0:
            self.selected_index -= 1
            product_idx = self.filtered_products[self.selected_index]
            self.select_product(self.all_products[product_idx], self.selected_index)
    
    def on_down_key(self, event):
        """Handle down arrow key"""
        if self.selected_index < len(self.filtered_products) - 1:
            self.selected_index += 1
            product_idx = self.filtered_products[self.selected_index]
            self.select_product(self.all_products[product_idx], self.selected_index)
    
    def on_return_key(self, event):
        """Handle Enter key"""
        if self.selected_index >= 0 and self.selected_index < len(self.filtered_products):
            product_idx = self.filtered_products[self.selected_index]
            self.select_product(self.all_products[product_idx], self.selected_index)
    
    def get(self):
        """Get selected product"""
        return self.selected_product


class Page(ctk.CTkFrame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, fg_color="#f8f9fa")
        self.go_back = go_back_callback
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.bill_items = []
        self.total_amount = 0.0
        self.bill_completed = False
        self.last_bill_data = None
        
        self.create_widgets()
    
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
            header, text="🧾 Billing / Cash Memo",
            font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
        )
        title.grid(row=0, column=1, sticky="w")
        
        # Main container with 3 sections: Input, Bill Items, Summary
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # ===== LEFT PANEL - ADD ITEMS INPUT =====
        left_panel = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
        left_panel.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        section_label = ctk.CTkLabel(
            left_panel, text="📦 Add Items",
            font=("Helvetica", 14, "bold"), text_color="#1f1f1f"
        )
        section_label.pack(padx=15, pady=(15, 10))
        
        # Product selection with search
        ctk.CTkLabel(left_panel, text="Product:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f").pack(anchor="w", padx=15, pady=(8, 2))
        
        # Searchable combo box
        all_products = get_all_products() or []
        self.product_combo = SearchableComboBox(
            left_panel,
            all_products,
            command=self.on_product_selected
        )
        self.product_combo.pack(padx=15, pady=(0, 8), fill="x", ipady=3)
        
        # Quantity
        ctk.CTkLabel(left_panel, text="Quantity:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f").pack(anchor="w", padx=15, pady=(8, 2))
        self.qty_entry = ctk.CTkEntry(left_panel, placeholder_text="Enter quantity", height=35, font=("Helvetica", 11))
        self.qty_entry.pack(padx=15, pady=(0, 10), fill="x")
        
        # Add button
        add_item_btn = ctk.CTkButton(
            left_panel, text="+ Add to Bill", height=40,
            command=self.add_item_to_bill, fg_color="#059669", hover_color="#047857",
            font=("Helvetica", 12, "bold")
        )
        add_item_btn.pack(padx=15, pady=(0, 15), fill="x")
        
        # ===== MIDDLE PANEL - BILL ITEMS DISPLAY =====
        middle_panel = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
        middle_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        middle_panel.grid_rowconfigure(1, weight=1)
        
        bill_items_label = ctk.CTkLabel(
            middle_panel, text="📋 Bill Items",
            font=("Helvetica", 14, "bold"), text_color="#1f1f1f"
        )
        bill_items_label.pack(padx=15, pady=(15, 10), anchor="w")
        
        self.bill_frame = ctk.CTkScrollableFrame(middle_panel, fg_color="transparent")
        self.bill_frame.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        
        # ===== RIGHT PANEL - SUMMARY & CUSTOMER =====
        right_panel = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
        right_panel.grid(row=0, column=2, sticky="nsew")
        right_panel.grid_rowconfigure(2, weight=1)
        
        summary_label = ctk.CTkLabel(
            right_panel, text="💵 Summary",
            font=("Helvetica", 14, "bold"), text_color="#1f1f1f"
        )
        summary_label.pack(padx=15, pady=(15, 15))
        
        # Total display
        self.total_label = ctk.CTkLabel(
            right_panel, text="Total: ₨0.00",
            font=("Helvetica", 20, "bold"), text_color="#2563EB"
        )
        self.total_label.pack(padx=15, pady=(0, 20))
        
        # Customer section
        customer_title = ctk.CTkLabel(right_panel, text="Customer:", font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
        customer_title.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.customer_name_entry = ctk.CTkEntry(right_panel, placeholder_text="Name", height=32, font=("Helvetica", 10))
        self.customer_name_entry.pack(padx=15, pady=(0, 5), fill="x")
        
        self.customer_phone_entry = ctk.CTkEntry(right_panel, placeholder_text="Phone", height=32, font=("Helvetica", 10))
        self.customer_phone_entry.pack(padx=15, pady=(0, 5), fill="x")
        
        self.customer_address_entry = ctk.CTkEntry(right_panel, placeholder_text="Address", height=32, font=("Helvetica", 10))
        self.customer_address_entry.pack(padx=15, pady=(0, 12), fill="x")
        
        # Payment section
        payment_title = ctk.CTkLabel(right_panel, text="Amount Paid (₨):", font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
        payment_title.pack(anchor="w", padx=15, pady=(8, 5))
        
        self.payment_entry = ctk.CTkEntry(right_panel, placeholder_text="Full by default", height=32, font=("Helvetica", 10))
        self.payment_entry.pack(padx=15, pady=(0, 15), fill="x")
        
        # Action buttons - Compact
        checkout_btn = ctk.CTkButton(
            right_panel, text="✓ Checkout", height=38,
            command=self.checkout, fg_color="#059669", hover_color="#047857",
            font=("Helvetica", 11, "bold")
        )
        checkout_btn.pack(padx=15, fill="x", pady=(0, 8))
        
        self.pdf_btn = ctk.CTkButton(
            right_panel, text="📄 PDF Bill", height=38,
            command=self.generate_pdf, fg_color="#2563EB", hover_color="#1E40AF",
            font=("Helvetica", 11, "bold"),
            state="disabled"
        )
        self.pdf_btn.pack(padx=15, fill="x", pady=(0, 8))
        
        clear_btn = ctk.CTkButton(
            right_panel, text="🔄 Clear", height=38,
            command=self.clear_bill, fg_color="#DC2626", hover_color="#B91C1C",
            font=("Helvetica", 11, "bold")
        )
        clear_btn.pack(padx=15, fill="x", pady=(0, 15))
    
    def on_product_selected(self, product):
        """Callback when product is selected from searchable combo"""
        # This callback is optional - product is already selected in combo
        pass
    
    def add_item_to_bill(self):
        """Add item to bill"""
        product = self.product_combo.get()
        qty_str = self.qty_entry.get()
        
        if not product:
            self.show_message("Please select a product", "⚠")
            return
        
        if not qty_str or not qty_str.isdigit():
            self.show_message("Enter valid quantity", "⚠")
            return
        
        prod_id, name, category, available_qty, pp, sp = product
        qty = int(qty_str)
        
        if qty > available_qty:
            self.show_message(f"Only {available_qty} items available", "⚠")
            return
        
        # Add to bill
        item = {
            "name": name,
            "qty": qty,
            "pp": pp,
            "sp": sp,
            "total": sp * qty
        }
        self.bill_items.append(item)
        
        self.qty_entry.delete(0, "end")
        self.update_bill_display()
    
    def update_bill_display(self):
        """Update bill items display"""
        for widget in self.bill_frame.winfo_children():
            widget.destroy()
        
        self.total_amount = 0
        
        for idx, item in enumerate(self.bill_items):
            self.total_amount += item["total"]
            
            item_frame = ctk.CTkFrame(self.bill_frame, fg_color="#f0f0f0", corner_radius=6)
            item_frame.pack(fill="x", pady=5)
            
            info_text = f"{item['name']} x{item['qty']} @ ₨{item['sp']:.2f} = ₨{item['total']:.2f}"
            info_label = ctk.CTkLabel(item_frame, text=info_text, font=("Helvetica", 11, "bold"), text_color="#1f1f1f")
            info_label.pack(side="left", padx=10, pady=8)
            
            remove_btn = ctk.CTkButton(
                item_frame, text="✕", width=30, height=30,
                font=("Helvetica", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C",
                command=lambda i=idx: self.remove_item(i)
            )
            remove_btn.pack(side="right", padx=5, pady=5)
        
        self.total_label.configure(text=f"Total: ₨{self.total_amount:.2f}")
    
    def remove_item(self, idx):
        """Remove item from bill"""
        if 0 <= idx < len(self.bill_items):
            self.bill_items.pop(idx)
            self.update_bill_display()
    
    def checkout(self):
        """Process checkout"""
        if not self.bill_items:
            self.show_message("Bill is empty", "⚠")
            return
        
        # Get customer info
        customer_name = self.customer_name_entry.get().strip()
        customer_phone = self.customer_phone_entry.get().strip()
        customer_address = self.customer_address_entry.get().strip()
        
        # Get payment amount
        payment_str = self.payment_entry.get()
        payment = self.total_amount
        if payment_str:
            try:
                payment = float(payment_str)
            except ValueError:
                self.show_message("Invalid payment amount", "⚠")
                return
        
        # Auto-create customer if name and phone provided
        if customer_name and customer_phone:
            customers = get_all_customers()
            customer_exists = any(c[1] == customer_name and c[2] == customer_phone for c in customers)
            
            if not customer_exists:
                # Auto-create customer with initial balance and address
                remaining = self.total_amount - payment
                add_customer(customer_name, customer_phone, customer_address)
                if remaining > 0:
                    update_customer_remaining(customer_name, customer_phone, remaining)
            else:
                # Update existing customer balance
                if payment < self.total_amount:
                    remaining = self.total_amount - payment
                    update_customer_remaining(customer_name, customer_phone, remaining)
        
        # Store bill data for PDF generation
        self.last_bill_data = {
            "items": [item.copy() for item in self.bill_items],
            "total": self.total_amount,
            "customer_name": customer_name if customer_name else "Walk-in Customer",
            "customer_phone": customer_phone if customer_phone else "N/A",
            "customer_address": customer_address if customer_address else "N/A",
            "payment": payment,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        
        # Process each item
        for item in self.bill_items:
            # Update inventory
            update_inventory_quantity(item["name"], -item["qty"])
            
            # Record sale
            add_sale(
                item["name"], item["qty"], item["pp"], item["sp"],
                customer_name if customer_name else None,
                customer_phone if customer_phone else None,
                payment
            )
        
        self.bill_completed = True
        self.pdf_btn.configure(state="normal")  # Enable PDF button
        self.show_message(f"✓ Bill completed!\n\nTotal: ₨{self.total_amount:.2f}\nPaid: ₨{payment:.2f}\n\nClick 'Generate PDF Bill' to print", "✓")
    
    def generate_pdf(self):
        """Generate professional PDF bill with logos and custom styling"""
        if not self.last_bill_data:
            self.show_message("No completed bill to print", "⚠")
            return
        
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists("bills"):
                os.makedirs("bills")
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bills/Bill_{timestamp}.pdf"
            
            # Create PDF
            pdf = SimpleDocTemplate(
                filename,
                pagesize=A4,
                rightMargin=0.4*inch,
                leftMargin=0.4*inch,
                topMargin=0.4*inch,
                bottomMargin=0.4*inch
            )
            
            elements = []
            styles = getSampleStyleSheet()
            
            # ===== LOGO SECTION =====
            script_dir = os.path.dirname(os.path.abspath(__file__)) + '/assets'
            logo_paths = [
                os.path.join(script_dir, "logo1.jpg"),
                os.path.join(script_dir, "logo2.jpg"),
            ]
            
            logo_elements = []
            for logo_path in logo_paths:
                if os.path.exists(logo_path):
                    try:
                        from reportlab.platypus import Image as RLImage
                        logo = RLImage(logo_path, width=0.8*inch, height=0.8*inch)
                        logo_elements.append(logo)
                    except Exception as e:
                        print(f"Could not load logo: {e}")
            
            # Logo table
            if logo_elements:
                logo_table = Table([logo_elements], colWidths=[1*inch, 1*inch])
                logo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elements.append(logo_table)
                elements.append(Spacer(1, 0.15*inch))
            
            # ===== TITLE =====
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor("#6B4423"),  # Brown color
                spaceAfter=6,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            title = Paragraph("INVOICE / BILL", title_style)
            elements.append(title)
            
            # Shop name
            shop_style = ParagraphStyle(
                'ShopName',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor("#6B4423"),  # Brown
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                spaceAfter=2
            )
            shop_name = Paragraph("Baba Online Khajoor and Precious Fragrance", shop_style)
            elements.append(shop_name)
            
            # Date and bill info
            info_style = ParagraphStyle(
                'Info',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor("#000000"),  # Black
                alignment=TA_CENTER,
                fontName='Helvetica',
                spaceAfter=12
            )
            bill_info = Paragraph(
                f"<b>Date:</b> {self.last_bill_data['date']}",
                info_style
            )
            elements.append(bill_info)
            
            # ===== CUSTOMER DETAILS =====
            customer_style = ParagraphStyle(
                'CustomerInfo',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor("#000000"),  # Black
                fontName='Helvetica',
                spaceAfter=10
            )
            customer_text = f"""
            <b>Customer Information:</b><br/>
            Name: {self.last_bill_data['customer_name']}<br/>
            Phone: {self.last_bill_data['customer_phone']}<br/>
            Address: {self.last_bill_data['customer_address']}
            """
            customer_info = Paragraph(customer_text, customer_style)
            elements.append(customer_info)
            elements.append(Spacer(1, 0.15*inch))
            
            # ===== BILL ITEMS TABLE =====
            bill_data = [["Sr.", "Product Name", "Quantity", "Unit Price", "Amount"]]
            
            sr_no = 1
            for item in self.last_bill_data['items']:
                bill_data.append([
                    str(sr_no),
                    item['name'],
                    str(item['qty']),
                    f"Rs {item['sp']:.2f}",
                    f"Rs {item['total']:.2f}"
                ])
                sr_no += 1
            
            # Create table with light brown border color
            table = Table(bill_data, colWidths=[0.5*inch, 2.4*inch, 1.0*inch, 1.2*inch, 1.2*inch])
            table.setStyle(TableStyle([
                # Header styling - light brown background
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#D2B48C")),  # Light brown
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#000000")),  # Black text
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Border styling - light brown
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#A0826D")),  # Dark brown border
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#000000")),  # Black text
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 1), (2, -1), 'CENTER'),
                ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5DC")]),  # Beige
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
            
            # ===== SUMMARY SECTION =====
            summary_data = [
                ["Subtotal:", f"Rs {self.last_bill_data['total']:.2f}"],
                ["Amount Paid:", f"Rs {self.last_bill_data['payment']:.2f}"],
                ["Balance Due:", f"Rs {max(0, self.last_bill_data['total'] - self.last_bill_data['payment']):.2f}"]
            ]
            
            summary_table = Table(summary_data, colWidths=[4.3*inch, 1.3*inch])
            summary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#000000")),  # Black text
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#A0826D")),  # Brown border
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#D2B48C")),  # Light brown
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(summary_table)
            elements.append(Spacer(1, 0.2*inch))
            
            # ===== FOOTER =====
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#6B4423"),  # Brown
                fontName='Helvetica-Oblique'
            )
            footer = Paragraph("Thank you for the shopping!.", footer_style)
            elements.append(footer)
            
            # Build PDF
            pdf.build(elements)
            
            self.show_message(f"✓ PDF Generated!\n\nSaved as: {filename}", "✓")
            
            # Optional: Open the PDF automatically
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(filename)
                elif os.name == 'posix':  # Mac/Linux
                    os.system(f'open "{filename}"')
            except Exception:
                pass  # Silent fail if auto-open doesn't work
            
        except Exception as e:
            self.show_message(f"Error generating PDF: {str(e)}", "⚠")
    
    def clear_bill(self):
        """Clear all items from bill"""
        self.bill_items = []
        self.total_amount = 0
        self.qty_entry.delete(0, "end")
        self.payment_entry.delete(0, "end")
        self.customer_name_entry.delete(0, "end")
        self.customer_phone_entry.delete(0, "end")
        self.customer_address_entry.delete(0, "end")
        self.bill_completed = False
        self.pdf_btn.configure(state="disabled")
        self.update_bill_display()
    
    def show_message(self, msg, icon):
        """Show message dialog"""
        dialog = ctk.CTkInputDialog(text=f"{msg}", title="Bill Status")
        dialog.get_input()