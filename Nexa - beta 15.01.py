# nexa_browser_complete_fixed.py
import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, QSettings, QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPalette, QColor, QAction, QKeySequence, QPainter, QLinearGradient
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QToolBar, QLineEdit, QPushButton, QTabWidget, QLabel, 
                            QToolButton, QMenu, QDialog, QDialogButtonBox, QFormLayout, 
                            QComboBox, QCheckBox, QSpinBox, QStackedWidget, QFrame,
                            QProgressBar, QMessageBox, QStyleFactory, QScrollArea, QSizePolicy,
                            QListWidget, QListWidgetItem, QSlider, QColorDialog, QGroupBox,
                            QCalendarWidget, QSplitter, QTextEdit, QRadioButton, QButtonGroup)

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage

class Translation:
    def __init__(self):
        self.current_language = "en"
        self.translations = {
            "en": {
                "app_name": "Nexa Browser",
                "new_tab": "New Tab",
                "new_window": "New Window",
                "private_browsing": "Private Browsing",
                "save_page": "Save Page As...",
                "print": "Print...",
                "cut": "Cut",
                "copy": "Copy",
                "paste": "Paste",
                "zoom_in": "Zoom In",
                "zoom_out": "Zoom Out",
                "actual_size": "Actual Size",
                "toolbars": "Toolbars",
                "navigation_bar": "Navigation Bar",
                "bookmarks_bar": "Bookmarks Bar",
                "browser_settings": "Browser Settings",
                "homepage_customization": "Homepage Customization",
                "appearance_settings": "Appearance Settings",
                "about": "About Nexa Browser",
                "help_support": "Help & Support",
                "file": "File",
                "edit": "Edit",
                "view": "View",
                "settings": "Settings",
                "help": "Help",
                "search_placeholder": "Search the web or enter address...",
                "search": "Search",
                "home": "Home",
                "welcome": "Welcome to Nexa Browser",
                "modern_fast_private": "Modern, Fast, and Private",
                "quick_links": "Quick Links",
                "calendar": "Calendar",
                "customize": "Customize",
                "add_widgets": "Add Widgets to Homepage",
                "available_widgets": "Available Widgets",
                "add_selected": "Add Selected",
                "cancel": "Cancel",
                "page_layout": "Page Layout",
                "minimal": "Minimal (Search box only)",
                "dashboard": "Dashboard (Multiple widgets)",
                "custom_layout": "Custom (Drag and drop)",
                "widget_management": "Widget Management",
                "add_new_widget": "Add New Widget",
                "remove_selected": "Remove Selected",
                "background": "Background",
                "choose_color": "Choose Color",
                "use_bg_image": "Use background image",
                "apply_changes": "Apply Changes",
                "changes_applied": "Changes Applied",
                "homepage_customized": "Homepage customization has been applied successfully.",
                "settings_saved": "Settings Saved",
                "settings_saved_msg": "Your settings have been saved successfully.",
                "reset_settings": "Reset to Default",
                "clear_now": "Clear Now",
                "general": "General",
                "appearance": "Appearance",
                "privacy": "Privacy",
                "advanced": "Advanced",
                "startup": "Startup",
                "on_startup": "On startup:",
                "open_homepage": "Open homepage",
                "continue_previous": "Continue where I left off",
                "open_specific": "Open specific pages",
                "homepage": "Homepage:",
                "search_engine": "Default search engine:",
                "instant_search": "Enable instant search",
                "theme": "Theme",
                "color_theme": "Color theme:",
                "dark": "Dark",
                "light": "Light",
                "auto": "Auto",
                "acrylic_effect": "Enable acrylic blur effect",
                "fonts": "Fonts",
                "font_family": "Font family:",
                "font_size": "Font size:",
                "privacy_security": "Privacy & Security",
                "accept_cookies": "Accept cookies",
                "block_tracking": "Block tracking cookies",
                "block_ads": "Block ads",
                "webrtc_leak": "Prevent WebRTC IP leak",
                "clear_browsing_data": "Clear Browsing Data",
                "browsing_history": "Browsing history",
                "cookies_data": "Cookies and site data",
                "cached_files": "Cached images and files",
                "performance": "Performance",
                "hardware_accel": "Use hardware acceleration",
                "preload_pages": "Preload pages for faster browsing",
                "developer_tools": "Developer Tools",
                "enable_dev_tools": "Enable developer tools",
                "js_console": "Show JavaScript console",
                "reset_confirm": "Reset Settings",
                "reset_confirm_msg": "Are you sure you want to reset all settings to default?",
                "reset_complete": "Settings Reset",
                "reset_complete_msg": "All settings have been reset to default.",
                "clear_data_confirm": "Clear Data",
                "clear_data_confirm_msg": "Are you sure you want to clear the selected browsing data?",
                "data_cleared": "Data Cleared",
                "data_cleared_msg": "Selected browsing data has been cleared.",
                "first_run_welcome": "Welcome to Nexa Browser Setup",
                "choose_language": "Choose Language",
                "theme_selection": "Choose Your Theme",
                "dark_mode": "Dark Mode",
                "light_mode": "Light Mode",
                "search_ai_settings": "Search & AI Settings",
                "homepage_customization_setup": "Homepage Customization",
                "show_calendar": "Show Calendar Widget",
                "show_quick_links": "Show Quick Links",
                "enable_ai": "Enable AI Assistant",
                "show_ai_sidebar": "Show AI Sidebar by default",
                "next": "Next",
                "back": "Back",
                "finish": "Finish",
                "ai_assistant": "AI Assistant",
                "ask_anything": "Ask me anything...",
                "send": "Send",
                "loading": "Loading...",
                "error": "Error",
                "success": "Success"
            },
            "fa": {
                "app_name": "مرورگر نکسا",
                "new_tab": "تب جدید",
                "new_window": "پنجره جدید",
                "private_browsing": "مرور ناشناس",
                "save_page": "ذخیره صفحه به عنوان...",
                "print": "چاپ...",
                "cut": "برش",
                "copy": "کپی",
                "paste": "چسباندن",
                "zoom_in": "بزرگنمایی",
                "zoom_out": "کوچکنمایی",
                "actual_size": "اندازه واقعی",
                "toolbars": "نوار ابزارها",
                "navigation_bar": "نوار ناوبری",
                "bookmarks_bar": "نوار نشانک‌ها",
                "browser_settings": "تنظیمات مرورگر",
                "homepage_customization": "سفارشی‌سازی صفحه اصلی",
                "appearance_settings": "تنظیمات ظاهر",
                "about": "درباره مرورگر نکسا",
                "help_support": "راهنما و پشتیبانی",
                "file": "فایل",
                "edit": "ویرایش",
                "view": "نمایش",
                "settings": "تنظیمات",
                "help": "راهنما",
                "search_placeholder": "جستجو در وب یا وارد کردن آدرس...",
                "search": "جستجو",
                "home": "خانه",
                "welcome": "به مرورگر نکسا خوش آمدید",
                "modern_fast_private": "مدرن، سریع و خصوصی",
                "quick_links": "لینک‌های سریع",
                "calendar": "تقویم",
                "customize": "سفارشی‌سازی",
                "add_widgets": "افزودن ویجت به صفحه اصلی",
                "available_widgets": "ویجت‌های موجود",
                "add_selected": "افزودن انتخاب شده",
                "cancel": "لغو",
                "page_layout": "طرح صفحه",
                "minimal": "مینیمال (فقط جعبه جستجو)",
                "dashboard": "داشبورد (چندین ویجت)",
                "custom_layout": "سفارشی (کشیدن و رها کردن)",
                "widget_management": "مدیریت ویجت‌ها",
                "add_new_widget": "افزودن ویجت جدید",
                "remove_selected": "حذف انتخاب شده",
                "background": "پس‌زمینه",
                "choose_color": "انتخاب رنگ",
                "use_bg_image": "استفاده از تصویر پس‌زمینه",
                "apply_changes": "اعمال تغییرات",
                "changes_applied": "تغییرات اعمال شد",
                "homepage_customized": "سفارشی‌سازی صفحه اصلی با موفقیت اعمال شد.",
                "settings_saved": "تنظیمات ذخیره شد",
                "settings_saved_msg": "تنظیمات شما با موفقیت ذخیره شد.",
                "reset_settings": "بازنشانی به پیش‌فرض",
                "clear_now": "پاک‌سازی اکنون",
                "general": "عمومی",
                "appearance": "ظاهر",
                "privacy": "حریم خصوصی",
                "advanced": "پیشرفته",
                "startup": "راه‌اندازی",
                "on_startup": "در هنگام راه‌اندازی:",
                "open_homepage": "باز کردن صفحه اصلی",
                "continue_previous": "ادامه از جایی که متوقف کردم",
                "open_specific": "باز کردن صفحات خاص",
                "homepage": "صفحه اصلی:",
                "search_engine": "موتور جستجوی پیش‌فرض:",
                "instant_search": "فعال کردن جستجوی فوری",
                "theme": "تم",
                "color_theme": "تم رنگی:",
                "dark": "تیره",
                "light": "روشن",
                "auto": "خودکار",
                "acrylic_effect": "فعال کردن اثر آکریلیک",
                "fonts": "فونت‌ها",
                "font_family": "خانواده فونت:",
                "font_size": "اندازه فونت:",
                "privacy_security": "حریم خصوصی و امنیت",
                "accept_cookies": "پذیرش کوکی‌ها",
                "block_tracking": "مسدود کردن کوکی‌های ردیابی",
                "block_ads": "مسدود کردن تبلیغات",
                "webrtc_leak": "جلوگیری از نشت IP در WebRTC",
                "clear_browsing_data": "پاک‌سازی اطلاعات مرور",
                "browsing_history": "تاریخچه مرور",
                "cookies_data": "کوکی‌ها و اطلاعات سایت",
                "cached_files": "تصاویر و فایل‌های کش شده",
                "performance": "عملکرد",
                "hardware_accel": "استفاده از شتاب‌دهنده سخت‌افزاری",
                "preload_pages": "پیش‌بارگذاری صفحات برای مرور سریع‌تر",
                "developer_tools": "ابزارهای توسعه‌دهنده",
                "enable_dev_tools": "فعال کردن ابزارهای توسعه‌دهنده",
                "js_console": "نمایش کنسول JavaScript",
                "reset_confirm": "بازنشانی تنظیمات",
                "reset_confirm_msg": "آیا مطمئن هستید که می‌خواهید همه تنظیمات را به حالت پیش‌فرض بازنشانی کنید؟",
                "reset_complete": "تنظیمات بازنشانی شد",
                "reset_complete_msg": "همه تنظیمات به حالت پیش‌فرض بازنشانی شد.",
                "clear_data_confirm": "پاک‌سازی اطلاعات",
                "clear_data_confirm_msg": "آیا مطمئن هستید که می‌خواهید اطلاعات مرور انتخاب شده را پاک‌سازی کنید؟",
                "data_cleared": "اطلاعات پاک‌سازی شد",
                "data_cleared_msg": "اطلاعات مرور انتخاب شده پاک‌سازی شد.",
                "first_run_welcome": "به راه‌اندازی مرورگر نکسا خوش آمدید",
                "choose_language": "انتخاب زبان",
                "theme_selection": "تم خود را انتخاب کنید",
                "dark_mode": "حالت تیره",
                "light_mode": "حالت روشن",
                "search_ai_settings": "تنظیمات جستجو و هوش مصنوعی",
                "homepage_customization_setup": "سفارشی‌سازی صفحه اصلی",
                "show_calendar": "نمایش ویجت تقویم",
                "show_quick_links": "نمایش لینک‌های سریع",
                "enable_ai": "فعال کردن دستیار هوش مصنوعی",
                "show_ai_sidebar": "نمایش نوار کناری هوش مصنوعی به طور پیش‌فرض",
                "next": "بعدی",
                "back": "قبلی",
                "finish": "پایان",
                "ai_assistant": "دستیار هوش مصنوعی",
                "ask_anything": "هر چیزی بپرسید...",
                "send": "ارسال",
                "loading": "در حال بارگذاری...",
                "error": "خطا",
                "success": "موفقیت"
            }
        }
    
    def set_language(self, language):
        if language in self.translations:
            self.current_language = language
    
    def get(self, key):
        return self.translations[self.current_language].get(key, key)
    
    def tr(self, key):
        return self.get(key)

