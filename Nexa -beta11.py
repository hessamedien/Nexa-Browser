import sys
import os
import json
import tempfile
import sqlite3
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTabWidget, QLineEdit, QToolBar, 
                            QStatusBar, QPushButton, QLabel, QProgressBar,
                            QDialog, QWizard, QWizardPage, QComboBox, 
                            QCheckBox, QSpinBox, QGroupBox, QListWidget,
                            QSplitter, QFrame, QMessageBox, QToolButton,
                            QStackedWidget, QScrollArea, QGridLayout, QListWidgetItem,
                            QDialogButtonBox, QFormLayout, QTextEdit, QSystemTrayIcon,
                            QMenu, QStyle, QSizePolicy, QRadioButton, QButtonGroup)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt, QSize, pyqtSignal, QTimer, QDateTime, QSettings, QPoint, QFileInfo
from PyQt6.QtGui import (QIcon, QPalette, QColor, QFont, QAction, QPixmap, QDesktopServices, 
                        QGuiApplication, QPainter, QLinearGradient, QBrush, QPen)

class FluentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw window background with blur effect simulation
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(40, 40, 40, 240))
        gradient.setColorAt(1, QColor(30, 30, 30, 240))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRoundedRect(self.rect(), 12, 12)

class FirstRunWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexa Browser Setup")
        self.setFixedSize(800, 600)
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setOption(QWizard.WizardOption.IndependentPages, True)
        
        self.settings = {}
        self.setStyleSheet("""
            QWizard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #3498db);
                color: white;
                border-radius: 12px;
            }
            QWizardPage {
                background: rgba(40, 40, 40, 220);
                border-radius: 10px;
                color: white;
            }
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #3498db;
            }
            QLabel {
                color: white;
            }
            QComboBox, QLineEdit, QSpinBox {
                background: rgba(255,255,255,0.1);
                border: 1px solid #7f8c8d;
                border-radius: 3px;
                padding: 5px;
                color: white;
            }
            QCheckBox {
                color: white;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #7f8c8d;
                border-radius: 3px;
                background: rgba(255,255,255,0.1);
            }
            QCheckBox::indicator:checked {
                background: #3498db;
                border: 1px solid #3498db;
            }
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        
        self.addPage(WelcomePage())
        self.addPage(ThemePage())
        self.addPage(HomePageConfig())
        self.addPage(SearchPage())
        self.addPage(AIPage())
        self.addPage(ProfessionalPage())
        self.addPage(CompletionPage())
        
    def get_settings(self):
        # Collect all field values
        settings = {}
        field_names = [
            "theme", "font_family", "font_size", "ui_density",
            "home_layout", "calendar_type", "time_format", "show_weather",
            "search_engine", "custom_search_url", "block_ads", "https_only", 
            "clear_on_exit", "dnt_header", "ai_enabled", "page_summary",
            "translation", "smart_fill", "content_gen", "ai_position", 
            "auto_trigger", "dev_tools", "js_console", "inspector",
            "hardware_accel", "memory_saver", "cache_optimize", "pwa_support",
            "vertical_tabs", "tab_groups"
        ]
        
        for field in field_names:
            if self.field(field) is not None:
                settings[field] = self.field(field)
        
        return settings

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("🚀 Welcome to Nexa Browser")
        self.setSubTitle("Your AI-Powered, Privacy-Focused Browsing Experience")
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Nexa Browser")
        header.setStyleSheet("font-size: 32px; font-weight: bold; color: #3498db; margin: 20px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Welcome message
        welcome_text = QLabel(
            "Thank you for choosing Nexa Browser - the next generation of web browsing!\n\n"
            "This quick setup will help you personalize your browsing experience with:\n"
            "• 🎨 Custom themes and appearance\n"
            "• 🤖 Built-in AI assistant\n"
            "• 🛡️ Enhanced privacy protection\n"
            "• ⚡ Performance optimization\n"
            "• 🛠️ Professional tools\n\n"
            "Let's create your perfect browser in just a few steps!"
        )
        welcome_text.setWordWrap(True)
        welcome_text.setStyleSheet("font-size: 14px; line-height: 1.5; margin: 20px;")
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_text)
        
        layout.addStretch()
        
        # Creator credit
        creator = QLabel("Created by Hessamedien")
        creator.setStyleSheet("color: #7f8c8d; margin: 10px;")
        creator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(creator)
        
        self.setLayout(layout)

class ThemePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("🎨 Appearance & Theme")
        self.setSubTitle("Customize the look and feel of your browser")
        
        layout = QVBoxLayout()
        
        # Theme selection with preview
        theme_group = QGroupBox("Color Theme")
        theme_layout = QHBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Modern", "Light Elegant", "Blue Professional", "Auto (System)"])
        self.theme_combo.currentTextChanged.connect(self.update_preview)
        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        # Theme preview
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(100, 60)
        self.update_preview()
        theme_layout.addWidget(QLabel("Preview:"))
        theme_layout.addWidget(self.preview_label)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Accent color
        accent_group = QGroupBox("Accent Color")
        accent_layout = QGridLayout()
        
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
        self.color_group = QButtonGroup()
        
        for i, color in enumerate(colors):
            btn = QRadioButton()
            btn.setStyleSheet(f"""
                QRadioButton::indicator {{
                    width: 30px;
                    height: 30px;
                    border-radius: 15px;
                    background: {color};
                }}
                QRadioButton::indicator:checked {{
                    border: 3px solid white;
                }}
            """)
            if i == 0:
                btn.setChecked(True)
            self.color_group.addButton(btn, i)
            accent_layout.addWidget(btn, i // 3, i % 3)
        
        accent_group.setLayout(accent_layout)
        layout.addWidget(accent_group)
        
        # Font settings
        font_group = QGroupBox("Font & Typography")
        font_layout = QGridLayout()
        
        font_layout.addWidget(QLabel("Font Family:"), 0, 0)
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Segoe UI Variable", "Inter", "SF Pro Display", "Arial", "Helvetica"])
        font_layout.addWidget(self.font_combo, 0, 1)
        
        font_layout.addWidget(QLabel("Font Size:"), 1, 0)
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(13)
        font_layout.addWidget(self.font_size, 1, 1)
        
        font_layout.addWidget(QLabel("UI Density:"), 2, 0)
        self.density_combo = QComboBox()
        self.density_combo.addItems(["Compact", "Comfortable", "Spacious"])
        font_layout.addWidget(self.density_combo, 2, 1)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("theme", self.theme_combo, "currentText")
        self.registerField("font_family", self.font_combo, "currentText")
        self.registerField("font_size", self.font_size, "value")
        self.registerField("ui_density", self.density_combo, "currentText")

    def update_preview(self):
        theme = self.theme_combo.currentText()
        colors = {
            "Dark Modern": "#2c3e50",
            "Light Elegant": "#ecf0f1", 
            "Blue Professional": "#34495e",
            "Auto (System)": "#3498db"
        }
        color = colors.get(theme, "#3498db")
        
        pixmap = QPixmap(100, 60)
        pixmap.fill(QColor(color))
        self.preview_label.setPixmap(pixmap)

class HomePageConfig(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("🏠 Home Page Setup")
        self.setSubTitle("Configure your start page and quick access")
        
        layout = QVBoxLayout()
        
        # Layout type
        layout_group = QGroupBox("Home Page Layout")
        layout_type = QVBoxLayout()
        
        self.layout_combo = QComboBox()
        self.layout_combo.addItems(["Modern Dashboard", "Minimal Search", "News Focus", "Custom Grid"])
        layout_type.addWidget(QLabel("Layout Style:"))
        layout_type.addWidget(self.layout_combo)
        layout_group.setLayout(layout_type)
        layout.addWidget(layout_group)
        
        # Quick access sites
        quick_group = QGroupBox("Quick Access Sites")
        quick_layout = QVBoxLayout()
        
        self.quick_sites = QListWidget()
        default_sites = ["Google", "YouTube", "Gmail", "GitHub", "Twitter", "Reddit"]
        for site in default_sites:
            self.quick_sites.addItem(site)
        quick_layout.addWidget(self.quick_sites)
        
        quick_buttons = QHBoxLayout()
        add_btn = QPushButton("Add")
        remove_btn = QPushButton("Remove")
        quick_buttons.addWidget(add_btn)
        quick_buttons.addWidget(remove_btn)
        quick_buttons.addStretch()
        quick_layout.addLayout(quick_buttons)
        
        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)
        
        # Calendar settings
        calendar_group = QGroupBox("Calendar & Time")
        calendar_layout = QGridLayout()
        
        calendar_layout.addWidget(QLabel("Primary Calendar:"), 0, 0)
        self.calendar_combo = QComboBox()
        self.calendar_combo.addItems(["Gregorian", "Jalali (Persian)", "Hijri (Arabic)", "Hebrew", "Chinese", "Indian"])
        calendar_layout.addWidget(self.calendar_combo, 0, 1)
        
        calendar_layout.addWidget(QLabel("Time Format:"), 1, 0)
        self.time_format = QComboBox()
        self.time_format.addItems(["24-hour", "12-hour"])
        calendar_layout.addWidget(self.time_format, 1, 1)
        
        self.show_weather = QCheckBox("Show weather information")
        self.show_weather.setChecked(True)
        calendar_layout.addWidget(self.show_weather, 2, 0, 1, 2)
        
        calendar_group.setLayout(calendar_layout)
        layout.addWidget(calendar_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("home_layout", self.layout_combo, "currentText")
        self.registerField("calendar_type", self.calendar_combo, "currentText")
        self.registerField("time_format", self.time_format, "currentText")
        self.registerField("show_weather", self.show_weather)

class SearchPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("🔍 Search & Privacy")
        self.setSubTitle("Configure your search preferences and privacy settings")
        
        layout = QVBoxLayout()
        
        # Search engine
        search_group = QGroupBox("Search Engine")
        search_layout = QVBoxLayout()
        
        self.search_combo = QComboBox()
        search_engines = [
            "Google", "Bing", "DuckDuckGo", "StartPage", "Ecosia", 
            "Brave Search", "You.com", "Custom"
        ]
        self.search_combo.addItems(search_engines)
        search_layout.addWidget(QLabel("Default Search Engine:"))
        search_layout.addWidget(self.search_combo)
        
        self.custom_search = QLineEdit()
        self.custom_search.setPlaceholderText("Enter custom search URL (use {searchTerms})")
        search_layout.addWidget(QLabel("Custom Search URL:"))
        search_layout.addWidget(self.custom_search)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Privacy settings
        privacy_group = QGroupBox("Privacy & Security")
        privacy_layout = QVBoxLayout()
        
        self.block_ads = QCheckBox("Block ads and trackers")
        self.block_ads.setChecked(True)
        privacy_layout.addWidget(self.block_ads)
        
        self.https_only = QCheckBox("Enforce HTTPS connections")
        self.https_only.setChecked(True)
        privacy_layout.addWidget(self.https_only)
        
        self.clear_on_exit = QCheckBox("Clear browsing data on exit")
        privacy_layout.addWidget(self.clear_on_exit)
        
        self.dnt_header = QCheckBox("Send Do Not Track header")
        privacy_layout.addWidget(self.dnt_header)
        
        privacy_group.setLayout(privacy_layout)
        layout.addWidget(privacy_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("search_engine", self.search_combo, "currentText")
        self.registerField("custom_search_url", self.custom_search, "text")
        self.registerField("block_ads", self.block_ads)
        self.registerField("https_only", self.https_only)
        self.registerField("clear_on_exit", self.clear_on_exit)
        self.registerField("dnt_header", self.dnt_header)

class AIPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("🤖 AI Assistant")
        self.setSubTitle("Configure your built-in AI assistant")
        
        layout = QVBoxLayout()
        
        # AI Enable/Disable
        ai_enable_group = QGroupBox("AI Assistant")
        ai_enable_layout = QVBoxLayout()
        
        self.ai_enable = QCheckBox("Enable AI Assistant (Nexa AI)")
        self.ai_enable.setChecked(True)
        ai_enable_layout.addWidget(self.ai_enable)
        
        ai_enable_group.setLayout(ai_enable_layout)
        layout.addWidget(ai_enable_group)
        
        # AI Features
        features_group = QGroupBox("AI Features")
        features_layout = QVBoxLayout()
        
        self.page_summary = QCheckBox("Page summarization")
        self.page_summary.setChecked(True)
        features_layout.addWidget(self.page_summary)
        
        self.translation = QCheckBox("Real-time translation")
        self.translation.setChecked(True)
        features_layout.addWidget(self.translation)
        
        self.smart_fill = QCheckBox("Smart form filling")
        features_layout.addWidget(self.smart_fill)
        
        self.content_gen = QCheckBox("Content generation")
        features_layout.addWidget(self.content_gen)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # AI Position
        position_group = QGroupBox("Assistant Interface")
        position_layout = QVBoxLayout()
        
        self.ai_position = QComboBox()
        self.ai_position.addItems(["Sidebar", "Bottom Panel", "Floating", "Minimized"])
        position_layout.addWidget(QLabel("Display Position:"))
        position_layout.addWidget(self.ai_position)
        
        self.auto_trigger = QCheckBox("Show AI suggestions automatically")
        self.auto_trigger.setChecked(True)
        position_layout.addWidget(self.auto_trigger)
        
        position_group.setLayout(position_layout)
        layout.addWidget(position_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("ai_enabled", self.ai_enable)
        self.registerField("page_summary", self.page_summary)
        self.registerField("translation", self.translation)
        self.registerField("smart_fill", self.smart_fill)
        self.registerField("content_gen", self.content_gen)
        self.registerField("ai_position", self.ai_position, "currentText")
        self.registerField("auto_trigger", self.auto_trigger)

class ProfessionalPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("🛠️ Professional Tools")
        self.setSubTitle("Configure advanced features for power users")
        
        layout = QVBoxLayout()
        
        # Developer options
        dev_group = QGroupBox("Developer Tools")
        dev_layout = QVBoxLayout()
        
        self.dev_tools = QCheckBox("Enable Developer Tools (F12)")
        self.dev_tools.setChecked(True)
        dev_layout.addWidget(self.dev_tools)
        
        self.js_console = QCheckBox("Show JavaScript console")
        dev_layout.addWidget(self.js_console)
        
        self.inspector = QCheckBox("Enable element inspector")
        self.inspector.setChecked(True)
        dev_layout.addWidget(self.inspector)
        
        dev_group.setLayout(dev_layout)
        layout.addWidget(dev_group)
        
        # Performance
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout()
        
        self.hardware_accel = QCheckBox("Enable hardware acceleration")
        self.hardware_accel.setChecked(True)
        perf_layout.addWidget(self.hardware_accel)
        
        self.memory_saver = QCheckBox("Enable memory saver for inactive tabs")
        self.memory_saver.setChecked(True)
        perf_layout.addWidget(self.memory_saver)
        
        self.cache_optimize = QCheckBox("Optimize cache for faster loading")
        perf_layout.addWidget(self.cache_optimize)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Advanced features
        advanced_group = QGroupBox("Advanced Features")
        advanced_layout = QVBoxLayout()
        
        self.pwa_support = QCheckBox("Enable PWA (Progressive Web App) support")
        self.pwa_support.setChecked(True)
        advanced_layout.addWidget(self.pwa_support)
        
        self.vertical_tabs = QCheckBox("Enable vertical tabs")
        advanced_layout.addWidget(self.vertical_tabs)
        
        self.tab_groups = QCheckBox("Enable tab grouping")
        advanced_layout.addWidget(self.tab_groups)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.registerField("dev_tools", self.dev_tools)
        self.registerField("js_console", self.js_console)
        self.registerField("inspector", self.inspector)
        self.registerField("hardware_accel", self.hardware_accel)
        self.registerField("memory_saver", self.memory_saver)
        self.registerField("cache_optimize", self.cache_optimize)
        self.registerField("pwa_support", self.pwa_support)
        self.registerField("vertical_tabs", self.vertical_tabs)
        self.registerField("tab_groups", self.tab_groups)

class CompletionPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("✅ Setup Complete")
        self.setSubTitle("Your Nexa Browser is ready to use!")
        
        layout = QVBoxLayout()
        
        completion_text = QLabel(
            "🎉 Excellent! Your Nexa Browser has been configured with your preferences.\n\n"
            "Here's what you've set up:\n"
            "• Personalized theme and appearance\n"
            "• Custom home page layout\n"  
            "• Privacy-focused search settings\n"
            "• AI assistant configuration\n"
            "• Professional tools and features\n\n"
            "Click 'Finish' to start browsing with Nexa!"
        )
        completion_text.setWordWrap(True)
        completion_text.setStyleSheet("font-size: 14px; line-height: 1.5; margin: 20px;")
        layout.addWidget(completion_text)
        
        # Quick tips
        tips_group = QGroupBox("Quick Tips")
        tips_layout = QVBoxLayout()
        
        tips = [
            "Press Ctrl+T to open a new tab",
            "Use Ctrl+Shift+B to show/hide bookmarks",
            "Right-click on tabs for more options",
            "Use the AI assistant for quick help",
            "Customize toolbar via Settings"
        ]
        
        for tip in tips:
            tip_label = QLabel(f"• {tip}")
            tips_layout.addWidget(tip_label)
        
        tips_group.setLayout(tips_layout)
        layout.addWidget(tips_group)
        
        layout.addStretch()
        self.setLayout(layout)

class DownloadItem(QWidget):
    def __init__(self, download_info):
        super().__init__()
        self.download_info = download_info
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        
        # File icon and name
        file_info = QLabel(f"📄 {self.download_info['filename']}")
        file_info.setStyleSheet("font-weight: bold;")
        layout.addWidget(file_info)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setValue(self.download_info.get('progress', 0))
        layout.addWidget(self.progress)
        
        # Status
        self.status = QLabel(self.download_info.get('status', 'Downloading'))
        layout.addWidget(self.status)
        
        # Speed
        self.speed = QLabel(self.download_info.get('speed', '0 KB/s'))
        layout.addWidget(self.speed)
        
        # Actions
        actions_layout = QHBoxLayout()
        self.pause_btn = QPushButton("⏸️")
        self.pause_btn.setFixedSize(30, 30)
        self.cancel_btn = QPushButton("❌")
        self.cancel_btn.setFixedSize(30, 30)
        
        actions_layout.addWidget(self.pause_btn)
        actions_layout.addWidget(self.cancel_btn)
        layout.addLayout(actions_layout)
        
        self.setLayout(layout)

class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Manager - Nexa Browser")
        self.setFixedSize(900, 500)
        self.downloads = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        
        self.pause_all_btn = QAction("⏸️ Pause All", self)
        self.resume_all_btn = QAction("▶️ Resume All", self) 
        self.clear_completed_btn = QAction("🗑️ Clear Completed", self)
        self.open_folder_btn = QAction("📁 Open Download Folder", self)
        
        toolbar.addAction(self.pause_all_btn)
        toolbar.addAction(self.resume_all_btn)
        toolbar.addAction(self.clear_completed_btn)
        toolbar.addAction(self.open_folder_btn)
        
        layout.addWidget(toolbar)
        
        # Downloads list
        self.downloads_list = QListWidget()
        self.downloads_list.setAlternatingRowColors(True)
        layout.addWidget(self.downloads_list)
        
        # Overall progress and info
        info_layout = QHBoxLayout()
        
        self.total_progress = QProgressBar()
        self.total_progress.setMaximumHeight(8)
        info_layout.addWidget(self.total_progress, 4)
        
        stats_layout = QVBoxLayout()
        self.active_label = QLabel("Active: 0")
        self.completed_label = QLabel("Completed: 0")
        self.speed_label = QLabel("Total Speed: 0 KB/s")
        
        stats_layout.addWidget(self.active_label)
        stats_layout.addWidget(self.completed_label)
        stats_layout.addWidget(self.speed_label)
        info_layout.addLayout(stats_layout)
        
        layout.addLayout(info_layout)
        self.setLayout(layout)
        
        # Connect signals
        self.pause_all_btn.triggered.connect(self.pause_all)
        self.resume_all_btn.triggered.connect(self.resume_all)
        self.clear_completed_btn.triggered.connect(self.clear_completed)
        self.open_folder_btn.triggered.connect(self.open_download_folder)
        
        # Test data
        self.add_test_downloads()
        
    def add_test_downloads(self):
        test_downloads = [
            {
                'filename': 'document.pdf',
                'progress': 75,
                'status': 'Downloading',
                'speed': '1.2 MB/s',
                'size': '4.5 MB'
            },
            {
                'filename': 'software_setup.exe', 
                'progress': 30,
                'status': 'Downloading',
                'speed': '800 KB/s',
                'size': '15.2 MB'
            },
            {
                'filename': 'image_collection.zip',
                'progress': 100,
                'status': 'Completed',
                'speed': '0 KB/s', 
                'size': '45.7 MB'
            }
        ]
        
        for download in test_downloads:
            self.add_download(download)
            
    def add_download(self, download_info):
        self.downloads.append(download_info)
        item = QListWidgetItem()
        widget = DownloadItem(download_info)
        item.setSizeHint(widget.sizeHint())
        self.downloads_list.addItem(item)
        self.downloads_list.setItemWidget(item, widget)
        self.update_stats()
        
    def update_stats(self):
        active = len([d for d in self.downloads if d.get('progress', 0) < 100])
        completed = len([d for d in self.downloads if d.get('progress', 0) == 100])
        
        self.active_label.setText(f"Active: {active}")
        self.completed_label.setText(f"Completed: {completed}")
        
        total_progress = sum(d.get('progress', 0) for d in self.downloads) 
        if self.downloads:
            self.total_progress.setValue(total_progress // len(self.downloads))
        
    def pause_all(self):
        for i in range(self.downloads_list.count()):
            item = self.downloads_list.item(i)
            widget = self.downloads_list.itemWidget(item)
            if widget and widget.download_info.get('progress', 0) < 100:
                widget.status.setText("Paused")
                
    def resume_all(self):
        for i in range(self.downloads_list.count()):
            item = self.downloads_list.item(i)
            widget = self.downloads_list.itemWidget(item)
            if widget and widget.download_info.get('progress', 0) < 100:
                widget.status.setText("Downloading")
                
    def clear_completed(self):
        for i in range(self.downloads_list.count() - 1, -1, -1):
            item = self.downloads_list.item(i)
            widget = self.downloads_list.itemWidget(item)
            if widget and widget.download_info.get('progress', 0) == 100:
                self.downloads_list.takeItem(i)
                
    def open_download_folder(self):
        download_path = Path.home() / "Downloads"
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(download_path)))

class AIAssistant(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nexa AI Assistant")
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🤖 Nexa AI Assistant")
        header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background: #2c3e50; color: white; border-radius: 5px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Chat area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Quick actions
        quick_actions = QGroupBox("Quick Actions")
        quick_layout = QGridLayout()
        
        actions = [
            ("Summarize Page", self.summarize_page),
            ("Translate Text", self.translate_text),
            ("Explain Content", self.explain_content),
            ("Find Similar", self.find_similar),
            ("Improve Writing", self.improve_writing),
            ("Research Topic", self.research_topic)
        ]
        
        for i, (text, slot) in enumerate(actions):
            btn = QPushButton(text)
            btn.setFixedHeight(30)
            btn.clicked.connect(slot)
            quick_layout.addWidget(btn, i // 2, i % 2)
            
        quick_actions.setLayout(quick_layout)
        layout.addWidget(quick_actions)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask Nexa AI anything...")
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
        
        # Add welcome message
        self.add_message("ai", "Hello! I'm Nexa AI, your browsing assistant. How can I help you today?")
        
    def add_message(self, sender, message):
        if sender == "user":
            formatted = f'<div style="text-align: right; margin: 5px;"><div style="background: #3498db; color: white; padding: 8px; border-radius: 10px; display: inline-block;">{message}</div></div>'
        else:
            formatted = f'<div style="text-align: left; margin: 5px;"><div style="background: #ecf0f1; color: #2c3e50; padding: 8px; border-radius: 10px; display: inline-block;">{message}</div></div>'
        
        current = self.chat_display.toHtml()
        self.chat_display.setHtml(current + formatted)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
        
    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            self.add_message("user", message)
            self.input_field.clear()
            
            # Simulate AI thinking
            QTimer.singleShot(1000, lambda: self.generate_ai_response(message))
            
    def generate_ai_response(self, user_message):
        responses = {
            "hello": "Hello! I'm Nexa AI, ready to help you browse smarter!",
            "help": "I can help with: summarizing pages, translations, research, writing assistance, and more! Try asking me to summarize this page or help with a task.",
            "time": f"The current time is {QDateTime.currentDateTime().toString('hh:mm AP on dddd, MMMM d, yyyy')}",
            "weather": "I can't access real-time weather data, but you can check your favorite weather website!"
        }
        
        response = responses.get(user_message.lower(), 
                               self.generate_smart_response(user_message))
        self.add_message("ai", response)
        
    def generate_smart_response(self, message):
        smart_responses = [
            f"I understand you're asking about '{message}'. Based on the current page content, I can help you find more information or summarize key points.",
            f"Great question! For '{message}', I recommend checking authoritative sources or using the search function to explore related content.",
            f"I'd be happy to help with '{message}'. Would you like me to search for more information or summarize what we have on this page?",
            f"Regarding '{message}', I can assist you by analyzing the page content or helping you research this topic further."
        ]
        import random
        return random.choice(smart_responses)
        
    def summarize_page(self):
        self.add_message("user", "Summarize this page")
        QTimer.singleShot(1000, lambda: self.add_message("ai", "Based on my analysis of this page, here are the key points:\n\n• The content appears to be well-structured and informative\n• Main topics are clearly presented\n• Key sections include navigation, main content, and supplementary information\n\nWould you like a more detailed summary of specific sections?"))
        
    def translate_text(self):
        self.add_message("user", "Translate selected text")
        self.add_message("ai", "I can translate text between multiple languages. Please select the text you want to translate and I'll help you convert it to your desired language.")
        
    def explain_content(self):
        self.add_message("user", "Explain this content")
        self.add_message("ai", "I'll analyze this content and provide a clear explanation. Based on the page structure, this appears to be informational content that would benefit from contextual explanation and key concept breakdown.")
        
    def find_similar(self):
        self.add_message("user", "Find similar content")
        self.add_message("ai", "I can help you discover related content and similar websites. Based on the current page topic, I suggest exploring these related areas for more comprehensive understanding.")
        
    def improve_writing(self):
        self.add_message("user", "Improve my writing")
        self.add_message("ai", "I'd be happy to help improve your writing! Please share the text you'd like me to review, and I'll provide suggestions for clarity, grammar, and style improvements.")
        
    def research_topic(self):
        self.add_message("user", "Research this topic")
        self.add_message("ai", "I'll help you research this topic comprehensively. Let me gather relevant information from reliable sources and organize it into a structured research summary for you.")

class HomePage(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.init_ui()
        self.update_styles()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        
        # Header with logo and search
        header_layout = QHBoxLayout()
        
        # Logo and title
        logo_section = QHBoxLayout()
        logo_label = QLabel("🌐")
        logo_label.setStyleSheet("font-size: 32px;")
        title_label = QLabel("Nexa Browser")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db; margin-left: 10px;")
        
        logo_section.addWidget(logo_label)
        logo_section.addWidget(title_label)
        header_layout.addLayout(logo_section)
        
        header_layout.addStretch()
        
        # Search bar
        search_container = QWidget()
        search_container.setFixedWidth(500)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search with Nexa or enter address...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #bdc3c7;
                border-radius: 25px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(40, 40)
        search_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                border: none;
                border-radius: 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_btn)
        header_layout.addWidget(search_container)
        
        header_layout.addStretch()
        
        # Time and weather
        time_section = QVBoxLayout()
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.date_label = QLabel()
        self.date_label.setStyleSheet("color: #7f8c8d;")
        
        time_section.addWidget(self.time_label)
        time_section.addWidget(self.date_label)
        header_layout.addLayout(time_section)
        
        layout.addLayout(header_layout)
        layout.addSpacing(30)
        
        # Quick access grid
        quick_access_label = QLabel("Quick Access")
        quick_access_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(quick_access_label)
        
        quick_access = QGridLayout()
        quick_access.setSpacing(15)
        
        sites = [
            ("Google", "https://google.com", "#ea4335"),
            ("YouTube", "https://youtube.com", "#ff0000"),
            ("Gmail", "https://gmail.com", "#34a853"), 
            ("GitHub", "https://github.com", "#333333"),
            ("Twitter", "https://twitter.com", "#1da1f2"),
            ("Reddit", "https://reddit.com", "#ff4500"),
            ("Instagram", "https://instagram.com", "#e4405f"),
            ("LinkedIn", "https://linkedin.com", "#0077b5"),
        ]
        
        for i, (name, url, color) in enumerate(sites):
            btn = QPushButton(name)
            btn.setFixedSize(100, 80)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background: {color};
                    opacity: 0.9;
                }}
            """)
            btn.clicked.connect(lambda checked, u=url: self.open_url(u))
            quick_access.addWidget(btn, i // 4, i % 4)
        
        layout.addLayout(quick_access)
        layout.addSpacing(30)
        
        # Calendar and productivity section
        productivity_layout = QHBoxLayout()
        
        # Calendar widget
        calendar_group = QGroupBox("Today")
        calendar_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        calendar_layout = QVBoxLayout()
        
        self.calendar_label = QLabel()
        self.calendar_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        calendar_layout.addWidget(self.calendar_label)
        
        self.hijri_label = QLabel()
        self.hijri_label.setStyleSheet("font-size: 12px; color: #95a5a6;")
        calendar_layout.addWidget(self.hijri_label)
        
        calendar_group.setLayout(calendar_layout)
        productivity_layout.addWidget(calendar_group)
        
        # Mini apps
        apps_group = QGroupBox("Quick Tools")
        apps_layout = QGridLayout()
        
        mini_apps = [
            ("📝 Notes", self.open_notes),
            ("📊 Stats", self.open_stats),
            ("🎵 Music", self.open_music),
            ("📷 Camera", self.open_camera)
        ]
        
        for i, (name, slot) in enumerate(mini_apps):
            btn = QPushButton(name)
            btn.setFixedHeight(40)
            btn.clicked.connect(slot)
            apps_layout.addWidget(btn, i // 2, i % 2)
            
        apps_group.setLayout(apps_layout)
        productivity_layout.addWidget(apps_group)
        
        productivity_layout.addStretch()
        layout.addLayout(productivity_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Update time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current = QDateTime.currentDateTime()
        
        # Main time and date
        self.time_label.setText(current.toString("hh:mm:ss AP"))
        self.date_label.setText(current.toString("dddd, MMMM d, yyyy"))
        
        # Multiple calendars
        gregorian = current.toString("yyyy-MM-dd")
        self.calendar_label.setText(f"Gregorian: {gregorian}")
        
        # Simulate other calendars (in real implementation, use proper calendar libraries)
        day_of_year = current.date().dayOfYear()
        self.hijri_label.setText(f"Other calendars: Jalali, Hijri, Hebrew available")

    def update_styles(self):
        theme = self.settings.value("theme", "Dark Modern")
        if "Dark" in theme:
            self.setStyleSheet("background: #2c3e50; color: white;")
        else:
            self.setStyleSheet("background: #ecf0f1; color: #2c3e50;")

    def open_url(self, url):
        # This will be connected to main browser navigation
        print(f"Opening: {url}")

    def open_notes(self):
        QMessageBox.information(self, "Notes", "Quick notes feature would open here")

    def open_stats(self):
        QMessageBox.information(self, "Statistics", "Browser statistics and usage data")

    def open_music(self):
        QMessageBox.information(self, "Music", "Integrated music player")

    def open_camera(self):
        QMessageBox.information(self, "Camera", "Camera and media tools")

class ModernTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.close_tab)
        
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: white;
            }
            QTabBar::tab {
                background: #ecf0f1;
                border: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background: #bdc3c7;
            }
        """)
        
        # Add initial tab
        self.add_new_tab()

    def add_new_tab(self, url=None, title="New Tab"):
        browser = QWebEngineView()
        
        if url:
            browser.setUrl(QUrl(url))
        else:
            browser.setUrl(QUrl("https://www.google.com"))
        
        index = self.addTab(browser, title)
        self.setCurrentIndex(index)
        
        # Update tab title when page title changes
        browser.titleChanged.connect(
            lambda title, browser=browser: 
            self.update_tab_title(browser, title)
        )
        
        browser.urlChanged.connect(
            lambda url, browser=browser:
            self.update_tab_url(browser, url)
        )
        
        return browser

    def update_tab_title(self, browser, title):
        index = self.indexOf(browser)
        if title:
            short_title = title[:25] + "..." if len(title) > 25 else title
            self.setTabText(index, short_title)
            self.setTabToolTip(index, title)

    def update_tab_url(self, browser, url):
        index = self.indexOf(browser)
        # You can add favicon loading here later

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)

class NexaBrowser(FluentWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("NexaBrowser", "Settings")
        self.check_first_run()
        self.init_ui()
        self.apply_theme()
        
    def check_first_run(self):
        if not self.settings.value("first_run_complete", False, type=bool):
            wizard = FirstRunWizard()
            if wizard.exec() == QDialog.DialogCode.Accepted:
                # Save all wizard settings
                wizard_settings = wizard.get_settings()
                for key, value in wizard_settings.items():
                    self.settings.setValue(key, value)
                self.settings.setValue("first_run_complete", True)
                self.settings.sync()
                print("First run setup completed successfully!")
                print(f"Settings saved: {list(wizard_settings.keys())}")

    def init_ui(self):
        self.setWindowTitle("Nexa Browser")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and layout
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create title bar
        self.create_title_bar()
        layout.addWidget(self.title_bar)
        
        # Create toolbar
        self.create_toolbar()
        layout.addWidget(self.toolbar)
        
        # Create tab widget
        self.tabs = ModernTabWidget()
        layout.addWidget(self.tabs)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Create download manager
        self.download_manager = DownloadManager(self)
        
        # Create AI assistant
        self.ai_assistant = AIAssistant(self)
        
        # Apply styles
        self.apply_styles()
        
        # Show homepage in first tab
        home_url = self.settings.value("homepage", "https://www.google.com")
        self.tabs.widget(0).setUrl(QUrl(home_url))

    def create_title_bar(self):
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2c3e50);
                color: white;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        
        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Logo and title
        title_layout = QHBoxLayout()
        logo = QLabel("🌐")
        logo.setStyleSheet("font-size: 16px;")
        title = QLabel("Nexa Browser")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        title_layout.addWidget(logo)
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Window controls
        controls_layout = QHBoxLayout()
        
        min_btn = QPushButton("─")
        min_btn.setFixedSize(25, 25)
        min_btn.clicked.connect(self.showMinimized)
        
        max_btn = QPushButton("□")
        max_btn.setFixedSize(25, 25)
        max_btn.clicked.connect(self.toggle_maximize)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.clicked.connect(self.close)
        
        for btn in [min_btn, max_btn, close_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid rgba(255,255,255,0.3);
                    border-radius: 3px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.2);
                }
            """)
        
        controls_layout.addWidget(min_btn)
        controls_layout.addWidget(max_btn)
        controls_layout.addWidget(close_btn)
        layout.addLayout(controls_layout)

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: rgba(255,255,255,0.95);
                border: none;
                spacing: 5px;
                padding: 5px;
            }
        """)
        
        # Navigation buttons
        back_btn = QAction("←", self)
        back_btn.triggered.connect(self.navigate_back)
        self.toolbar.addAction(back_btn)
        
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(forward_btn)
        
        reload_btn = QAction("↻", self)
        reload_btn.triggered.connect(self.reload_page)
        self.toolbar.addAction(reload_btn)
        
        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.go_home)
        self.toolbar.addAction(home_btn)
        
        self.toolbar.addSeparator()
        
        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter website address...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #bdc3c7;
                border-radius: 20px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        self.toolbar.addWidget(self.url_bar)
        
        # Search button
        search_btn = QAction("🔍", self)
        search_btn.triggered.connect(self.search_web)
        self.toolbar.addAction(search_btn)
        
        self.toolbar.addSeparator()
        
        # New tab button
        new_tab_btn = QAction("＋", self)
        new_tab_btn.triggered.connect(self.tabs.add_new_tab)
        self.toolbar.addAction(new_tab_btn)
        
        # AI Assistant button
        ai_btn = QAction("🤖", self)
        ai_btn.triggered.connect(self.toggle_ai_assistant)
        self.toolbar.addAction(ai_btn)
        
        # Downloads button
        download_btn = QAction("📥", self)
        download_btn.triggered.connect(self.show_download_manager)
        self.toolbar.addAction(download_btn)
        
        # Settings button
        settings_btn = QAction("⚙️", self)
        settings_btn.triggered.connect(self.show_settings)
        self.toolbar.addAction(settings_btn)

    def apply_theme(self):
        theme = self.settings.value("theme", "Dark Modern")
        
        if "Dark" in theme:
            self.apply_dark_theme()
        elif "Light" in theme:
            self.apply_light_theme()
        else:
            # Auto theme based on system
            if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
                self.apply_dark_theme()
            else:
                self.apply_light_theme()

    def apply_dark_theme(self):
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
        QApplication.setPalette(dark_palette)

    def apply_light_theme(self):
        light_palette = QPalette()
        light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
        light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        light_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        light_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        QApplication.setPalette(light_palette)

    def apply_styles(self):
        self.setStyleSheet("""
            #centralWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #3498db);
                border-radius: 12px;
            }
        """)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

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
        current_browser = self.tabs.currentWidget()
        if current_browser:
            home_url = self.settings.value("homepage", "https://www.google.com")
            current_browser.setUrl(QUrl(home_url))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'https://' + url
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def search_web(self):
        search_term = self.url_bar.text()
        if not search_term.strip():
            return
            
        search_engine = self.settings.value("search_engine", "Google")
        
        search_urls = {
            "Google": f"https://www.google.com/search?q={search_term}",
            "Bing": f"https://www.bing.com/search?q={search_term}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={search_term}",
            "StartPage": f"https://www.startpage.com/sp/search?q={search_term}",
            "Ecosia": f"https://www.ecosia.org/search?q={search_term}",
            "Brave Search": f"https://search.brave.com/search?q={search_term}",
            "You.com": f"https://you.com/search?q={search_term}"
        }
        
        url = search_urls.get(search_engine, search_urls["Google"])
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def toggle_ai_assistant(self):
        if self.ai_assistant.isVisible():
            self.ai_assistant.hide()
        else:
            self.ai_assistant.show()
            self.ai_assistant.raise_()

    def show_download_manager(self):
        self.download_manager.show()
        self.download_manager.raise_()

    def show_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Nexa Browser Settings")
        settings_dialog.setFixedSize(600, 400)
        
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        # General tab
        general_tab = QWidget()
        general_layout = QFormLayout()
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark Modern", "Light Elegant", "Blue Professional", "Auto (System)"])
        theme_combo.setCurrentText(self.settings.value("theme", "Dark Modern"))
        
        search_combo = QComboBox()
        search_combo.addItems(["Google", "Bing", "DuckDuckGo", "StartPage", "Ecosia", "Brave Search", "You.com"])
        search_combo.setCurrentText(self.settings.value("search_engine", "Google"))
        
        general_layout.addRow("Theme:", theme_combo)
        general_layout.addRow("Search Engine:", search_combo)
        general_tab.setLayout(general_layout)
        
        tabs.addTab(general_tab, "General")
        
        # Privacy tab
        privacy_tab = QWidget()
        privacy_layout = QVBoxLayout()
        
        block_ads = QCheckBox("Block ads and trackers")
        block_ads.setChecked(self.settings.value("block_ads", True, type=bool))
        
        https_only = QCheckBox("Enforce HTTPS connections")
        https_only.setChecked(self.settings.value("https_only", True, type=bool))
        
        privacy_layout.addWidget(block_ads)
        privacy_layout.addWidget(https_only)
        privacy_layout.addStretch()
        privacy_tab.setLayout(privacy_layout)
        
        tabs.addTab(privacy_tab, "Privacy")
        
        layout.addWidget(tabs)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(settings_dialog.accept)
        buttons.rejected.connect(settings_dialog.reject)
        layout.addWidget(buttons)
        
        settings_dialog.setLayout(layout)
        
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            self.settings.setValue("theme", theme_combo.currentText())
            self.settings.setValue("search_engine", search_combo.currentText())
            self.settings.setValue("block_ads", block_ads.isChecked())
            self.settings.setValue("https_only", https_only.isChecked())
            self.apply_theme()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_start_position'):
            self.move(event.globalPosition().toPoint() - self.drag_start_position)
            event.accept()

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Hessamedien")
    app.setOrganizationDomain("hessamedien.com")
    
    # Set application-wide styles
    app.setStyleSheet("""
        QMainWindow {
            background: transparent;
        }
    """)
    
    browser = NexaBrowser()
    browser.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
