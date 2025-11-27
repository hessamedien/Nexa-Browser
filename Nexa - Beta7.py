# nexa_browser.py
# Nexa Browser - Modern AI-Powered Web Browser for Windows
# Created by Hessamedien (https://www.instagram.com/hessamedien)

import sys
import os
import json
import asyncio
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, quote
import zipfile
import hashlib
from typing import Dict, List, Optional, Any
import threading
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QToolBar, QTabWidget, QLineEdit, QPushButton, QToolButton, 
                            QLabel, QProgressBar, QFrame, QSplitter, QStackedWidget,
                            QDialog, QWizard, QWizardPage, QComboBox, QCheckBox, 
                            QSpinBox, QSlider, QGroupBox, QListWidget, QListWidgetItem,
                            QScrollArea, QStyleFactory, QMessageBox, QFileDialog,
                            QSystemTrayIcon, QMenu, QStyle, QSizePolicy, QDialogButtonBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, QSettings, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont, QFontDatabase, QPainter, QLinearGradient, 
                       QGuiApplication, QCursor, QAction, QDesktopServices, QPixmap, QBrush

# AI Integration Classes
class AIAssistant(QThread):
    response_received = pyqtSignal(str, str)  # query, response
    
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.api_key = ""
        
    def set_api_key(self, key: str):
        self.api_key = key
        
    def enable(self, enabled: bool):
        self.enabled = enabled
        
    def process_query(self, query: str, context: str = ""):
        if not self.enabled or not self.api_key:
            return
            
        self.query = query
        self.context = context
        self.start()
        
    def run(self):
        # Simulate AI processing - in production, integrate with actual AI API
        import time
        time.sleep(1)  # Simulate processing time
        
        responses = {
            "summarize": f"Summary of the page content: This is a simulated summary for demonstration purposes. Context: {self.context[:100]}...",
            "translate": "Translation feature would be available with proper AI integration",
            "explain": f"Explanation based on context: {self.context[:200]}...",
            "general": f"I received your query: '{self.query}'. This is a demo response from Nexa Browser's AI assistant."
        }
        
        if "summarize" in self.query.lower():
            response = responses["summarize"]
        elif "translate" in self.query.lower():
            response = responses["translate"]
        elif "explain" in self.query.lower():
            response = responses["explain"]
        else:
            response = responses["general"]
            
        self.response_received.emit(self.query, response)

# Download Manager
class DownloadManager:
    def __init__(self):
        self.downloads = []
        self.download_folder = str(Path.home() / "Downloads")
        
    def add_download(self, download_item: QWebEngineDownloadRequest):
        download_info = {
            'item': download_item,
            'path': download_item.downloadFileName(),
            'url': download_item.url().toString(),
            'progress': 0,
            'status': 'downloading',
            'start_time': datetime.now(),
            'speed': 0
        }
        self.downloads.append(download_info)
        
        download_item.accept()
        download_item.downloadProgress.connect(lambda received, total: self.update_progress(download_item, received, total))
        download_item.finished.connect(lambda: self.download_finished(download_item))
        
    def update_progress(self, download_item, received, total):
        for dl in self.downloads:
            if dl['item'] == download_item:
                dl['progress'] = (received / total * 100) if total > 0 else 0
                break
                
    def download_finished(self, download_item):
        for dl in self.downloads:
            if dl['item'] == download_item:
                dl['status'] = 'completed'
                dl['progress'] = 100
                break

# Modern Title Bar
class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setStyleSheet("""
            TitleBar {
                background-color: transparent;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        
        # App icon and title
        self.icon_label = QLabel("🌐 Nexa")
        self.icon_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(self.icon_label)
        
        self.layout.addStretch()
        
        # Window controls
        self.minimize_btn = QPushButton("−")
        self.maximize_btn = QPushButton("□")
        self.close_btn = QPushButton("×")
        
        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e5e5e5;
                }
                QPushButton:pressed {
                    background-color: #d5d5d5;
                }
            """)
            self.layout.addWidget(btn)
            
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.parent.close)
        
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

