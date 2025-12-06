#!/usr/bin/env python3
"""
Nexa Browser - Modern, Lightweight, Highly Customizable AI-Powered Web Browser
Creator: Hessamedien (https://www.instagram.com/hessamedien)
Platform: Windows 11+
Style: Fluent Design, Office-inspired UI, modern aesthetics
"""

import sys
import os
import json
import tempfile
import math
from pathlib import Path
from datetime import datetime
import webbrowser

# Third-party imports (you'll need to install these)
try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QTabWidget, QLineEdit, QToolButton, 
                                QToolBar, QLabel, QPushButton, QFrame, QSplitter,
                                QDialog, QWizard, QWizardPage, QComboBox, QCheckBox,
                                QSpinBox, QListWidget, QStackedWidget, QProgressBar,
                                QMessageBox, QSystemTrayIcon, QMenu, QStyle)
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
    from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, QSettings, pyqtSignal, QPoint
    from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QAction, QPalette
except ImportError:
    print("Required PyQt6 modules not found. Please install PyQt6 and PyQtWebEngine:")
    print("pip install PyQt6 PyQtWebEngine")
    sys.exit(1)


class BlackWhiteIcons:
    """Utility class for creating black and white icons programmatically"""
    
    @staticmethod
    def create_icon(name, size=24):
        """Create a simple black and white icon based on name"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set color based on theme (will be adjusted in runtime)
        color = QColor(0, 0, 0)  # Default black
        painter.setPen(color)
        painter.setBrush(color)
        
        if name == "home":
            # Home icon (house shape)
            painter.drawRect(8, 12, 8, 8)
            points = [QPoint(12, 6), QPoint(16, 10), QPoint(8, 10)]
            painter.drawPolygon(points)
        elif name == "back":
            # Back arrow
            points = [QPoint(16, 6), QPoint(8, 12), QPoint(16, 18)]
            painter.drawPolygon(points)
        elif name == "forward":
            # Forward arrow
            points = [QPoint(8, 6), QPoint(16, 12), QPoint(8, 18)]
            painter.drawPolygon(points)
        elif name == "refresh":
            # Refresh icon (circular arrow)
            painter.drawEllipse(6, 6, 12, 12)
            painter.drawLine(16, 8, 14, 6)
        elif name == "search":
            # Search icon (magnifying glass)
            painter.drawEllipse(6, 6, 10, 10)
            painter.drawLine(14, 14, 16, 16)
        elif name == "settings":
            # Settings icon (gear)
            painter.drawEllipse(7, 7, 10, 10)
            painter.drawRect(11, 5, 2, 4)
            painter.drawRect(11, 15, 2, 4)
            painter.drawRect(5, 11, 4, 2)
            painter.drawRect(15, 11, 4, 2)
        elif name == "download":
            # Download icon (arrow down)
            painter.drawLine(12, 6, 12, 16)
            painter.drawLine(12, 16, 8, 12)
            painter.drawLine(12, 16, 16, 12)
        elif name == "star":
            # Star icon
            points = []
            for i in range(5):
                angle = math.radians(i * 72 - 90)
                x = 12 + int(8 * math.cos(angle))
                y = 12 + int(8 * math.sin(angle))
                points.append(QPoint(x, y))
            painter.drawPolygon(points)
        elif name == "menu":
            # Menu icon (hamburger)
            painter.drawRect(6, 8, 12, 2)
            painter.drawRect(6, 11, 12, 2)
            painter.drawRect(6, 14, 12, 2)
        else:
            # Default icon (square)
            painter.drawRect(6, 6, 12, 12)
        
        painter.end()
        return QIcon(pixmap)


class FirstRunWizard(QWizard):
    """First-run wizard for initial browser configuration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nexa Browser Setup")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedSize(600, 500)
        
        # Pages
        self.addPage(WelcomePage())
        self.addPage(ThemePage())
        self.addPage(SearchPage())
        self.addPage(AIPage())
        self.addPage(FinishPage())
        
        self.settings = {}
    
    def get_settings(self):
        """Return the collected settings"""
        # Collect all field values
        self.settings = {
            'theme': self.field("theme"),
            'font': self.field("font"),
            'font_size': self.field("font_size"),
            'search_engine': self.field("search_engine"),
            'homepage': self.field("homepage"),
            'ai_enabled': self.field("ai_enabled"),
            'ai_provider': self.field("ai_provider"),
            'ai_position': self.field("ai_position")
        }
        return self.settings


