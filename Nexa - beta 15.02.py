# nexa_browser_complete_enhanced.py
import sys
import os
import json
import sqlite3
import tempfile
import webbrowser
from pathlib import Path
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, QSettings, QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPalette, QColor, QAction, QKeySequence, QPainter, QLinearGradient, QDesktopServices, QGuiApplication
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QToolBar, QLineEdit, QPushButton, QTabWidget, QLabel, 
                            QToolButton, QMenu, QDialog, QDialogButtonBox, QFormLayout, 
                            QComboBox, QCheckBox, QSpinBox, QStackedWidget, QFrame,
                            QProgressBar, QMessageBox, QStyleFactory, QScrollArea, QSizePolicy,
                            QListWidget, QListWidgetItem, QSlider, QColorDialog, QGroupBox,
                            QCalendarWidget, QSplitter, QTextEdit, QRadioButton, QButtonGroup,
                            QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QSystemTrayIcon)

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEngineScript
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter

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
                "success": "Success",
                "bookmarks": "Bookmarks",
                "history": "History",
                "downloads": "Downloads",
                "extensions": "Extensions",
                "add_bookmark": "Add Bookmark",
                "bookmark_added": "Bookmark Added",
                "bookmark_removed": "Bookmark Removed",
                "download_started": "Download Started",
                "download_completed": "Download Completed",
                "incognito_mode": "Incognito Mode",
                "fullscreen": "Fullscreen",
                "find_in_page": "Find in Page",
                "view_source": "View Source",
                "inspect_element": "Inspect Element",
                "task_manager": "Task Manager",
                "clear_cache": "Clear Cache",
                "password_manager": "Password Manager",
                "sync_data": "Sync Data",
                "restore_session": "Restore Session",
                "export_data": "Export Data",
                "import_data": "Import Data",
                "check_updates": "Check for Updates",
                "report_issue": "Report Issue",
                "user_guide": "User Guide",
                "keyboard_shortcuts": "Keyboard Shortcuts",
                "feedback": "Feedback",
                "rate_app": "Rate Application",
                "close_tab": "Close Tab",
                "close_window": "Close Window",
                "reopen_closed_tab": "Reopen Closed Tab",
                "pin_tab": "Pin Tab",
                "mute_tab": "Mute Tab",
                "duplicate_tab": "Duplicate Tab",
                "bookmark_all_tabs": "Bookmark All Tabs",
                "add_to_favorites": "Add to Favorites",
                "manage_search_engines": "Manage Search Engines",
                "site_permissions": "Site Permissions",
                "translate_page": "Translate Page",
                "cast_to_device": "Cast to Device",
                "take_screenshot": "Take Screenshot",
                "reader_mode": "Reader Mode",
                "focus_mode": "Focus Mode",
                "picture_in_picture": "Picture in Picture"
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
                "success": "موفقیت",
                "bookmarks": "نشانک‌ها",
                "history": "تاریخچه",
                "downloads": "دانلودها",
                "extensions": "افزونه‌ها",
                "add_bookmark": "افزودن نشانک",
                "bookmark_added": "نشانک افزوده شد",
                "bookmark_removed": "نشانک حذف شد",
                "download_started": "دانلود شروع شد",
                "download_completed": "دانلود کامل شد",
                "incognito_mode": "حالت ناشناس",
                "fullscreen": "تمام صفحه",
                "find_in_page": "جستجو در صفحه",
                "view_source": "مشاهده منبع",
                "inspect_element": "بازرسی عنصر",
                "task_manager": "مدیریت وظایف",
                "clear_cache": "پاک‌سازی کش",
                "password_manager": "مدیریت رمز عبور",
                "sync_data": "همگام‌سازی داده‌ها",
                "restore_session": "بازیابی نشست",
                "export_data": "صدور داده‌ها",
                "import_data": "ورود داده‌ها",
                "check_updates": "بررسی به‌روزرسانی‌ها",
                "report_issue": "گزارش مشکل",
                "user_guide": "راهنمای کاربر",
                "keyboard_shortcuts": "میانبرهای صفحه کلید",
                "feedback": "بازخورد",
                "rate_app": "امتیاز به برنامه",
                "close_tab": "بستن تب",
                "close_window": "بستن پنجره",
                "reopen_closed_tab": "باز کردن تب بسته شده",
                "pin_tab": "سنجاق کردن تب",
                "mute_tab": "بی‌صدا کردن تب",
                "duplicate_tab": "تکثیر تب",
                "bookmark_all_tabs": "نشانک گذاری همه تب‌ها",
                "add_to_favorites": "افزودن به علاقه‌مندی‌ها",
                "manage_search_engines": "مدیریت موتورهای جستجو",
                "site_permissions": "مجوزهای سایت",
                "translate_page": "ترجمه صفحه",
                "cast_to_device": "ارسال به دستگاه",
                "take_screenshot": "گرفتن عکس از صفحه",
                "reader_mode": "حالت مطالعه",
                "focus_mode": "حالت تمرکز",
                "picture_in_picture": "تصویر در تصویر"
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

