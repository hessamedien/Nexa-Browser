# nexa_browser.py
# Nexa Browser - Modern AI-Powered Web Browser for Windows
# Created by Hessamedien (https://www.instagram.com/hessamedien)

import sys
import os
import json
import asyncio
import tempfile
import sqlite3
import hashlib
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, quote, urljoin
from typing import Dict, List, Optional, Any, Tuple
import threading
from concurrent.futures import ThreadPoolExecutor
import webbrowser
import ctypes
from ctypes import wintypes
from collections import OrderedDict

# PyQt6 imports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QToolBar, QTabWidget, QLineEdit, QPushButton, QToolButton, 
                            QLabel, QProgressBar, QFrame, QSplitter, QStackedWidget,
                            QDialog, QWizard, QWizardPage, QComboBox, QCheckBox, 
                            QSpinBox, QSlider, QGroupBox, QListWidget, QListWidgetItem,
                            QScrollArea, QStyleFactory, QMessageBox, QFileDialog,
                            QSystemTrayIcon, QMenu, QStyle, QSizePolicy, QDialogButtonBox,
                            QGridLayout, QFormLayout, QRadioButton, QButtonGroup, QTextEdit,
                            QInputDialog, QColorDialog, QFontDialog, QToolBox, QSplitterHandle)
from PyQt6.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEngineScript, QWebEngineScriptCollection
from PyQt6.QtCore import (Qt, QUrl, QSize, QTimer, QSettings, QPoint, QPropertyAnimation, 
                         QEasingCurve, pyqtProperty, pyqtSignal, QThread, QByteArray, 
                         QEvent, QMargins, QRect, QSequentialAnimationGroup, QParallelAnimationGroup)
from PyQt6.QtGui import (QIcon, QPalette, QColor, QFont, QFontDatabase, QPainter, QLinearGradient, 
                        QGuiApplication, QCursor, QAction, QDesktopServices, QPixmap, QBrush,
                        QGradient, QPen, QPainterPath, QRegion, QKeySequence, QShortcut,
                        QMouseEvent, QWheelEvent, QContextMenuEvent)

