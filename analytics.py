"""
Analytics & Business Insights Page with Charts
File: analytics.py - ENHANCED VERSION
"""

import customtkinter as ctk
from db import get_all_sales, get_all_products, get_low_stock_products, get_total_profit_loss
from collections import defaultdict
from datetime import datetime, timedelta
import math

class Page(ctk.CTkFrame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, fg_color="#f8f9fa")
        self.go_back = go_back_callback
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Cache for analytics data
        self.analytics_cache = {}
        
        self.create_widgets()
        self.load_analytics()
    
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
            header, text="📈 Analytics & Insights",
            font=("Helvetica", 28, "bold"), text_color="#1f1f1f"
        )
        title.grid(row=0, column=1, sticky="w")
        
        refresh_btn = ctk.CTkButton(
            header, text="🔄 Refresh", width=100, height=40,
            command=self.load_analytics, fg_color="#2563EB", hover_color="#1E40AF",
            font=("Helvetica", 12, "bold")
        )
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Main container with scrollable content
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        container.grid_columnconfigure(0, weight=1)
        
        # KPI Cards - Enhanced Design
        kpi_frame = ctk.CTkFrame(container, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 25))
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total Profit/Loss card
        total_pl = get_total_profit_loss()
        pl_color = "#059669" if total_pl >= 0 else "#DC2626"
        pl_symbol = "📈" if total_pl >= 0 else "📉"
        
        card1 = self.create_kpi_card(kpi_frame, f"{pl_symbol} Total Profit/Loss", f"₨{total_pl:.2f}", pl_color)
        card1.grid(row=0, column=0, padx=8)
        
        # Total Products
        total_products = len(get_all_products())
        card2 = self.create_kpi_card(kpi_frame, "📦 Total Products", str(total_products), "#2563EB")
        card2.grid(row=0, column=1, padx=8)
        
        # Low Stock Alert
        low_stock = len(get_low_stock_products())
        alert_color = "#DC2626" if low_stock > 0 else "#059669"
        card3 = self.create_kpi_card(kpi_frame, "⚠️  Low Stock Items", str(low_stock), alert_color)
        card3.grid(row=0, column=2, padx=8)
        
        # Charts Section - Two column layout
        charts_frame = ctk.CTkFrame(container, fg_color="transparent")
        charts_frame.pack(fill="both", expand=False, pady=12)
        charts_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Profit by Product - Bar Chart
        profit_chart = self.create_chart_section(
            charts_frame, 
            "💰 Top 5 Profitable Products", 
            self.get_profit_chart_data
        )
        profit_chart.grid(row=0, column=0, padx=8, sticky="nsew")
        
        # Sales by Product - Bar Chart
        sales_chart = self.create_chart_section(
            charts_frame,
            "🛍️  Top 5 Best Sellers",
            self.get_sales_chart_data
        )
        sales_chart.grid(row=0, column=1, padx=8, sticky="nsew")
        
        # Insights Sections - Full width
        self.create_insight_section(container, "📉 Low Stock Alert", self.get_low_stock_alert, "#FEF3C7")
        self.create_insight_section(container, "⚠️  Slow-Moving Products", self.get_low_selling_products, "#FEE2E2")
        self.create_insight_section(container, "✅ Quick Wins", self.get_quick_stats, "#DCFCE7")
    
    def create_kpi_card(self, parent, title, value, color):
        """Create enhanced KPI card with gradient background"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        
        # Top accent bar
        accent = ctk.CTkFrame(card, fg_color=color, corner_radius=12)
        accent.pack(fill="x", padx=0, pady=0)
        
        # Spacer
        space = ctk.CTkFrame(card, fg_color="white", height=4, corner_radius=12)
        space.pack(fill="x", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(card, text=title, font=("Helvetica", 12, "bold"), text_color="#666666")
        title_label.pack(padx=15, pady=(12, 3))
        
        value_label = ctk.CTkLabel(card, text=value, font=("Helvetica", 24, "bold"), text_color=color)
        value_label.pack(padx=15, pady=(0, 12))
        
        return card
    
    def create_chart_section(self, parent, title, data_func):
        """Create chart section with bar visualization"""
        section = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        
        # Title
        title_label = ctk.CTkLabel(section, text=title, font=("Helvetica", 13, "bold"), text_color="#1f1f1f")
        title_label.pack(anchor="w", padx=15, pady=(15, 12))
        
        # Get data
        data = data_func()
        
        if not data:
            empty = ctk.CTkLabel(section, text="No data available", text_color="#999999", font=("Helvetica", 11))
            empty.pack(padx=15, pady=20)
        else:
            # Chart container
            chart_container = ctk.CTkFrame(section, fg_color="transparent")
            chart_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
            
            # Draw bars
            max_value = max([v for _, v in data]) if data else 1
            
            for idx, (name, value) in enumerate(data):
                bar_frame = ctk.CTkFrame(chart_container, fg_color="transparent")
                bar_frame.pack(fill="x", pady=8)
                
                # Label
                label = ctk.CTkLabel(
                    bar_frame, 
                    text=f"{name[:20]}...",
                    font=("Helvetica", 10, "bold"),
                    text_color="#1f1f1f",
                    width=150,
                    anchor="w"
                )
                label.pack(side="left", padx=(0, 10), anchor="w")
                
                # Bar with value
                bar_container = ctk.CTkFrame(bar_frame, fg_color="transparent")
                bar_container.pack(side="left", fill="both", expand=True)
                
                bar_width_percent = (value / max_value * 100) if max_value > 0 else 0
                
                bar = ctk.CTkFrame(bar_container, fg_color="#2563EB", corner_radius=4, height=20)
                bar.pack(fill="x", expand=False)
                
                # Value label
                value_label = ctk.CTkLabel(
                    bar,
                    text=f"  ₨{value:.0f}",
                    font=("Helvetica", 9, "bold"),
                    text_color="white",
                    anchor="w"
                )
                value_label.pack(side="left", padx=5, pady=2)
        
        return section
    
    def create_insight_section(self, parent, title, data_func, bg_color):
        """Create insight section with custom background"""
        section = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=12)
        section.pack(fill="x", pady=12)
        
        # Title
        title_label = ctk.CTkLabel(section, text=title, font=("Helvetica", 13, "bold"), text_color="#1f1f1f")
        title_label.pack(anchor="w", padx=15, pady=(15, 12))
        
        # Get data
        data = data_func()
        
        if not data:
            empty = ctk.CTkLabel(section, text="No items to display", text_color="#666666", font=("Helvetica", 11))
            empty.pack(padx=15, pady=10)
        else:
            for item in data:
                item_frame = ctk.CTkFrame(section, fg_color="white", corner_radius=8)
                item_frame.pack(fill="x", padx=15, pady=5)
                
                label = ctk.CTkLabel(
                    item_frame,
                    text=item,
                    font=("Helvetica", 11, "bold"),
                    text_color="#1f1f1f",
                    anchor="w",
                    justify="left"
                )
                label.pack(anchor="w", padx=12, pady=10)
        
        # Bottom spacer
        ctk.CTkFrame(section, fg_color=bg_color, height=5).pack(fill="x")
    
    def get_profit_chart_data(self):
        """Get top 5 profitable products (optimized)"""
        if 'profit_data' in self.analytics_cache:
            return self.analytics_cache['profit_data']
        
        sales = get_all_sales()
        profit_by_product = defaultdict(float)
        
        for sale in sales:
            product_name = sale[0]
            profit_loss = sale[4]
            profit_by_product[product_name] += profit_loss
        
        sorted_products = sorted(profit_by_product.items(), key=lambda x: x[1], reverse=True)[:5]
        
        result = [(name, profit) for name, profit in sorted_products]
        self.analytics_cache['profit_data'] = result
        return result
    
    def get_sales_chart_data(self):
        """Get top 5 best selling products (optimized)"""
        if 'sales_data' in self.analytics_cache:
            return self.analytics_cache['sales_data']
        
        sales = get_all_sales()
        qty_by_product = defaultdict(int)
        
        for sale in sales:
            product_name = sale[0]
            qty_sold = sale[1]
            qty_by_product[product_name] += qty_sold
        
        sorted_products = sorted(qty_by_product.items(), key=lambda x: x[1], reverse=True)[:5]
        
        result = [(name, qty) for name, qty in sorted_products]
        self.analytics_cache['sales_data'] = result
        return result
    
    def get_low_selling_products(self):
        """Get low-selling products (optimized)"""
        if 'low_sellers' in self.analytics_cache:
            return self.analytics_cache['low_sellers']
        
        sales = get_all_sales()
        qty_by_product = defaultdict(int)
        
        for sale in sales:
            product_name = sale[0]
            qty_sold = sale[1]
            qty_by_product[product_name] += qty_sold
        
        all_products = get_all_products()
        low_sellers = []
        
        for product in all_products:
            product_name = product[1]
            if product_name not in qty_by_product or qty_by_product[product_name] < 3:
                sold_qty = qty_by_product.get(product_name, 0)
                low_sellers.append((product_name, sold_qty))
        
        low_sellers.sort(key=lambda x: x[1])
        
        result = []
        for name, qty in low_sellers[:5]:
            result.append(f"📦 {name} — {qty} units sold (Consider removing or discounting)")
        
        self.analytics_cache['low_sellers'] = result
        return result
    
    def get_low_stock_alert(self):
        """Get low stock products (optimized)"""
        if 'low_stock' in self.analytics_cache:
            return self.analytics_cache['low_stock']
        
        low_stock = get_low_stock_products()
        result = []
        
        for product_name, qty in low_stock:
            if qty <= 2:
                emoji = "🔴"
                status = "Critical"
            elif qty <= 5:
                emoji = "🟡"
                status = "Low"
            else:
                emoji = "🟢"
                status = "Okay"
            
            result.append(f"{emoji} {product_name} — {qty} items remaining ({status})")
        
        self.analytics_cache['low_stock'] = result
        return result
    
    def get_quick_stats(self):
        """Get quick statistics and recommendations"""
        if 'quick_stats' in self.analytics_cache:
            return self.analytics_cache['quick_stats']
        
        sales = get_all_sales()
        products = get_all_products()
        
        result = []
        
        # Total sales
        total_sales = sum(sale[1] for sale in sales)
        result.append(f"✅ Total Units Sold: {total_sales} units")
        
        # Average profit per sale
        if sales:
            avg_profit = sum(sale[4] for sale in sales) / len(sales)
            result.append(f"✅ Average Profit per Sale: ₨{avg_profit:.2f}")
        
        # Total products
        result.append(f"✅ Active Products: {len(products)} items")
        
        # Most recent sale
        if sales:
            result.append(f"✅ Last Sale: {datetime.now().strftime('%d-%m-%Y')}")
        
        self.analytics_cache['quick_stats'] = result
        return result
    
    def load_analytics(self):
        """Load analytics data and clear cache"""
        self.analytics_cache.clear()  # Clear cache for fresh data
        self.winfo_toplevel().after(100, lambda: None)  # Trigger UI refresh