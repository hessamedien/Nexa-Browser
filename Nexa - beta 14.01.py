# nexa_browser_advanced_fixed.py
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
                            QCalendarWidget, QSplitter, QTextEdit)

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage

class DraggableWidget(QFrame):
    def __init__(self, title, widget, removable=True, parent=None):
        super().__init__(parent)
        self.title = title
        self.widget = widget
        self.removable = removable
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setStyleSheet("""
            DraggableWidget {
                background-color: rgba(40, 40, 40, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Header with title and close button
        header_layout = QHBoxLayout()
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: white; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        if self.removable:
            self.close_btn = QToolButton()
            self.close_btn.setText("×")
            self.close_btn.setStyleSheet("""
                QToolButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                }
                QToolButton:hover {
                    color: #ff4444;
                }
            """)
            self.close_btn.setFixedSize(20, 20)
            self.close_btn.clicked.connect(self.remove_self)
            header_layout.addWidget(self.close_btn)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.widget)

    def remove_self(self):
        self.setParent(None)
        self.deleteLater()

class WidgetSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Widgets to Homepage")
        self.setFixedSize(400, 500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Available widgets list
        self.widgets_list = QListWidget()
        widgets = [
            "Calendar Widget",
            "Quick Links", 
            "Weather Widget",
            "News Feed",
            "Bookmarks Bar",
            "Notes Widget",
            "Download Manager",
            "System Monitor",
            "Clock & Date",
            "Search History"
        ]
        
        for widget in widgets:
            item = QListWidgetItem(widget)
            self.widgets_list.addItem(item)
            
        layout.addWidget(QLabel("Available Widgets:"))
        layout.addWidget(self.widgets_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = ModernButton("Add Selected")
        add_btn.clicked.connect(self.accept)
        cancel_btn = ModernButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_selected_widget(self):
        if self.widgets_list.currentItem():
            return self.widgets_list.currentItem().text()
        return None

class CalendarWidget(QWidget):
    def __init__(self, calendar_type="Gregory", parent=None):
        super().__init__(parent)
        self.calendar_type = calendar_type
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Calendar type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Calendar:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Gregory", "Jalali", "Hijri", "Hebrew", "Chinese"])
        self.type_combo.setCurrentText(self.calendar_type)
        self.type_combo.currentTextChanged.connect(self.change_calendar_type)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Calendar display
        self.calendar_display = QLabel()
        self.calendar_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.calendar_display.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 15px;
                color: white;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.calendar_display)
        
        self.update_calendar()
        self.setLayout(layout)
    
    def change_calendar_type(self, new_type):
        self.calendar_type = new_type
        self.update_calendar()
    
    def update_calendar(self):
        now = datetime.now()
        
        if self.calendar_type == "Gregory":
            text = now.strftime("%A, %B %d, %Y\n%H:%M:%S")
        elif self.calendar_type == "Jalali":
            # Simplified Jalali conversion
            text = f"تقویم جلالی\n{now.strftime('%Y/%m/%d')}"
        elif self.calendar_type == "Hijri":
            text = f"التقويم الهجري\n{now.strftime('%Y/%m/%d')}"
        elif self.calendar_type == "Hebrew":
            text = f"הלוח העברי\n{now.strftime('%Y/%m/%d')}"
        elif self.calendar_type == "Chinese":
            text = f"农历\n{now.strftime('%Y年%m月%d日')}"
            
        self.calendar_display.setText(text)

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
        file_menu = self.addMenu("📁 File")
        
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.parent().add_new_tab())
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction("New Window", self)
        new_window_action.triggered.connect(lambda: print("New Window"))
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        file_menu.addAction(new_window_action)
        
        private_action = QAction("Private Browsing", self)
        private_action.triggered.connect(lambda: print("Private Browsing"))
        private_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        file_menu.addAction(private_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save Page As...", self)
        save_action.triggered.connect(lambda: print("Save Page"))
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        file_menu.addAction(save_action)
        
        print_action = QAction("Print...", self)
        print_action.triggered.connect(lambda: print("Print"))
        print_action.setShortcut(QKeySequence("Ctrl+P"))
        file_menu.addAction(print_action)
        
        # Edit section
        edit_menu = self.addMenu("✏️ Edit")
        
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(lambda: print("Cut"))
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(lambda: print("Copy"))
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(lambda: print("Paste"))
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        edit_menu.addAction(paste_action)
        
        # View section
        view_menu = self.addMenu("👁️ View")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(lambda: print("Zoom In"))
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(lambda: print("Zoom Out"))
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        view_menu.addAction(zoom_out_action)
        
        actual_size_action = QAction("Actual Size", self)
        actual_size_action.triggered.connect(lambda: print("Actual Size"))
        actual_size_action.setShortcut(QKeySequence("Ctrl+0"))
        view_menu.addAction(actual_size_action)
        
        view_menu.addSeparator()
        
        # Toolbars submenu
        toolbars_menu = view_menu.addMenu("Toolbars")
        self.nav_action = QAction("Navigation Bar", self)
        self.nav_action.setCheckable(True)
        self.nav_action.setChecked(True)
        self.nav_action.toggled.connect(self.toggle_navigation_bar)
        toolbars_menu.addAction(self.nav_action)
        
        self.bookmarks_action = QAction("Bookmarks Bar", self)
        self.bookmarks_action.setCheckable(True)
        self.bookmarks_action.setChecked(False)
        toolbars_menu.addAction(self.bookmarks_action)
        
        # Settings section
        settings_menu = self.addMenu("⚙️ Settings")
        
        browser_settings_action = QAction("Browser Settings", self)
        browser_settings_action.triggered.connect(lambda: self.parent().show_settings_dialog())
        settings_menu.addAction(browser_settings_action)
        
        homepage_action = QAction("Homepage Customization", self)
        homepage_action.triggered.connect(lambda: self.parent().show_homepage_customization())
        settings_menu.addAction(homepage_action)
        
        appearance_action = QAction("Appearance Settings", self)
        appearance_action.triggered.connect(lambda: self.parent().show_appearance_settings())
        settings_menu.addAction(appearance_action)
        
        # Help section
        help_menu = self.addMenu("❓ Help")
        
        about_action = QAction("About Nexa Browser", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        help_action = QAction("Help & Support", self)
        help_action.triggered.connect(lambda: print("Help"))
        help_menu.addAction(help_action)
    
    def toggle_navigation_bar(self, visible):
        self.parent().toolbar.setVisible(visible)
    
    def show_about(self):
        QMessageBox.about(self.parent(), "About Nexa Browser", 
                         "Nexa Browser v2.0\n\nA modern, customizable browser with AI integration")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browser Settings")
        self.setFixedSize(600, 700)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Tab widget for different settings categories
        tab_widget = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "General")
        
        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        tab_widget.addTab(appearance_tab, "Appearance")
        
        # Privacy tab
        privacy_tab = self.create_privacy_tab()
        tab_widget.addTab(privacy_tab, "Privacy")
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Advanced")
        
        layout.addWidget(tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = ModernButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = ModernButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        reset_btn = ModernButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_settings)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def create_general_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Startup section
        startup_group = QGroupBox("Startup")
        startup_layout = QFormLayout()
        
        self.startup_combo = QComboBox()
        self.startup_combo.addItems(["Open homepage", "Continue where I left off", "Open specific pages"])
        startup_layout.addRow("On startup:", self.startup_combo)
        
        self.homepage_edit = QLineEdit()
        self.homepage_edit.setText("about:home")
        startup_layout.addRow("Homepage:", self.homepage_edit)
        
        startup_group.setLayout(startup_layout)
        layout.addWidget(startup_group)
        
        # Search section
        search_group = QGroupBox("Search")
        search_layout = QFormLayout()
        
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo"])
        search_layout.addRow("Default search engine:", self.search_combo)
        
        self.instant_search = QCheckBox("Enable instant search")
        self.instant_search.setChecked(True)
        search_layout.addRow(self.instant_search)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_appearance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Theme section
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        theme_layout.addWidget(QLabel("Color theme:"))
        theme_layout.addWidget(self.theme_combo)
        
        self.acrylic_effect = QCheckBox("Enable acrylic blur effect")
        self.acrylic_effect.setChecked(True)
        theme_layout.addWidget(self.acrylic_effect)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Fonts section
        font_group = QGroupBox("Fonts")
        font_layout = QFormLayout()
        
        self.font_family = QComboBox()
        self.font_family.addItems(["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Verdana"])
        font_layout.addRow("Font family:", self.font_family)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        font_layout.addRow("Font size:", self.font_size)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_privacy_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Privacy settings
        privacy_group = QGroupBox("Privacy & Security")
        privacy_layout = QVBoxLayout()
        
        self.cookies = QCheckBox("Accept cookies")
        self.cookies.setChecked(True)
        privacy_layout.addWidget(self.cookies)
        
        self.tracking = QCheckBox("Block tracking cookies")
        self.tracking.setChecked(True)
        privacy_layout.addWidget(self.tracking)
        
        self.ads = QCheckBox("Block ads")
        self.ads.setChecked(True)
        privacy_layout.addWidget(self.ads)
        
        self.webrtc = QCheckBox("Prevent WebRTC IP leak")
        self.webrtc.setChecked(True)
        privacy_layout.addWidget(self.webrtc)
        
        privacy_group.setLayout(privacy_layout)
        layout.addWidget(privacy_group)
        
        # Clear data
        clear_group = QGroupBox("Clear Browsing Data")
        clear_layout = QVBoxLayout()
        
        self.clear_history = QCheckBox("Browsing history")
        clear_layout.addWidget(self.clear_history)
        
        self.clear_cookies = QCheckBox("Cookies and site data")
        clear_layout.addWidget(self.clear_cookies)
        
        self.clear_cache = QCheckBox("Cached images and files")
        clear_layout.addWidget(self.clear_cache)
        
        clear_btn = ModernButton("Clear Now")
        clear_btn.clicked.connect(self.clear_data)
        clear_layout.addWidget(clear_btn)
        
        clear_group.setLayout(clear_layout)
        layout.addWidget(clear_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_advanced_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Performance
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout()
        
        self.hardware_accel = QCheckBox("Use hardware acceleration")
        self.hardware_accel.setChecked(True)
        perf_layout.addWidget(self.hardware_accel)
        
        self.preload = QCheckBox("Preload pages for faster browsing")
        self.preload.setChecked(True)
        perf_layout.addWidget(self.preload)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Developer tools
        dev_group = QGroupBox("Developer Tools")
        dev_layout = QVBoxLayout()
        
        self.dev_tools = QCheckBox("Enable developer tools")
        self.dev_tools.setChecked(True)
        dev_layout.addWidget(self.dev_tools)
        
        self.js_console = QCheckBox("Show JavaScript console")
        dev_layout.addWidget(self.js_console)
        
        dev_group.setLayout(dev_layout)
        layout.addWidget(dev_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def save_settings(self):
        # Save settings implementation
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully.")
        self.accept()
    
    def reset_settings(self):
        reply = QMessageBox.question(self, "Reset Settings", 
                                   "Are you sure you want to reset all settings to default?")
        if reply == QMessageBox.StandardButton.Yes:
            # Reset implementation
            QMessageBox.information(self, "Settings Reset", "All settings have been reset to default.")
    
    def clear_data(self):
        reply = QMessageBox.question(self, "Clear Data", 
                                   "Are you sure you want to clear the selected browsing data?")
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Data Cleared", "Selected browsing data has been cleared.")

class HomePageCustomizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Homepage Customization")
        self.setFixedSize(500, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Layout options
        layout_group = QGroupBox("Page Layout")
        layout_options = QVBoxLayout()
        
        self.layout_minimal = QCheckBox("Minimal (Search box only)")
        self.layout_dashboard = QCheckBox("Dashboard (Multiple widgets)")
        self.layout_dashboard.setChecked(True)
        self.layout_custom = QCheckBox("Custom (Drag and drop)")
        
        layout_options.addWidget(self.layout_minimal)
        layout_options.addWidget(self.layout_dashboard)
        layout_options.addWidget(self.layout_custom)
        
        layout_group.setLayout(layout_options)
        layout.addWidget(layout_group)
        
        # Widget management
        widget_group = QGroupBox("Widget Management")
        widget_layout = QVBoxLayout()
        
        self.available_widgets = QListWidget()
        widgets = ["Calendar", "Quick Links", "Weather", "News", "Bookmarks", "Notes", "Clock"]
        for widget in widgets:
            item = QListWidgetItem(widget)
            item.setCheckState(Qt.CheckState.Checked)
            self.available_widgets.addItem(item)
        
        widget_layout.addWidget(self.available_widgets)
        
        # Add/remove buttons
        widget_buttons = QHBoxLayout()
        add_widget_btn = ModernButton("Add New Widget")
        add_widget_btn.clicked.connect(self.add_widget)
        remove_widget_btn = ModernButton("Remove Selected")
        remove_widget_btn.clicked.connect(self.remove_widget)
        
        widget_buttons.addWidget(add_widget_btn)
        widget_buttons.addWidget(remove_widget_btn)
        widget_layout.addLayout(widget_buttons)
        
        widget_group.setLayout(widget_layout)
        layout.addWidget(widget_group)
        
        # Background customization
        bg_group = QGroupBox("Background")
        bg_layout = QFormLayout()
        
        self.bg_color = QPushButton("Choose Color")
        self.bg_color.clicked.connect(self.choose_bg_color)
        bg_layout.addRow("Background color:", self.bg_color)
        
        self.bg_image = QCheckBox("Use background image")
        bg_layout.addRow(self.bg_image)
        
        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = ModernButton("Apply Changes")
        apply_btn.clicked.connect(self.apply_changes)
        cancel_btn = ModernButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(apply_btn)
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def add_widget(self):
        dialog = WidgetSelectorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            widget_name = dialog.get_selected_widget()
            if widget_name:
                item = QListWidgetItem(widget_name)
                item.setCheckState(Qt.CheckState.Checked)
                self.available_widgets.addItem(item)
    
    def remove_widget(self):
        current_row = self.available_widgets.currentRow()
        if current_row >= 0:
            self.available_widgets.takeItem(current_row)
    
    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color.setStyleSheet(f"background-color: {color.name()};")
    
    def apply_changes(self):
        QMessageBox.information(self, "Changes Applied", 
                              "Homepage customization has been applied successfully.")
        self.accept()

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgets = []
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Header with title and customization button
        header_layout = QHBoxLayout()
        title = QLabel("Nexa Browser")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setWeight(QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.customize_btn = ModernButton("Customize")
        self.customize_btn.clicked.connect(self.show_customization)
        header_layout.addWidget(self.customize_btn)
        
        self.main_layout.addLayout(header_layout)
        
        # Search box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search the web or enter address...")
        self.search_box.setMinimumHeight(44)
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 22px;
                padding: 0px 20px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        search_layout.addWidget(self.search_box)
        
        search_btn = ModernButton("Search")
        search_btn.setFixedSize(80, 44)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 22px;
                color: white;
                font-weight: bold;
                margin-left: 5px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        search_layout.addWidget(search_btn)
        
        self.main_layout.addLayout(search_layout)
        
        # Widgets area
        self.widgets_layout = QVBoxLayout()
        self.main_layout.addLayout(self.widgets_layout)
        
        # Add default widgets
        self.add_default_widgets()
        
        self.setLayout(self.main_layout)
        
        # Connect search
        self.search_box.returnPressed.connect(self.perform_search)
        search_btn.clicked.connect(self.perform_search)
    
    def add_default_widgets(self):
        # Add calendar widget
        calendar_widget = CalendarWidget()
        draggable_calendar = DraggableWidget("Calendar", calendar_widget)
        self.widgets_layout.addWidget(draggable_calendar)
        
        # Add quick links
        quick_links = self.create_quick_links()
        draggable_links = DraggableWidget("Quick Links", quick_links)
        self.widgets_layout.addWidget(draggable_links)
        
        self.widgets.extend([draggable_calendar, draggable_links])
    
    def create_quick_links(self):
        widget = QWidget()
        layout = QHBoxLayout()
        
        links = [
            ("Google", "https://www.google.com"),
            ("YouTube", "https://www.youtube.com"),
            ("Gmail", "https://mail.google.com"),
            ("GitHub", "https://www.github.com")
        ]
        
        for name, url in links:
            btn = ModernButton(name)
            btn.setFixedSize(80, 60)
            btn.clicked.connect(lambda checked, u=url: self.parent().parent().load_url(u))
            layout.addWidget(btn)
        
        widget.setLayout(layout)
        return widget
    
    def show_customization(self):
        dialog = HomePageCustomizationDialog(self)
        dialog.exec()
    
    def perform_search(self):
        query = self.search_box.text()
        if query:
            self.parent().parent().load_url(query)
    
    def add_widget(self, widget_type):
        # Add new widget based on type
        if widget_type == "Calendar Widget":
            widget = CalendarWidget()
            draggable = DraggableWidget("Calendar", widget)
        elif widget_type == "Quick Links":
            widget = self.create_quick_links()
            draggable = DraggableWidget("Quick Links", widget)
        else:
            # Placeholder for other widgets
            widget = QLabel(f"Widget: {widget_type}")
            widget.setStyleSheet("color: white; padding: 20px;")
            draggable = DraggableWidget(widget_type, widget)
        
        self.widgets_layout.addWidget(draggable)
        self.widgets.append(draggable)
    
    def clear_widgets(self):
        for widget in self.widgets:
            self.widgets_layout.removeWidget(widget)
            widget.deleteLater()
        self.widgets.clear()

class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadFinished.connect(self.on_load_finished)
        
        # Enable developer tools
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        
    def on_load_finished(self, success):
        if success:
            print(f"Page loaded: {self.url().toString()}")

class NexaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexa Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Settings
        self.settings = QSettings("NexaBrowser", "Nexa")
        
        # Apply theme
        self.apply_theme()
        
        # Initialize UI
        self.init_ui()
        
        # Load homepage
        self.load_homepage()
    
    def apply_theme(self):
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
        self.address_bar.setPlaceholderText("Enter URL or search term...")
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
    
    def show_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def show_homepage_customization(self):
        dialog = HomePageCustomizationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Refresh homepage with new settings
            self.load_homepage()
    
    def show_appearance_settings(self):
        # Simplified appearance settings
        QMessageBox.information(self, "Appearance Settings", 
                              "Appearance settings would be shown here.")
    
    def add_new_tab(self, url=None):
        tab = BrowserTab()
        
        # Connect signals
        tab.urlChanged.connect(lambda u: self.update_url_bar(u, tab))
        tab.loadProgress.connect(self.update_progress)
        tab.loadFinished.connect(self.on_load_finished)
        
        index = self.tab_widget.addTab(tab, "New Tab")
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
            # Create homepage widget container
            container = QWidget()
            layout = QVBoxLayout(container)
            
            homepage = HomePage(self)
            layout.addWidget(homepage)
            
            # Set as the tab's content
            scroll_area = QScrollArea()
            scroll_area.setWidget(container)
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("background-color: #1e1e1e; border: none;")
            
            # Clear existing layout and add scroll area
            if current_tab.layout():
                # Remove existing widgets
                while current_tab.layout().count():
                    item = current_tab.layout().takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            else:
                current_tab.setLayout(QVBoxLayout())
            
            current_tab.layout().addWidget(scroll_area)
    
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

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("2.0")
    
    # Set dark theme
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