# Windows API for acrylic effect
try:
    from ctypes import windll, byref, Structure, POINTER
    from ctypes.wintypes import DWORD, ULONG, BOOL, HRGN
    
    class ACCENTPOLICY(Structure):
        _fields_ = [
            ("AccentState", DWORD),
            ("AccentFlags", DWORD),
            ("GradientColor", DWORD),
            ("AnimationId", DWORD)
        ]
    
    class WINDOWCOMPOSITIONATTRIBDATA(Structure):
        _fields_ = [
            ("Attribute", DWORD),
            ("Data", POINTER(ACCENTPOLICY)),
            ("SizeOfData", DWORD)
        ]
    
    SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
    SetWindowCompositionAttribute.argtypes = [wintypes.HWND, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
    SetWindowCompositionAttribute.restype = wintypes.BOOL
except:
    SetWindowCompositionAttribute = None

# AI Service Integration
class AIService:
    def __init__(self):
        self.enabled = True
        self.api_key = ""
        self.provider = "openai"  # openai, gemini, local
        
    def set_provider(self, provider: str, api_key: str = ""):
        self.provider = provider
        self.api_key = api_key
        
    async def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate AI response using selected provider"""
        if not self.enabled:
            return "AI assistant is disabled"
            
        # Simulate API call - replace with actual API integration
        await asyncio.sleep(0.5)
        
        responses = {
            "summarize": f"📝 **Summary**: This page discusses {context[:100]}... The main points include key concepts and important information relevant to the topic.",
            "translate": f"🌐 **Translation**: Translation would convert this content to your desired language. Context: {context[:200]}...",
            "explain": f"🔍 **Explanation**: This content explains {context[:150]}... In simpler terms, it's about the main subject with detailed insights.",
            "generate": f"✨ **Generated Content**: Based on your request '{prompt}', here's a professionally crafted response that meets your requirements.",
            "general": f"🤖 **Nexa AI**: I understand you're asking about '{prompt}'. Based on the current page context, I can help you with summarization, translation, or content generation."
        }
        
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ['summarize', 'summary', 'summarise']):
            return responses["summarize"]
        elif any(word in prompt_lower for word in ['translate', 'translation']):
            return responses["translate"]
        elif any(word in prompt_lower for word in ['explain', 'what is', 'how does']):
            return responses["explain"]
        elif any(word in prompt_lower for word in ['write', 'create', 'generate', 'compose']):
            return responses["generate"]
        else:
            return responses["general"]

class AIAssistant(QThread):
    response_received = pyqtSignal(str, str)  # query, response
    
    def __init__(self, ai_service: AIService):
        super().__init__()
        self.ai_service = ai_service
        
    def process_query(self, query: str, context: str = ""):
        self.query = query
        self.context = context
        self.start()
        
    def run(self):
        try:
            # Run async function in thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                self.ai_service.generate_response(self.query, self.context)
            )
            loop.close()
            
            self.response_received.emit(self.query, response)
        except Exception as e:
            self.response_received.emit(self.query, f"Error: {str(e)}")

# Download Manager with Advanced Features
class DownloadItem:
    def __init__(self, download_request: QWebEngineDownloadRequest = None):
        self.id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        self.url = download_request.url().toString() if download_request else ""
        self.filename = download_request.downloadFileName() if download_request else ""
        self.path = ""
        self.progress = 0
        self.speed = 0
        self.eta = "Unknown"
        self.status = "queued"  # queued, downloading, paused, completed, error
        self.size = 0
        self.downloaded = 0
        self.start_time = datetime.now()
        self.download_request = download_request
        
class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloads = OrderedDict()
        self.download_folder = str(Path.home() / "Downloads")
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Nexa Download Manager")
        self.setMinimumSize(800, 500)
        
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        
        self.pause_btn = QAction("⏸️ Pause", self)
        self.resume_btn = QAction("▶️ Resume", self)
        self.cancel_btn = QAction("❌ Cancel", self)
        self.clear_btn = QAction("🗑️ Clear Completed", self)
        self.folder_btn = QAction("📁 Open Folder", self)
        
        toolbar.addAction(self.pause_btn)
        toolbar.addAction(self.resume_btn)
        toolbar.addAction(self.cancel_btn)
        toolbar.addAction(self.clear_btn)
        toolbar.addAction(self.folder_btn)
        
        layout.addWidget(toolbar)
        
        # Downloads list
        self.downloads_list = QListWidget()
        self.downloads_list.setAlternatingRowColors(True)
        layout.addWidget(self.downloads_list)
        
        # Progress section
        progress_layout = QHBoxLayout()
        self.global_progress = QProgressBar()
        self.speed_label = QLabel("Total Speed: 0 KB/s")
        self.active_label = QLabel("Active Downloads: 0")
        
        progress_layout.addWidget(QLabel("Overall Progress:"))
        progress_layout.addWidget(self.global_progress, 1)
        progress_layout.addWidget(self.speed_label)
        progress_layout.addWidget(self.active_label)
        
        layout.addLayout(progress_layout)
        
        # Connect signals
        self.pause_btn.triggered.connect(self.pause_selected)
        self.resume_btn.triggered.connect(self.resume_selected)
        self.cancel_btn.triggered.connect(self.cancel_selected)
        self.clear_btn.triggered.connect(self.clear_completed)
        self.folder_btn.triggered.connect(self.open_download_folder)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)
        
    def add_download(self, download_request: QWebEngineDownloadRequest):
        item = DownloadItem(download_request)
        self.downloads[item.id] = item
        
        download_request.accept()
        download_request.downloadProgress.connect(
            lambda received, total: self.update_progress(item.id, received, total)
        )
        download_request.finished.connect(
            lambda: self.download_finished(item.id)
        )
        
        # Create temp file path
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=item.filename)
        item.path = temp_file.name
        temp_file.close()
        
        download_request.setDownloadDirectory(Path(item.path).parent)
        download_request.setDownloadFileName(Path(item.path).name)
        
    def update_progress(self, download_id: str, received: int, total: int):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            item.downloaded = received
            item.size = total
            item.progress = (received / total * 100) if total > 0 else 0
            
            # Calculate speed and ETA
            elapsed = (datetime.now() - item.start_time).total_seconds()
            if elapsed > 0:
                item.speed = received / elapsed
                if item.speed > 0:
                    remaining = (total - received) / item.speed
                    item.eta = str(timedelta(seconds=int(remaining)))
                    
    def download_finished(self, download_id: str):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            item.status = "completed"
            item.progress = 100
            
    def pause_selected(self):
        for item in self.downloads.values():
            if item.status == "downloading":
                item.status = "paused"
                
    def resume_selected(self):
        for item in self.downloads.values():
            if item.status == "paused":
                item.status = "downloading"
                
    def cancel_selected(self):
        current_item = self.downloads_list.currentItem()
        if current_item:
            download_id = current_item.data(Qt.ItemDataRole.UserRole)
            if download_id in self.downloads:
                item = self.downloads[download_id]
                item.status = "cancelled"
                if item.download_request:
                    item.download_request.cancel()
                    
    def clear_completed(self):
        completed_ids = [did for did, item in self.downloads.items() 
                        if item.status == "completed"]
        for did in completed_ids:
            del self.downloads[did]
            
    def open_download_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.download_folder))
        
    def update_display(self):
        self.downloads_list.clear()
        
        total_progress = 0
        active_downloads = 0
        total_speed = 0
        
        for item in self.downloads.values():
            # Create list item
            item_text = (f"{item.filename} - {item.progress:.1f}% - "
                        f"Speed: {item.speed/1024:.1f} KB/s - ETA: {item.eta}")
            if item.status == "completed":
                item_text += " ✅"
            elif item.status == "paused":
                item_text += " ⏸️"
            elif item.status == "error":
                item_text += " ❌"
                
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item.id)
            self.downloads_list.addItem(list_item)
            
            # Update statistics
            if item.status in ["downloading", "queued"]:
                total_progress += item.progress
                active_downloads += 1
                total_speed += item.speed
                
        # Update UI
        if active_downloads > 0:
            self.global_progress.setValue(total_progress / active_downloads)
        else:
            self.global_progress.setValue(0)
            
        self.speed_label.setText(f"Total Speed: {total_speed/1024:.1f} KB/s")
        self.active_label.setText(f"Active Downloads: {active_downloads}")

# Modern Title Bar with Acrylic Effect
class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(5)
        
        # App icon and title
        self.icon_label = QLabel("🌐 Nexa Browser")
        self.icon_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #0078d4;")
        self.layout.addWidget(self.icon_label)
        
        self.layout.addStretch()
        
        # Window controls
        self.minimize_btn = QPushButton("−")
        self.maximize_btn = QPushButton("□")
        self.close_btn = QPushButton("×")
        
        controls = [self.minimize_btn, self.maximize_btn, self.close_btn]
        for btn in controls:
            btn.setFixedSize(28, 28)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e5e5e5;
                }
                QPushButton:pressed {
                    background-color: #d5d5d5;
                }
                QPushButton:focus {
                    outline: none;
                }
            """)
            self.layout.addWidget(btn)
            
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.parent.close)
        
        # Enable window dragging
        self.dragging = False
        self.drag_position = QPoint()
        
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
            
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.parent.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging = False
        event.accept()

