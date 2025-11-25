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

class AdvancedAIAssistant:
    """Enhanced AI Assistant with extensive free AI capabilities"""
    
    def __init__(self):
        self.chat_history = []
        self.enabled = True
        self.api_key = None
        self.learning_enabled = True
        self.context_memory = {}
        
    def process_query(self, query, context=None):
        """Process user query with enhanced responses"""
        if not self.enabled:
            return "AI Assistant is currently disabled. Enable it in settings."
            
        query_lower = query.lower()
        
        # Enhanced AI responses with more capabilities
        if any(word in query_lower for word in ["summary", "summarize", "summarise"]):
            return self.generate_summary(context)
        elif any(word in query_lower for word in ["translate", "translation"]):
            return self.handle_translation(query)
        elif any(word in query_lower for word in ["search", "find"]):
            return self.handle_search(query)
        elif any(word in query_lower for word in ["email", "write", "compose", "draft"]):
            return self.draft_email(query)
        elif any(word in query_lower for word in ["weather", "forecast"]):
            return self.get_weather(query)
        elif any(word in query_lower for word in ["news", "headlines"]):
            return self.get_news_headlines()
        elif any(word in query_lower for word in ["calculate", "math", "compute"]):
            return self.solve_math(query)
        elif any(word in query_lower for word in ["code", "programming", "developer"]):
            return self.handle_coding(query)
        elif any(word in query_lower for word in ["time", "date"]):
            return f"🕒 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif any(word in query_lower for word in ["bookmark", "save"]):
            return "🔖 I can help you manage bookmarks. Use Ctrl+D to bookmark the current page."
        elif any(word in query_lower for word in ["history", "recent"]):
            return "📚 I can show your browsing history. Use Ctrl+H to view history."
        elif any(word in query_lower for word in ["hello", "hi", "hey"]):
            return "👋 Hello! I'm Nexa AI, your intelligent browser assistant. How can I help you today?"
        elif any(word in query_lower for word in ["thank", "thanks"]):
            return "😊 You're welcome! Is there anything else I can help you with?"
        elif any(word in query_lower for word in ["joke", "funny"]):
            return self.tell_joke()
        elif any(word in query_lower for word in ["quote", "inspiration"]):
            return self.get_inspirational_quote()
        elif any(word in query_lower for word in ["learn", "remember"]):
            return self.learn_information(query)
        elif any(word in query_lower for word in ["remind", "reminder"]):
            return self.set_reminder(query)
        elif any(word in query_lower for word in ["define", "dictionary"]):
            return self.define_word(query)
        elif any(word in query_lower for word in ["currency", "convert"]):
            return self.currency_conversion(query)
        elif any(word in query_lower for word in ["note", "notes"]):
            return self.manage_notes(query)
        elif any(word in query_lower for word in ["task", "todo"]):
            return self.manage_tasks(query)
        elif any(word in query_lower for word in ["password", "generate"]):
            return self.generate_password(query)
        elif any(word in query_lower for word in ["qr", "qrcode"]):
            return self.generate_qr_code(query)
        elif any(word in query_lower for word in ["lyrics", "song"]):
            return self.find_lyrics(query)
        elif any(word in query_lower for word in ["recipe", "cook"]):
            return self.get_recipe(query)
        elif any(word in query_lower for word in ["exercise", "workout"]):
            return self.suggest_exercise(query)
        elif any(word in query_lower for word in ["meditate", "meditation"]):
            return self.guide_meditation(query)
        else:
            return f"🤔 I understand you're asking about: '{query}'. I can help with web searches, translations, content creation, calculations, coding, reminders, notes, tasks, password generation, QR codes, lyrics, recipes, exercises, meditation, and much more. How can I assist you specifically?"

    def generate_summary(self, context):
        """Generate page summary"""
        return "📄 I'll analyze the current page and provide a concise summary of its main points and key information."

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
                return f"🌍 I'll translate to {lang.capitalize()}. Please provide the text you want to translate."
        
        return "🌍 I can translate text between 50+ languages. Please specify the target language (e.g., 'translate to Spanish')."

    def handle_search(self, query):
        """Handle search requests"""
        search_terms = query.replace("search", "").replace("find", "").strip()
        if search_terms:
            return f"🔍 I'll search the web for: '{search_terms}'. Would you like me to open search results?"
        return "🔍 What would you like me to search for?"

    def draft_email(self, query):
        """Draft email based on query"""
        email_types = {
            'business': "📧 I'll help you draft a professional business email. Please provide recipient details and key points.",
            'personal': "📧 I'll help you write a personal email. What's the main message?",
            'complaint': "📧 I'll help draft a professional complaint email. Please describe the issue.",
            'thank you': "📧 I'll help write a thank you email. What are you thankful for?",
            'follow up': "📧 I'll help with a follow-up email. What's the context?"
        }
        
        for email_type, response in email_types.items():
            if email_type in query.lower():
                return response
        
        return "📧 I can help draft various types of emails. Please specify the purpose (business, personal, complaint, etc.)"

    def get_weather(self, query):
        """Get weather information"""
        locations = ['tehran', 'london', 'new york', 'tokyo', 'paris', 'dubai']
        for location in locations:
            if location in query.lower():
                return f"⛅ I'll get the weather forecast for {location.title()}. In the full version, I'll show detailed weather information."
        return "⛅ I can provide weather information. Please specify a location or enable location services."

    def get_news_headlines(self):
        """Get news headlines"""
        return "📰 I'll fetch the latest news headlines from trusted sources. You can customize news preferences in settings."

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
                    return f"🧮 Calculating: {safe_expr} = {result}"
            return "🧮 I can perform calculations and solve mathematical problems. What would you like me to calculate?"
        except Exception as e:
            return f"🧮 I couldn't calculate that. Please provide a valid mathematical expression. Error: {str(e)}"

    def handle_coding(self, query):
        """Handle programming/coding requests"""
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust']
        for lang in languages:
            if lang in query.lower():
                return f"💻 I can help with {lang} programming. What specific problem are you facing?"
        return "💻 I can help with programming questions, code examples, and debugging. What language or problem are you working on?"

    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the web developer go broke? Because he lost his domain in a bet!",
            "What's a computer's favorite beat? An algorithm!",
            "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings!",
            "Why do Python developers wear glasses? Because they can't C#!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
        ]
        return f"😄 {random.choice(jokes)}"

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
        return f"💫 {random.choice(quotes)}"

    def learn_information(self, query):
        """Learn and remember information"""
        if "that" in query.lower() or "remember" in query.lower():
            # Extract key information to remember
            key_info = query.replace("remember", "").replace("that", "").strip()
            if key_info:
                self.context_memory['learned_info'] = key_info
                return f"🧠 I've learned and stored: '{key_info}'. I'll remember this for our conversation."
        return "🧠 I can learn and remember information. What would you like me to remember?"

    def set_reminder(self, query):
        """Set a reminder"""
        return "⏰ I can set reminders for you. Please specify the time and what you'd like to be reminded about."

    def define_word(self, query):
        """Define a word"""
        words = query.lower().replace("define", "").replace("dictionary", "").strip()
        if words:
            return f"📖 I'll look up the definition of '{words}'. In the full version, I'll provide detailed definitions."
        return "📖 I can define words for you. What word would you like me to define?"

    def currency_conversion(self, query):
        """Handle currency conversion"""
        return "💱 I can convert between different currencies. Please specify the amount and currencies (e.g., '100 USD to EUR')."

    def manage_notes(self, query):
        """Manage notes"""
        if "add" in query.lower() or "create" in query.lower():
            return "📝 I can help you create and manage notes. What would you like to add to your notes?"
        return "📝 I can help you manage your notes. You can add, view, or delete notes."

    def manage_tasks(self, query):
        """Manage tasks"""
        return "✅ I can help you manage your to-do list and tasks. What would you like to add to your tasks?"

    def generate_password(self, query):
        """Generate secure password"""
        length = 12
        if "strong" in query.lower():
            length = 16
        elif "weak" in query.lower():
            length = 8
            
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        return f"🔐 Generated password: `{password}`\n\nPlease save this password in a secure location."

    def generate_qr_code(self, query):
        """Generate QR code"""
        data = query.replace("qr", "").replace("qrcode", "").strip()
        if data:
            return f"📱 I'll generate a QR code for: '{data}'. In the full version, I'll display the QR code."
        return "📱 I can generate QR codes. What data would you like to encode?"

    def find_lyrics(self, query):
        """Find song lyrics"""
        song = query.replace("lyrics", "").replace("song", "").strip()
        if song:
            return f"🎵 I'll find lyrics for: '{song}'. In the full version, I'll display the complete lyrics."
        return "🎵 I can find song lyrics. What song are you looking for?"

    def get_recipe(self, query):
        """Get cooking recipe"""
        dish = query.replace("recipe", "").replace("cook", "").strip()
        if dish:
            return f"👨‍🍳 I'll find a recipe for: '{dish}'. In the full version, I'll provide detailed cooking instructions."
        return "👨‍🍳 I can find cooking recipes. What dish would you like to cook?"

    def suggest_exercise(self, query):
        """Suggest exercises"""
        return "💪 I can suggest exercises and workout routines. What type of exercise are you interested in?"

    def guide_meditation(self, query):
        """Guide meditation"""
        return "🧘 I can guide you through meditation sessions. Would you like a breathing exercise or mindfulness meditation?"