# Modern Tab Widget
class ModernTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setDocumentMode(True)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 8px 8px 0 0;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #e8e8e8;
            }
        """)

# AI Sidebar
class AISidebar(QWidget):
    def __init__(self, ai_assistant):
        super().__init__()
        self.ai_assistant = ai_assistant
        self.setFixedWidth(300)
        self.setStyleSheet("""
            AISidebar {
                background-color: #f8f9fa;
                border-left: 1px solid #e0e0e0;
            }
        ")
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("🤖 Nexa AI Assistant")
        header.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Chat area
        self.chat_area = QListWidget()
        self.chat_area.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: none;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.chat_area)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask AI...")
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        # Quick actions
        quick_actions = QWidget()
        quick_layout = QHBoxLayout(quick_actions)
        
        actions = ["Summarize", "Translate", "Explain"]
        for action in actions:
            btn = QPushButton(action)
            btn.setStyleSheet("font-size: 10px; padding: 4px;")
            btn.clicked.connect(lambda checked, a=action: self.quick_action(a))
            quick_layout.addWidget(btn)
            
        layout.addWidget(quick_actions)
        
        # Connect AI signals
        self.ai_assistant.response_received.connect(self.display_response)
        
    def send_message(self):
        query = self.input_field.text().strip()
        if query:
            self.display_message(query, "user")
            self.ai_assistant.process_query(query)
            self.input_field.clear()
            
    def quick_action(self, action):
        query = f"{action} this page"
        self.display_message(query, "user")
        self.ai_assistant.process_query(query)
        
    def display_message(self, message: str, sender: str):
        item = QListWidgetItem(f"{'You' if sender == 'user' else 'AI'}: {message}")
        self.chat_area.addItem(item)
        self.chat_area.scrollToBottom()
        
    def display_response(self, query: str, response: str):
        self.display_message(response, "ai")

# Home Page with Widgets
class HomePage(QWidget):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Welcome section
        welcome = QLabel("Welcome to Nexa Browser 🌐")
        welcome.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search or enter address...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #0078d4;
                border-radius: 25px;
                font-size: 14px;
                margin: 10px;
            }
        """)
        self.search_bar.returnPressed.connect(self.perform_search)
        
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)
        
        # Quick access grid
        quick_access = QLabel("Quick Access")
        quick_access.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(quick_access)
        
        grid_layout = QHBoxLayout()
        sites = [
            ("Google", "https://google.com"),
            ("YouTube", "https://youtube.com"),
            ("GitHub", "https://github.com"),
            ("Twitter", "https://twitter.com")
        ]
        
        for name, url in sites:
            btn = QPushButton(name)
            btn.setFixedSize(80, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            btn.clicked.connect(lambda checked, u=url: self.browser.open_url(u))
            grid_layout.addWidget(btn)
            
        layout.addLayout(grid_layout)
        
        # Calendar widget
        calendar_widget = self.create_calendar_widget()
        layout.addWidget(calendar_widget)
        
    def create_calendar_widget(self):
        group = QGroupBox("Calendar & Time")
        layout = QVBoxLayout(group)
        
        # Time display
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.update_time()
        
        # Calendar type selector
        self.calendar_combo = QComboBox()
        self.calendar_combo.addItems(["Gregorian", "Jalali", "Hijri", "Chinese"])
        self.calendar_combo.currentTextChanged.connect(self.update_time)
        
        layout.addWidget(self.time_label)
        layout.addWidget(QLabel("Calendar Type:"))
        layout.addWidget(self.calendar_combo)
        
        # Update time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        return group
        
    def update_time(self):
        now = datetime.now()
        calendar_type = self.calendar_combo.currentText()
        
        if calendar_type == "Gregorian":
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        elif calendar_type == "Jalali":
            # Simplified - in production use proper Jalali conversion
            time_str = f"Jalali: {now.strftime('%H:%M:%S')}"
        else:
            time_str = f"{calendar_type}: {now.strftime('%H:%M:%S')}"
            
        self.time_label.setText(time_str)
        
    def perform_search(self):
        query = self.search_bar.text()
        if query:
            if '.' in query and ' ' not in query:
                url = query if query.startswith('http') else f'https://{query}'
            else:
                url = f'https://google.com/search?q={quote(query)}'
            self.browser.open_url(url)

# First Run Wizard
class FirstRunWizard(QWizard):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setWindowTitle("Nexa Browser Setup")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QWizard {
                background-color: white;
            }
            QWizardPage {
                background-color: white;
            }
        """)
        
        self.addPage(WelcomePage())
        self.addPage(ThemePage())
        self.addPage(SearchEnginePage())
        self.addPage(AISetupPage())
        self.addPage(AdvancedPage())
        
    def accept(self):
        # Save settings
        settings = QSettings("NexaBrowser", "Settings")
        settings.setValue("first_run", False)
        settings.setValue("theme", self.field("theme"))
        settings.setValue("font_size", self.field("font_size"))
        settings.setValue("search_engine", self.field("search_engine"))
        settings.setValue("ai_enabled", self.field("ai_enabled"))
        
        super().accept()

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to Nexa Browser")
        
        layout = QVBoxLayout()
        welcome_label = QLabel("""
            <h1>Welcome to Nexa Browser! 🌐</h1>
            <p>Thank you for choosing Nexa Browser. Let's customize your browsing experience.</p>
            <p>This quick setup will help you configure the browser to your preferences.</p>
        """)
        welcome_label.setWordWrap(True)
        layout.addWidget(welcome_label)
        self.setLayout(layout)

class ThemePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Appearance Settings")
        
        layout = QVBoxLayout()
        
        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])
        theme_layout.addWidget(QLabel("Select Theme:"))
        theme_layout.addWidget(self.theme_combo)
        self.registerField("theme", self.theme_combo, "currentText")
        
        # Font size
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(font_group)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size)
        self.registerField("font_size", self.font_size, "value")
        
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        self.setLayout(layout)

class SearchEnginePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Search Settings")
        
        layout = QVBoxLayout()
        
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo"])
        layout.addWidget(QLabel("Default Search Engine:"))
        layout.addWidget(self.search_combo)
        self.registerField("search_engine", self.search_combo, "currentText")
        
        self.setLayout(layout)

class AISetupPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("AI Assistant Setup")
        
        layout = QVBoxLayout()
        
        self.ai_enabled = QCheckBox("Enable AI Assistant")
        self.ai_enabled.setChecked(True)
        layout.addWidget(self.ai_enabled)
        self.registerField("ai_enabled", self.ai_enabled)
        
        ai_desc = QLabel("""
            <p>The AI Assistant can help you with:</p>
            <ul>
                <li>Page summarization</li>
                <li>Real-time translation</li>
                <li>Content explanation</li>
                <li>Smart search</li>
            </ul>
        """)
        ai_desc.setWordWrap(True)
        layout.addWidget(ai_desc)
        
        self.setLayout(layout)

class AdvancedPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Advanced Settings")
        
        layout = QVBoxLayout()
        
        options = [
            ("Enable hardware acceleration", True),
            ("Show bookmark bar", True),
            ("Block pop-ups", True),
            ("Enable do not track", False)
        ]
        
        for text, default in options:
            checkbox = QCheckBox(text)
            checkbox.setChecked(default)
            layout.addWidget(checkbox)
            
        self.setLayout(layout)

# Download Manager Dialog
class DownloadManagerDialog(QDialog):
    def __init__(self, download_manager):
        super().__init__()
        self.download_manager = download_manager
        self.setWindowTitle("Downloads")
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Downloads list
        self.downloads_list = QListWidget()
        layout.addWidget(self.downloads_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Completed")
        self.open_btn = QPushButton("Open Folder")
        self.close_btn = QPushButton("Close")
        
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.open_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.clear_btn.clicked.connect(self.clear_completed)
        self.open_btn.clicked.connect(self.open_download_folder)
        self.close_btn.clicked.connect(self.close)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_list)
        self.update_timer.start(1000)
        
    def update_list(self):
        self.downloads_list.clear()
        for dl in self.download_manager.downloads:
            item_text = f"{dl['path']} - {dl['progress']:.1f}%"
            if dl['status'] == 'completed':
                item_text += " ✓"
            item = QListWidgetItem(item_text)
            self.downloads_list.addItem(item)
            
    def clear_completed(self):
        self.download_manager.downloads = [dl for dl in self.download_manager.downloads 
                                         if dl['status'] != 'completed']
        
    def open_download_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.download_manager.download_folder))

