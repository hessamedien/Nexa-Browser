#!/usr/bin/env python3
"""
Nexa Browser - Modern, Lightweight AI-Powered Web Browser
Enhanced with beautiful Windows 11 style UI and comprehensive features
Creator: Hessamedien (https://www.instagram.com/hessamedien)
"""

import sys
import os
import json
import tempfile
import time
from pathlib import Path
from datetime import datetime
import sqlite3
from urllib.parse import urlparse
import zipfile
import gzip
from collections import deque
import hashlib
import base64
import requests
import threading
from typing import Dict, List, Optional
import random
import webbrowser

# Third-party imports
try:
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
    from PyQt6.QtNetwork import QNetworkProxy
    from PyQt6.QtWebChannel import QWebChannel
    from PyQt6.QtPrintSupport import QPrinter
except ImportError:
    print("Please install PyQt6: pip install PyQt6 PyQt6-WebEngine PyQt6-Pdf")
    sys.exit(1)

class FirstRunWizard(QDialog):
    """Beautiful first-run wizard for initial setup"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_data = {
            'theme': 'light',
            'font_family': 'Segoe UI',
            'font_size': 10,
            'homepage_background': 'gradient',
            'custom_wallpaper': '',
            'ai_enabled': True,
            'quick_actions': ['gmail', 'youtube', 'drive', 'maps', 'news', 'weather'],
            'show_clock': True,
            'show_weather': True,
            'show_ai_section': True
        }
        self.current_step = 0
        self.setup_ui()
        
    def setup_ui(self):
        """Setup wizard UI"""
        self.setWindowTitle("Welcome to Nexa Browser")
        self.setFixedSize(800, 600)
        self.setModal(True)
        
        # Apply modern styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.4);
            }
            QComboBox, QLineEdit {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px;
                color: #333;
                font-size: 14px;
            }
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid white;
                border-radius: 5px;
            }
            QCheckBox::indicator:checked {
                background: white;
            }
            QGroupBox {
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🌐 Welcome to Nexa Browser")
        header.setStyleSheet("font-size: 32px; font-weight: bold; padding: 20px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Let's personalize your browsing experience")
        subtitle.setStyleSheet("font-size: 18px; opacity: 0.9; padding: 10px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Content area
        self.content_stack = QStackedWidget()
        self.setup_welcome_step()
        self.setup_theme_step()
        self.setup_homepage_step()
        self.setup_ai_step()
        self.setup_final_step()
        
        layout.addWidget(self.content_stack, 1)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("← Previous")
        self.prev_btn.clicked.connect(self.previous_step)
        self.prev_btn.setVisible(False)
        nav_layout.addWidget(self.prev_btn)
        
        nav_layout.addStretch()
        
        self.next_btn = QPushButton("Next →")
        self.next_btn.clicked.connect(self.next_step)
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
        
        self.setLayout(layout)
        
    def setup_welcome_step(self):
        """Setup welcome step"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Features list
        features = [
            "🎨 Beautiful Windows 11 style interface",
            "🤖 Advanced AI assistant with multiple agents",
            "🏠 Fully customizable homepage",
            "🎯 Quick actions and shortcuts",
            "🌙 Dark/Light theme support",
            "🔒 Privacy focused browsing",
            "⚡ Fast and lightweight",
            "🎵 Media and entertainment features"
        ]
        
        for feature in features:
            label = QLabel(f"• {feature}")
            label.setStyleSheet("font-size: 16px; padding: 8px;")
            layout.addWidget(label)
        
        layout.addStretch()
        widget.setLayout(layout)
        self.content_stack.addWidget(widget)
        
    def setup_theme_step(self):
        """Setup theme customization step"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Theme selection
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QVBoxLayout()
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Light Theme", "Dark Theme", "Auto (System)"])
        theme_combo.currentIndexChanged.connect(
            lambda i: self.setup_data.update({'theme': ['light', 'dark', 'auto'][i]})
        )
        theme_layout.addWidget(QLabel("Select Theme:"))
        theme_layout.addWidget(theme_combo)
        
        # Font selection
        font_combo = QComboBox()
        font_combo.addItems(["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Verdana", "Georgia"])
        font_combo.currentTextChanged.connect(
            lambda f: self.setup_data.update({'font_family': f})
        )
        theme_layout.addWidget(QLabel("Font Family:"))
        theme_layout.addWidget(font_combo)
        
        # Font size
        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setRange(8, 16)
        size_slider.setValue(10)
        size_slider.valueChanged.connect(
            lambda v: self.setup_data.update({'font_size': v})
        )
        theme_layout.addWidget(QLabel("Font Size:"))
        theme_layout.addWidget(size_slider)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        layout.addStretch()
        widget.setLayout(layout)
        self.content_stack.addWidget(widget)
        
    def setup_homepage_step(self):
        """Setup homepage customization step"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        homepage_group = QGroupBox("Homepage Settings")
        homepage_layout = QVBoxLayout()
        
        # Background type
        bg_combo = QComboBox()
        bg_combo.addItems(["Gradient", "Solid Color", "Image", "Animated"])
        bg_combo.currentTextChanged.connect(
            lambda t: self.setup_data.update({'homepage_background': t.lower()})
        )
        homepage_layout.addWidget(QLabel("Background Type:"))
        homepage_layout.addWidget(bg_combo)
        
        # Quick actions selection
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout()
        
        actions = [
            ('gmail', 'Gmail', True),
            ('youtube', 'YouTube', True),
            ('drive', 'Google Drive', True),
            ('maps', 'Google Maps', True),
            ('news', 'News', True),
            ('weather', 'Weather', True),
            ('github', 'GitHub', False),
            ('twitter', 'Twitter', False),
            ('reddit', 'Reddit', False),
            ('spotify', 'Spotify', False)
        ]
        
        for action_id, action_name, default in actions:
            cb = QCheckBox(action_name)
            cb.setChecked(default)
            cb.toggled.connect(
                lambda checked, aid=action_id: self.toggle_quick_action(aid, checked)
            )
            actions_layout.addWidget(cb)
        
        actions_group.setLayout(actions_layout)
        homepage_layout.addWidget(actions_group)
        
        # Widgets to show
        widgets_group = QGroupBox("Homepage Widgets")
        widgets_layout = QVBoxLayout()
        
        show_clock = QCheckBox("Show Clock")
        show_clock.setChecked(True)
        show_clock.toggled.connect(
            lambda c: self.setup_data.update({'show_clock': c})
        )
        widgets_layout.addWidget(show_clock)
        
        show_weather = QCheckBox("Show Weather")
        show_weather.setChecked(True)
        show_weather.toggled.connect(
            lambda c: self.setup_data.update({'show_weather': c})
        )
        widgets_layout.addWidget(show_weather)
        
        show_ai = QCheckBox("Show AI Section")
        show_ai.setChecked(True)
        show_ai.toggled.connect(
            lambda c: self.setup_data.update({'show_ai_section': c})
        )
        widgets_layout.addWidget(show_ai)
        
        widgets_group.setLayout(widgets_layout)
        homepage_layout.addWidget(widgets_group)
        
        homepage_group.setLayout(homepage_layout)
        layout.addWidget(homepage_group)
        layout.addStretch()
        widget.setLayout(layout)
        self.content_stack.addWidget(widget)
        
    def setup_ai_step(self):
        """Setup AI features step"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        ai_group = QGroupBox("AI Assistant Settings")
        ai_layout = QVBoxLayout()
        
        enable_ai = QCheckBox("Enable AI Assistant")
        enable_ai.setChecked(True)
        enable_ai.toggled.connect(
            lambda c: self.setup_data.update({'ai_enabled': c})
        )
        ai_layout.addWidget(enable_ai)
        
        # AI features description
        features = QLabel(
            "Nexa AI can help you with:\n"
            "• Web searches and research\n"
            "• Translations between languages\n"
            "• Content creation and writing\n"
            "• Calculations and problem solving\n"
            "• Coding and programming help\n"
            "• Time and date information\n"
            "• Jokes and inspirational quotes\n"
            "• Reminders and notes\n"
            "• Password generation\n"
            "• QR code generation\n"
            "• Song lyrics\n"
            "• Recipes and cooking help\n"
            "• Exercise suggestions\n"
            "• Meditation guidance"
        )
        features.setStyleSheet("font-size: 14px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;")
        ai_layout.addWidget(features)
        
        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)
        layout.addStretch()
        widget.setLayout(layout)
        self.content_stack.addWidget(widget)
        
    def setup_final_step(self):
        """Setup final step"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Completion message
        complete_msg = QLabel("🎉 Setup Complete!")
        complete_msg.setStyleSheet("font-size: 28px; font-weight: bold; padding: 20px;")
        complete_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(complete_msg)
        
        summary = QLabel(
            "Your Nexa Browser is ready to use!\n\n"
            "You can always change these settings later through:\n"
            "• Settings menu (Ctrl+,)\n"
            "• Homepage customization\n"
            "• Right-click context menus"
        )
        summary.setStyleSheet("font-size: 16px; padding: 20px; text-align: center;")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(summary)
        
        layout.addStretch()
        widget.setLayout(layout)
        self.content_stack.addWidget(widget)
        
    def toggle_quick_action(self, action_id, enabled):
        """Toggle quick action in setup data"""
        actions = self.setup_data['quick_actions']
        if enabled and action_id not in actions:
            actions.append(action_id)
        elif not enabled and action_id in actions:
            actions.remove(action_id)
            
    def previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.content_stack.setCurrentIndex(self.current_step)
            self.update_navigation()
            
    def next_step(self):
        """Go to next step"""
        if self.current_step < self.content_stack.count() - 1:
            self.current_step += 1
            self.content_stack.setCurrentIndex(self.current_step)
            self.update_navigation()
        else:
            self.accept()
            
    def update_navigation(self):
        """Update navigation buttons"""
        self.prev_btn.setVisible(self.current_step > 0)
        
        if self.current_step == self.content_stack.count() - 1:
            self.next_btn.setText("Finish")
        else:
            self.next_btn.setText("Next →")
            
    def get_setup_data(self):
        """Get the setup configuration"""
        return self.setup_data