# Fluent Design Browser Tab
class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.setup_tab()
        
    def setup_tab(self):
        # Configure settings for better performance
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        
        # Enable hardware acceleration
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        
    def contextMenuEvent(self, event: QContextMenuEvent):
        # Custom context menu
        menu = self.createStandardContextMenu()
        
        # Add custom actions
        menu.addSeparator()
        reader_mode_action = menu.addAction("📖 Reader Mode")
        take_screenshot_action = menu.addAction("📸 Take Screenshot")
        menu.addSeparator()
        
        reader_mode_action.triggered.connect(self.activate_reader_mode)
        take_screenshot_action.triggered.connect(self.take_screenshot)
        
        menu.exec(event.globalPos())
        
    def activate_reader_mode(self):
        # Inject reader mode CSS
        script = """
        // Simple reader mode implementation
        document.querySelectorAll('nav, header, footer, aside, .ad, .advertisement').forEach(el => el.style.display = 'none');
        document.body.style.maxWidth = '800px';
        document.body.style.margin = '0 auto';
        document.body.style.padding = '20px';
        document.body.style.fontFamily = 'Georgia, serif';
        document.body.style.fontSize = '18px';
        document.body.style.lineHeight = '1.6';
        """
        self.page().runJavaScript(script)
        
    def take_screenshot(self):
        # Take screenshot of visible area
        pixmap = self.grab()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "", "PNG Images (*.png);;All Files (*)"
        )
        if file_path:
            pixmap.save(file_path, "PNG")