# Main Browser Window
class NexaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("NexaBrowser", "Settings")
        self.download_manager = DownloadManager()
        self.ai_assistant = AIAssistant()
        
        self.check_first_run()
        self.setup_ui()
        self.apply_settings()
        
    def check_first_run(self):
        if self.settings.value("first_run", True, type=bool):
            wizard = FirstRunWizard(self)
            wizard.exec()
            
    def setup_ui(self):
        self.setWindowTitle("Nexa Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title bar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Browser area
        self.browser_area = QWidget()
        browser_layout = QVBoxLayout(self.browser_area)
        browser_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        self.setup_toolbar()
        browser_layout.addWidget(self.toolbar)
        
        # Tab widget
        self.tabs = ModernTabWidget()
        self.tabs.tabCloseRequested.connect(self.close_tab)
        browser_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        browser_layout.addWidget(self.status_bar)
        
        content_splitter.addWidget(self.browser_area)
        
        # AI Sidebar (initially hidden)
        self.ai_sidebar = AISidebar(self.ai_assistant)
        self.ai_sidebar.hide()
        content_splitter.addWidget(self.ai_sidebar)
        
        content_splitter.setSizes([800, 300])
        
        # Create initial tab
        self.add_new_tab()
        
    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(20, 20))
        
        # Navigation buttons
        self.back_btn = QAction("←", self)
        self.forward_btn = QAction("→", self)
        self.reload_btn = QAction("↻", self)
        self.home_btn = QAction("🏠", self)
        
        self.back_btn.triggered.connect(self.navigate_back)
        self.forward_btn.triggered.connect(self.navigate_forward)
        self.reload_btn.triggered.connect(self.reload_page)
        self.home_btn.triggered.connect(self.go_home)
        
        self.toolbar.addAction(self.back_btn)
        self.toolbar.addAction(self.forward_btn)
        self.toolbar.addAction(self.reload_btn)
        self.toolbar.addAction(self.home_btn)
        
        self.toolbar.addSeparator()
        
        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)
        
        self.toolbar.addSeparator()
        
        # AI toggle
        self.ai_toggle = QAction("🤖", self)
        self.ai_toggle.triggered.connect(self.toggle_ai_sidebar)
        self.toolbar.addAction(self.ai_toggle)
        
        # Downloads
        self.downloads_btn = QAction("📥", self)
        self.downloads_btn.triggered.connect(self.show_downloads)
        self.toolbar.addAction(self.downloads_btn)
        
        # New tab
        self.new_tab_btn = QAction("➕", self)
        self.new_tab_btn.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(self.new_tab_btn)
        
    def add_new_tab(self, url: str = None):
        if url is None:
            url = "https://www.google.com"
            
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        
        # Connect signals
        browser.urlChanged.connect(lambda qurl: self.update_urlbar(qurl, browser))
        browser.loadProgress.connect(lambda p: self.status_bar.showMessage(f"Loading... {p}%"))
        browser.loadFinished.connect(lambda: self.status_bar.clearMessage())
        
        # Setup download handler
        profile = browser.page().profile()
        profile.downloadRequested.connect(self.download_manager.add_download)
        
        # Add tab
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        # Update title when page loads
        browser.titleChanged.connect(lambda title: self.tabs.setTabText(index, title[:15]))
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            
    def navigate_to_url(self):
        url = self.url_bar.text()
        self.open_url(url)
        
    def open_url(self, url: str):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            current_browser.setUrl(QUrl(url))
            
    def update_urlbar(self, qurl: QUrl, browser: QWebEngineView = None):
        if browser != self.tabs.currentWidget():
            return
            
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)
        
    def navigate_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()
            
    def navigate_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()
            
    def reload_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()
            
    def go_home(self):
        self.open_url("https://www.google.com")
        
    def toggle_ai_sidebar(self):
        if self.ai_sidebar.isVisible():
            self.ai_sidebar.hide()
        else:
            self.ai_sidebar.show()
            
    def show_downloads(self):
        dialog = DownloadManagerDialog(self.download_manager)
        dialog.exec()
        
    def apply_settings(self):
        # Apply theme
        theme = self.settings.value("theme", "Light")
        self.apply_theme(theme)
        
        # Apply font size
        font_size = self.settings.value("font_size", 12, type=int)
        app = QApplication.instance()
        app.setFont(QFont("Segoe UI", font_size))
        
        # Apply AI settings
        ai_enabled = self.settings.value("ai_enabled", True, type=bool)
        self.ai_assistant.enable(ai_enabled)
        
    def apply_theme(self, theme: str):
        if theme == "Dark" or (theme == "Auto" and self.is_dark_time()):
            self.set_dark_theme()
        else:
            self.set_light_theme()
            
    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        app = QApplication.instance()
        app.setPalette(dark_palette)
        
    def set_light_theme(self):
        app = QApplication.instance()
        app.setPalette(app.style().standardPalette())
        
    def is_dark_time(self):
        now = datetime.now().time()
        return now.hour >= 18 or now.hour < 6

# Custom Status Bar
class QStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QStatusBar {
                background-color: #f0f0f0;
                border-top: 1px solid #e0e0e0;
            }
        """)

# Application Entry Point
def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Hessamedien")
    
    # Set modern fusion style
    app.setStyle(QStyleFactory.create("Fusion"))
    
    browser = NexaBrowser()
    browser.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