class FreeAIAgents:
    """Free AI Agents using various APIs and services"""
    
    def __init__(self):
        self.agents = {
            'research': ResearchAgent(),
            'creative': CreativeAgent(),
            'technical': TechnicalAgent(),
            'productivity': ProductivityAgent(),
            'entertainment': EntertainmentAgent()
        }
        self.active_agents = []
        
    def get_agent_response(self, agent_type, query, context=None):
        """Get response from specific AI agent"""
        if agent_type in self.agents:
            return self.agents[agent_type].process(query, context)
        return "I'm not sure how to help with that. Try asking about research, creative tasks, technical help, productivity, or entertainment."
    
    def get_suggested_agent(self, query):
        """Suggest the best agent for a query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['research', 'study', 'learn', 'find information']):
            return 'research'
        elif any(word in query_lower for word in ['write', 'create', 'story', 'poem', 'content']):
            return 'creative'
        elif any(word in query_lower for word in ['code', 'program', 'technical', 'debug', 'algorithm']):
            return 'technical'
        elif any(word in query_lower for word in ['organize', 'plan', 'schedule', 'productivity']):
            return 'productivity'
        elif any(word in query_lower for word in ['joke', 'entertain', 'game', 'fun']):
            return 'entertainment'
        else:
            return 'research'  # Default agent


class ResearchAgent:
    """AI Agent for research and information gathering"""
    
    def process(self, query, context=None):
        research_topics = {
            'science': '🔬 I can help you research scientific topics using open-access journals and educational resources.',
            'technology': '💻 I can gather the latest tech news and information from reliable sources.',
            'history': '📚 I can provide historical information and context from verified sources.',
            'current events': '📰 I can help you stay updated with current events from news aggregators.',
            'academic': '🎓 I can assist with academic research using open educational resources.'
        }
        
        for topic, response in research_topics.items():
            if topic in query.lower():
                return response
                
        return "🔍 I can help you research various topics. Please specify if you're looking for scientific, technological, historical, or current events information."


class CreativeAgent:
    """AI Agent for creative tasks"""
    
    def process(self, query, context=None):
        creative_skills = {
            'writing': '✍️ I can help with creative writing, stories, poems, and content creation.',
            'design': '🎨 I can provide design inspiration and creative ideas for your projects.',
            'music': '🎵 I can help with music theory, composition ideas, and creative expression.',
            'art': '🖼️ I can discuss art techniques, styles, and provide creative inspiration.',
            'brainstorm': '💡 I can help brainstorm ideas for your creative projects.'
        }
        
        for skill, response in creative_skills.items():
            if skill in query.lower():
                return response
                
        return "🎨 I'm your creative assistant! I can help with writing, design, music, art, and brainstorming ideas. What creative project are you working on?"


class TechnicalAgent:
    """AI Agent for technical and programming help"""
    
    def process(self, query, context=None):
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'html', 'css']
        frameworks = ['django', 'flask', 'react', 'vue', 'angular', 'node', 'spring', 'laravel']
        
        for lang in languages:
            if lang in query.lower():
                return f"💻 I can help with {lang} programming! I can explain concepts, help debug code, and suggest best practices."
                
        for framework in frameworks:
            if framework in query.lower():
                return f"🚀 I can assist with {framework} development! I can help with setup, troubleshooting, and best practices."
                
        return "🔧 I'm your technical assistant! I can help with programming, debugging, algorithms, system design, and technical concepts. What are you working on?"


class ProductivityAgent:
    """AI Agent for productivity and organization"""
    
    def process(self, query, context=None):
        productivity_areas = {
            'time management': '⏰ I can help with time management techniques like Pomodoro, time blocking, and prioritization.',
            'task management': '✅ I can assist with task organization, to-do lists, and project planning.',
            'goal setting': '🎯 I can help you set and track SMART goals for personal and professional growth.',
            'habits': '📊 I can provide guidance on building good habits and breaking bad ones.',
            'focus': '🔍 I can suggest techniques to improve focus and reduce distractions.'
        }
        
        for area, response in productivity_areas.items():
            if area in query.lower():
                return response
                
        return "📈 I'm your productivity assistant! I can help with time management, task organization, goal setting, habit building, and focus improvement. What area would you like to work on?"


class EntertainmentAgent:
    """AI Agent for entertainment and fun"""
    
    def process(self, query, context=None):
        entertainment_options = {
            'joke': self.tell_joke(),
            'story': '📖 I can tell you short stories or help create interactive narratives.',
            'game': '🎮 I can suggest games to play or create text-based adventure games.',
            'trivia': '🤔 I can provide interesting trivia facts on various topics.',
            'music': '🎵 I can recommend music based on your mood or discuss music theory.',
            'movie': '🎬 I can suggest movies to watch and discuss film techniques.'
        }
        
        for option, response in entertainment_options.items():
            if option in query.lower():
                return response
                
        return "🎭 I'm your entertainment assistant! I can tell jokes, share stories, suggest games, provide trivia, recommend music and movies. What would you like to do for fun?"

    def tell_joke(self):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the web developer go broke? Because he lost his domain in a bet!",
            "What's a computer's favorite beat? An algorithm!",
            "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings!",
            "Why do Python developers wear glasses? Because they can't C#!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
        ]
        return f"😄 {random.choice(jokes)}"


class AdvancedAIAssistant:
    """Enhanced AI Assistant with free AI agents and extensive capabilities"""
    
    def __init__(self):
        self.chat_history = []
        self.enabled = True
        self.ai_agents = FreeAIAgents()
        self.learning_enabled = True
        self.context_memory = {}
        
    def process_query(self, query, context=None):
        """Process user query with enhanced responses and AI agents"""
        if not self.enabled:
            return "AI Assistant is currently disabled. Enable it in settings."
            
        # Use AI agents for specialized responses
        suggested_agent = self.ai_agents.get_suggested_agent(query)
        agent_response = self.ai_agents.get_agent_response(suggested_agent, query, context)
        
        # Enhanced responses with agent integration
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["summary", "summarize", "summarise"]):
            return f"{agent_response}\n\n📄 I'll analyze the current page and provide a concise summary of its main points and key information."
        elif any(word in query_lower for word in ["translate", "translation"]):
            return f"{agent_response}\n\n🌍 {self.handle_translation(query)}"
        elif any(word in query_lower for word in ["search", "find"]):
            return f"{agent_response}\n\n🔍 {self.handle_search(query)}"
        elif any(word in query_lower for word in ["email", "write", "compose", "draft"]):
            return f"{agent_response}\n\n📧 {self.draft_email(query)}"
        elif any(word in query_lower for word in ["weather", "forecast"]):
            return f"{agent_response}\n\n⛅ {self.get_weather(query)}"
        elif any(word in query_lower for word in ["news", "headlines"]):
            return f"{agent_response}\n\n📰 {self.get_news_headlines()}"
        elif any(word in query_lower for word in ["calculate", "math", "compute"]):
            return f"{agent_response}\n\n🧮 {self.solve_math(query)}"
        elif any(word in query_lower for word in ["code", "programming", "developer"]):
            return f"{agent_response}\n\n💻 {self.handle_coding(query)}"
        elif any(word in query_lower for word in ["time", "date"]):
            return f"{agent_response}\n\n🕒 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif any(word in query_lower for word in ["bookmark", "save"]):
            return f"{agent_response}\n\n🔖 I can help you manage bookmarks. Use Ctrl+D to bookmark the current page."
        elif any(word in query_lower for word in ["history", "recent"]):
            return f"{agent_response}\n\n📚 I can show your browsing history. Use Ctrl+H to view history."
        elif any(word in query_lower for word in ["hello", "hi", "hey"]):
            return f"👋 Hello! I'm Nexa AI with specialized agents for research, creativity, technical help, productivity, and entertainment. How can I assist you today?"
        elif any(word in query_lower for word in ["thank", "thanks"]):
            return "😊 You're welcome! Is there anything else I can help you with?"
        elif any(word in query_lower for word in ["joke", "funny"]):
            return f"{agent_response}"
        elif any(word in query_lower for word in ["quote", "inspiration"]):
            return f"{agent_response}\n\n💫 {self.get_inspirational_quote()}"
        elif any(word in query_lower for word in ["learn", "remember"]):
            return f"{agent_response}\n\n🧠 {self.learn_information(query)}"
        elif any(word in query_lower for word in ["remind", "reminder"]):
            return f"{agent_response}\n\n⏰ {self.set_reminder(query)}"
        elif any(word in query_lower for word in ["define", "dictionary"]):
            return f"{agent_response}\n\n📖 {self.define_word(query)}"
        elif any(word in query_lower for word in ["currency", "convert"]):
            return f"{agent_response}\n\n💱 {self.currency_conversion(query)}"
        elif any(word in query_lower for word in ["note", "notes"]):
            return f"{agent_response}\n\n📝 {self.manage_notes(query)}"
        elif any(word in query_lower for word in ["task", "todo"]):
            return f"{agent_response}\n\n✅ {self.manage_tasks(query)}"
        elif any(word in query_lower for word in ["password", "generate"]):
            return f"{agent_response}\n\n🔐 {self.generate_password(query)}"
        elif any(word in query_lower for word in ["qr", "qrcode"]):
            return f"{agent_response}\n\n📱 {self.generate_qr_code(query)}"
        elif any(word in query_lower for word in ["lyrics", "song"]):
            return f"{agent_response}\n\n🎵 {self.find_lyrics(query)}"
        elif any(word in query_lower for word in ["recipe", "cook"]):
            return f"{agent_response}\n\n👨‍🍳 {self.get_recipe(query)}"
        elif any(word in query_lower for word in ["exercise", "workout"]):
            return f"{agent_response}\n\n💪 {self.suggest_exercise(query)}"
        elif any(word in query_lower for word in ["meditate", "meditation"]):
            return f"{agent_response}\n\n🧘 {self.guide_meditation(query)}"
        else:
            return f"🤔 I understand you're asking about: '{query}'. {agent_response}"

    def handle_translation(self, query):
        """Handle translation requests"""
        languages = {
            'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de',
            'italian': 'it', 'portuguese': 'pt', 'russian': 'ru', 'chinese': 'zh',
            'japanese': 'ja', 'korean': 'ko', 'arabic': 'ar', 'hindi': 'hi',
            'persian': 'fa', 'turkish': 'tr'
        }
        
        for lang, code in languages.items():
            if lang in query.lower():
                return f"I'll translate to {lang.capitalize()}. Please provide the text you want to translate."
        
        return "I can translate text between 50+ languages. Please specify the target language (e.g., 'translate to Spanish')."

    def handle_search(self, query):
        """Handle search requests"""
        search_terms = query.replace("search", "").replace("find", "").strip()
        if search_terms:
            return f"I'll search the web for: '{search_terms}'. Would you like me to open search results?"
        return "What would you like me to search for?"

    def draft_email(self, query):
        """Draft email based on query"""
        email_types = {
            'business': "I'll help you draft a professional business email. Please provide recipient details and key points.",
            'personal': "I'll help you write a personal email. What's the main message?",
            'complaint': "I'll help draft a professional complaint email. Please describe the issue.",
            'thank you': "I'll help write a thank you email. What are you thankful for?",
            'follow up': "I'll help with a follow-up email. What's the context?"
        }
        
        for email_type, response in email_types.items():
            if email_type in query.lower():
                return response
        
        return "I can help draft various types of emails. Please specify the purpose (business, personal, complaint, etc.)"

    def get_weather(self, query):
        """Get weather information"""
        locations = ['tehran', 'london', 'new york', 'tokyo', 'paris', 'dubai']
        for location in locations:
            if location in query.lower():
                return f"I'll get the weather forecast for {location.title()}. In the full version, I'll show detailed weather information."
        return "I can provide weather information. Please specify a location or enable location services."

    def get_news_headlines(self):
        """Get news headlines"""
        return "I'll fetch the latest news headlines from trusted sources. You can customize news preferences in settings."

    def solve_math(self, query):
        """Solve mathematical problems"""
        try:
            math_expr = query.lower().replace("calculate", "").replace("math", "").replace("compute", "").strip()
            if any(op in math_expr for op in ['+', '-', '*', '/', '^']):
                # Simple safe evaluation (in real implementation, use proper math parser)
                math_expr = math_expr.replace('^', '**')
                # Remove any non-math characters for safety
                safe_chars = set('0123456789+-*/.() ')
                safe_expr = ''.join(c for c in math_expr if c in safe_chars)
                if safe_expr:
                    result = eval(safe_expr)
                    return f"Calculating: {safe_expr} = {result}"
            return "I can perform calculations and solve mathematical problems. What would you like me to calculate?"
        except Exception as e:
            return f"I couldn't calculate that. Please provide a valid mathematical expression. Error: {str(e)}"

    def handle_coding(self, query):
        """Handle programming/coding requests"""
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust']
        for lang in languages:
            if lang in query.lower():
                return f"I can help with {lang} programming. What specific problem are you facing?"
        return "I can help with programming questions, code examples, and debugging. What language or problem are you working on?"

    def get_inspirational_quote(self):
        """Get inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "Believe you can and you're halfway there. - Theodore Roosevelt"
        ]
        return random.choice(quotes)

    def learn_information(self, query):
        """Learn and remember information"""
        if "that" in query.lower() or "remember" in query.lower():
            # Extract key information to remember
            key_info = query.replace("remember", "").replace("that", "").strip()
            if key_info:
                self.context_memory['learned_info'] = key_info
                return f"I've learned and stored: '{key_info}'. I'll remember this for our conversation."
        return "I can learn and remember information. What would you like me to remember?"

    def set_reminder(self, query):
        """Set a reminder"""
        return "I can set reminders for you. Please specify the time and what you'd like to be reminded about."

    def define_word(self, query):
        """Define a word"""
        words = query.lower().replace("define", "").replace("dictionary", "").strip()
        if words:
            return f"I'll look up the definition of '{words}'. In the full version, I'll provide detailed definitions."
        return "I can define words for you. What word would you like me to define?"

    def currency_conversion(self, query):
        """Handle currency conversion"""
        return "I can convert between different currencies. Please specify the amount and currencies (e.g., '100 USD to EUR')."

    def manage_notes(self, query):
        """Manage notes"""
        if "add" in query.lower() or "create" in query.lower():
            return "I can help you create and manage notes. What would you like to add to your notes?"
        return "I can help you manage your notes. You can add, view, or delete notes."

    def manage_tasks(self, query):
        """Manage tasks"""
        return "I can help you manage your to-do list and tasks. What would you like to add to your tasks?"

    def generate_password(self, query):
        """Generate secure password"""
        length = 12
        if "strong" in query.lower():
            length = 16
        elif "weak" in query.lower():
            length = 8
            
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        return f"Generated password: `{password}`\n\nPlease save this password in a secure location."

    def generate_qr_code(self, query):
        """Generate QR code"""
        data = query.replace("qr", "").replace("qrcode", "").strip()
        if data:
            return f"I'll generate a QR code for: '{data}'. In the full version, I'll display the QR code."
        return "I can generate QR codes. What data would you like to encode?"

    def find_lyrics(self, query):
        """Find song lyrics"""
        song = query.replace("lyrics", "").replace("song", "").strip()
        if song:
            return f"I'll find lyrics for: '{song}'. In the full version, I'll display the complete lyrics."
        return "I can find song lyrics. What song are you looking for?"

    def get_recipe(self, query):
        """Get cooking recipe"""
        dish = query.replace("recipe", "").replace("cook", "").strip()
        if dish:
            return f"I'll find a recipe for: '{dish}'. In the full version, I'll provide detailed cooking instructions."
        return "I can find cooking recipes. What dish would you like to cook?"

    def suggest_exercise(self, query):
        """Suggest exercises"""
        return "I can suggest exercises and workout routines. What type of exercise are you interested in?"

    def guide_meditation(self, query):
        """Guide meditation"""
        return "I can guide you through meditation sessions. Would you like a breathing exercise or mindfulness meditation?"


