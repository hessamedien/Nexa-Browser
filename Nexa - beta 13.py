# nexa_browser.py
import sys
import os
import json
import tempfile
from pathlib import Path
from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, QSettings, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPalette, QColor, QAction, QKeySequence, QPainter, QLinearGradient
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QToolBar, QLineEdit, QPushButton, QTabWidget, QLabel, 
                            QToolButton, QMenu, QDialog, QDialogButtonBox, QFormLayout, 
                            QComboBox, QCheckBox, QSpinBox, QStackedWidget, QFrame,
                            QProgressBar, QMessageBox, QStyleFactory, QScrollArea, QSizePolicy)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage

class ModernButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(32)
        
        # Modern styling
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
        self.setWindowTitle("Nexa Browser Setup")
        self.setFixedSize(700, 600)
        self.setModal(True)
        
        # Apply dark theme by default
        self.apply_dark_theme()
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Welcome to Nexa Browser")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setWeight(QFont.Weight.Bold)
        header.setFont(header_font)
        header.setStyleSheet("color: white; margin: 20px;")
        layout.addWidget(header)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
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
        self.back_btn = ModernButton("Back")
        self.back_btn.clicked.connect(self.previous_page)
        self.next_btn = ModernButton("Next")
        self.next_btn.clicked.connect(self.next_page)
        self.finish_btn = ModernButton("Finish")
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
    
    def create_theme_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Choose Your Theme")
        title_font = QFont()
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Theme selection
        theme_layout = QHBoxLayout()
        
        dark_theme = RoundedFrame()
        dark_layout = QVBoxLayout(dark_theme)
        dark_preview = QLabel("Dark Theme")
        dark_preview.setStyleSheet("""
            background-color: #1e1e1e; 
            color: white; 
            padding: 40px; 
            border-radius: 8px;
            font-weight: bold;
        """)
        dark_layout.addWidget(dark_preview)
        dark_radio = QCheckBox("Dark Mode")
        dark_radio.setChecked(True)
        dark_radio.setStyleSheet("color: white;")
        dark_layout.addWidget(dark_radio)
        theme_layout.addWidget(dark_theme)
        
        light_theme = RoundedFrame()
        light_layout = QVBoxLayout(light_theme)
        light_preview = QLabel("Light Theme")
        light_preview.setStyleSheet("""
            background-color: #f5f5f5; 
            color: #333; 
            padding: 40px; 
            border-radius: 8px;
            font-weight: bold;
        """)
        light_layout.addWidget(light_preview)
        light_radio = QCheckBox("Light Mode")
        light_radio.setStyleSheet("color: white;")
        light_layout.addWidget(light_radio)
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
        
        title = QLabel("Search & AI Settings")
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
        search_layout.addRow("Default Search Engine:", self.search_engine)
        layout.addLayout(search_layout)
        
        # AI Assistant
        ai_frame = RoundedFrame()
        ai_layout = QVBoxLayout(ai_frame)
        
        ai_title = QLabel("AI Assistant")
        ai_title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        ai_layout.addWidget(ai_title)
        
        self.ai_enabled = QCheckBox("Enable AI Assistant")
        self.ai_enabled.setChecked(True)
        self.ai_enabled.setStyleSheet("color: white;")
        ai_layout.addWidget(self.ai_enabled)
        
        self.ai_sidebar = QCheckBox("Show AI Sidebar by default")
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
        
        title = QLabel("Homepage Customization")
        title_font = QFont()
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Homepage layout options
        layout_options = QHBoxLayout()
        
        minimal_layout = RoundedFrame()
        minimal_layout_layout = QVBoxLayout(minimal_layout)
        minimal_preview = QLabel("Minimal\n\nSearch Box\nQuick Links")
        minimal_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        minimal_preview.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.05); 
            color: rgba(255, 255, 255, 0.7); 
            padding: 30px; 
            border-radius: 8px;
        """)
        minimal_layout_layout.addWidget(minimal_preview)
        minimal_radio = QCheckBox("Minimal")
        minimal_radio.setStyleSheet("color: white;")
        minimal_layout_layout.addWidget(minimal_radio)
        layout_options.addWidget(minimal_layout)
        
        dashboard_layout = RoundedFrame()
        dashboard_layout_layout = QVBoxLayout(dashboard_layout)
        dashboard_preview = QLabel("Dashboard\n\nSearch\nNews\nWeather\nBookmarks")
        dashboard_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dashboard_preview.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.05); 
            color: rgba(255, 255, 255, 0.7); 
            padding: 30px; 
            border-radius: 8px;
        """)
        dashboard_layout_layout.addWidget(dashboard_preview)
        dashboard_radio = QCheckBox("Dashboard")
        dashboard_radio.setChecked(True)
        dashboard_radio.setStyleSheet("color: white;")
        dashboard_layout_layout.addWidget(dashboard_radio)
        layout_options.addWidget(dashboard_layout)
        
        layout.addLayout(layout_options)
        
        # Additional options
        options_layout = QVBoxLayout()
        
        self.show_calendar = QCheckBox("Show Calendar Widget")
        self.show_calendar.setChecked(True)
        self.show_calendar.setStyleSheet("color: white;")
        options_layout.addWidget(self.show_calendar)
        
        self.show_quick_links = QCheckBox("Show Quick Links")
        self.show_quick_links.setChecked(True)
        self.show_quick_links.setStyleSheet("color: white;")
        options_layout.addWidget(self.show_quick_links)
        
        layout.addLayout(options_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
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

class AISidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #2d2d2d;")
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Nexa AI Assistant")
        header.setStyleSheet("color: white; font-weight: bold; padding: 10px; border-bottom: 1px solid #444;")
        layout.addWidget(header)
        
        # Chat area
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("background-color: #2d2d2d; border: none;")
        chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(chat_widget)
        self.chat_layout.addStretch()
        self.chat_area.setWidget(chat_widget)
        layout.addWidget(self.chat_area)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me anything...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                border: 1px solid #555;
                border-radius: 18px;
                padding: 8px 15px;
                color: white;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedSize(60, 36)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 18px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.send_btn.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
    
    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return
        
        # Add user message
        user_msg = QLabel(f"You: {message}")
        user_msg.setStyleSheet("""
            QLabel {
                background-color: #0078d4;
                color: white;
                padding: 8px 12px;
                border-radius: 12px;
                margin: 5px;
            }
        """)
        user_msg.setWordWrap(True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, user_msg)
        
        # Clear input
        self.input_field.clear()
        
        # Simulate AI response
        QTimer.singleShot(1000, lambda: self.add_ai_response(message))
    
    def add_ai_response(self, user_message):
        # Simple response simulation
        responses = [
            f"I understand you're asking about '{user_message}'. This is a simulated response from the AI assistant.",
            f"Based on your query '{user_message}', I can provide information and assistance with various tasks.",
            f"Regarding '{user_message}', I can help summarize content, translate text, or generate ideas as needed."
        ]
        
        import random
        response = random.choice(responses)
        
        ai_msg = QLabel(f"AI: {response}")
        ai_msg.setStyleSheet("""
            QLabel {
                background-color: #3d3d3d;
                color: white;
                padding: 8px 12px;
                border-radius: 12px;
                margin: 5px;
            }
        """)
        ai_msg.setWordWrap(True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_msg)
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e;")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo and title
        title = QLabel("Nexa Browser")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setWeight(QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Modern, Fast, and Private")
        subtitle.setStyleSheet("color: #aaa; margin-bottom: 30px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
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
        
        search_btn = QPushButton("Search")
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
        
        layout.addLayout(search_layout)
        
        # Quick links
        quick_links_frame = RoundedFrame()
        quick_links_layout = QVBoxLayout(quick_links_frame)
        
        quick_links_title = QLabel("Quick Links")
        quick_links_title.setStyleSheet("color: white; font-weight: bold; margin-bottom: 10px;")
        quick_links_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quick_links_layout.addWidget(quick_links_title)
        
        links_layout = QHBoxLayout()
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
            links_layout.addWidget(btn)
        
        quick_links_layout.addLayout(links_layout)
        layout.addWidget(quick_links_frame)
        
        # Calendar widget
        calendar_frame = RoundedFrame()
        calendar_layout = QVBoxLayout(calendar_frame)
        
        calendar_title = QLabel("Calendar")
        calendar_title.setStyleSheet("color: white; font-weight: bold; margin-bottom: 10px;")
        calendar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calendar_layout.addWidget(calendar_title)
        
        from datetime import datetime
        now = datetime.now()
        date_label = QLabel(now.strftime("%A, %B %d, %Y"))
        date_label.setStyleSheet("color: white; font-size: 14px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calendar_layout.addWidget(date_label)
        
        layout.addWidget(calendar_frame)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Connect search
        self.search_box.returnPressed.connect(lambda: self.parent().parent().load_url(self.search_box.text()))
        search_btn.clicked.connect(lambda: self.parent().parent().load_url(self.search_box.text()))

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
        
        # Check if first run
        if not self.settings.value("first_run_complete", False, type=bool):
            self.show_first_run_wizard()
        
        # Apply theme
        self.apply_theme()
        
        # Initialize UI
        self.init_ui()
        
        # Load homepage
        self.load_homepage()
    
    def show_first_run_wizard(self):
        wizard = FirstRunWizard(self)
        if wizard.exec() == QDialog.DialogCode.Accepted:
            self.settings.setValue("first_run_complete", True)
    
    def apply_theme(self):
        # Apply dark theme by default
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
        """)
    
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # AI Sidebar (initially hidden)
        self.ai_sidebar = AISidebar()
        self.ai_sidebar.hide()
        main_layout.addWidget(self.ai_sidebar)
        
        # Browser area
        browser_area = QVBoxLayout()
        
        # Toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.toolbar)
        
        # Navigation buttons
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.go_back)
        self.toolbar.addAction(back_btn)
        
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_btn)
        
        reload_btn = QAction("Reload", self)
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
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.load_homepage)
        self.toolbar.addAction(home_btn)
        
        self.toolbar.addSeparator()
        
        # AI Sidebar toggle
        ai_btn = QAction("AI", self)
        ai_btn.triggered.connect(self.toggle_ai_sidebar)
        self.toolbar.addAction(ai_btn)
        
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
            # Create homepage widget
            homepage = HomePage()
            
            # Use a QWebEngineView to display the homepage
            current_tab.setHtml(self.get_homepage_html(), QUrl("about:home"))
    
    def get_homepage_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    background-color: #1e1e1e;
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                .title {
                    font-size: 2.5em;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .subtitle {
                    color: #aaa;
                    margin-bottom: 30px;
                }
                .search-box {
                    width: 600px;
                    padding: 12px 20px;
                    border-radius: 24px;
                    border: 2px solid #444;
                    background-color: #2d2d2d;
                    color: white;
                    font-size: 16px;
                    outline: none;
                }
                .search-box:focus {
                    border-color: #0078d4;
                }
                .quick-links {
                    margin-top: 30px;
                    display: flex;
                    gap: 15px;
                }
                .link {
                    padding: 10px 20px;
                    background-color: #2d2d2d;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                .link:hover {
                    background-color: #3d3d3d;
                }
            </style>
        </head>
        <body>
            <div class="title">Nexa Browser</div>
            <div class="subtitle">Modern, Fast, and Private</div>
            <input type="text" class="search-box" placeholder="Search the web or enter address..." id="search">
            <div class="quick-links">
                <div class="link" onclick="window.location.href='https://www.google.com'">Google</div>
                <div class="link" onclick="window.location.href='https://www.youtube.com'">YouTube</div>
                <div class="link" onclick="window.location.href='https://mail.google.com'">Gmail</div>
                <div class="link" onclick="window.location.href='https://www.github.com'">GitHub</div>
            </div>
            <script>
                document.getElementById('search').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        let query = this.value;
                        if (!query.startsWith('http')) {
                            window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query);
                        } else {
                            window.location.href = query;
                        }
                    }
                });
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
    
    def toggle_ai_sidebar(self):
        if self.ai_sidebar.isVisible():
            self.ai_sidebar.hide()
        else:
            self.ai_sidebar.show()

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("1.0.0")
    
    # Set dark theme palette
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