class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to Nexa Browser")
        self.setSubTitle("Let's set up your browsing experience")
        
        layout = QVBoxLayout()
        label = QLabel("Thank you for choosing Nexa Browser! This wizard will help you configure your browser settings.")
        label.setWordWrap(True)
        layout.addWidget(label)
        
        self.setLayout(layout)


class ThemePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Appearance Settings")
        self.setSubTitle("Choose your preferred theme and font settings")
        
        layout = QVBoxLayout()
        
        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Auto (System)", "Dark", "Light", "High Contrast"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        # Font selection
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Verdana"])
        font_layout.addWidget(self.font_combo)
        font_layout.addStretch()
        layout.addLayout(font_layout)
        
        # Font size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Font Size:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 24)
        self.size_spin.setValue(12)
        size_layout.addWidget(self.size_spin)
        size_layout.addStretch()
        layout.addLayout(size_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Register fields
        self.registerField("theme", self.theme_combo, "currentText")
        self.registerField("font", self.font_combo, "currentText")
        self.registerField("font_size", self.size_spin, "value")


class SearchPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Search Settings")
        self.setSubTitle("Configure your default search engine and homepage")
        
        layout = QVBoxLayout()
        
        # Search engine
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Engine:"))
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo", "Custom"])
        search_layout.addWidget(self.search_combo)
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # Homepage
        home_layout = QHBoxLayout()
        home_layout.addWidget(QLabel("Homepage:"))
        self.home_edit = QLineEdit()
        self.home_edit.setText("https://www.google.com")
        home_layout.addWidget(self.home_edit)
        layout.addLayout(home_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("search_engine", self.search_combo, "currentText")
        self.registerField("homepage", self.home_edit)


class AIPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("AI Assistant Settings")
        self.setSubTitle("Configure the built-in AI assistant")
        
        layout = QVBoxLayout()
        
        # Enable AI
        self.ai_checkbox = QCheckBox("Enable AI Assistant")
        self.ai_checkbox.setChecked(True)
        layout.addWidget(self.ai_checkbox)
        
        # AI Provider
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("AI Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI GPT", "Local Model", "Custom API"])
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        layout.addLayout(provider_layout)
        
        # AI Position
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("AI Panel Position:"))
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Sidebar", "Bottom Panel", "Floating"])
        position_layout.addWidget(self.position_combo)
        position_layout.addStretch()
        layout.addLayout(position_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("ai_enabled", self.ai_checkbox)
        self.registerField("ai_provider", self.provider_combo, "currentText")
        self.registerField("ai_position", self.position_combo, "currentText")


class FinishPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Setup Complete")
        self.setSubTitle("Your browser is ready to use!")
        
        layout = QVBoxLayout()
        label = QLabel("Click Finish to start using Nexa Browser with your customized settings.")
        label.setWordWrap(True)
        layout.addWidget(label)
        
        self.setLayout(layout)


class BrowserTab(QWebEngineView):
    """Individual browser tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        
        # Configure settings for better performance
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        
        # Connect signals
        self.urlChanged.connect(self.on_url_changed)
        self.titleChanged.connect(self.on_title_changed)
        self.loadProgress.connect(self.on_load_progress)
        self.loadFinished.connect(self.on_load_finished)
    
    def on_url_changed(self, url):
        if self.parent_browser and hasattr(self.parent_browser, 'update_url_bar'):
            self.parent_browser.update_url_bar(url)
    
    def on_title_changed(self, title):
        if self.parent_browser and hasattr(self.parent_browser, 'update_tab_title'):
            self.parent_browser.update_tab_title(self, title)
    
    def on_load_progress(self, progress):
        if self.parent_browser and hasattr(self.parent_browser, 'update_progress'):
            self.parent_browser.update_progress(progress)
    
    def on_load_finished(self, ok):
        if self.parent_browser and hasattr(self.parent_browser, 'page_loaded'):
            self.parent_browser.page_loaded(ok)


class AIPanel(QWidget):
    """AI Assistant Panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Nexa AI Assistant")
        header.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")
        layout.addWidget(header)
        
        # Chat area
        self.chat_area = QListWidget()
        layout.addWidget(self.chat_area)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me anything...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        
        # AI Features
        features_layout = QHBoxLayout()
        self.summarize_btn = QPushButton("Summarize")
        self.summarize_btn.clicked.connect(self.summarize_page)
        features_layout.addWidget(self.summarize_btn)
        
        self.translate_btn = QPushButton("Translate")
        self.translate_btn.clicked.connect(self.translate_page)
        features_layout.addWidget(self.translate_btn)
        
        layout.addLayout(features_layout)
        
        self.setLayout(layout)
    
    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            self.chat_area.addItem(f"You: {message}")
            self.input_field.clear()
            
            # Simulate AI response (in a real implementation, this would call an AI API)
            self.chat_area.addItem("AI: I'm a simulated AI response. In a full implementation, I would provide intelligent answers.")
    
    def summarize_page(self):
        self.chat_area.addItem("AI: Page summarization would appear here in the full implementation.")
    
    def translate_page(self):
        self.chat_area.addItem("AI: Translation feature would be available in the full implementation.")


class DownloadManager(QWidget):
    """Download manager similar to Free Download Manager"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.downloads = []
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Downloads")
        header.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")
        layout.addWidget(header)
        
        # Downloads list
        self.downloads_list = QListWidget()
        layout.addWidget(self.downloads_list)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_download)
        controls_layout.addWidget(self.pause_btn)
        
        self.resume_btn = QPushButton("Resume")
        self.resume_btn.clicked.connect(self.resume_download)
        controls_layout.addWidget(self.resume_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_download)
        controls_layout.addWidget(self.cancel_btn)
        
        self.clear_btn = QPushButton("Clear Completed")
        self.clear_btn.clicked.connect(self.clear_completed)
        controls_layout.addWidget(self.clear_btn)
        
        layout.addLayout(controls_layout)
        
        # Progress and info
        info_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        info_layout.addWidget(self.progress_bar)
        
        self.info_label = QLabel("No active downloads")
        info_layout.addWidget(self.info_label)
        
        layout.addLayout(info_layout)
        
        self.setLayout(layout)
    
    def add_download(self, url, path):
        """Add a new download"""
        download_item = {
            'url': url,
            'path': path,
            'progress': 0,
            'status': 'downloading'  # downloading, paused, completed, cancelled
        }
        self.downloads.append(download_item)
        self.downloads_list.addItem(f"Downloading: {os.path.basename(path)}")
        
        # Simulate download progress (in real implementation, this would be actual download)
        self.simulate_download(len(self.downloads) - 1)
    
    def simulate_download(self, index):
        """Simulate download progress (for demo purposes)"""
        if index < len(self.downloads):
            timer = QTimer(self)
            timer.timeout.connect(lambda: self.update_progress(index, timer))
            timer.start(100)  # Update every 100ms
    
    def update_progress(self, index, timer):
        """Update download progress"""
        if index < len(self.downloads) and self.downloads[index]['status'] == 'downloading':
            self.downloads[index]['progress'] += 5
            self.progress_bar.setValue(self.downloads[index]['progress'])
            
            if self.downloads[index]['progress'] >= 100:
                self.downloads[index]['status'] = 'completed'
                self.downloads_list.item(index).setText(f"Completed: {os.path.basename(self.downloads[index]['path'])}")
                self.info_label.setText("Download completed")
                timer.stop()
    
    def pause_download(self):
        """Pause selected download"""
        current_row = self.downloads_list.currentRow()
        if current_row >= 0 and current_row < len(self.downloads):
            self.downloads[current_row]['status'] = 'paused'
            self.info_label.setText("Download paused")
    
    def resume_download(self):
        """Resume selected download"""
        current_row = self.downloads_list.currentRow()
        if current_row >= 0 and current_row < len(self.downloads):
            self.downloads[current_row]['status'] = 'downloading'
            self.info_label.setText("Download resuming...")
            self.simulate_download(current_row)
    
    def cancel_download(self):
        """Cancel selected download"""
        current_row = self.downloads_list.currentRow()
        if current_row >= 0 and current_row < len(self.downloads):
            self.downloads[current_row]['status'] = 'cancelled'
            self.downloads_list.item(current_row).setText(f"Cancelled: {os.path.basename(self.downloads[current_row]['path'])}")
            self.info_label.setText("Download cancelled")
    
    def clear_completed(self):
        """Clear completed downloads from list"""
        for i in range(self.downloads_list.count() - 1, -1, -1):
            if i < len(self.downloads) and self.downloads[i]['status'] == 'completed':
                self.downloads_list.takeItem(i)
                if i < len(self.downloads):
                    self.downloads.pop(i)


class HomePage(QWidget):
    """Customizable homepage with widgets and mini-apps"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Header with search
        header_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search or enter address...")
        self.search_bar.returnPressed.connect(self.perform_search)
        header_layout.addWidget(self.search_bar)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)
        header_layout.addWidget(search_btn)
        
        layout.addLayout(header_layout)
        
        # Quick links
        quick_links_layout = QVBoxLayout()
        quick_links_label = QLabel("Quick Links")
        quick_links_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        quick_links_layout.addWidget(quick_links_label)
        
        links_grid = QHBoxLayout()
        links = [
            ("Google", "https://www.google.com"),
            ("YouTube", "https://www.youtube.com"),
            ("Gmail", "https://mail.google.com"),
            ("GitHub", "https://github.com")
        ]
        
        for name, url in links:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, u=url: self.open_link(u))
            links_grid.addWidget(btn)
        
        quick_links_layout.addLayout(links_grid)
        layout.addLayout(quick_links_layout)
        
        # Date and time widget
        time_layout = QVBoxLayout()
        time_label = QLabel("Date & Time")
        time_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        time_layout.addWidget(time_label)
        
        self.time_display = QLabel()
        self.time_display.setStyleSheet("font-size: 14px; padding: 5px;")
        time_layout.addWidget(self.time_display)
        
        # Calendar type selector
        calendar_layout = QHBoxLayout()
        calendar_layout.addWidget(QLabel("Calendar:"))
        self.calendar_combo = QComboBox()
        self.calendar_combo.addItems(["Gregorian", "Jalali", "Hijri", "Hebrew", "Chinese"])
        self.calendar_combo.currentTextChanged.connect(self.update_time_display)
        calendar_layout.addWidget(self.calendar_combo)
        calendar_layout.addStretch()
        time_layout.addLayout(calendar_layout)
        
        layout.addLayout(time_layout)
        
        # Mini apps area
        apps_layout = QVBoxLayout()
        apps_label = QLabel("Mini Apps")
        apps_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        apps_layout.addWidget(apps_label)
        
        apps_grid = QHBoxLayout()
        app_buttons = [
            ("Notes", self.open_notes),
            ("Calculator", self.open_calculator),
            ("Weather", self.open_weather)
        ]
        
        for name, handler in app_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(handler)
            apps_grid.addWidget(btn)
        
        apps_layout.addLayout(apps_grid)
        layout.addLayout(apps_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Start time updates
        self.update_time_display()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_display)
        self.timer.start(1000)  # Update every second
    
    def perform_search(self):
        query = self.search_bar.text().strip()
        if query:
            if '.' in query and ' ' not in query:
                # Likely a URL
                if not query.startswith(('http://', 'https://')):
                    query = 'https://' + query
                self.parent_browser.current_tab().setUrl(QUrl(query))
            else:
                # Search query
                search_url = f"https://www.google.com/search?q={query}"
                self.parent_browser.current_tab().setUrl(QUrl(search_url))
    
    def open_link(self, url):
        self.parent_browser.current_tab().setUrl(QUrl(url))
    
    def update_time_display(self):
        now = datetime.now()
        calendar_type = self.calendar_combo.currentText()
        
        if calendar_type == "Gregorian":
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        elif calendar_type == "Jalali":
            # In a real implementation, you would use a library like jdatetime
            time_str = f"Jalali: {now.strftime('%H:%M:%S')} (Not implemented)"
        elif calendar_type == "Hijri":
            time_str = f"Hijri: {now.strftime('%H:%M:%S')} (Not implemented)"
        else:
            time_str = f"{calendar_type}: {now.strftime('%H:%M:%S')} (Not implemented)"
        
        self.time_display.setText(time_str)
    
    def open_notes(self):
        QMessageBox.information(self, "Notes", "Notes app would open here in full implementation")
    
    def open_calculator(self):
        QMessageBox.information(self, "Calculator", "Calculator app would open here in full implementation")
    
    def open_weather(self):
        QMessageBox.information(self, "Weather", "Weather app would open here in full implementation")


