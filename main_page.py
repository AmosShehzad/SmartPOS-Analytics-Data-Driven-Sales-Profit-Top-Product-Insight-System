import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import os
import sys

from db import init_database, get_todays_sales, get_todays_transactions, get_total_products

init_database()


class ModernPOSFrontend(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("B&P - Point of Sale System")

        # FIXED: Proper fullscreen for Windows (reliable way)
        self.after(10, lambda: self.state("zoomed"))

        # Modern Color Scheme
        self.colors = {
            'primary': '#2563EB',
            'primary_dark': '#1E40AF',
            'secondary': '#7C3AED',
            'accent': '#F59E0B',
            'success': '#10B981',
            'danger': '#EF4444',
            'background': '#F8FAFC',
            'card': '#FFFFFF',
            'text_dark': '#1E293B',
            'text_light': '#64748B',
            'border': '#E2E8F0'
        }

        self.configure(fg_color=self.colors['background'])

        # Store current theme (light/dark)
        self.is_dark_mode = False

        # Animation variables
        self.card_hover_scale = 1.05
        self.animation_duration = 200

        self.setup_ui()

    def setup_ui(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=20)

        self.create_header(main_container)
        self.create_welcome_section(main_container)
        self.create_navigation_cards(main_container)
        self.create_footer(main_container)

    def create_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        header.pack(fill="x", pady=(0, 15))
        header.pack_propagate(False)

        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y")

        logo_frame = ctk.CTkFrame(
            left_frame,
            fg_color=self.colors['primary'],
            width=55,
            height=55,
            corner_radius=12
        )
        logo_frame.pack(side="left", padx=(0, 12))
        logo_frame.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="B&P",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="y")

        ctk.CTkLabel(
            title_frame,
            text="B&P POS System",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Professional Point of Sale System",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_light']
        ).pack(anchor="w")

        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", fill="y")

        self.theme_btn = ctk.CTkButton(
            right_frame,
            text="🌙 Dark",
            width=100,
            height=38,
            fg_color=self.colors['card'],
            text_color=self.colors['text_dark'],
            hover_color=self.colors['border'],
            border_width=2,
            border_color=self.colors['border'],
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right", padx=8)

        minimize_btn = ctk.CTkButton(
            right_frame,
            text="—",
            width=38,
            height=38,
            fg_color=self.colors['card'],
            text_color=self.colors['text_dark'],
            hover_color=self.colors['border'],
            border_width=2,
            border_color=self.colors['border'],
            command=self.iconify
        )
        minimize_btn.pack(side="right", padx=4)

        close_btn = ctk.CTkButton(
            right_frame,
            text="✕",
            width=38,
            height=38,
            fg_color=self.colors['danger'],
            text_color="white",
            hover_color="#DC2626",
            command=self.quit_app
        )
        close_btn.pack(side="right", padx=4)

    def create_welcome_section(self, parent):
        welcome_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['primary'],
            corner_radius=16,
            height=120
        )
        welcome_frame.pack(fill="x", pady=(0, 20))
        welcome_frame.pack_propagate(False)

        text_container = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        text_container.pack(side="left", padx=30, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            text_container,
            text="Welcome Back! 👋",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_container,
            text="Select an option below to get started with your POS operations",
            font=ctk.CTkFont(size=13),
            text_color="white",
            wraplength=450,
            justify="left"
        ).pack(anchor="w", pady=(3, 0))

        stats_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        stats_frame.pack(side="right", padx=30, pady=15)

        todays_sales = get_todays_sales()
        todays_transactions = get_todays_transactions()
        total_products = get_total_products()

        stats_data = [
            ("Today's Sales", f"₨ {todays_sales:,.0f}", self.colors['success']),
            ("Transactions", str(todays_transactions), self.colors['accent']),
            ("Active Products", str(total_products), self.colors['secondary'])
        ]

        for title, value, color in stats_data:
            stat_card = ctk.CTkFrame(
                stats_frame,
                fg_color="white",
                width=125,
                height=70,
                corner_radius=10
            )
            stat_card.pack(side="left", padx=6)
            stat_card.pack_propagate(False)

            ctk.CTkLabel(
                stat_card,
                text=value,
                font=ctk.CTkFont(size=17, weight="bold"),
                text_color=color
            ).pack(pady=(10, 0))

            ctk.CTkLabel(
                stat_card,
                text=title,
                font=ctk.CTkFont(size=10),
                text_color=self.colors['text_light']
            ).pack()

    def create_navigation_cards(self, parent):
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True, pady=(0, 10))

        nav_options = [
            {'title': 'New Sale', 'icon': '🛒', 'description': 'Start a new transaction and process customer purchases',
             'color': self.colors['success'], 'command': self.open_billing},
            {'title': 'Products', 'icon': '📦', 'description': 'Manage inventory, add products, and update prices',
             'color': self.colors['primary'], 'command': self.open_products},
            {'title': 'Sales History', 'icon': '📊', 'description': 'View sales records, invoices, and transaction history',
             'color': self.colors['secondary'], 'command': self.open_sales},
            {'title': 'Customers', 'icon': '👥', 'description': 'Manage customer database and loyalty programs',
             'color': self.colors['accent'], 'command': self.open_customers},
            {'title': 'Analytics', 'icon': '📈', 'description': 'View reports, charts, and business insights',
             'color': '#EC4899', 'command': self.open_analytics}
        ]

        for row in range(2):
            row_frame = ctk.CTkFrame(cards_frame, fg_color="transparent")
            row_frame.pack(fill="both", expand=True, pady=6)

            for col in range(3):
                idx = row * 3 + col
                if idx < len(nav_options):
                    self.create_card(row_frame, nav_options[idx])

    def create_card(self, parent, data):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['card'],
            corner_radius=16,
            border_width=2,
            border_color=self.colors['border']
        )
        card.pack(side="left", fill="both", expand=True, padx=8, pady=5)

        card.bind("<Button-1>", lambda e: data['command']())

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=18)
        content.bind("<Button-1>", lambda e: data['command']())

        icon_frame = ctk.CTkFrame(
            content,
            fg_color=data['color'],
            width=60,
            height=60,
            corner_radius=30
        )
        icon_frame.pack(pady=(0, 10))
        icon_frame.pack_propagate(False)
        icon_frame.bind("<Button-1>", lambda e: data['command']())

        icon_label = ctk.CTkLabel(icon_frame, text=data['icon'], font=ctk.CTkFont(size=28))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        icon_label.bind("<Button-1>", lambda e: data['command']())

        title_label = ctk.CTkLabel(
            content,
            text=data['title'],
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_dark']
        )
        title_label.pack()
        title_label.bind("<Button-1>", lambda e: data['command']())

        desc_label = ctk.CTkLabel(
            content,
            text=data['description'],
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_light'],
            wraplength=180,
            justify="center"
        )
        desc_label.pack(pady=(5, 0))
        desc_label.bind("<Button-1>", lambda e: data['command']())

        def on_enter(e):
            card.configure(border_color=data['color'], border_width=3)
            card.configure(fg_color=self.colors['background'])

        def on_leave(e):
            card.configure(border_color=self.colors['border'], border_width=2)
            card.configure(fg_color=self.colors['card'])

        for widget in [card, content, icon_frame, icon_label, title_label, desc_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_footer(self, parent):
        footer = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        footer.pack(fill="x", pady=(10, 0))
        footer.pack_propagate(False)

        left_info = ctk.CTkLabel(
            footer,
            text="© 2025 B&P POS • Version 1.0.0",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_light']
        )
        left_info.pack(side="left")

        status_frame = ctk.CTkFrame(footer, fg_color="transparent")
        status_frame.pack(side="right")

        status_dot = ctk.CTkFrame(
            status_frame,
            fg_color=self.colors['success'],
            width=9,
            height=9,
            corner_radius=5
        )
        status_dot.pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            status_frame,
            text="System Online",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_light']
        ).pack(side="left")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode

        if self.is_dark_mode:
            self.colors['background'] = '#0F172A'
            self.colors['card'] = '#1E293B'
            self.colors['text_dark'] = '#F1F5F9'
            self.colors['text_light'] = '#94A3B8'
            self.colors['border'] = '#334155'
            self.theme_btn.configure(text="☀ Light")
        else:
            self.colors['background'] = '#F8FAFC'
            self.colors['card'] = '#FFFFFF'
            self.colors['text_dark'] = '#1E293B'
            self.colors['text_light'] = '#64748B'
            self.colors['border'] = '#E2E8F0'
            self.theme_btn.configure(text="🌙 Dark")

        self.configure(fg_color=self.colors['background'])
        self.refresh_ui()

    def refresh_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

    def open_billing(self):
        try:
            import billing
            self.open_page("New Sale", billing.Page)
        except ImportError:
            self.show_error("Module 'billing' not found. Please create billing.py")
        except Exception as e:
            self.show_error(f"Error opening billing: {str(e)}")

    def open_products(self):
        try:
            import inventory
            self.open_page("Products", inventory.Page)
        except ImportError:
            self.show_error("Module 'inventory' not found. Please create inventory.py")
        except Exception as e:
            self.show_error(f"Error opening inventory: {str(e)}")

    def open_sales(self):
        try:
            import sales
            self.open_page("Sales History", sales.Page)
        except ImportError:
            self.show_error("Module 'sales' not found. Please create sales.py")
        except Exception as e:
            self.show_error(f"Error opening sales: {str(e)}")

    def open_customers(self):
        try:
            import customers
            self.open_page("Customers", customers.Page)
        except ImportError:
            self.show_error("Module 'customers' not found. Please create customers.py")
        except Exception as e:
            self.show_error(f"Error opening customers: {str(e)}")

    def open_analytics(self):
        try:
            import analytics
            self.open_page("Analytics", analytics.Page)
        except ImportError:
            self.show_error("Module 'analytics' not found. Please create analytics.py")
        except Exception as e:
            self.show_error(f"Error opening analytics: {str(e)}")

    def open_page(self, title, PageClass):
        self.withdraw()

        page_window = ctk.CTkToplevel(self)
        page_window.title(title)

        # already correct
        page_window.state("zoomed")

        def on_close():
            page_window.destroy()
            self.deiconify()

        page_window.protocol("WM_DELETE_WINDOW", on_close)

        try:
            page = PageClass(page_window, on_close)
            page.pack(fill="both", expand=True)
        except TypeError:
            try:
                page = PageClass(page_window)
                page.pack(fill="both", expand=True)
            except Exception as e:
                page_window.destroy()
                self.deiconify()
                self.show_error(f"Error creating page: {str(e)}")

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x180")
        error_window.resizable(False, False)
        error_window.attributes('-topmost', True)

        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (error_window.winfo_screenheight() // 2) - (180 // 2)
        error_window.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(error_window, fg_color=self.colors['card'])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="⚠", font=ctk.CTkFont(size=40)).pack(pady=(10, 5))

        ctk.CTkLabel(
            frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color=self.colors['danger'],
            wraplength=350
        ).pack(pady=10)

        ctk.CTkButton(
            frame,
            text="OK",
            command=error_window.destroy,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark'],
            width=100
        ).pack(pady=10)

    def quit_app(self):
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ModernPOSFrontend()
    app.mainloop()