# AI Sidebar with Chat Interface
class AISidebar(QWidget):
    def __init__(self, ai_assistant: AIAssistant):
        super().__init__()
        self.ai_assistant = ai_assistant
        self.chat_history = []
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedWidth(350)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with gradient
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:1 #00bcf2);
                color: white;
                font-weight: bold;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        ai_icon = QLabel("🤖")
        ai_icon.setStyleSheet("font-size: 20px;")
        header_layout.addWidget(ai_icon)
        
        title = QLabel("Nexa AI Assistant")
        title.setStyleSheet("font-size: 14px; color: white;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
                border-radius: 12px;
            }
        """)
        header_layout.addWidget(self.close_btn)
        
        layout.addWidget(header)
        
        # Chat area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(10)
        
        self.chat_scroll.setWidget(self.chat_widget)
        layout.addWidget(self.chat_scroll, 1)
        
        # Input area
        input_container = QWidget()
        input_container.setFixedHeight(100)
        input_container.setStyleSheet("background-color: #f8f9fa; border-top: 1px solid #e0e0e0;")
        
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(60)
        self.input_field.setPlaceholderText("Ask AI anything...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        button_layout = QHBoxLayout()
        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedHeight(30)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        
        # Quick action buttons
        quick_actions = QHBoxLayout()
        actions = [
            ("📝 Summarize", "summarize"),
            ("🌐 Translate", "translate"),
            ("🔍 Explain", "explain"),
            ("✨ Generate", "generate")
        ]
        
        for text, action in actions:
            btn = QPushButton(text)
            btn.setFixedHeight(25)
            btn.setStyleSheet("font-size: 10px; padding: 2px;")
            btn.clicked.connect(lambda checked, a=action: self.quick_action(a))
            quick_actions.addWidget(btn)
            
        input_layout.addLayout(quick_actions)
        input_layout.addWidget(self.input_field)
        input_layout.addLayout(button_layout)
        button_layout.addWidget(self.send_btn)
        
        layout.addWidget(input_container)
        
        # Connect signals
        self.send_btn.clicked.connect(self.send_message)
        self.close_btn.clicked.connect(self.hide)
        self.ai_assistant.response_received.connect(self.display_response)
        
    def add_message(self, message: str, is_user: bool = True):
        message_widget = QWidget()
        message_widget.setStyleSheet("background: transparent;")
        
        message_layout = QHBoxLayout(message_widget)
        message_layout.setContentsMargins(10, 5, 10, 5)
        
        if not is_user:
            message_layout.addWidget(QLabel("🤖"))
            
        text_widget = QLabel(message)
        text_widget.setWordWrap(True)
        text_widget.setStyleSheet(f"""
            QLabel {{
                background-color: {'#0078d4' if is_user else '#f0f0f0'};
                color: {'white' if is_user else 'black'};
                padding: 10px;
                border-radius: 12px;
                font-size: 12px;
            }}
        """)
        text_widget.setMinimumWidth(200)
        text_widget.setMaximumWidth(280)
        
        if is_user:
            message_layout.addStretch()
            message_layout.addWidget(text_widget)
        else:
            message_layout.addWidget(text_widget)
            message_layout.addStretch()
            
        self.chat_layout.addWidget(message_widget)
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        message = self.input_field.toPlainText().strip()
        if message:
            self.add_message(message, True)
            self.input_field.clear()
            self.ai_assistant.process_query(message)
            
    def quick_action(self, action: str):
        actions = {
            "summarize": "Please summarize the current page",
            "translate": "Translate this page to English",
            "explain": "Explain the main concepts of this page",
            "generate": "Generate a professional email about this content"
        }
        self.input_field.setPlainText(actions[action])
        self.send_message()
        
    def display_response(self, query: str, response: str):
        self.add_message(response, False)

# Home Page with Customizable Widgets
class HomePage(QWidget):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.widgets = {}
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Background with slight gradient
        self.setStyleSheet("""
            HomePage {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        # Welcome section
        self.setup_welcome_section()
        
        # Search section
        self.setup_search_section()
        
        # Quick access
        self.setup_quick_access()
        
        # Widgets area
        self.setup_widgets_area()
        
    def setup_welcome_section(self):
        welcome_container = QWidget()
        welcome_container.setFixedHeight(80)
        welcome_container.setStyleSheet("background: transparent;")
        
        welcome_layout = QVBoxLayout(welcome_container)
        
        welcome_label = QLabel("Welcome to Nexa Browser 🌐")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #0078d4;
                padding: 10px;
            }
        """)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        date_label = QLabel()
        date_label.setStyleSheet("font-size: 14px; color: #666;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(date_label)
        
        self.layout.addWidget(welcome_container)
        
        # Update date
        self.update_date_timer = QTimer()
        self.update_date_timer.timeout.connect(lambda: self.update_date(date_label))
        self.update_date_timer.start(1000)
        self.update_date(date_label)
        
    def update_date(self, label: QLabel):
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y | %I:%M:%S %p")
        label.setText(date_str)
        
    def setup_search_section(self):
        search_container = QWidget()
        search_container.setFixedHeight(80)
        search_container.setStyleSheet("background: transparent;")
        
        search_layout = QHBoxLayout(search_container)
        search_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.search_bar = QLineEdit()
        self.search_bar.setFixedWidth(500)
        self.search_bar.setFixedHeight(40)
        self.search_bar.setPlaceholderText("Search or enter website address...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #0078d4;
                border-radius: 20px;
                padding: 0 20px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #00bcf2;
            }
        """)
        self.search_bar.returnPressed.connect(self.perform_search)
        
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(40, 40)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        search_btn.clicked.connect(self.perform_search)
        
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_btn)
        
        self.layout.addWidget(search_container)
        
    def setup_quick_access(self):
        quick_container = QWidget()
        quick_container.setFixedHeight(100)
        quick_container.setStyleSheet("background: transparent;")
        
        quick_layout = QHBoxLayout(quick_container)
        quick_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        sites = [
            ("Google", "https://google.com", "#4285f4"),
            ("YouTube", "https://youtube.com", "#ff0000"),
            ("GitHub", "https://github.com", "#333333"),
            ("Twitter", "https://twitter.com", "#1da1f2"),
            ("Outlook", "https://outlook.com", "#0078d4"),
            ("Drive", "https://drive.google.com", "#34a853")
        ]
        
        for name, url, color in sites:
            btn = QPushButton(name)
            btn.setFixedSize(80, 60)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                }}
            """)
            btn.clicked.connect(lambda checked, u=url: self.browser.open_url(u))
            quick_layout.addWidget(btn)
            
        self.layout.addWidget(quick_container)
        
    def setup_widgets_area(self):
        self.widgets_stack = QStackedWidget()
        self.layout.addWidget(self.widgets_stack, 1)
        
        # Add default widgets
        self.add_calendar_widget()
        self.add_notes_widget()
        
    def add_calendar_widget(self):
        calendar_widget = QGroupBox("📅 Calendar & Time")
        calendar_widget.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #ccc;
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
        
        layout = QVBoxLayout(calendar_widget)
        
        # Calendar type selector
        calendar_layout = QHBoxLayout()
        calendar_layout.addWidget(QLabel("Calendar:"))
        
        self.calendar_combo = QComboBox()
        self.calendar_combo.addItems(["Gregorian", "Jalali", "Hijri", "Chinese", "Hebrew"])
        calendar_layout.addWidget(self.calendar_combo)
        calendar_layout.addStretch()
        
        # Time display
        self.time_display = QLabel()
        self.time_display.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078d4;")
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Date display
        self.date_display = QLabel()
        self.date_display.setStyleSheet("font-size: 14px; color: #666;")
        self.date_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(calendar_layout)
        layout.addWidget(self.time_display)
        layout.addWidget(self.date_display)
        
        self.widgets_stack.addWidget(calendar_widget)
        
        # Update timer
        self.calendar_timer = QTimer()
        self.calendar_timer.timeout.connect(self.update_calendar_display)
        self.calendar_timer.start(1000)
        self.update_calendar_display()
        
    def update_calendar_display(self):
        now = datetime.now()
        calendar_type = self.calendar_combo.currentText()
        
        time_str = now.strftime("%H:%M:%S")
        
        if calendar_type == "Gregorian":
            date_str = now.strftime("%A, %B %d, %Y")
        elif calendar_type == "Jalali":
            # Simplified - in production use proper jalaali conversion
            date_str = f"Jalali Calendar - {now.strftime('%Y/%m/%d')}"
        elif calendar_type == "Hijri":
            date_str = f"Hijri Calendar - {now.strftime('%Y/%m/%d')}"
        else:
            date_str = f"{calendar_type} Calendar"
            
        self.time_display.setText(time_str)
        self.date_display.setText(date_str)
        
    def add_notes_widget(self):
        notes_widget = QGroupBox("📝 Quick Notes")
        notes_widget.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        
        layout = QVBoxLayout(notes_widget)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Take quick notes here...")
        self.notes_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        layout.addWidget(self.notes_edit)
        
        self.widgets_stack.addWidget(notes_widget)
        
    def perform_search(self):
        query = self.search_bar.text().strip()
        if query:
            if '.' in query and ' ' not in query:
                url = query if query.startswith('http') else f'https://{query}'
            else:
                search_engine = self.browser.settings.value("search_engine", "Google")
                if search_engine == "Google":
                    url = f'https://www.google.com/search?q={quote(query)}'
                elif search_engine == "Bing":
                    url = f'https://www.bing.com/search?q={quote(query)}'
                else:
                    url = f'https://duckduckgo.com/?q={quote(query)}'
                    
            self.browser.open_url(url)

# First Run Wizard
class FirstRunWizard(QWizard):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Nexa Browser Setup")
        self.setFixedSize(700, 550)
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
        # Save all settings
        settings = self.browser.settings
        
        settings.setValue("first_run", False)
        settings.setValue("theme", self.field("theme"))
        settings.setValue("font_size", self.field("font_size"))
        settings.setValue("font_family", self.field("font_family"))
        settings.setValue("search_engine", self.field("search_engine"))
        settings.setValue("ai_enabled", self.field("ai_enabled"))
        settings.setValue("ai_provider", self.field("ai_provider"))
        settings.setValue("hardware_acceleration", self.field("hardware_acceleration"))
        settings.setValue("show_bookmarks", self.field("show_bookmarks"))
        
        # Apply settings
        self.browser.apply_settings()
        
        super().accept()

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to Nexa Browser")
        self.setSubTitle("Thank you for choosing Nexa Browser. Let's get started with the setup.")
        
        layout = QVBoxLayout()
        
        welcome_text = QLabel("""
            <html>
            <h1>Welcome to Nexa Browser! 🌐</h1>
            <p>Thank you for choosing Nexa Browser - your modern, AI-powered browsing companion.</p>
            <p>This quick setup will help you customize the browser to your preferences and unlock all its powerful features.</p>
            <br>
            <p><b>Features you'll enjoy:</b></p>
            <ul>
                <li>🤖 Built-in AI Assistant for smart browsing</li>
                <li>🎨 Fully customizable modern interface</li>
                <li>⚡ Lightning-fast performance</li>
                <li>🔒 Enhanced privacy and security</li>
                <li>📥 Advanced download manager</li>
            </ul>
            </html>
        """)
        welcome_text.setWordWrap(True)
        layout.addWidget(welcome_text)
        
        self.setLayout(layout)

class ThemePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Appearance Customization")
        self.setSubTitle("Choose how Nexa Browser looks and feels")
        
        layout = QVBoxLayout()
        
        # Theme selection
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QVBoxLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto (System)"])
        theme_layout.addWidget(QLabel("Color Theme:"))
        theme_layout.addWidget(self.theme_combo)
        self.registerField("theme", self.theme_combo, "currentText")
        
        # Font selection
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Verdana"])
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        
        font_layout.addRow("Font Family:", self.font_combo)
        font_layout.addRow("Font Size:", self.font_size)
        
        self.registerField("font_family", self.font_combo, "currentText")
        self.registerField("font_size", self.font_size, "value")
        
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        self.setLayout(layout)

class SearchEnginePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Search Settings")
        self.setSubTitle("Choose your default search engine")
        
        layout = QVBoxLayout()
        
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo"])
        layout.addWidget(QLabel("Default Search Engine:"))
        layout.addWidget(self.search_combo)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.registerField("search_engine", self.search_combo, "currentText")

class AISetupPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("AI Assistant Setup")
        self.setSubTitle("Configure your AI-powered browsing companion")
        
        layout = QVBoxLayout()
        
        self.ai_enabled = QCheckBox("Enable AI Assistant")
        self.ai_enabled.setChecked(True)
        layout.addWidget(self.ai_enabled)
        self.registerField("ai_enabled", self.ai_enabled)
        
        ai_desc = QLabel("""
            <p>The Nexa AI Assistant can help you with:</p>
            <ul>
                <li>📝 <b>Page Summarization</b> - Get quick summaries of long articles</li>
                <li>🌐 <b>Real-time Translation</b> - Translate content between languages</li>
                <li>🔍 <b>Content Explanation</b> - Understand complex topics easily</li>
                <li>✨ <b>Content Generation</b> - Write emails, posts, and more</li>
                <li>💡 <b>Smart Suggestions</b> - Context-aware help and ideas</li>
            </ul>
        """)
        ai_desc.setWordWrap(True)
        layout.addWidget(ai_desc)
        
        provider_group = QGroupBox("AI Provider (Advanced)")
        provider_layout = QVBoxLayout(provider_group)
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI GPT", "Google Gemini", "Microsoft Copilot", "Local AI"])
        provider_layout.addWidget(QLabel("AI Service Provider:"))
        provider_layout.addWidget(self.provider_combo)
        
        layout.addWidget(provider_group)
        
        self.registerField("ai_provider", self.provider_combo, "currentText")
        self.setLayout(layout)

class AdvancedPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Advanced Settings")
        self.setSubTitle("Configure additional options for power users")
        
        layout = QVBoxLayout()
        
        options = [
            ("Enable hardware acceleration", "hardware_acceleration", True),
            ("Show bookmark bar by default", "show_bookmarks", True),
            ("Block pop-up windows", "block_popups", True),
            ("Enable Do Not Track", "do_not_track", False),
            ("Warn before closing multiple tabs", "warn_multiple_tabs", True),
            ("Automatically update browser", "auto_update", True)
        ]
        
        for text, field, default in options:
            checkbox = QCheckBox(text)
            checkbox.setChecked(default)
            layout.addWidget(checkbox)
            self.registerField(field, checkbox)
            
        layout.addStretch()
        
        self.setLayout(layout)

# Main Browser Window
class NexaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("NexaBrowser", "Settings")
        self.ai_service = AIService()
        self.ai_assistant = AIAssistant(self.ai_service)
        self.download_manager = DownloadManager(self)
        
        self.check_first_run()
        self.setup_ui()
        self.apply_settings()
        
    def check_first_run(self):
        if self.settings.value("first_run", True, type=bool):
            wizard = FirstRunWizard(self)
            wizard.exec()
            
    def setup_ui(self):
        self.setWindowTitle("Nexa Browser")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set window properties for modern look
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        
        # Title bar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Main content with splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.main_splitter, 1)
        
        # Browser area
        self.setup_browser_area()
        self.main_splitter.addWidget(self.browser_area)
        
        # AI Sidebar (initially hidden)
        self.ai_sidebar = AISidebar(self.ai_assistant)
        self.ai_sidebar.hide()
        self.main_splitter.addWidget(self.ai_sidebar)
        
        self.main_splitter.setSizes([1000, 350])
        
        # Create initial tab
        self.add_new_tab()
        
        # Apply styles
        self.apply_stylesheet()
        
    def setup_browser_area(self):
        self.browser_area = QWidget()
        browser_layout = QVBoxLayout(self.browser_area)
        browser_layout.setContentsMargins(0, 0, 0, 0)
        browser_layout.setSpacing(0)
        
        # Toolbar
        self.setup_toolbar()
        browser_layout.addWidget(self.toolbar)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        browser_layout.addWidget(self.tabs)
        
    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(18, 18))
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f8f9fa;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                spacing: 3px;
                padding: 3px;
            }
        """)
        
        # Navigation buttons
        nav_actions = [
            ("←", "Back", self.navigate_back),
            ("→", "Forward", self.navigate_forward),
            ("↻", "Reload", self.reload_page),
            ("🏠", "Home", self.go_home),
        ]
        
        for icon, tip, slot in nav_actions:
            action = QAction(icon, self)
            action.setToolTip(tip)
            action.triggered.connect(slot)
            self.toolbar.addAction(action)
            
        self.toolbar.addSeparator()
        
        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter website address or search...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
                background: white;
                min-width: 400px;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)
        self.toolbar.addWidget(self.url_bar)
        
        self.toolbar.addSeparator()
        
        # Feature buttons
        feature_actions = [
            ("🤖", "AI Assistant", self.toggle_ai_sidebar),
            ("📥", "Downloads", self.show_downloads),
            ("➕", "New Tab", self.add_new_tab),
            ("⚙️", "Settings", self.show_settings),
        ]
        
        for icon, tip, slot in feature_actions:
            action = QAction(icon, self)
            action.setToolTip(tip)
            action.triggered.connect(slot)
            self.toolbar.addAction(action)
            
    def add_new_tab(self, url: str = None, make_current: bool = True):
        if url is None:
            # Show home page for new tabs
            home_widget = HomePage(self)
            browser = QWebEngineView()
            self.tabs.addTab(home_widget, "🏠 Home")
            
            # Add a proper browser tab as well
            browser = QWebEngineView()
            browser.setUrl(QUrl("https://www.google.com"))
        else:
            browser = QWebEngineView()
            browser.setUrl(QUrl(url))
            
        # Configure browser
        browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))
        browser.urlChanged.connect(lambda url: self.update_urlbar(url, browser))
        browser.loadProgress.connect(self.update_progress)
        browser.loadFinished.connect(self.page_loaded)
        
        # Add to tabs
        index = self.tabs.addTab(browser, "New Tab")
        if make_current:
            self.tabs.setCurrentIndex(index)
            
        return browser
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            
    def tab_changed(self, index):
        if index >= 0:
            current_widget = self.tabs.widget(index)
            if isinstance(current_widget, QWebEngineView):
                self.update_urlbar(current_widget.url(), current_widget)
                
    def update_tab_title(self, browser: QWebEngineView, title: str):
        index = self.tabs.indexOf(browser)
        if index != -1:
            display_title = title[:20] + "..." if len(title) > 23 else title
            self.tabs.setTabText(index, display_title)
            self.tabs.setTabToolTip(index, title)
            
    def update_urlbar(self, url: QUrl, browser: QWebEngineView = None):
        if browser is None or browser == self.tabs.currentWidget():
            self.url_bar.setText(url.toString())
            self.url_bar.setCursorPosition(0)
            
    def update_progress(self, progress: int):
        # Could update progress bar in future
        pass
        
    def page_loaded(self):
        # Handle page load completion
        pass
        
    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        self.open_url(url)
        
    def open_url(self, url: str):
        current_widget = self.tabs.currentWidget()
        
        if isinstance(current_widget, HomePage):
            # Replace home page with browser view
            index = self.tabs.currentIndex()
            browser = QWebEngineView()
            
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            browser.setUrl(QUrl(url))
            browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))
            browser.urlChanged.connect(lambda url: self.update_urlbar(url, browser))
            
            self.tabs.removeTab(index)
            new_index = self.tabs.addTab(browser, "Loading...")
            self.tabs.setCurrentIndex(new_index)
        elif isinstance(current_widget, QWebEngineView):
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            current_widget.setUrl(QUrl(url))
            
    def navigate_back(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QWebEngineView):
            current_widget.back()
            
    def navigate_forward(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QWebEngineView):
            current_widget.forward()
            
    def reload_page(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QWebEngineView):
            current_widget.reload()
            
    def go_home(self):
        index = self.tabs.currentIndex()
        home_page = HomePage(self)
        self.tabs.removeTab(index)
        self.tabs.insertTab(index, home_page, "🏠 Home")
        self.tabs.setCurrentIndex(index)
        
    def toggle_ai_sidebar(self):
        if self.ai_sidebar.isVisible():
            self.ai_sidebar.hide()
        else:
            self.ai_sidebar.show()
            
    def show_downloads(self):
        self.download_manager.show()
        self.download_manager.raise_()
        
    def show_settings(self):
        # Could implement settings dialog
        QMessageBox.information(self, "Settings", "Settings dialog will be implemented here")
        
    def apply_settings(self):
        # Apply theme
        theme = self.settings.value("theme", "Light")
        self.apply_theme(theme)
        
        # Apply font
        font_family = self.settings.value("font_family", "Segoe UI")
        font_size = self.settings.value("font_size", 12, type=int)
        app = QApplication.instance()
        app.setFont(QFont(font_family, font_size))
        
        # Apply AI settings
        ai_enabled = self.settings.value("ai_enabled", True, type=bool)
        self.ai_service.enabled = ai_enabled
        
    def apply_theme(self, theme: str):
        if theme == "Dark" or (theme == "Auto (System)" and self.is_dark_time()):
            self.set_dark_theme()
        else:
            self.set_light_theme()
            
    def set_dark_theme(self):
        self.apply_stylesheet("dark")
        
    def set_light_theme(self):
        self.apply_stylesheet("light")
        
    def apply_stylesheet(self, theme: str = "light"):
        if theme == "dark":
            style = """
                #centralWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 8px;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #2d2d2d;
                }
                QTabBar::tab {
                    background-color: #3d3d3d;
                    color: white;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-radius: 4px 4px 0 0;
                }
                QTabBar::tab:selected {
                    background-color: #0078d4;
                }
                QTabBar::tab:hover {
                    background-color: #555;
                }
            """
        else:
            style = """
                #centralWidget {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: white;
                }
                QTabBar::tab {
                    background-color: #f0f0f0;
                    color: black;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-radius: 4px 4px 0 0;
                }
                QTabBar::tab:selected {
                    background-color: white;
                    border-bottom: 2px solid #0078d4;
                }
                QTabBar::tab:hover {
                    background-color: #e8e8e8;
                }
            """
            
        self.centralWidget().setStyleSheet(style)
        
    def is_dark_time(self):
        now = datetime.now().time()
        return now.hour >= 18 or now.hour < 6
        
    def closeEvent(self, event):
        # Save window state
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        event.accept()

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
    app.setOrganizationDomain("hessamedien.com")
    
    # Set modern fusion style
    app.setStyle(QStyleFactory.create("Fusion"))
    
    # Create and show browser
    browser = NexaBrowser()
    browser.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()