class NexaBrowser(QMainWindow):
    """Main browser window"""
    
    def __init__(self, first_run_settings=None):
        super().__init__()
        
        # Apply first run settings or load from storage
        self.settings = first_run_settings or self.load_settings()
        
        # Initialize UI
        self.setup_ui()
        self.apply_theme()
        
        # Create first tab
        self.add_new_tab()
        
        # Show homepage initially
        self.show_homepage()
    
    def setup_ui(self):
        """Set up the main browser UI"""
        self.setWindowTitle("Nexa Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create toolbar
        self.create_toolbar()
        main_layout.addWidget(self.toolbar)
        
        # Create main content area with splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Left panel (for AI or bookmarks)
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(300)
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        
        # AI Panel
        self.ai_panel = AIPanel(self)
        self.left_panel_layout.addWidget(self.ai_panel)
        
        self.splitter.addWidget(self.left_panel)
        
        # Main browser area
        self.browser_area = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_area)
        self.browser_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        
        self.browser_layout.addWidget(self.tabs)
        self.splitter.addWidget(self.browser_area)
        
        # Set splitter proportions
        self.splitter.setSizes([200, 800])
        
        # Status bar
        self.status_bar = self.statusBar()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Apply theme
        self.apply_theme()
    
    def create_toolbar(self):
        """Create the main toolbar with navigation buttons"""
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(20, 20))
        
        # Back button
        back_btn = QToolButton()
        back_btn.setIcon(BlackWhiteIcons.create_icon("back"))
        back_btn.clicked.connect(self.navigate_back)
        self.toolbar.addWidget(back_btn)
        
        # Forward button
        forward_btn = QToolButton()
        forward_btn.setIcon(BlackWhiteIcons.create_icon("forward"))
        forward_btn.clicked.connect(self.navigate_forward)
        self.toolbar.addWidget(forward_btn)
        
        # Refresh button
        refresh_btn = QToolButton()
        refresh_btn.setIcon(BlackWhiteIcons.create_icon("refresh"))
        refresh_btn.clicked.connect(self.refresh_page)
        self.toolbar.addWidget(refresh_btn)
        
        # Home button
        home_btn = QToolButton()
        home_btn.setIcon(BlackWhiteIcons.create_icon("home"))
        home_btn.clicked.connect(self.show_homepage)
        self.toolbar.addWidget(home_btn)
        
        self.toolbar.addSeparator()
        
        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)
        
        # Search button
        search_btn = QToolButton()
        search_btn.setIcon(BlackWhiteIcons.create_icon("search"))
        search_btn.clicked.connect(self.navigate_to_url)
        self.toolbar.addWidget(search_btn)
        
        self.toolbar.addSeparator()
        
        # New tab button
        new_tab_btn = QToolButton()
        new_tab_btn.setText("+")
        new_tab_btn.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(new_tab_btn)
        
        # Downloads button
        downloads_btn = QToolButton()
        downloads_btn.setIcon(BlackWhiteIcons.create_icon("download"))
        downloads_btn.clicked.connect(self.show_downloads)
        self.toolbar.addWidget(downloads_btn)
        
        # Settings button
        settings_btn = QToolButton()
        settings_btn.setIcon(BlackWhiteIcons.create_icon("settings"))
        settings_btn.clicked.connect(self.show_settings)
        self.toolbar.addWidget(settings_btn)
    
    def add_new_tab(self, url=None):
        """Add a new browser tab"""
        if url is None:
            url = QUrl("https://www.google.com")
        
        browser_tab = BrowserTab(self)
        browser_tab.setUrl(url)
        
        # Add to tabs
        index = self.tabs.addTab(browser_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        return browser_tab
    
    def close_tab(self, index):
        """Close a browser tab"""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
    
    def current_tab(self):
        """Get the current browser tab"""
        return self.tabs.currentWidget()
    
    def navigate_back(self):
        """Navigate back in current tab"""
        if self.current_tab():
            self.current_tab().back()
    
    def navigate_forward(self):
        """Navigate forward in current tab"""
        if self.current_tab():
            self.current_tab().forward()
    
    def refresh_page(self):
        """Refresh current tab"""
        if self.current_tab():
            self.current_tab().reload()
    
    def navigate_to_url(self):
        """Navigate to URL in address bar"""
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if self.current_tab():
            self.current_tab().setUrl(QUrl(url))
    
    def show_homepage(self):
        """Show the custom homepage"""
        homepage = HomePage(self)
        index = self.tabs.currentIndex()
        self.tabs.insertTab(index, homepage, "Home")
        self.tabs.setCurrentIndex(index)
        # Don't remove the original tab - just switch to homepage
    
    def show_downloads(self):
        """Show download manager"""
        downloads_dialog = QDialog(self)
        downloads_dialog.setWindowTitle("Download Manager")
        downloads_dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        download_manager = DownloadManager(self)
        layout.addWidget(download_manager)
        
        # Add a test download for demonstration
        test_url = "https://example.com/samplefile.zip"
        test_path = os.path.join(tempfile.gettempdir(), "samplefile.zip")
        download_manager.add_download(test_url, test_path)
        
        downloads_dialog.setLayout(layout)
        downloads_dialog.exec()
    
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", "Settings dialog would open here in full implementation")
    
    def update_url_bar(self, url):
        """Update the URL bar when page changes"""
        if self.current_tab() and self.sender() == self.current_tab():
            self.url_bar.setText(url.toString())
    
    def update_tab_title(self, tab, title):
        """Update tab title when page title changes"""
        index = self.tabs.indexOf(tab)
        if index != -1:
            # Shorten long titles
            if len(title) > 20:
                title = title[:20] + "..."
            self.tabs.setTabText(index, title)
    
    def update_progress(self, progress):
        """Update progress bar"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setVisible(progress < 100)
    
    def page_loaded(self, ok):
        """Handle page loaded event"""
        if not ok:
            self.status_bar.showMessage("Failed to load page", 3000)
        else:
            self.status_bar.showMessage("Page loaded", 2000)
    
    def tab_changed(self, index):
        """Handle tab change"""
        if index >= 0 and self.tabs.widget(index):
            current_tab = self.tabs.widget(index)
            if hasattr(current_tab, 'url'):
                self.update_url_bar(current_tab.url())
    
    def apply_theme(self):
        """Apply theme based on settings"""
        theme = self.settings.get('theme', 'Auto (System)')
        
        if theme == "Dark" or (theme == "Auto (System)" and self.is_dark_mode()):
            self.set_dark_theme()
        else:
            self.set_light_theme()
    
    def is_dark_mode(self):
        """Check if system is in dark mode"""
        # This is a simplified check - in a real implementation, 
        # you would use platform-specific APIs
        return False  # Placeholder
    
    def set_dark_theme(self):
        """Apply dark theme"""
        dark_stylesheet = """
        QMainWindow, QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QToolBar {
            background-color: #3c3c3c;
            border: none;
            spacing: 5px;
            padding: 5px;
        }
        QLineEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 3px;
            padding: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #2b2b2b;
        }
        QTabBar::tab {
            background-color: #3c3c3c;
            color: #ffffff;
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #2b2b2b;
            border-bottom: 2px solid #0078d7;
        }
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 3px;
            padding: 5px;
        }
        QToolButton:hover {
            background-color: #404040;
        }
        QPushButton {
            background-color: #005a9e;
            color: white;
            border: none;
            border-radius: 3px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #0078d7;
        }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def set_light_theme(self):
        """Apply light theme"""
        light_stylesheet = """
        QMainWindow, QWidget {
            background-color: #ffffff;
            color: #000000;
        }
        QToolBar {
            background-color: #f3f3f3;
            border: none;
            spacing: 5px;
            padding: 5px;
        }
        QLineEdit {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 3px;
            padding: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #ccc;
            background-color: #ffffff;
        }
        QTabBar::tab {
            background-color: #f3f3f3;
            color: #000000;
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #ffffff;
            border-bottom: 2px solid #0078d7;
        }
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 3px;
            padding: 5px;
        }
        QToolButton:hover {
            background-color: #e1e1e1;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 3px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        """
        self.setStyleSheet(light_stylesheet)
    
    def load_settings(self):
        """Load settings from storage"""
        # In a real implementation, this would load from a config file
        return {
            'theme': 'Auto (System)',
            'font': 'Segoe UI',
            'font_size': 12,
            'search_engine': 'Google',
            'homepage': 'https://www.google.com',
            'ai_enabled': True,
            'ai_provider': 'OpenAI GPT',
            'ai_position': 'Sidebar'
        }
    
    def save_settings(self):
        """Save settings to storage"""
        # In a real implementation, this would save to a config file
        pass


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Hessamedien")
    
    # Check if first run - use a simple approach
    settings = QSettings("Hessamedien", "Nexa Browser")
    first_run = settings.value("first_run", True, type=bool)
    
    if first_run:
        # Show first-run wizard
        wizard = FirstRunWizard()
        if wizard.exec() == QWizard.WizardResult.Accepted:
            # Get settings from wizard
            browser_settings = wizard.get_settings()
            # Mark first run as complete
            settings.setValue("first_run", False)
            settings.setValue("user_settings", browser_settings)
            
            # Create and show browser with settings
            browser = NexaBrowser(browser_settings)
            browser.show()
            
            # Start the application event loop
            sys.exit(app.exec())
        else:
            # User cancelled wizard
            sys.exit(0)
    else:
        # Load existing settings and start browser
        browser_settings = settings.value("user_settings", {})
        browser = NexaBrowser(browser_settings)
        browser.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()