# Create global translation instance
trans = Translation()

class FirstRunWizard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(trans.tr("first_run_welcome"))
        self.setFixedSize(700, 600)
        self.setModal(True)
        self.apply_dark_theme()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel(trans.tr("first_run_welcome"))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setWeight(QFont.Weight.Bold)
        header.setFont(header_font)
        header.setStyleSheet("color: white; margin: 20px;")
        layout.addWidget(header)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Page 0: Language Selection
        page0 = self.create_language_page()
        self.stacked_widget.addWidget(page0)
        
        # Page 1: Theme Selection
        page1 = self.create_theme_page()
        self.stacked_widget.addWidget(page1)
        
        # Page 2: Search & AI Settings
        page2 = self.create_search_ai_page()
        self.stacked_widget.addWidget(page2)
        
        # Page 3: Homepage Customization
        page3 = self.create_homepage_page()
        self.stacked_widget.addWidget(page3)
        
        layout.addWidget(self.stacked_widget)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.back_btn = ModernButton(trans.tr("back"))
        self.back_btn.clicked.connect(self.previous_page)
        self.next_btn = ModernButton(trans.tr("next"))
        self.next_btn.clicked.connect(self.next_page)
        self.finish_btn = ModernButton(trans.tr("finish"))
        self.finish_btn.clicked.connect(self.accept)
        self.finish_btn.hide()
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.finish_btn)
        
        layout.addLayout(nav_layout)
        
        self.setLayout(layout)
        
        self.current_page = 0
        self.update_navigation()
    
    def create_language_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(trans.tr("choose_language"))
        title_font = QFont()
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Language selection
        lang_layout = QVBoxLayout()
        
        self.english_radio = QRadioButton("English")
        self.english_radio.setChecked(True)
        self.english_radio.toggled.connect(lambda: self.on_language_changed("en"))
        self.english_radio.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        lang_layout.addWidget(self.english_radio)
        
        self.persian_radio = QRadioButton("فارسی (Persian)")
        self.persian_radio.toggled.connect(lambda: self.on_language_changed("fa"))
        self.persian_radio.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        lang_layout.addWidget(self.persian_radio)
        
        layout.addLayout(lang_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_theme_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(trans.tr("theme_selection"))
        title_font = QFont()
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Theme selection
        theme_layout = QHBoxLayout()
        
        dark_theme = RoundedFrame()
        dark_layout = QVBoxLayout(dark_theme)
        dark_preview = QLabel(trans.tr("dark_mode"))
        dark_preview.setStyleSheet("""
            background-color: #1e1e1e; 
            color: white; 
            padding: 40px; 
            border-radius: 8px;
            font-weight: bold;
        """)
        dark_layout.addWidget(dark_preview)
        self.dark_radio = QRadioButton(trans.tr("dark_mode"))
        self.dark_radio.setChecked(True)
        self.dark_radio.setStyleSheet("color: white;")
        dark_layout.addWidget(self.dark_radio)
        theme_layout.addWidget(dark_theme)
        
        light_theme = RoundedFrame()
        light_layout = QVBoxLayout(light_theme)
        light_preview = QLabel(trans.tr("light_mode"))
        light_preview.setStyleSheet("""
            background-color: #f5f5f5; 
            color: #333; 
            padding: 40px; 
            border-radius: 8px;
            font-weight: bold;
        """)
        light_layout.addWidget(light_preview)
        self.light_radio = QRadioButton(trans.tr("light_mode"))
        self.light_radio.setStyleSheet("color: white;")
        light_layout.addWidget(self.light_radio)
        theme_layout.addWidget(light_theme)
        
        layout.addLayout(theme_layout)
        
        # Font settings
        font_layout = QFormLayout()
        font_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Verdana"])
        self.font_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 6px;
                color: white;
            }
        """)
        font_layout.addRow("Font Family:", self.font_combo)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 24)
        self.font_size.setValue(12)
        self.font_size.setStyleSheet("""
            QSpinBox {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 6px;
                color: white;
            }
        """)
        font_layout.addRow("Font Size:", self.font_size)
        
        layout.addLayout(font_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_search_ai_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(trans.tr("search_ai_settings"))
        title_font = QFont()
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Search engine
        search_layout = QFormLayout()
        self.search_engine = QComboBox()
        self.search_engine.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo", "Custom"])
        self.search_engine.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 6px;
                color: white;
            }
        """)
        search_layout.addRow(trans.tr("search_engine"), self.search_engine)
        layout.addLayout(search_layout)
        
        # AI Assistant
        ai_frame = RoundedFrame()
        ai_layout = QVBoxLayout(ai_frame)
        
        ai_title = QLabel(trans.tr("ai_assistant"))
        ai_title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        ai_layout.addWidget(ai_title)
        
        self.ai_enabled = QCheckBox(trans.tr("enable_ai"))
        self.ai_enabled.setChecked(True)
        self.ai_enabled.setStyleSheet("color: white;")
        ai_layout.addWidget(self.ai_enabled)
        
        self.ai_sidebar = QCheckBox(trans.tr("show_ai_sidebar"))
        self.ai_sidebar.setChecked(True)
        self.ai_sidebar.setStyleSheet("color: white;")
        ai_layout.addWidget(self.ai_sidebar)
        
        layout.addWidget(ai_frame)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_homepage_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(trans.tr("homepage_customization_setup"))
        title_font = QFont()
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Homepage layout options
        layout_options = QVBoxLayout()
        
        self.show_calendar = QCheckBox(trans.tr("show_calendar"))
        self.show_calendar.setChecked(True)
        self.show_calendar.setStyleSheet("color: white;")
        layout_options.addWidget(self.show_calendar)
        
        self.show_quick_links = QCheckBox(trans.tr("show_quick_links"))
        self.show_quick_links.setChecked(True)
        self.show_quick_links.setStyleSheet("color: white;")
        layout_options.addWidget(self.show_quick_links)
        
        layout.addLayout(layout_options)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def on_language_changed(self, language):
        trans.set_language(language)
        # Update UI texts dynamically
        self.back_btn.setText(trans.tr("back"))
        self.next_btn.setText(trans.tr("next"))
        self.finish_btn.setText(trans.tr("finish"))
        self.setWindowTitle(trans.tr("first_run_welcome"))
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: white;
            }
            QRadioButton {
                color: white;
            }
            QCheckBox {
                color: white;
            }
        """)
    
    def next_page(self):
        if self.current_page < self.stacked_widget.count() - 1:
            self.current_page += 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.update_navigation()
    
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.update_navigation()
    
    def update_navigation(self):
        self.back_btn.setVisible(self.current_page > 0)
        
        if self.current_page == self.stacked_widget.count() - 1:
            self.next_btn.hide()
            self.finish_btn.show()
        else:
            self.next_btn.show()
            self.finish_btn.hide()
    
    def get_settings(self):
        return {
            "language": "fa" if self.persian_radio.isChecked() else "en",
            "theme": "dark" if self.dark_radio.isChecked() else "light",
            "font_family": self.font_combo.currentText(),
            "font_size": self.font_size.value(),
            "search_engine": self.search_engine.currentText(),
            "ai_enabled": self.ai_enabled.isChecked(),
            "ai_sidebar": self.ai_sidebar.isChecked(),
            "show_calendar": self.show_calendar.isChecked(),
            "show_quick_links": self.show_quick_links.isChecked()
        }

class ModernButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(32)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 6px 12px;
                color: white;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.5);
            }
        """)

class RoundedFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background-color: rgba(30, 30, 30, 0.7); border-radius: 10px;")

class HamburgerMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
            }
            QMenu::item:selected {
                background-color: #0078d4;
            }
            QMenu::separator {
                height: 1px;
                background-color: #444;
                margin: 4px 0px;
            }
        """)
        self.setup_menu()
    
    def setup_menu(self):
        # File section
        file_menu = self.addMenu("📁 " + trans.tr("file"))
        
        new_tab_action = QAction(trans.tr("new_tab"), self)
        new_tab_action.triggered.connect(lambda: self.parent().add_new_tab())
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction(trans.tr("new_window"), self)
        new_window_action.triggered.connect(lambda: self.parent().new_window())
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        file_menu.addAction(new_window_action)
        
        private_action = QAction(trans.tr("private_browsing"), self)
        private_action.triggered.connect(lambda: self.parent().private_browsing())
        private_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        file_menu.addAction(private_action)
        
        file_menu.addSeparator()
        
        save_action = QAction(trans.tr("save_page"), self)
        save_action.triggered.connect(lambda: self.parent().save_page())
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        file_menu.addAction(save_action)
        
        print_action = QAction(trans.tr("print"), self)
        print_action.triggered.connect(lambda: self.parent().print_page())
        print_action.setShortcut(QKeySequence("Ctrl+P"))
        file_menu.addAction(print_action)
        
        # Edit section
        edit_menu = self.addMenu("✏️ " + trans.tr("edit"))
        
        cut_action = QAction(trans.tr("cut"), self)
        cut_action.triggered.connect(lambda: self.parent().cut())
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        edit_menu.addAction(cut_action)
        
        copy_action = QAction(trans.tr("copy"), self)
        copy_action.triggered.connect(lambda: self.parent().copy())
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        edit_menu.addAction(copy_action)
        
        paste_action = QAction(trans.tr("paste"), self)
        paste_action.triggered.connect(lambda: self.parent().paste())
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        edit_menu.addAction(paste_action)
        
        # View section
        view_menu = self.addMenu("👁️ " + trans.tr("view"))
        
        zoom_in_action = QAction(trans.tr("zoom_in"), self)
        zoom_in_action.triggered.connect(lambda: self.parent().zoom_in())
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction(trans.tr("zoom_out"), self)
        zoom_out_action.triggered.connect(lambda: self.parent().zoom_out())
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        view_menu.addAction(zoom_out_action)
        
        actual_size_action = QAction(trans.tr("actual_size"), self)
        actual_size_action.triggered.connect(lambda: self.parent().actual_size())
        actual_size_action.setShortcut(QKeySequence("Ctrl+0"))
        view_menu.addAction(actual_size_action)
        
        view_menu.addSeparator()
        
        # Toolbars submenu
        toolbars_menu = view_menu.addMenu(trans.tr("toolbars"))
        self.nav_action = QAction(trans.tr("navigation_bar"), self)
        self.nav_action.setCheckable(True)
        self.nav_action.setChecked(True)
        self.nav_action.toggled.connect(self.toggle_navigation_bar)
        toolbars_menu.addAction(self.nav_action)
        
        self.bookmarks_action = QAction(trans.tr("bookmarks_bar"), self)
        self.bookmarks_action.setCheckable(True)
        self.bookmarks_action.setChecked(False)
        toolbars_menu.addAction(self.bookmarks_action)
        
        # Settings section
        settings_menu = self.addMenu("⚙️ " + trans.tr("settings"))
        
        browser_settings_action = QAction(trans.tr("browser_settings"), self)
        browser_settings_action.triggered.connect(lambda: self.parent().show_settings_dialog())
        settings_menu.addAction(browser_settings_action)
        
        homepage_action = QAction(trans.tr("homepage_customization"), self)
        homepage_action.triggered.connect(lambda: self.parent().show_homepage_customization())
        settings_menu.addAction(homepage_action)
        
        appearance_action = QAction(trans.tr("appearance_settings"), self)
        appearance_action.triggered.connect(lambda: self.parent().show_appearance_settings())
        settings_menu.addAction(appearance_action)
        
        # Help section
        help_menu = self.addMenu("❓ " + trans.tr("help"))
        
        about_action = QAction(trans.tr("about"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        help_action = QAction(trans.tr("help_support"), self)
        help_action.triggered.connect(lambda: self.parent().show_help())
        help_menu.addAction(help_action)
    
    def toggle_navigation_bar(self, visible):
        self.parent().toolbar.setVisible(visible)
    
    def show_about(self):
        QMessageBox.about(self.parent(), trans.tr("about"), 
                         f"{trans.tr('app_name')} v3.0\n\n{trans.tr('modern_fast_private')}")

class BrowserTab(QWebEngineView):
    def __init__(self, browser_instance, parent=None):
        super().__init__(parent)
        self.browser = browser_instance  # Store reference to browser instance
        self.loadFinished.connect(self.on_load_finished)
        self.loadProgress.connect(self.on_load_progress)
        
        # Enable developer tools
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        
    def on_load_finished(self, success):
        if success:
            print(f"Page loaded: {self.url().toString()}")
    
    def on_load_progress(self, progress):
        # Fix: Use the stored browser reference instead of parent()
        self.browser.update_progress(progress)

class NexaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("NexaBrowser", "Nexa")
        
        # Check first run
        if not self.settings.value("first_run_complete", False, type=bool):
            self.show_first_run_wizard()
        
        # Apply settings
        self.apply_settings()
        
        # Initialize UI
        self.init_ui()
        
        # Load homepage
        self.load_homepage()
    
    def show_first_run_wizard(self):
        wizard = FirstRunWizard(self)
        if wizard.exec() == QDialog.DialogCode.Accepted:
            settings = wizard.get_settings()
            # Save settings
            for key, value in settings.items():
                self.settings.setValue(key, value)
            self.settings.setValue("first_run_complete", True)
            # Apply language immediately
            trans.set_language(settings["language"])
    
    def apply_settings(self):
        # Apply language
        language = self.settings.value("language", "en")
        trans.set_language(language)
        
        # Apply theme
        theme = self.settings.value("theme", "dark")
        self.apply_theme(theme)
        
        self.setWindowTitle(trans.tr("app_name"))
        self.setGeometry(100, 100, 1200, 800)
    
    def apply_theme(self, theme="dark"):
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QToolBar {
                    background-color: #2d2d2d;
                    border: none;
                    padding: 5px;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #1e1e1e;
                }
                QTabBar::tab {
                    background-color: #2d2d2d;
                    color: white;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                }
                QTabBar::tab:selected {
                    background-color: #1e1e1e;
                    border-bottom: 2px solid #0078d4;
                }
                QTabBar::tab:hover {
                    background-color: #3d3d3d;
                }
                QGroupBox {
                    color: white;
                    border: 1px solid #444;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                }
                QToolBar {
                    background-color: #f0f0f0;
                    border: none;
                    padding: 5px;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #e0e0e0;
                    color: #333333;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                }
                QTabBar::tab:selected {
                    background-color: #ffffff;
                    border-bottom: 2px solid #0078d4;
                }
                QTabBar::tab:hover {
                    background-color: #d0d0d0;
                }
                QGroupBox {
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
            """)
    
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Browser area
        browser_area = QVBoxLayout()
        
        # Toolbar with hamburger menu
        self.setup_toolbar()
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        # New tab button
        new_tab_btn = QToolButton()
        new_tab_btn.setText("+")
        new_tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_tab_btn.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(new_tab_btn)
        
        browser_area.addWidget(self.tab_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
            }
        """)
        browser_area.addWidget(self.progress_bar)
        
        main_layout.addLayout(browser_area)
        
        # Add initial tab
        self.add_new_tab()
    
    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.toolbar)
        
        # Hamburger menu button
        self.menu_btn = QToolButton()
        self.menu_btn.setText("☰")
        self.menu_btn.setStyleSheet("""
            QToolButton {
                color: white;
                background-color: transparent;
                border: none;
                padding: 8px;
                font-size: 16px;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
        """)
        self.menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.hamburger_menu = HamburgerMenu(self)
        self.menu_btn.setMenu(self.hamburger_menu)
        self.menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        self.toolbar.addWidget(self.menu_btn)
        self.toolbar.addSeparator()
        
        # Navigation buttons
        back_btn = QAction("←", self)
        back_btn.triggered.connect(self.go_back)
        self.toolbar.addAction(back_btn)
        
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_btn)
        
        reload_btn = QAction("↻", self)
        reload_btn.triggered.connect(self.reload_page)
        self.toolbar.addAction(reload_btn)
        
        self.toolbar.addSeparator()
        
        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText(trans.tr("search_placeholder"))
        self.address_bar.returnPressed.connect(self.load_url)
        self.address_bar.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 6px 12px;
                color: white;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        self.toolbar.addWidget(self.address_bar)
        
        # Home button
        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.load_homepage)
        self.toolbar.addAction(home_btn)
    
    # Navigation methods
    def add_new_tab(self, url=None):
        # Fix: Pass browser instance to BrowserTab
        tab = BrowserTab(self)
        
        # Connect signals
        tab.urlChanged.connect(lambda u: self.update_url_bar(u, tab))
        tab.loadFinished.connect(self.on_load_finished)
        
        index = self.tab_widget.addTab(tab, trans.tr("new_tab"))
        self.tab_widget.setCurrentIndex(index)
        
        if url:
            tab.load(QUrl(url))
        else:
            self.load_homepage()
        
        return tab
    
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.widget(index).deleteLater()
            self.tab_widget.removeTab(index)
    
    def tab_changed(self, index):
        if index >= 0:
            current_tab = self.tab_widget.widget(index)
            self.update_url_bar(current_tab.url(), current_tab)
    
    def update_url_bar(self, url, tab):
        if tab == self.tab_widget.currentWidget():
            self.address_bar.setText(url.toString())
            
            # Update tab title
            title = tab.page().title()
            if title:
                index = self.tab_widget.indexOf(tab)
                self.tab_widget.setTabText(index, title[:15] + "..." if len(title) > 15 else title)
    
    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            QTimer.singleShot(500, lambda: self.progress_bar.setValue(0))
    
    def on_load_finished(self, success):
        if success:
            print("Page loaded successfully")
    
    def load_url(self, url=None):
        if not url:
            url = self.address_bar.text()
        
        # If no protocol specified, assume it's a search query
        if not url.startswith(('http://', 'https://', 'file://')):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                url = f'https://www.google.com/search?q={url.replace(" ", "+")}'
        
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.load(QUrl(url))
    
    def load_homepage(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            # For now, load a simple homepage
            current_tab.setHtml(self.get_homepage_html())
    
    def get_homepage_html(self):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    background-color: #1e1e1e;
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }}
                .title {{
                    font-size: 2.5em;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .subtitle {{
                    color: #aaa;
                    margin-bottom: 30px;
                }}
                .search-box {{
                    width: 600px;
                    padding: 12px 20px;
                    border-radius: 24px;
                    border: 2px solid #444;
                    background-color: #2d2d2d;
                    color: white;
                    font-size: 16px;
                    outline: none;
                }}
                .search-box:focus {{
                    border-color: #0078d4;
                }}
                .quick-links {{
                    margin-top: 30px;
                    display: flex;
                    gap: 15px;
                }}
                .link {{
                    padding: 10px 20px;
                    background-color: #2d2d2d;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }}
                .link:hover {{
                    background-color: #3d3d3d;
                }}
            </style>
        </head>
        <body>
            <div class="title">{trans.tr('app_name')}</div>
            <div class="subtitle">{trans.tr('modern_fast_private')}</div>
            <input type="text" class="search-box" placeholder="{trans.tr('search_placeholder')}" id="search">
            <div class="quick-links">
                <div class="link" onclick="window.location.href='https://www.google.com'">Google</div>
                <div class="link" onclick="window.location.href='https://www.youtube.com'">YouTube</div>
                <div class="link" onclick="window.location.href='https://mail.google.com'">Gmail</div>
                <div class="link" onclick="window.location.href='https://www.github.com'">GitHub</div>
            </div>
            <script>
                document.getElementById('search').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        let query = this.value;
                        if (!query.startsWith('http')) {{
                            window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query);
                        }} else {{
                            window.location.href = query;
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """
    
    def go_back(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.back()
    
    def go_forward(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.forward()
    
    def reload_page(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.reload()
    
    # Menu action methods
    def new_window(self):
        new_browser = NexaBrowser()
        new_browser.show()
    
    def private_browsing(self):
        QMessageBox.information(self, trans.tr("private_browsing"), "Private browsing mode would open here.")
    
    def save_page(self):
        QMessageBox.information(self, trans.tr("save_page"), "Save page functionality would be implemented here.")
    
    def print_page(self):
        QMessageBox.information(self, trans.tr("print"), "Print functionality would be implemented here.")
    
    def cut(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.page().triggerAction(QWebEnginePage.WebAction.Cut)
    
    def copy(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.page().triggerAction(QWebEnginePage.WebAction.Copy)
    
    def paste(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.page().triggerAction(QWebEnginePage.WebAction.Paste)
    
    def zoom_in(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.setZoomFactor(current_tab.zoomFactor() + 0.1)
    
    def zoom_out(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.setZoomFactor(current_tab.zoomFactor() - 0.1)
    
    def actual_size(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.setZoomFactor(1.0)
    
    def show_settings_dialog(self):
        QMessageBox.information(self, trans.tr("browser_settings"), "Browser settings dialog would open here.")
    
    def show_homepage_customization(self):
        QMessageBox.information(self, trans.tr("homepage_customization"), "Homepage customization dialog would open here.")
    
    def show_appearance_settings(self):
        QMessageBox.information(self, trans.tr("appearance_settings"), "Appearance settings dialog would open here.")
    
    def show_help(self):
        QMessageBox.information(self, trans.tr("help_support"), "Help and support documentation would open here.")

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("3.0")
    
    # Set dark theme by default
    app.setStyle(QStyleFactory.create("Fusion"))
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 212))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 212))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)
    
    browser = NexaBrowser()
    browser.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()