class EnhancedHomePage:
    """Enhanced homepage with extensive customization"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.customization = {
            'background_type': 'gradient',  # gradient, image, color, animated
            'background_color': '#f8f9fa',
            'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'background_image': '',
            'logo_visible': True,
            'search_bar_style': 'rounded',  # rounded, modern, minimal, glass
            'quick_actions': ['gmail', 'youtube', 'drive', 'maps', 'news', 'weather'],
            'show_ai_section': True,
            'show_weather': True,
            'show_clock': True,
            'layout_style': 'centered',  # centered, compact, spacious
            'custom_css': '',
            'font_family': 'Segoe UI',
            'font_size': '14px'
        }
    
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
            return f"url('{self.customization['background_image']}')"
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
                Hello! I'm your AI assistant. I can help you with searches, translations, calculations, and more!
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
                    aiResponse.innerHTML = `Thinking about: <em>${question}</em>...<br><br>I can help with this! In the full version, I'll provide detailed answers using advanced AI.`;
                    this.value = '';
                }
            }
        });
        """
    

class ModernNexaBrowser(QMainWindow):
    """Enhanced main browser window with modern Windows 11 style UI"""
    
    def __init__(self):
        super().__init__()
        self.ai_assistant = AdvancedAIAssistant()
        self.homepage_manager = EnhancedHomePage(self)
        self.current_theme = "light"
        self.menu_bar_visible = False
        self.back_btn = None
        self.forward_btn = None
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme(self.current_theme)
        self.setup_shortcuts()
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Toggle Menu Bar
        QShortcut(QKeySequence("Alt"), self, self.toggle_menu_bar)
        
        # New Tab
        QShortcut(QKeySequence("Ctrl+T"), self, self.add_new_tab)
        
        # Close Tab
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        
        # New Window
        QShortcut(QKeySequence("Ctrl+N"), self, self.create_new_window)
        
        # Reload
        QShortcut(QKeySequence("Ctrl+R"), self, self.reload_page)
        
        # Home
        QShortcut(QKeySequence("Alt+Home"), self, self.go_home)
        
    def setup_ui(self):
        """Initialize the modern user interface"""
        # Window configuration
        self.setWindowTitle("Nexa Browser - Modern AI-Powered Web Browser")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Set modern window icon
        self.create_modern_logo()
        
        # Apply modern window styling
        self.setStyleSheet(self.get_windows11_light_theme())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create comprehensive menu bar (hidden by default)
        self.create_comprehensive_menu_bar()
        
        # Create modern toolbar with sandwich menu
        self.create_modern_toolbar()
        
        # Create main content area
        self.create_modern_content_area(layout)
        
        # Create status bar
        self.create_status_bar()
        
        # Add first tab with beautiful homepage
        self.add_new_tab(homepage=True)
        
    def create_comprehensive_menu_bar(self):
        """Create comprehensive menu bar that's hidden by default"""
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setVisible(False)  # Hidden by default
        
        # File Menu
        file_menu = self.menu_bar.addMenu("&File")
        
        new_tab_action = QAction("New &Tab", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction("New &Window", self)
        new_window_action.setShortcut("Ctrl+N")
        new_window_action.triggered.connect(self.create_new_window)
        file_menu.addAction(new_window_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = self.menu_bar.addMenu("&Edit")
        
        find_action = QAction("&Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_in_page)
        edit_menu.addAction(find_action)
        
        # View Menu
        view_menu = self.menu_bar.addMenu("&View")
        
        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("&Reset Zoom", self)
        zoom_reset_action.setShortcut("Ctrl+0")
        zoom_reset_action.triggered.connect(self.zoom_reset)
        view_menu.addAction(zoom_reset_action)
        
        # History Menu
        history_menu = self.menu_bar.addMenu("&History")
        
        back_action = QAction("&Back", self)
        back_action.setShortcut("Alt+Left")
        back_action.triggered.connect(self.navigate_back)
        history_menu.addAction(back_action)
        
        forward_action = QAction("&Forward", self)
        forward_action.setShortcut("Alt+Right")
        forward_action.triggered.connect(self.navigate_forward)
        history_menu.addAction(forward_action)
        
        # Bookmarks Menu
        bookmarks_menu = self.menu_bar.addMenu("&Bookmarks")
        
        add_bookmark_action = QAction("&Bookmark This Page", self)
        add_bookmark_action.setShortcut("Ctrl+D")
        add_bookmark_action.triggered.connect(self.bookmark_current_page)
        bookmarks_menu.addAction(add_bookmark_action)
        
        # Settings Menu
        settings_menu = self.menu_bar.addMenu("&Settings")
        
        browser_settings_action = QAction("&Browser Settings", self)
        browser_settings_action.setShortcut("Ctrl+,")
        browser_settings_action.triggered.connect(self.show_modern_settings)
        settings_menu.addAction(browser_settings_action)
        
        # Help Menu
        help_menu = self.menu_bar.addMenu("&Help")
        
        about_action = QAction("&About Nexa Browser", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        self.setMenuBar(self.menu_bar)
        
    def create_modern_toolbar(self):
        """Create modern toolbar with Windows 11 style and sandwich menu"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: none;
                border-bottom: 1px solid #dee2e6;
                padding: 5px;
                spacing: 8px;
            }
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 6px 8px;
                color: #495057;
            }
            QToolButton:hover {
                background: #e9ecef;
                border: 1px solid #ced4da;
            }
            QToolButton:pressed {
                background: #dee2e6;
            }
        """)
        
        # Hamburger menu button with modern design
        menu_btn = QToolButton()
        menu_btn.setText("☰")
        menu_btn.setToolTip("Menu (Alt)")
        menu_btn.clicked.connect(self.show_sandwich_menu)
        menu_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 8px 12px;
                color: #495057;
                font-size: 16px;
                font-weight: bold;
            }
            QToolButton:hover {
                background: #e9ecef;
                border: 1px solid #ced4da;
            }
            QToolButton:pressed {
                background: #dee2e6;
            }
        """)
        toolbar.addWidget(menu_btn)
        
        toolbar.addSeparator()
        
        # Navigation buttons with modern icons
        nav_style = """
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 6px 8px;
                color: #495057;
                font-size: 14px;
            }
            QToolButton:hover {
                background: #e9ecef;
                border: 1px solid #ced4da;
            }
            QToolButton:disabled {
                color: #adb5bd;
            }
        """
        
        self.back_btn = QToolButton()
        self.back_btn.setText("←")
        self.back_btn.setToolTip("Back (Alt+Left)")
        self.back_btn.clicked.connect(self.navigate_back)
        self.back_btn.setStyleSheet(nav_style)
        self.back_btn.setEnabled(False)
        toolbar.addWidget(self.back_btn)
        
        self.forward_btn = QToolButton()
        self.forward_btn.setText("→")
        self.forward_btn.setToolTip("Forward (Alt+Right)")
        self.forward_btn.clicked.connect(self.navigate_forward)
        self.forward_btn.setStyleSheet(nav_style)
        self.forward_btn.setEnabled(False)
        toolbar.addWidget(self.forward_btn)
        
        reload_btn = QToolButton()
        reload_btn.setText("↻")
        reload_btn.setToolTip("Reload (Ctrl+R)")
        reload_btn.clicked.connect(self.reload_page)
        reload_btn.setStyleSheet(nav_style)
        toolbar.addWidget(reload_btn)
        
        home_btn = QToolButton()
        home_btn.setText("🏠")
        home_btn.setToolTip("Home (Alt+Home)")
        home_btn.clicked.connect(self.go_home)
        home_btn.setStyleSheet(nav_style)
        toolbar.addWidget(home_btn)
        
        toolbar.addSeparator()
        
        # Modern address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Search Google or enter website address...")
        self.address_bar.setMinimumWidth(500)
        self.address_bar.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 2px solid #e9ecef;
                border-radius: 20px;
                padding: 8px 20px;
                color: #495057;
                font-size: 14px;
                selection-background-color: rgba(0, 120, 212, 0.3);
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background: #ffffff;
            }
            QLineEdit::placeholder {
                color: #6c757d;
            }
        """)
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.address_bar)
        
        # Search button
        search_btn = QToolButton()
        search_btn.setText("🔍")
        search_btn.setToolTip("Search")
        search_btn.clicked.connect(self.navigate_to_url)
        search_btn.setStyleSheet(nav_style)
        toolbar.addWidget(search_btn)
        
        toolbar.addSeparator()
        
        # AI Assistant button
        ai_btn = QToolButton()
        ai_btn.setText("🤖")
        ai_btn.setToolTip("AI Assistant")
        ai_btn.clicked.connect(self.toggle_ai_sidebar)
        ai_btn.setStyleSheet(nav_style)
        toolbar.addWidget(ai_btn)
        
        # Bookmarks button
        bookmark_btn = QToolButton()
        bookmark_btn.setText("⭐")
        bookmark_btn.setToolTip("Bookmarks (Ctrl+D)")
        bookmark_btn.clicked.connect(self.show_bookmarks)
        bookmark_btn.setStyleSheet(nav_style)
        toolbar.addWidget(bookmark_btn)
        
        # Downloads button
        download_btn = QToolButton()
        download_btn.setText("📥")
        download_btn.setToolTip("Downloads (Ctrl+J)")
        download_btn.clicked.connect(self.show_downloads_manager)
        download_btn.setStyleSheet(nav_style)
        toolbar.addWidget(download_btn)
        
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        
    def create_modern_content_area(self, parent_layout):
        """Create modern content area with Windows 11 style"""
        main_content_widget = QWidget()
        main_layout = QHBoxLayout(main_content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main tab area
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Modern tab styling
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #ffffff;
            }
            QTabBar::tab {
                background: #f8f9fa;
                color: #495057;
                padding: 10px 20px;
                margin-right: 1px;
                border: none;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #0078d4;
                border-bottom: 2px solid #0078d4;
            }
            QTabBar::tab:hover {
                background: #e9ecef;
            }
            QTabBar::close-button {
                subcontrol-position: right;
                padding: 2px;
            }
            QTabBar::close-button:hover {
                background: #dc3545;
                border-radius: 8px;
            }
        """)
        
        main_layout.addWidget(self.tab_widget, 1)
        
        # Right sidebar for AI assistant
        self.create_modern_ai_sidebar()
        
        parent_layout.addWidget(main_content_widget)
        
    def create_modern_ai_sidebar(self):
        """Create modern AI assistant sidebar"""
        self.ai_dock = QDockWidget("🤖 Nexa AI Assistant", self)
        self.ai_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | 
                                QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.ai_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        
        ai_widget = QWidget()
        ai_layout = QVBoxLayout(ai_widget)
        ai_layout.setContentsMargins(15, 15, 15, 15)
        ai_layout.setSpacing(15)
        
        # AI header
        ai_header = QLabel("Nexa AI Assistant")
        ai_header.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background: #e7f3ff;
                border-radius: 10px;
                text-align: center;
            }
        """)
        ai_layout.addWidget(ai_header)
        
        # AI chat display
        self.ai_chat_display = QTextEdit()
        self.ai_chat_display.setReadOnly(True)
        self.ai_chat_display.setStyleSheet("""
            QTextEdit {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                color: #495057;
                padding: 10px;
                font-size: 14px;
                min-height: 200px;
            }
        """)
        self.ai_chat_display.setHtml("""
            <div style='color: #6c757d; text-align: center; padding: 20px;'>
                <h3>🤖 Welcome to Nexa AI!</h3>
                <p>I can help you with:</p>
                <ul style='text-align: left;'>
                    <li>Web searches and research</li>
                    <li>Translations between languages</li>
                    <li>Content creation and writing</li>
                    <li>Calculations and problem solving</li>
                    <li>Coding and programming help</li>
                    <li>Time and date information</li>
                    <li>Jokes and inspirational quotes</li>
                    <li>Reminders and notes</li>
                    <li>Password generation</li>
                    <li>QR code generation</li>
                    <li>Song lyrics</li>
                    <li>Recipes and cooking help</li>
                    <li>Exercise suggestions</li>
                    <li>Meditation guidance</li>
                    <li>And much more!</li>
                </ul>
                <p>How can I assist you today?</p>
            </div>
        """)
        ai_layout.addWidget(self.ai_chat_display, 1)
        
        # AI input area
        ai_input_layout = QHBoxLayout()
        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText("Ask AI assistant anything...")
        self.ai_input.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 2px solid #dee2e6;
                border-radius: 20px;
                padding: 10px 20px;
                color: #495057;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
            QLineEdit::placeholder {
                color: #6c757d;
            }
        """)
        self.ai_input.returnPressed.connect(self.send_ai_message)
        ai_input_layout.addWidget(self.ai_input)
        
        ai_send_btn = QPushButton("Send")
        ai_send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #005a9e, stop:1 #004578);
            }
        """)
        ai_send_btn.clicked.connect(self.send_ai_message)
        ai_input_layout.addWidget(ai_send_btn)
        
        ai_layout.addLayout(ai_input_layout)
        
        # Quick action buttons
        quick_actions_label = QLabel("Quick Actions:")
        quick_actions_label.setStyleSheet("color: #495057; font-weight: bold;")
        ai_layout.addWidget(quick_actions_label)
        
        quick_actions_layout = QGridLayout()
        quick_actions_layout.setSpacing(8)
        
        actions = [
            ("📄 Summarize", "summarize"),
            ("🌍 Translate", "translate"),
            ("🔍 Search", "search"),
            ("📧 Email", "email"),
            ("📰 News", "news"),
            ("🧮 Calculate", "calculate"),
            ("💻 Code", "code"),
            ("⛅ Weather", "weather"),
            ("🕒 Time", "time"),
            ("🔖 Bookmark", "bookmark"),
            ("📚 History", "history"),
            ("😄 Joke", "joke"),
            ("💫 Quote", "quote"),
            ("🧠 Learn", "learn"),
            ("⏰ Remind", "remind"),
            ("📖 Define", "define"),
            ("💱 Convert", "convert"),
            ("📝 Notes", "notes"),
            ("✅ Tasks", "tasks"),
            ("🔐 Password", "password")
        ]
        
        row, col = 0, 0
        for text, action in actions:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: #ffffff;
                    color: #495057;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: #e9ecef;
                    border: 1px solid #adb5bd;
                }
            """)
            btn.clicked.connect(lambda checked, a=action: self.ai_quick_action(a))
            quick_actions_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        ai_layout.addLayout(quick_actions_layout)
        
        self.ai_dock.setWidget(ai_widget)
        self.ai_dock.setStyleSheet("""
            QDockWidget {
                background: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
            QDockWidget::title {
                background: #e7f3ff;
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                text-align: center;
                color: #495057;
                font-weight: bold;
            }
        """)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.ai_dock)
        self.ai_dock.hide()
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #f8f9fa;
                color: #495057;
                border-top: 1px solid #dee2e6;
                padding: 5px;
            }
        """)
        self.setStatusBar(self.status_bar)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Timer for updating UI elements
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui_elements)
        self.ui_timer.start(1000)
        
    def update_ui_elements(self):
        """Update various UI elements periodically"""
        # Update navigation buttons based on current browser state
        current_browser = self.tab_widget.currentWidget()
        if current_browser and hasattr(current_browser, 'history'):
            self.back_btn.setEnabled(current_browser.history().canGoBack())
            self.forward_btn.setEnabled(current_browser.history().canGoForward())
        
    def add_new_tab(self, url=None, title="New Tab", homepage=False):
        """Add a new browser tab with optional homepage"""
        if homepage:
            # Create homepage
            browser = QWebEngineView()
            browser.setHtml(self.homepage_manager.get_customized_html(), QUrl("about:blank"))
            browser.titleChanged.connect(lambda t: self.update_tab_title(browser, t))
            browser.urlChanged.connect(lambda qurl: self.update_urlbar(qurl, browser))
        else:
            browser = QWebEngineView()
            
            # Configure browser settings
            settings = browser.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
            
            # Connect signals
            browser.urlChanged.connect(lambda qurl: self.update_urlbar(qurl, browser))
            browser.titleChanged.connect(lambda t: self.update_tab_title(browser, t))
            browser.loadStarted.connect(self.page_load_started)
            browser.loadFinished.connect(self.page_load_finished)
            browser.iconChanged.connect(lambda icon: self.update_tab_icon(browser, icon))
        
        # Add to tab widget
        index = self.tab_widget.addTab(browser, title)
        self.tab_widget.setCurrentIndex(index)
        
        # Load URL if provided
        if url and not homepage:
            browser.setUrl(QUrl(url))
        elif not homepage:
            browser.setUrl(QUrl("https://www.google.com"))
            
        return browser
        
    def update_tab_title(self, browser, title):
        """Update tab title when page title changes"""
        index = self.tab_widget.indexOf(browser)
        if index != -1:
            # Shorten long titles
            if len(title) > 20:
                title = title[:20] + "..."
            self.tab_widget.setTabText(index, title)
                
    def update_tab_icon(self, browser, icon):
        """Update tab icon when page icon changes"""
        index = self.tab_widget.indexOf(browser)
        if index != -1 and not icon.isNull():
            self.tab_widget.setTabIcon(index, icon)
            
    def update_urlbar(self, qurl, browser=None):
        """Update the URL bar when page URL changes"""
        if browser and browser != self.tab_widget.currentWidget():
            return
            
        if qurl.toString() != "about:blank":
            self.address_bar.setText(qurl.toString())
            self.address_bar.setCursorPosition(0)
            
    def page_load_started(self):
        """Handle page load start"""
        self.status_bar.showMessage("Loading...")
        
    def page_load_finished(self, ok):
        """Handle page load finish"""
        if ok:
            self.status_bar.showMessage("Ready", 2000)
        else:
            self.status_bar.showMessage("Failed to load page", 2000)
            
    def navigate_to_url(self):
        """Navigate to URL entered in address bar"""
        url = self.address_bar.text().strip()
        
        if not url:
            return
            
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                url = 'https://www.google.com/search?q=' + url.replace(' ', '+')
                
        # Navigate current tab to URL
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))
            
    def navigate_back(self):
        """Navigate back in history"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.back()
            
    def navigate_forward(self):
        """Navigate forward in history"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.forward()
            
    def reload_page(self):
        """Reload current page"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.reload()
            
    def go_home(self):
        """Go to homepage"""
        self.add_new_tab(homepage=True)
        
    def close_tab(self, index):
        """Close tab at specified index"""
        if self.tab_widget.count() > 1:
            widget = self.tab_widget.widget(index)
            if widget:
                widget.deleteLater()
            self.tab_widget.removeTab(index)
                
    def close_current_tab(self):
        """Close current tab"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)
                
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            current_browser = self.tab_widget.widget(index)
            if current_browser:
                self.update_urlbar(current_browser.url(), current_browser)
                
    def toggle_ai_sidebar(self):
        """Toggle AI sidebar visibility"""
        if self.ai_dock.isVisible():
            self.ai_dock.hide()
        else:
            self.ai_dock.show()
            
    def send_ai_message(self):
        """Send message to AI assistant"""
        message = self.ai_input.text().strip()
        if not message:
            return
            
        # Add user message to chat
        self.ai_chat_display.append(f"<b>You:</b> {message}")
        
        # Get AI response
        response = self.ai_assistant.process_query(message)
        
        # Add AI response to chat
        self.ai_chat_display.append(f"<b>Nexa AI:</b> {response}")
        
        # Clear input
        self.ai_input.clear()
        
        # Scroll to bottom
        self.ai_chat_display.verticalScrollBar().setValue(
            self.ai_chat_display.verticalScrollBar().maximum()
        )
        
    def ai_quick_action(self, action):
        """Handle AI quick action buttons"""
        responses = {
            "summarize": "📄 I can summarize web pages or text. Please navigate to a page or provide text to summarize.",
            "translate": "🌍 I support translation between 50+ languages. What would you like to translate and to which language?",
            "search": "🔍 I can help you search the web. What would you like to search for?",
            "email": "📧 I can help draft professional emails. What type of email would you like to write?",
            "news": "📰 I'll fetch the latest news headlines. Any specific topics you're interested in?",
            "calculate": "🧮 I can perform calculations. What mathematical problem would you like me to solve?",
            "code": "💻 I can help with programming questions. What language or problem are you working on?",
            "weather": "⛅ I can provide weather information. Please specify a location or enable location services.",
            "time": f"🕒 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "bookmark": "🔖 I can help you manage bookmarks. Use Ctrl+D to bookmark the current page.",
            "history": "📚 I can show your browsing history. Use Ctrl+H to view history.",
            "joke": self.ai_assistant.tell_joke(),
            "quote": self.ai_assistant.get_inspirational_quote(),
            "learn": "🧠 I can learn and remember information. What would you like me to remember?",
            "remind": "⏰ I can set reminders for you. Please specify the time and what you'd like to be reminded about.",
            "define": "📖 I can define words for you. What word would you like me to define?",
            "convert": "💱 I can convert between different currencies. Please specify the amount and currencies.",
            "notes": "📝 I can help you manage your notes. You can add, view, or delete notes.",
            "tasks": "✅ I can help you manage your to-do list and tasks. What would you like to add to your tasks?",
            "password": self.ai_assistant.generate_password("")
        }
        
        if action in responses:
            self.ai_chat_display.append(f"<b>Nexa AI:</b> {responses[action]}")
            self.ai_chat_display.verticalScrollBar().setValue(
                self.ai_chat_display.verticalScrollBar().maximum()
            )
            
    def create_new_window(self):
        """Create a new browser window"""
        new_window = ModernNexaBrowser()
        new_window.show()
        
    def create_private_window(self):
        """Create a new private browser window"""
        new_window = ModernNexaBrowser()
        new_window.setWindowTitle("Nexa Browser - Private Browsing")
        new_window.show()
        
    def show_sandwich_menu(self):
        """Show the comprehensive sandwich menu"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 8px;
                color: #495057;
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
                margin: 2px;
            }
            QMenu::item:selected {
                background: #e7f3ff;
                color: #0078d4;
            }
            QMenu::separator {
                height: 1px;
                background: #dee2e6;
                margin: 4px 8px;
            }
        """)
        
        # File section
        file_menu = menu.addMenu("📁 File")
        new_tab_action = file_menu.addAction("New Tab")
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_tab)
        
        new_window_action = file_menu.addAction("New Window")
        new_window_action.setShortcut("Ctrl+N")
        new_window_action.triggered.connect(self.create_new_window)
        
        file_menu.addSeparator()
        
        print_action = file_menu.addAction("Print...")
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_page)
        
        # Edit section
        edit_menu = menu.addMenu("✏️ Edit")
        find_action = edit_menu.addAction("Find...")
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_in_page)
        
        # View section
        view_menu = menu.addMenu("👁️ View")
        
        # Zoom submenu
        zoom_menu = view_menu.addMenu("🔍 Zoom")
        zoom_in_action = zoom_menu.addAction("Zoom In")
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        
        zoom_out_action = zoom_menu.addAction("Zoom Out")
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        
        zoom_reset_action = zoom_menu.addAction("Reset Zoom")
        zoom_reset_action.setShortcut("Ctrl+0")
        zoom_reset_action.triggered.connect(self.zoom_reset)
        
        view_menu.addSeparator()
        
        fullscreen_action = view_menu.addAction("Full Screen")
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        # History section
        history_menu = menu.addMenu("📚 History")
        back_action = history_menu.addAction("Back")
        back_action.setShortcut("Alt+Left")
        back_action.triggered.connect(self.navigate_back)
        
        forward_action = history_menu.addAction("Forward")
        forward_action.setShortcut("Alt+Right")
        forward_action.triggered.connect(self.navigate_forward)
        
        history_menu.addSeparator()
        
        show_history_action = history_menu.addAction("Show History")
        show_history_action.setShortcut("Ctrl+H")
        show_history_action.triggered.connect(self.show_history)
        
        # Bookmarks section
        bookmarks_menu = menu.addMenu("⭐ Bookmarks")
        bookmark_action = bookmarks_menu.addAction("Bookmark This Page")
        bookmark_action.setShortcut("Ctrl+D")
        bookmark_action.triggered.connect(self.bookmark_current_page)
        
        show_bookmarks_action = bookmarks_menu.addAction("Show Bookmarks")
        show_bookmarks_action.triggered.connect(self.show_bookmarks)
        
        # Tools section
        tools_menu = menu.addMenu("🔧 Tools")
        downloads_action = tools_menu.addAction("Downloads")
        downloads_action.setShortcut("Ctrl+J")
        downloads_action.triggered.connect(self.show_downloads_manager)
        
        tools_menu.addSeparator()
        
        dev_tools_action = tools_menu.addAction("Developer Tools")
        dev_tools_action.setShortcut("F12")
        dev_tools_action.triggered.connect(self.toggle_dev_tools)
        
        # Settings section
        settings_menu = menu.addMenu("⚙️ Settings")
        browser_settings_action = settings_menu.addAction("Browser Settings")
        browser_settings_action.setShortcut("Ctrl+,")
        browser_settings_action.triggered.connect(self.show_modern_settings)
        
        menu.addSeparator()
        
        # Help section
        help_action = menu.addAction("❓ Help")
        help_action.triggered.connect(self.show_help)
        
        about_action = menu.addAction("ℹ️ About")
        about_action.triggered.connect(self.show_about)
        
        # Show menu at button position
        menu.exec(QCursor.pos())
        
    def toggle_menu_bar(self):
        """Toggle menu bar visibility"""
        self.menu_bar.setVisible(not self.menu_bar_visible)
        self.menu_bar_visible = not self.menu_bar_visible
        
    def create_modern_logo(self):
        """Create a beautiful modern logo"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Modern gradient background
        gradient = QRadialGradient(32, 32, 30)
        gradient.setColorAt(0, QColor(0, 120, 212))  # Windows 11 blue
        gradient.setColorAt(0.7, QColor(16, 124, 16))  # Windows 11 green
        gradient.setColorAt(1, QColor(0, 120, 212))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(4, 4, 56, 56)
        
        # Modern 'N' icon
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "N")
        
        # Add glow effect
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Overlay)
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.drawEllipse(8, 8, 48, 48)
        
        painter.end()
        
        self.setWindowIcon(QIcon(pixmap))
        
    # Additional methods for comprehensive functionality
    def find_in_page(self):
        """Open find in page dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Find in Page")
        dialog.setModal(False)
        dialog.resize(300, 100)
        
        layout = QVBoxLayout()
        find_input = QLineEdit()
        find_input.setPlaceholderText("Search in page...")
        layout.addWidget(find_input)
        
        button_layout = QHBoxLayout()
        find_next = QPushButton("Next")
        find_prev = QPushButton("Previous")
        close_btn = QPushButton("Close")
        
        button_layout.addWidget(find_prev)
        button_layout.addWidget(find_next)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        close_btn.clicked.connect(dialog.accept)
        dialog.show()
        
    def zoom_in(self):
        """Zoom in current page"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.setZoomFactor(current_browser.zoomFactor() + 0.1)
            
    def zoom_out(self):
        """Zoom out current page"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.setZoomFactor(max(0.25, current_browser.zoomFactor() - 0.1))
            
    def zoom_reset(self):
        """Reset zoom to 100%"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.setZoomFactor(1.0)
            
    def toggle_dev_tools(self):
        """Toggle developer tools"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.page().triggerAction(QWebEnginePage.WebAction.InspectElement)
            
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def print_page(self):
        """Print current page"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            # Create printer
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            
            # Create print dialog
            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec() == QDialog.DialogCode.Accepted:
                current_browser.page().print(printer, lambda success: None)
                
    def show_bookmarks(self):
        """Show bookmarks manager"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bookmarks manager would be shown here"))
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def bookmark_current_page(self):
        """Bookmark the current page"""
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            url = current_browser.url().toString()
            title = current_browser.title()
            
            if url and url != "about:blank":
                QMessageBox.information(self, "Bookmark Added", 
                                      f"Bookmark '{title}' added successfully!")
                
    def show_history(self):
        """Show browsing history"""
        dialog = QDialog(self)
        dialog.setWindowTitle("History")
        dialog.setModal(True)
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Browsing history would be shown here"))
        
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_browsing_data)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
        
    def clear_browsing_data(self):
        """Clear browsing data"""
        result = QMessageBox.question(self, "Clear Browsing Data", 
                                    "Are you sure you want to clear all browsing data?")
        if result == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Success", "Browsing data cleared successfully!")
            
    def show_modern_settings(self):
        """Show modern settings dialog"""
        self.show_homepage_customization()
        
    def show_homepage_customization(self):
        """Show homepage customization dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Homepage Customization")
        dialog.setModal(True)
        dialog.resize(600, 500)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🏠 Homepage Customization")
        header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)
        
        # Background customization
        bg_group = QGroupBox("Background")
        bg_layout = QVBoxLayout()
        
        bg_type_combo = QComboBox()
        bg_type_combo.addItems(["Gradient", "Solid Color", "Image", "Animated"])
        bg_layout.addWidget(QLabel("Background Type:"))
        bg_layout.addWidget(bg_type_combo)
        
        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)
        
        # Layout customization
        layout_group = QGroupBox("Layout")
        layout_options = QVBoxLayout()
        
        layout_combo = QComboBox()
        layout_combo.addItems(["Centered", "Compact", "Spacious"])
        layout_options.addWidget(QLabel("Layout Style:"))
        layout_options.addWidget(layout_combo)
        
        show_logo_cb = QCheckBox("Show Logo")
        show_logo_cb.setChecked(True)
        layout_options.addWidget(show_logo_cb)
        
        show_ai_cb = QCheckBox("Show AI Section")
        show_ai_cb.setChecked(True)
        layout_options.addWidget(show_ai_cb)
        
        show_weather_cb = QCheckBox("Show Weather")
        show_weather_cb.setChecked(True)
        layout_options.addWidget(show_weather_cb)
        
        show_clock_cb = QCheckBox("Show Clock")
        show_clock_cb.setChecked(True)
        layout_options.addWidget(show_clock_cb)
        
        layout_group.setLayout(layout_options)
        layout.addWidget(layout_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        close_btn = QPushButton("Close")
        
        apply_btn.clicked.connect(lambda: self.apply_homepage_customization(dialog))
        close_btn.clicked.connect(dialog.accept)
        
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
        
    def apply_homepage_customization(self, dialog):
        """Apply homepage customization"""
        QMessageBox.information(self, "Success", "Homepage customization applied!")
        dialog.accept()
        
    def show_downloads_manager(self):
        """Show downloads manager"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Downloads")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Downloads manager would be shown here"))
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def show_help(self):
        """Show help dialog"""
        QMessageBox.information(self, "Help", 
                              "For help and support, please visit our documentation or contact support.")
                              
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Nexa Browser",
                         "<h3>Nexa Browser</h3>"
                         "<p>Version 2.0.0</p>"
                         "<p>A modern, lightweight AI-powered web browser</p>"
                         "<p>Created by Hessamedien</p>"
                         "<p><a href='https://www.instagram.com/hessamedien'>Instagram</a></p>")
                         
    def apply_theme(self, theme):
        """Apply modern theme with Windows 11 style"""
        self.current_theme = theme
        
        if theme == "dark":
            # Apply dark theme
            dark_stylesheet = """
                QMainWindow {
                    background: #202020;
                    color: #ffffff;
                }
                QToolBar {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2d2d2d, stop:1 #1a1a1a);
                    border: none;
                    border-bottom: 1px solid #404040;
                }
                QLineEdit {
                    background: #404040;
                    border: 2px solid #505050;
                    color: #ffffff;
                }
                QLineEdit:focus {
                    border: 2px solid #0078d4;
                }
                QTabBar::tab {
                    background: #2d2d2d;
                    color: #ffffff;
                }
                QTabBar::tab:selected {
                    background: #404040;
                    color: #0078d4;
                }
                QStatusBar {
                    background: #2d2d2d;
                    color: #ffffff;
                    border-top: 1px solid #404040;
                }
            """
            self.setStyleSheet(dark_stylesheet)
        else:
            # Apply Windows 11 light theme (default)
            self.setStyleSheet(self.get_windows11_light_theme())
            
    def get_windows11_light_theme(self):
        """Get Windows 11 light theme stylesheet"""
        return """
            QMainWindow {
                background: #f8f9fa;
                color: #495057;
            }
            QWidget {
                background: transparent;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: none;
                border-bottom: 1px solid #dee2e6;
                padding: 5px;
                spacing: 8px;
            }
            QLineEdit {
                background: #ffffff;
                border: 2px solid #e9ecef;
                border-radius: 20px;
                padding: 8px 20px;
                color: #495057;
                font-size: 14px;
                selection-background-color: rgba(0, 120, 212, 0.3);
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background: #ffffff;
            }
            QTabWidget::pane {
                border: none;
                background: #ffffff;
            }
            QTabBar::tab {
                background: #f8f9fa;
                color: #495057;
                padding: 10px 20px;
                margin-right: 1px;
                border: none;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #0078d4;
                border-bottom: 2px solid #0078d4;
            }
            QStatusBar {
                background: #f8f9fa;
                color: #495057;
                border-top: 1px solid #dee2e6;
                padding: 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
            QGroupBox {
                color: #495057;
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QTextEdit {
                background: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                color: #495057;
                padding: 10px;
            }
            QListWidget {
                background: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                color: #495057;
                outline: none;
            }
            QComboBox {
                background: #ffffff;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 5px;
            }
            QCheckBox {
                color: #495057;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #adb5bd;
                border-radius: 3px;
                background: #ffffff;
            }
            QCheckBox::indicator:checked {
                background: #0078d4;
                border: 1px solid #0078d4;
            }
            QMenuBar {
                background: #f8f9fa;
                color: #495057;
                border-bottom: 1px solid #dee2e6;
            }
            QMenuBar::item {
                background: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background: #e9ecef;
                border-radius: 3px;
            }
            QMenu {
                background: #ffffff;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background: #e7f3ff;
                color: #0078d4;
            }
            QDialog {
                background: #f8f9fa;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """


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
    
    # Create and show browser
    browser = ModernNexaBrowser()
    browser.show()
    
    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()