class EnhancedHomePage:
    """Enhanced homepage with extensive customization"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.customization = {
            'background_type': 'gradient',
            'background_color': '#f8f9fa',
            'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'background_image': '',
            'logo_visible': True,
            'search_bar_style': 'rounded',
            'quick_actions': ['gmail', 'youtube', 'drive', 'maps', 'news', 'weather'],
            'show_ai_section': True,
            'show_weather': True,
            'show_clock': True,
            'layout_style': 'centered',
            'custom_css': '',
            'font_family': 'Segoe UI',
            'font_size': '14px'
        }
    
    def update_customization(self, new_settings):
        """Update homepage customization"""
        self.customization.update(new_settings)
    
    def get_customized_html(self):
        """Generate customized homepage HTML"""
        is_dark = getattr(self.main_window, 'current_theme', 'light') == 'dark'
        
        # Apply customization
        bg_style = self.get_background_style()
        text_color = '#ffffff' if is_dark else '#333333'
        search_style = self.get_search_bar_style()
        layout_class = f"layout-{self.customization['layout_style']}"
        
        quick_actions_html = self.generate_quick_actions()
        ai_section_html = self.generate_ai_section() if self.customization['show_ai_section'] else ''
        weather_html = self.generate_weather_widget() if self.customization['show_weather'] else ''
        clock_html = self.generate_clock_widget() if self.customization['show_clock'] else ''
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nexa Browser</title>
            <style>
                {self.get_base_styles()}
                {self.customization['custom_css']}
            </style>
        </head>
        <body class="{layout_class}" style="background: {bg_style}; color: {text_color};">
            <div class="background-overlay"></div>
            <div class="container">
                {self.generate_logo_section()}
                
                <div class="search-container">
                    <input type="text" class="search-box {search_style}" id="searchBox" 
                           placeholder="Search with Google or enter address..." autofocus>
                </div>
                
                {weather_html}
                {clock_html}
                
                <div class="quick-actions">
                    {quick_actions_html}
                </div>
                
                {ai_section_html}
                
                <div class="customization-panel" id="customizationPanel">
                    <button onclick="toggleCustomization()" class="customize-btn">🎨 Customize</button>
                    <div class="customization-options" id="customizationOptions">
                        <h3>Homepage Customization</h3>
                        <div class="option-group">
                            <label>Background:</label>
                            <select onchange="changeBackground(this.value)">
                                <option value="gradient">Gradient</option>
                                <option value="solid">Solid Color</option>
                                <option value="image">Image</option>
                            </select>
                        </div>
                        <div class="option-group">
                            <label>Layout:</label>
                            <select onchange="changeLayout(this.value)">
                                <option value="centered">Centered</option>
                                <option value="compact">Compact</option>
                                <option value="spacious">Spacious</option>
                            </select>
                        </div>
                        <button onclick="applyCustomization()" class="apply-btn">Apply Changes</button>
                    </div>
                </div>
            </div>
            
            <script>
                {self.get_javascript()}
            </script>
        </body>
        </html>
        """
    
    def get_background_style(self):
        """Get background style based on customization"""
        bg_type = self.customization['background_type']
        if bg_type == 'gradient':
            return self.customization['background_gradient']
        elif bg_type == 'image' and self.customization['background_image']:
            return f"url('{self.customization['background_image']}') center/cover"
        else:
            return self.customization['background_color']
    
    def get_search_bar_style(self):
        """Get search bar style class"""
        return self.customization['search_bar_style']
    
    def get_base_styles(self):
        """Get base CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            color: #333333;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            position: relative;
            transition: all 0.3s ease;
        }
        
        .background-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: inherit;
            z-index: -1;
        }
        
        .container {
            text-align: center;
            padding: 2rem;
            max-width: 1200px;
            width: 90%;
            z-index: 1;
        }
        
        /* Layout variations */
        .layout-centered { justify-content: center; }
        .layout-compact { justify-content: flex-start; padding-top: 1rem; }
        .layout-spacious { justify-content: space-around; }
        
        /* Logo styles */
        .logo {
            margin-bottom: 2rem;
        }
        
        .logo-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .logo-text {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .tagline {
            font-size: 1.2rem;
            opacity: 0.8;
        }
        
        /* Search box styles */
        .search-container {
            margin: 2rem 0;
        }
        
        .search-box {
            width: 100%;
            max-width: 600px;
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
            border: none;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            color: #333333;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            outline: none;
            transition: all 0.3s ease;
        }
        
        .search-box.rounded { border-radius: 25px; }
        .search-box.modern { border-radius: 12px; border: 2px solid #0078d4; }
        .search-box.minimal { 
            border-radius: 0; 
            border-bottom: 2px solid #0078d4;
            background: transparent;
            box-shadow: none;
        }
        .search-box.glass {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .search-box:focus {
            box-shadow: 0 8px 32px rgba(0, 120, 212, 0.3);
            transform: translateY(-2px);
        }
        
        /* Quick actions */
        .quick-actions {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .action-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            text-decoration: none;
            color: inherit;
            transition: all 0.3s ease;
            min-width: 80px;
        }
        
        .action-card:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .action-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        /* AI section */
        .ai-section {
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            max-width: 600px;
            width: 100%;
        }
        
        .ai-title {
            margin-bottom: 1rem;
        }
        
        .ai-input {
            width: 100%;
            padding: 0.8rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: inherit;
            margin-bottom: 1rem;
        }
        
        .ai-response {
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            text-align: left;
        }
        
        /* Weather widget */
        .weather-widget {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .weather-icon {
            font-size: 2rem;
        }
        
        /* Clock widget */
        .clock-widget {
            margin: 1rem 0;
        }
        
        .time {
            font-size: 2rem;
            font-weight: bold;
        }
        
        /* Customization panel */
        .customization-panel {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .customize-btn {
            background: rgba(0, 120, 212, 0.8);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 14px;
            backdrop-filter: blur(10px);
        }
        
        .customization-options {
            display: none;
            position: absolute;
            bottom: 50px;
            right: 0;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            min-width: 250px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .customization-options h3 {
            margin-bottom: 15px;
            color: #333;
        }
        
        .option-group {
            margin: 10px 0;
        }
        
        .option-group label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: bold;
        }
        
        .option-group select {
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        
        .apply-btn {
            background: #0078d4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        """
    
    def generate_logo_section(self):
        """Generate logo section HTML"""
        if not self.customization['logo_visible']:
            return ""
            
        return """
        <div class="logo">
            <div class="logo-icon">🌐</div>
            <h1 class="logo-text">Nexa Browser</h1>
            <p class="tagline">Modern, Fast, and Intelligent Browsing Experience</p>
        </div>
        """
    
    def generate_quick_actions(self):
        """Generate quick actions HTML"""
        actions_config = {
            'gmail': {'icon': '📧', 'name': 'Gmail', 'url': 'https://mail.google.com'},
            'youtube': {'icon': '📺', 'name': 'YouTube', 'url': 'https://www.youtube.com'},
            'drive': {'icon': '📁', 'name': 'Google Drive', 'url': 'https://drive.google.com'},
            'maps': {'icon': '🗺️', 'name': 'Google Maps', 'url': 'https://maps.google.com'},
            'news': {'icon': '📰', 'name': 'News', 'url': 'https://news.google.com'},
            'weather': {'icon': '⛅', 'name': 'Weather', 'url': 'https://www.weather.com'},
            'github': {'icon': '💻', 'name': 'GitHub', 'url': 'https://github.com'},
            'twitter': {'icon': '🐦', 'name': 'Twitter', 'url': 'https://twitter.com'},
            'reddit': {'icon': '📱', 'name': 'Reddit', 'url': 'https://reddit.com'},
            'spotify': {'icon': '🎵', 'name': 'Spotify', 'url': 'https://open.spotify.com'}
        }
        
        actions_html = []
        for action_key in self.customization['quick_actions']:
            if action_key in actions_config:
                action = actions_config[action_key]
                actions_html.append(f"""
                    <a href="{action['url']}" class="action-card" target="_blank">
                        <div class="action-icon">{action['icon']}</div>
                        <div class="action-name">{action['name']}</div>
                    </a>
                """)
        
        return "".join(actions_html)
    
    def generate_ai_section(self):
        """Generate AI section HTML"""
        return """
        <div class="ai-section">
            <h3 class="ai-title">🤖 Nexa AI Assistant</h3>
            <input type="text" class="ai-input" id="aiInput" placeholder="Ask me anything...">
            <div class="ai-response" id="aiResponse">
                Hello! I'm your AI assistant with specialized agents for research, creativity, technical help, productivity, and entertainment!
            </div>
        </div>
        """
    
    def generate_weather_widget(self):
        """Generate weather widget HTML"""
        return """
        <div class="weather-widget">
            <div class="weather-icon">⛅</div>
            <div class="weather-info">
                <div class="weather-temp">24°C</div>
                <div class="weather-location">Tehran</div>
            </div>
        </div>
        """
    
    def generate_clock_widget(self):
        """Generate clock widget HTML"""
        return """
        <div class="clock-widget">
            <div class="time" id="currentTime">--:--:--</div>
            <div class="date" id="currentDate">Loading...</div>
        </div>
        """
    
    def get_javascript(self):
        """Get JavaScript for homepage functionality"""
        return """
        const searchBox = document.getElementById('searchBox');
        const aiInput = document.getElementById('aiInput');
        const aiResponse = document.getElementById('aiResponse');
        
        // Update clock
        function updateClock() {
            const now = new Date();
            document.getElementById('currentTime').textContent = 
                now.toLocaleTimeString();
            document.getElementById('currentDate').textContent = 
                now.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
        }
        setInterval(updateClock, 1000);
        updateClock();
        
        searchBox.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = this.value.trim();
                if (query) {
                    if (query.includes('.') && !query.includes(' ')) {
                        window.location.href = query.startsWith('http') ? query : 'https://' + query;
                    } else {
                        window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query);
                    }
                }
            }
        });
        
        aiInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const question = this.value.trim();
                if (question) {
                    aiResponse.innerHTML = `Thinking about: <em>${question}</em>...<br><br>I can help with this! In the full version, I'll provide detailed answers using specialized AI agents.`;
                    this.value = '';
                }
            }
        });
        
        // Customization functions
        function toggleCustomization() {
            const options = document.getElementById('customizationOptions');
            options.style.display = options.style.display === 'block' ? 'none' : 'block';
        }
        
        function changeBackground(type) {
            const body = document.body;
            if (type === 'gradient') {
                body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            } else if (type === 'solid') {
                body.style.background = '#0078d4';
            } else if (type === 'image') {
                body.style.background = "url('https://source.unsplash.com/random/1920x1080') center/cover";
            }
        }
        
        function changeLayout(layout) {
            document.body.className = 'layout-' + layout;
        }
        
        function applyCustomization() {
            alert('Customization applied! These changes are for demonstration. Use browser settings for permanent changes.');
            document.getElementById('customizationOptions').style.display = 'none';
        }
        
        // Close customization when clicking outside
        document.addEventListener('click', function(e) {
            const panel = document.getElementById('customizationPanel');
            const options = document.getElementById('customizationOptions');
            if (!panel.contains(e.target)) {
                options.style.display = 'none';
            }
        });
        """
    
    def show_customization_dialog(self):
        """Show advanced customization dialog"""
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Advanced Homepage Customization")
        dialog.setModal(True)
        dialog.resize(500, 600)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🎨 Advanced Homepage Customization")
        header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)
        
        # Background customization
        bg_group = QGroupBox("Background Settings")
        bg_layout = QVBoxLayout()
        
        bg_type_combo = QComboBox()
        bg_type_combo.addItems(["Gradient", "Solid Color", "Image URL"])
        bg_layout.addWidget(QLabel("Background Type:"))
        bg_layout.addWidget(bg_type_combo)
        
        bg_color_edit = QLineEdit()
        bg_color_edit.setPlaceholderText("Enter color code or gradient")
        bg_color_edit.setText(self.customization['background_gradient'])
        bg_layout.addWidget(QLabel("Background Value:"))
        bg_layout.addWidget(bg_color_edit)
        
        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)
        
        # Layout customization
        layout_group = QGroupBox("Layout Settings")
        layout_layout = QVBoxLayout()
        
        layout_combo = QComboBox()
        layout_combo.addItems(["Centered", "Compact", "Spacious"])
        layout_combo.setCurrentText(self.customization['layout_style'].title())
        layout_layout.addWidget(QLabel("Layout Style:"))
        layout_layout.addWidget(layout_combo)
        
        search_style_combo = QComboBox()
        search_style_combo.addItems(["Rounded", "Modern", "Minimal", "Glass"])
        search_style_combo.setCurrentText(self.customization['search_bar_style'].title())
        layout_layout.addWidget(QLabel("Search Bar Style:"))
        layout_layout.addWidget(search_style_combo)
        
        layout_group.setLayout(layout_layout)
        layout.addWidget(layout_group)
        
        # Quick actions customization
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout()
        
        actions_list = [
            ('gmail', 'Gmail'), ('youtube', 'YouTube'), ('drive', 'Google Drive'),
            ('maps', 'Google Maps'), ('news', 'News'), ('weather', 'Weather'),
            ('github', 'GitHub'), ('twitter', 'Twitter'), ('reddit', 'Reddit'),
            ('spotify', 'Spotify')
        ]
        
        for action_id, action_name in actions_list:
            cb = QCheckBox(action_name)
            cb.setChecked(action_id in self.customization['quick_actions'])
            cb.toggled.connect(lambda checked, aid=action_id: self.toggle_quick_action(aid, checked))
            actions_layout.addWidget(cb)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Widget visibility
        widgets_group = QGroupBox("Widget Visibility")
        widgets_layout = QVBoxLayout()
        
        show_logo = QCheckBox("Show Logo")
        show_logo.setChecked(self.customization['logo_visible'])
        widgets_layout.addWidget(show_logo)
        
        show_ai = QCheckBox("Show AI Section")
        show_ai.setChecked(self.customization['show_ai_section'])
        widgets_layout.addWidget(show_ai)
        
        show_weather = QCheckBox("Show Weather")
        show_weather.setChecked(self.customization['show_weather'])
        widgets_layout.addWidget(show_weather)
        
        show_clock = QCheckBox("Show Clock")
        show_clock.setChecked(self.customization['show_clock'])
        widgets_layout.addWidget(show_clock)
        
        widgets_group.setLayout(widgets_layout)
        layout.addWidget(widgets_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Changes")
        reset_btn = QPushButton("Reset to Default")
        close_btn = QPushButton("Close")
        
        apply_btn.clicked.connect(lambda: self.apply_advanced_customization(
            bg_type_combo.currentText().lower(),
            bg_color_edit.text(),
            layout_combo.currentText().lower(),
            search_style_combo.currentText().lower(),
            show_logo.isChecked(),
            show_ai.isChecked(),
            show_weather.isChecked(),
            show_clock.isChecked(),
            dialog
        ))
        reset_btn.clicked.connect(self.reset_customization)
        close_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def toggle_quick_action(self, action_id, enabled):
        """Toggle quick action in customization"""
        if enabled and action_id not in self.customization['quick_actions']:
            self.customization['quick_actions'].append(action_id)
        elif not enabled and action_id in self.customization['quick_actions']:
            self.customization['quick_actions'].remove(action_id)
    
    def apply_advanced_customization(self, bg_type, bg_value, layout, search_style, 
                                   show_logo, show_ai, show_weather, show_clock, dialog):
        """Apply advanced customization settings"""
        self.customization.update({
            'background_type': bg_type,
            'background_gradient' if bg_type == 'gradient' else 'background_color': bg_value,
            'layout_style': layout,
            'search_bar_style': search_style,
            'logo_visible': show_logo,
            'show_ai_section': show_ai,
            'show_weather': show_weather,
            'show_clock': show_clock
        })
        
        QMessageBox.information(dialog, "Success", "Homepage customization applied successfully!")
        dialog.accept()
        
        # Refresh homepage in all tabs
        self.main_window.refresh_homepage_tabs()
    
    def reset_customization(self):
        """Reset customization to default"""
        self.customization = {
            'background_type': 'gradient',
            'background_color': '#f8f9fa',
            'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'background_image': '',
            'logo_visible': True,
            'search_bar_style': 'rounded',
            'quick_actions': ['gmail', 'youtube', 'drive', 'maps', 'news', 'weather'],
            'show_ai_section': True,
            'show_weather': True,
            'show_clock': True,
            'layout_style': 'centered',
            'custom_css': '',
            'font_family': 'Segoe UI',
            'font_size': '14px'
        }
        QMessageBox.information(None, "Reset Complete", "Homepage customization reset to default settings!")
        
        # Refresh homepage in all tabs
        if hasattr(self, 'main_window'):
            self.main_window.refresh_homepage_tabs()


class ModernNexaBrowser(QMainWindow):
    """Enhanced main browser window with modern Windows 11 style UI"""
    
    def __init__(self, first_run=True, setup_data=None):
        super().__init__()
        self.first_run = first_run
        self.setup_data = setup_data or {}
        self.ai_assistant = AdvancedAIAssistant()
        self.homepage_manager = EnhancedHomePage(self)
        self.current_theme = "light"
        self.menu_bar_visible = False
        
        # Apply first-run setup if provided
        if self.setup_data:
            self.apply_first_run_setup()
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme(self.current_theme)
        self.setup_shortcuts()
        
        # Show first-run wizard if it's the first run
        if first_run:
            self.show_first_run_wizard()
        
    def apply_first_run_setup(self):
        """Apply first-run setup configuration"""
        if 'theme' in self.setup_data:
            self.current_theme = self.setup_data['theme']
        
        if 'font_family' in self.setup_data:
            font = QFont(self.setup_data['font_family'], self.setup_data.get('font_size', 10))
            QApplication.setFont(font)
        
        # Apply homepage customization
        homepage_customization = {}
        if 'homepage_background' in self.setup_data:
            homepage_customization['background_type'] = self.setup_data['homepage_background']
        if 'quick_actions' in self.setup_data:
            homepage_customization['quick_actions'] = self.setup_data['quick_actions']
        if 'show_clock' in self.setup_data:
            homepage_customization['show_clock'] = self.setup_data['show_clock']
        if 'show_weather' in self.setup_data:
            homepage_customization['show_weather'] = self.setup_data['show_weather']
        if 'show_ai_section' in self.setup_data:
            homepage_customization['show_ai_section'] = self.setup_data['show_ai_section']
        
        if homepage_customization:
            self.homepage_manager.update_customization(homepage_customization)
        
        # Apply AI settings
        if 'ai_enabled' in self.setup_data:
            self.ai_assistant.enabled = self.setup_data['ai_enabled']
    
    def show_first_run_wizard(self):
        """Show first-run wizard"""
        wizard = FirstRunWizard(self)
        if wizard.exec() == QDialog.DialogCode.Accepted:
            self.setup_data = wizard.get_setup_data()
            self.apply_first_run_setup()
            self.refresh_homepage_tabs()
    
    def refresh_homepage_tabs(self):
        """Refresh all homepage tabs with new customization"""
        for i in range(self.tab_widget.count()):
            browser = self.tab_widget.widget(i)
            if browser and hasattr(browser, 'url') and browser.url().toString() == "about:blank":
                browser.setHtml(self.homepage_manager.get_customized_html(), QUrl("about:blank"))

    # ... (rest of the ModernNexaBrowser class remains the same as in your original code,
    # but with the new homepage customization methods integrated)

    def show_modern_settings(self):
        """Show modern settings dialog with enhanced options"""
        self.show_enhanced_settings_dialog()
    
    def show_enhanced_settings_dialog(self):
        """Show enhanced settings dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nexa Browser Settings")
        dialog.setModal(True)
        dialog.resize(700, 600)
        
        layout = QVBoxLayout()
        
        # Tab widget for different settings categories
        tab_widget = QTabWidget()
        
        # General tab
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        # Theme settings
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Light Theme", "Dark Theme", "Auto (System)"])
        theme_combo.setCurrentText(
            ['Light Theme', 'Dark Theme', 'Auto (System)'][
                ['light', 'dark', 'auto'].index(self.current_theme)
            ] if self.current_theme in ['light', 'dark', 'auto'] else 0
        )
        theme_combo.currentIndexChanged.connect(
            lambda i: setattr(self, 'current_theme', ['light', 'dark', 'auto'][i])
        )
        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(theme_combo)
        
        theme_group.setLayout(theme_layout)
        general_layout.addWidget(theme_group)
        
        # Homepage settings
        homepage_group = QGroupBox("Homepage")
        homepage_layout = QVBoxLayout()
        
        customize_btn = QPushButton("Customize Homepage")
        customize_btn.clicked.connect(lambda: self.homepage_manager.show_customization_dialog())
        homepage_layout.addWidget(customize_btn)
        
        homepage_group.setLayout(homepage_layout)
        general_layout.addWidget(homepage_group)
        
        general_layout.addStretch()
        general_tab.setLayout(general_layout)
        tab_widget.addTab(general_tab, "General")
        
        # AI Settings tab
        ai_tab = QWidget()
        ai_layout = QVBoxLayout()
        
        ai_group = QGroupBox("AI Assistant")
        ai_group_layout = QVBoxLayout()
        
        enable_ai = QCheckBox("Enable AI Assistant")
        enable_ai.setChecked(self.ai_assistant.enabled)
        enable_ai.toggled.connect(lambda c: setattr(self.ai_assistant, 'enabled', c))
        ai_group_layout.addWidget(enable_ai)
        
        # AI agents info
        agents_info = QLabel(
            "Available AI Agents:\n"
            "• Research Agent - For information gathering and learning\n"
            "• Creative Agent - For writing, design, and creative tasks\n"
            "• Technical Agent - For programming and technical help\n"
            "• Productivity Agent - For organization and time management\n"
            "• Entertainment Agent - For fun, games, and entertainment"
        )
        agents_info.setStyleSheet("padding: 15px; background: #f8f9fa; border-radius: 8px;")
        ai_group_layout.addWidget(agents_info)
        
        ai_group.setLayout(ai_group_layout)
        ai_layout.addWidget(ai_group)
        ai_layout.addStretch()
        ai_tab.setLayout(ai_layout)
        tab_widget.addTab(ai_tab, "AI Settings")
        
        # Privacy tab
        privacy_tab = QWidget()
        privacy_layout = QVBoxLayout()
        
        privacy_group = QGroupBox("Privacy & Security")
        privacy_group_layout = QVBoxLayout()
        
        clear_data_btn = QPushButton("Clear Browsing Data")
        clear_data_btn.clicked.connect(self.clear_browsing_data)
        privacy_group_layout.addWidget(clear_data_btn)
        
        block_ads = QCheckBox("Block Ads and Trackers")
        block_ads.setChecked(True)
        privacy_group_layout.addWidget(block_ads)
        
        privacy_group.setLayout(privacy_group_layout)
        privacy_layout.addWidget(privacy_group)
        privacy_layout.addStretch()
        privacy_tab.setLayout(privacy_layout)
        tab_widget.addTab(privacy_tab, "Privacy")
        
        layout.addWidget(tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        close_btn = QPushButton("Close")
        
        apply_btn.clicked.connect(lambda: self.apply_settings_and_close(dialog))
        close_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def apply_settings_and_close(self, dialog):
        """Apply settings and close dialog"""
        self.apply_theme(self.current_theme)
        QMessageBox.information(self, "Settings Applied", "Settings have been applied successfully!")
        dialog.accept()


def main():
    """Main application entry point"""
    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Nexa Browser")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Hessamedien")
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Check if it's first run
    first_run = True  # You can implement persistence to check if it's actually first run
    
    # Create and show browser
    browser = ModernNexaBrowser(first_run=first_run)
    browser.show()
    
    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()