class DatabaseManager:
    def __init__(self):
        self.db_path = Path.home() / ".nexabrowser" / "browser_data.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create bookmarks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                visit_count INTEGER DEFAULT 1,
                last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create downloads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                url TEXT NOT NULL,
                path TEXT NOT NULL,
                size INTEGER,
                progress INTEGER DEFAULT 0,
                status TEXT DEFAULT 'downloading',
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_bookmark(self, title, url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookmarks (title, url) VALUES (?, ?)', (title, url))
        conn.commit()
        conn.close()
    
    def get_bookmarks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bookmarks ORDER BY date_added DESC')
        bookmarks = cursor.fetchall()
        conn.close()
        return bookmarks
    
    def delete_bookmark(self, bookmark_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
        conn.commit()
        conn.close()
    
    def add_history(self, title, url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if URL already exists
        cursor.execute('SELECT id, visit_count FROM history WHERE url = ?', (url,))
        result = cursor.fetchone()
        
        if result:
            # Update existing entry
            cursor.execute('UPDATE history SET title = ?, visit_count = ?, last_visit = CURRENT_TIMESTAMP WHERE id = ?',
                         (title, result[1] + 1, result[0]))
        else:
            # Insert new entry
            cursor.execute('INSERT INTO history (title, url) VALUES (?, ?)', (title, url))
        
        conn.commit()
        conn.close()
    
    def get_history(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM history ORDER BY last_visit DESC LIMIT ?', (limit,))
        history = cursor.fetchall()
        conn.close()
        return history
    
    def clear_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history')
        conn.commit()
        conn.close()

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

class BrowserTab(QWebEngineView):
    def __init__(self, browser_instance, parent=None):
        super().__init__(parent)
        self.browser = browser_instance
        self.loadFinished.connect(self.on_load_finished)
        self.loadProgress.connect(self.on_load_progress)
        self.urlChanged.connect(self.on_url_changed)
        self.titleChanged.connect(self.on_title_changed)
        
        # Enable developer tools and other settings
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.WebAttribute.AutoLoadImages, True)
        
        # Set up profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    def on_load_finished(self, success):
        if success:
            print(f"Page loaded: {self.url().toString()}")
    
    def on_load_progress(self, progress):
        self.browser.update_progress(progress)
    
    def on_url_changed(self, url):
        self.browser.update_url_bar(url, self)
    
    def on_title_changed(self, title):
        self.browser.update_tab_title(title, self)

class BookmarksManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.setWindowTitle(trans.tr("bookmarks"))
        self.setGeometry(200, 200, 600, 400)
        self.setup_ui()
        self.load_bookmarks()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.add_btn = ModernButton(trans.tr("add_bookmark"))
        self.add_btn.clicked.connect(self.add_bookmark)
        self.delete_btn = ModernButton(trans.tr("delete"))
        self.delete_btn.clicked.connect(self.delete_bookmark)
        
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Bookmarks list
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(self.bookmarks_list)
        
        self.setLayout(layout)
    
    def load_bookmarks(self):
        self.bookmarks_list.clear()
        bookmarks = self.db.get_bookmarks()
        for bookmark in bookmarks:
            item = QListWidgetItem(f"{bookmark[1]} - {bookmark[2]}")
            item.setData(Qt.ItemDataRole.UserRole, bookmark[0])  # Store ID
            self.bookmarks_list.addItem(item)
    
    def add_bookmark(self):
        current_tab = self.parent().tab_widget.currentWidget()
        if current_tab:
            title = current_tab.page().title()
            url = current_tab.url().toString()
            if title and url:
                self.db.add_bookmark(title, url)
                self.load_bookmarks()
                QMessageBox.information(self, trans.tr("success"), trans.tr("bookmark_added"))
    
    def delete_bookmark(self):
        current_item = self.bookmarks_list.currentItem()
        if current_item:
            bookmark_id = current_item.data(Qt.ItemDataRole.UserRole)
            self.db.delete_bookmark(bookmark_id)
            self.load_bookmarks()
    
    def open_bookmark(self, item):
        url = item.text().split(" - ")[1]
        self.parent().load_url(url)
        self.close()

class HistoryManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.setWindowTitle(trans.tr("history"))
        self.setGeometry(200, 200, 800, 500)
        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.clear_btn = ModernButton(trans.tr("clear_now"))
        self.clear_btn.clicked.connect(self.clear_history)
        toolbar.addWidget(self.clear_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Title", "URL", "Last Visit"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.doubleClicked.connect(self.open_history_item)
        
        layout.addWidget(self.history_table)
        
        self.setLayout(layout)
    
    def load_history(self):
        self.history_table.setRowCount(0)
        history = self.db.get_history()
        for row, item in enumerate(history):
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(item[1]))  # Title
            self.history_table.setItem(row, 1, QTableWidgetItem(item[2]))  # URL
            self.history_table.setItem(row, 2, QTableWidgetItem(item[4]))  # Last visit
            self.history_table.setRowHeight(row, 30)
    
    def clear_history(self):
        self.db.clear_history()
        self.load_history()
    
    def open_history_item(self, index):
        url = self.history_table.item(index.row(), 1).text()
        self.parent().load_url(url)
        self.close()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(trans.tr("browser_settings"))
        self.setGeometry(100, 100, 700, 500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Tab widget for different settings categories
        self.tab_widget = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        self.tab_widget.addTab(general_tab, trans.tr("general"))
        
        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        self.tab_widget.addTab(appearance_tab, trans.tr("appearance"))
        
        # Privacy tab
        privacy_tab = self.create_privacy_tab()
        self.tab_widget.addTab(privacy_tab, trans.tr("privacy"))
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        self.tab_widget.addTab(advanced_tab, trans.tr("advanced"))
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = ModernButton(trans.tr("apply_changes"))
        self.save_btn.clicked.connect(self.save_settings)
        self.reset_btn = ModernButton(trans.tr("reset_settings"))
        self.reset_btn.clicked.connect(self.reset_settings)
        self.cancel_btn = ModernButton(trans.tr("cancel"))
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.load_settings()
    
    def create_general_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Startup section
        startup_group = QGroupBox(trans.tr("startup"))
        startup_layout = QVBoxLayout()
        
        self.startup_homepage = QRadioButton(trans.tr("open_homepage"))
        self.startup_previous = QRadioButton(trans.tr("continue_previous"))
        self.startup_specific = QRadioButton(trans.tr("open_specific"))
        
        startup_layout.addWidget(self.startup_homepage)
        startup_layout.addWidget(self.startup_previous)
        startup_layout.addWidget(self.startup_specific)
        
        startup_group.setLayout(startup_layout)
        layout.addWidget(startup_group)
        
        # Search engine
        search_layout = QFormLayout()
        self.search_engine = QComboBox()
        self.search_engine.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo"])
        search_layout.addRow(trans.tr("search_engine"), self.search_engine)
        
        self.instant_search = QCheckBox(trans.tr("instant_search"))
        search_layout.addRow(self.instant_search)
        
        layout.addLayout(search_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_appearance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Theme
        theme_layout = QFormLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([trans.tr("light"), trans.tr("dark"), trans.tr("auto")])
        theme_layout.addRow(trans.tr("theme"), self.theme_combo)
        
        self.acrylic_effect = QCheckBox(trans.tr("acrylic_effect"))
        theme_layout.addRow(self.acrylic_effect)
        
        layout.addLayout(theme_layout)
        
        # Fonts
        fonts_group = QGroupBox(trans.tr("fonts"))
        fonts_layout = QFormLayout()
        
        self.font_family = QComboBox()
        self.font_family.addItems(["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Verdana"])
        fonts_layout.addRow(trans.tr("font_family"), self.font_family)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        fonts_layout.addRow(trans.tr("font_size"), self.font_size)
        
        fonts_group.setLayout(fonts_layout)
        layout.addWidget(fonts_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_privacy_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Privacy settings
        privacy_layout = QVBoxLayout()
        
        self.accept_cookies = QCheckBox(trans.tr("accept_cookies"))
        self.block_tracking = QCheckBox(trans.tr("block_tracking"))
        self.block_ads = QCheckBox(trans.tr("block_ads"))
        self.webrtc_leak = QCheckBox(trans.tr("webrtc_leak"))
        
        privacy_layout.addWidget(self.accept_cookies)
        privacy_layout.addWidget(self.block_tracking)
        privacy_layout.addWidget(self.block_ads)
        privacy_layout.addWidget(self.webrtc_leak)
        
        layout.addLayout(privacy_layout)
        
        # Clear browsing data
        clear_group = QGroupBox(trans.tr("clear_browsing_data"))
        clear_layout = QVBoxLayout()
        
        self.clear_history_check = QCheckBox(trans.tr("browsing_history"))
        self.clear_cookies_check = QCheckBox(trans.tr("cookies_data"))
        self.clear_cache_check = QCheckBox(trans.tr("cached_files"))
        
        clear_layout.addWidget(self.clear_history_check)
        clear_layout.addWidget(self.clear_cookies_check)
        clear_layout.addWidget(self.clear_cache_check)
        
        self.clear_now_btn = ModernButton(trans.tr("clear_now"))
        self.clear_now_btn.clicked.connect(self.clear_browsing_data)
        clear_layout.addWidget(self.clear_now_btn)
        
        clear_group.setLayout(clear_layout)
        layout.addWidget(clear_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_advanced_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Performance
        performance_group = QGroupBox(trans.tr("performance"))
        performance_layout = QVBoxLayout()
        
        self.hardware_accel = QCheckBox(trans.tr("hardware_accel"))
        self.preload_pages = QCheckBox(trans.tr("preload_pages"))
        
        performance_layout.addWidget(self.hardware_accel)
        performance_layout.addWidget(self.preload_pages)
        
        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)
        
        # Developer tools
        dev_group = QGroupBox(trans.tr("developer_tools"))
        dev_layout = QVBoxLayout()
        
        self.enable_dev_tools = QCheckBox(trans.tr("enable_dev_tools"))
        self.js_console = QCheckBox(trans.tr("js_console"))
        
        dev_layout.addWidget(self.enable_dev_tools)
        dev_layout.addWidget(self.js_console)
        
        dev_group.setLayout(dev_layout)
        layout.addWidget(dev_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def load_settings(self):
        settings = QSettings("NexaBrowser", "Nexa")
        
        # Load general settings
        search_engine = settings.value("search_engine", "Google")
        index = self.search_engine.findText(search_engine)
        if index >= 0:
            self.search_engine.setCurrentIndex(index)
        
        self.instant_search.setChecked(settings.value("instant_search", True, type=bool))
        
        # Load appearance settings
        theme = settings.value("theme", "dark")
        theme_index = {"light": 0, "dark": 1, "auto": 2}.get(theme, 1)
        self.theme_combo.setCurrentIndex(theme_index)
        
        self.acrylic_effect.setChecked(settings.value("acrylic_effect", False, type=bool))
        self.font_family.setCurrentText(settings.value("font_family", "Segoe UI"))
        self.font_size.setValue(settings.value("font_size", 12, type=int))
        
        # Load privacy settings
        self.accept_cookies.setChecked(settings.value("accept_cookies", True, type=bool))
        self.block_tracking.setChecked(settings.value("block_tracking", True, type=bool))
        self.block_ads.setChecked(settings.value("block_ads", True, type=bool))
        self.webrtc_leak.setChecked(settings.value("webrtc_leak", True, type=bool))
        
        # Load advanced settings
        self.hardware_accel.setChecked(settings.value("hardware_accel", True, type=bool))
        self.preload_pages.setChecked(settings.value("preload_pages", True, type=bool))
        self.enable_dev_tools.setChecked(settings.value("enable_dev_tools", False, type=bool))
        self.js_console.setChecked(settings.value("js_console", False, type=bool))
    
    def save_settings(self):
        settings = QSettings("NexaBrowser", "Nexa")
        
        # Save general settings
        settings.setValue("search_engine", self.search_engine.currentText())
        settings.setValue("instant_search", self.instant_search.isChecked())
        
        # Save appearance settings
        theme_index = self.theme_combo.currentIndex()
        theme = ["light", "dark", "auto"][theme_index]
        settings.setValue("theme", theme)
        settings.setValue("acrylic_effect", self.acrylic_effect.isChecked())
        settings.setValue("font_family", self.font_family.currentText())
        settings.setValue("font_size", self.font_size.value())
        
        # Save privacy settings
        settings.setValue("accept_cookies", self.accept_cookies.isChecked())
        settings.setValue("block_tracking", self.block_tracking.isChecked())
        settings.setValue("block_ads", self.block_ads.isChecked())
        settings.setValue("webrtc_leak", self.webrtc_leak.isChecked())
        
        # Save advanced settings
        settings.setValue("hardware_accel", self.hardware_accel.isChecked())
        settings.setValue("preload_pages", self.preload_pages.isChecked())
        settings.setValue("enable_dev_tools", self.enable_dev_tools.isChecked())
        settings.setValue("js_console", self.js_console.isChecked())
        
        QMessageBox.information(self, trans.tr("settings_saved"), trans.tr("settings_saved_msg"))
        self.accept()
    
    def reset_settings(self):
        reply = QMessageBox.question(self, trans.tr("reset_confirm"), trans.tr("reset_confirm_msg"))
        if reply == QMessageBox.StandardButton.Yes:
            settings = QSettings("NexaBrowser", "Nexa")
            settings.clear()
            self.load_settings()
            QMessageBox.information(self, trans.tr("reset_complete"), trans.tr("reset_complete_msg"))
    
    def clear_browsing_data(self):
        reply = QMessageBox.question(self, trans.tr("clear_data_confirm"), trans.tr("clear_data_confirm_msg"))
        if reply == QMessageBox.StandardButton.Yes:
            db = DatabaseManager()
            if self.clear_history_check.isChecked():
                db.clear_history()
            # Note: Cookies and cache clearing would require additional implementation
            QMessageBox.information(self, trans.tr("data_cleared"), trans.tr("data_cleared_msg"))

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
        edit_menu = self.addMenu( " + trans.tr("edit"))
        
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
        
        fullscreen_action = QAction(trans.tr("fullscreen"), self)
        fullscreen_action.triggered.connect(lambda: self.parent().toggle_fullscreen())
        fullscreen_action.setShortcut(QKeySequence("F11"))
        view_menu.addAction(fullscreen_action)
        
        # Bookmarks section
        bookmarks_menu = self.addMenu("🔖 " + trans.tr("bookmarks"))
        
        show_bookmarks_action = QAction(trans.tr("bookmarks"), self)
        show_bookmarks_action.triggered.connect(lambda: self.parent().show_bookmarks())
        bookmarks_menu.addAction(show_bookmarks_action)
        
        add_bookmark_action = QAction(trans.tr("add_bookmark"), self)
        add_bookmark_action.triggered.connect(lambda: self.parent().add_current_bookmark())
        add_bookmark_action.setShortcut(QKeySequence("Ctrl+D"))
        bookmarks_menu.addAction(add_bookmark_action)
        
        # History section
        history_menu = self.addMenu("📜 " + trans.tr("history"))
        
        show_history_action = QAction(trans.tr("history"), self)
        show_history_action.triggered.connect(lambda: self.parent().show_history())
        history_menu.addAction(show_history_action)
        
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
        
        report_issue_action = QAction(trans.tr("report_issue"), self)
        report_issue_action.triggered.connect(lambda: self.parent().report_issue())
        help_menu.addAction(report_issue_action)
    
    def toggle_navigation_bar(self, visible):
        self.parent().toolbar.setVisible(visible)
    
    def show_about(self):
        QMessageBox.about(self.parent(), trans.tr("about"), 
                         f"{trans.tr('app_name')} v3.0\n\n{trans.tr('modern_fast_private')}")

class NexaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("NexaBrowser", "Nexa")
        self.db = DatabaseManager()
        self.is_fullscreen = False
        
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
        back_btn = QToolButton()
        back_btn.setText("←")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        back_btn.setStyleSheet("""
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
        self.toolbar.addWidget(back_btn)
        
        forward_btn = QToolButton()
        forward_btn.setText("→")
        forward_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forward_btn.clicked.connect(self.go_forward)
        forward_btn.setStyleSheet("""
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
        self.toolbar.addWidget(forward_btn)
        
        reload_btn = QToolButton()
        reload_btn.setText("↻")
        reload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reload_btn.clicked.connect(self.reload_page)
        reload_btn.setStyleSheet("""
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
        self.toolbar.addWidget(reload_btn)
        
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
        home_btn = QToolButton()
        home_btn.setText("🏠")
        home_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        home_btn.clicked.connect(self.load_homepage)
        home_btn.setStyleSheet("""
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
        self.toolbar.addWidget(home_btn)
    
    # Navigation methods
    def add_new_tab(self, url=None):
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
    
    def update_tab_title(self, title, tab):
        index = self.tab_widget.indexOf(tab)
        if index >= 0:
            display_title = title[:20] + "..." if len(title) > 20 else title
            self.tab_widget.setTabText(index, display_title)
            
            # Add to history
            if title and tab.url().toString():
                self.db.add_history(title, tab.url().toString())
    
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
                search_engine = self.settings.value("search_engine", "Google")
                if search_engine == "Google":
                    url = f'https://www.google.com/search?q={url.replace(" ", "+")}'
                elif search_engine == "Bing":
                    url = f'https://www.bing.com/search?q={url.replace(" ", "+")}'
                elif search_engine == "DuckDuckGo":
                    url = f'https://duckduckgo.com/?q={url.replace(" ", "+")}'
                elif search_engine == "Yahoo":
                    url = f'https://search.yahoo.com/search?p={url.replace(" ", "+")}'
                else:
                    url = f'https://www.google.com/search?q={url.replace(" ", "+")}'
        
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.load(QUrl(url))
    
    def load_homepage(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.setHtml(self.get_homepage_html())
    
    def get_homepage_html(self):
        show_calendar = self.settings.value("show_calendar", True, type=bool)
        show_quick_links = self.settings.value("show_quick_links", True, type=bool)
        
        calendar_html = ""
        if show_calendar:
            calendar_html = """
            <div class="widget">
                <h3>Calendar</h3>
                <div id="calendar"></div>
            </div>
            """
        
        quick_links_html = ""
        if show_quick_links:
            quick_links_html = """
            <div class="quick-links">
                <div class="link" onclick="window.location.href='https://www.google.com'">Google</div>
                <div class="link" onclick="window.location.href='https://www.youtube.com'">YouTube</div>
                <div class="link" onclick="window.location.href='https://mail.google.com'">Gmail</div>
                <div class="link" onclick="window.location.href='https://www.github.com'">GitHub</div>
                <div class="link" onclick="window.location.href='https://www.wikipedia.org'">Wikipedia</div>
                <div class="link" onclick="window.location.href='https://www.twitter.com'">Twitter</div>
            </div>
            """
        
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
                    margin-bottom: 30px;
                }}
                .search-box:focus {{
                    border-color: #0078d4;
                }}
                .quick-links {{
                    margin-top: 30px;
                    display: flex;
                    gap: 15px;
                    flex-wrap: wrap;
                    justify-content: center;
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
                .widget {{
                    background-color: #2d2d2d;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px;
                    min-width: 300px;
                }}
            </style>
        </head>
        <body>
            <div class="title">{trans.tr('app_name')}</div>
            <div class="subtitle">{trans.tr('modern_fast_private')}</div>
            <input type="text" class="search-box" placeholder="{trans.tr('search_placeholder')}" id="search">
            {quick_links_html}
            {calendar_html}
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
    
    # Enhanced menu action methods
    def new_window(self):
        new_browser = NexaBrowser()
        new_browser.show()
    
    def private_browsing(self):
        QMessageBox.information(self, trans.tr("private_browsing"), "Private browsing mode would open here.")
    
    def save_page(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            file_path, _ = QFileDialog.getSaveFileName(self, trans.tr("save_page"), "", "HTML Files (*.html *.htm)")
            if file_path:
                current_tab.page().toHtml(lambda html: self.save_html_to_file(html, file_path))
    
    def save_html_to_file(self, html, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            QMessageBox.information(self, trans.tr("success"), trans.tr("page_saved"))
        except Exception as e:
            QMessageBox.warning(self, trans.tr("error"), f"Failed to save page: {str(e)}")
    
    def print_page(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            printer = QPrinter()
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                current_tab.print(printer)
    
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
    
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True
    
    def show_bookmarks(self):
        bookmarks_dialog = BookmarksManager(self)
        bookmarks_dialog.exec()
    
    def show_history(self):
        history_dialog = HistoryManager(self)
        history_dialog.exec()
    
    def add_current_bookmark(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            title = current_tab.page().title()
            url = current_tab.url().toString()
            if title and url:
                self.db.add_bookmark(title, url)
                QMessageBox.information(self, trans.tr("success"), trans.tr("bookmark_added"))
    
    def show_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()
        # Re-apply settings after dialog closes
        self.apply_settings()
    
    def show_homepage_customization(self):
        QMessageBox.information(self, trans.tr("homepage_customization"), "Homepage customization dialog would open here.")
    
    def show_appearance_settings(self):
        QMessageBox.information(self, trans.tr("appearance_settings"), "Appearance settings dialog would open here.")
    
    def show_help(self):
        QMessageBox.information(self, trans.tr("help_support"), "Help and support documentation would open here.")
    
    def report_issue(self):
        QMessageBox.information(self, trans.tr("report_issue"), "Issue reporting would open here.")

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
