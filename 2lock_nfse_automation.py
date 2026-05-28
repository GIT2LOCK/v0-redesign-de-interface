#!/usr/bin/env python3
"""
2LOCK - Automação NFS-e
Design EXTREMAMENTE FIEL ao site 2lock.com.br
Python 3.13 + PyQt6

Cores extraídas diretamente do site:
- Azul principal: #5599FF (rgb(85, 153, 255))
- Fundo: #FFFFFF (branco)
- Texto: #333333 (rgb(51, 51, 51))
- Fonte: Saira (Google Fonts)
- Border radius: 5px
"""

import sys
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QFrame, QStackedWidget, QScrollArea, QLineEdit,
    QHeaderView, QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
    QProgressBar, QGraphicsOpacityEffect
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize,
    pyqtSignal, QParallelAnimationGroup, QPoint
)
from PyQt6.QtGui import (
    QColor, QFont, QIcon, QPainter, QBrush, QLinearGradient,
    QPen, QPixmap, QPainterPath
)


class LogType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class LogEntry:
    timestamp: str
    message: str
    type: LogType = LogType.INFO


@dataclass
class HistoryEntry:
    id: int
    date: str
    file: str
    records: int
    status: str
    duration: str


@dataclass
class SpreadsheetRow:
    id: int
    empresa: str
    cnpj: str
    valor: str
    status: str


# ============== CORES EXATAS DO SITE 2LOCK ==============

class Theme:
    """Cores extraídas diretamente de 2lock.com.br"""
    
    # Cores principais do site
    BLUE_PRIMARY = "#5599FF"      # rgb(85, 153, 255) - Botões principais
    BLUE_HOVER = "#4488EE"        # Hover dos botões
    BLUE_LIGHT = "#E8F1FF"        # Fundo claro azulado
    
    WHITE = "#FFFFFF"             # Fundo principal
    GRAY_BG = "#F8FAFC"          # Fundo secundário (cinza bem claro)
    
    TEXT_DARK = "#333333"         # rgb(51, 51, 51) - Texto principal
    TEXT_SECONDARY = "#6B7280"    # Texto secundário
    TEXT_LIGHT = "#9CA3AF"        # Texto terciário
    
    BORDER = "#E5E7EB"            # Bordas
    BORDER_LIGHT = "#F3F4F6"      # Bordas mais claras
    
    SUCCESS = "#10B981"           # Verde sucesso
    WARNING = "#F59E0B"           # Amarelo warning
    ERROR = "#EF4444"             # Vermelho erro
    
    # Border radius padrão do site
    RADIUS = "5px"
    RADIUS_LG = "10px"
    
    # Fonte do site
    FONT_FAMILY = "Segoe UI"  # Fallback para Saira
    
    @classmethod
    def get_light_theme(cls) -> dict:
        """Tema claro - Padrão do site 2LOCK"""
        return {
            "background": cls.WHITE,
            "background_secondary": cls.GRAY_BG,
            "card": cls.WHITE,
            "foreground": cls.TEXT_DARK,
            "foreground_secondary": cls.TEXT_SECONDARY,
            "primary": cls.BLUE_PRIMARY,
            "primary_hover": cls.BLUE_HOVER,
            "primary_light": cls.BLUE_LIGHT,
            "success": cls.SUCCESS,
            "warning": cls.WARNING,
            "error": cls.ERROR,
            "border": cls.BORDER,
            "border_light": cls.BORDER_LIGHT,
            "input_bg": cls.WHITE,
            "shadow": "rgba(0, 0, 0, 0.08)",
        }
    
    @classmethod
    def get_dark_theme(cls) -> dict:
        """Tema escuro - Versão dark do site"""
        return {
            "background": "#0F1629",
            "background_secondary": "#1A2744",
            "card": "#1E2D4D",
            "foreground": "#FFFFFF",
            "foreground_secondary": "#A0AEC0",
            "primary": cls.BLUE_PRIMARY,
            "primary_hover": cls.BLUE_HOVER,
            "primary_light": "#1E3A5F",
            "success": cls.SUCCESS,
            "warning": cls.WARNING,
            "error": cls.ERROR,
            "border": "#2D3E5F",
            "border_light": "#1E2D4D",
            "input_bg": "#0F1629",
            "shadow": "rgba(0, 0, 0, 0.3)",
        }


# ============== WIDGETS CUSTOMIZADOS ==============

class Logo2Lock(QWidget):
    """Logo da 2LOCK fiel ao site"""
    
    def __init__(self, size: int = 40, parent=None):
        super().__init__(parent)
        self.size = size
        self.setFixedSize(size, size)
        self._is_dark = False
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fundo circular azul
        painter.setBrush(QBrush(QColor(Theme.BLUE_PRIMARY)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.size, self.size)
        
        # Texto "2L" branco
        painter.setPen(QPen(QColor("#FFFFFF")))
        font = QFont(Theme.FONT_FAMILY, int(self.size * 0.35), QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "2L")


class Button2Lock(QPushButton):
    """Botão no estilo exato do site 2LOCK"""
    
    def __init__(self, text: str, variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self._is_dark = False
        self._apply_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self._apply_style()
    
    def _apply_style(self):
        if self.variant == "primary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Theme.BLUE_PRIMARY};
                    color: #FFFFFF;
                    border: none;
                    border-radius: {Theme.RADIUS};
                    padding: 12px 24px;
                    font-family: {Theme.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {Theme.BLUE_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: #3377DD;
                }}
            """)
        elif self.variant == "outline":
            border_color = Theme.BLUE_PRIMARY
            text_color = Theme.BLUE_PRIMARY if not self._is_dark else "#FFFFFF"
            bg_hover = Theme.BLUE_LIGHT if not self._is_dark else "rgba(85, 153, 255, 0.1)"
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {text_color};
                    border: 2px solid {border_color};
                    border-radius: {Theme.RADIUS};
                    padding: 10px 22px;
                    font-family: {Theme.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {bg_hover};
                }}
            """)
        elif self.variant == "ghost":
            text_color = Theme.TEXT_DARK if not self._is_dark else "#FFFFFF"
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {text_color};
                    border: none;
                    border-radius: {Theme.RADIUS};
                    padding: 10px 16px;
                    font-family: {Theme.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {"#F3F4F6" if not self._is_dark else "rgba(255,255,255,0.1)"};
                }}
            """)


class Card2Lock(QFrame):
    """Card no estilo do site 2LOCK"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self._apply_style()
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self._apply_style()
    
    def _apply_style(self):
        theme = Theme.get_dark_theme() if self._is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            Card2Lock {{
                background-color: {theme["card"]};
                border: 1px solid {theme["border"]};
                border-radius: {Theme.RADIUS_LG};
            }}
        """)
        
        # Sombra sutil como no site
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 25 if not self._is_dark else 50))
        self.setGraphicsEffect(shadow)


class NavTab2Lock(QPushButton):
    """Tab de navegação no estilo do site"""
    
    def __init__(self, text: str, icon_text: str = "", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.icon_text = icon_text
        self._is_active = False
        self._is_dark = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(44)
        self._apply_style()
    
    def set_active(self, active: bool):
        self._is_active = active
        self._apply_style()
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self._apply_style()
    
    def _apply_style(self):
        if self._is_active:
            bg = Theme.BLUE_PRIMARY
            color = "#FFFFFF"
        else:
            bg = "transparent"
            color = Theme.TEXT_SECONDARY if not self._is_dark else "#A0AEC0"
        
        hover_bg = Theme.BLUE_LIGHT if not self._is_dark else "rgba(85, 153, 255, 0.15)"
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: none;
                border-radius: {Theme.RADIUS};
                padding: 8px 16px;
                font-family: {Theme.FONT_FAMILY};
                font-size: 14px;
                font-weight: {"600" if self._is_active else "500"};
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {bg if self._is_active else hover_bg};
                color: {color if self._is_active else Theme.BLUE_PRIMARY};
            }}
        """)


class InputField2Lock(QLineEdit):
    """Campo de input no estilo do site"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._is_dark = False
        self._apply_style()
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self._apply_style()
    
    def _apply_style(self):
        theme = Theme.get_dark_theme() if self._is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {theme["input_bg"]};
                color: {theme["foreground"]};
                border: 1px solid {theme["border"]};
                border-radius: {Theme.RADIUS};
                padding: 10px 14px;
                font-family: {Theme.FONT_FAMILY};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Theme.BLUE_PRIMARY};
                padding: 9px 13px;
            }}
            QLineEdit::placeholder {{
                color: {theme["foreground_secondary"]};
            }}
        """)


class StatusBadge(QLabel):
    """Badge de status como no site"""
    
    def __init__(self, text: str, status: str = "default", parent=None):
        super().__init__(text, parent)
        self.status = status
        self._apply_style()
    
    def set_status(self, status: str):
        self.status = status
        self._apply_style()
    
    def _apply_style(self):
        colors = {
            "success": (Theme.SUCCESS, "#ECFDF5", "#065F46"),
            "warning": (Theme.WARNING, "#FFFBEB", "#92400E"),
            "error": (Theme.ERROR, "#FEF2F2", "#991B1B"),
            "info": (Theme.BLUE_PRIMARY, Theme.BLUE_LIGHT, "#1E40AF"),
            "default": ("#6B7280", "#F3F4F6", "#374151"),
        }
        
        border_color, bg_color, text_color = colors.get(self.status, colors["default"])
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color}33;
                border-radius: 12px;
                padding: 4px 12px;
                font-family: {Theme.FONT_FAMILY};
                font-size: 12px;
                font-weight: 600;
            }}
        """)


# ============== SIDEBAR ==============

class Sidebar(QFrame):
    """Sidebar no estilo do site 2LOCK"""
    
    tab_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self.setFixedWidth(260)
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)
        
        # Logo e nome
        header = QHBoxLayout()
        header.setSpacing(12)
        
        self.logo = Logo2Lock(40)
        header.addWidget(self.logo)
        
        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(0)
        
        self.brand_name = QLabel("2LOCK")
        self.brand_name.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 18px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        brand_layout.addWidget(self.brand_name)
        
        self.brand_subtitle = QLabel("Automação NFS-e")
        self.brand_subtitle.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 12px;
            color: {Theme.TEXT_SECONDARY};
        """)
        brand_layout.addWidget(self.brand_subtitle)
        
        header.addLayout(brand_layout)
        header.addStretch()
        
        # Status online
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet(f"color: {Theme.SUCCESS}; font-size: 10px;")
        header.addWidget(self.status_dot)
        
        layout.addLayout(header)
        
        # Separador
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {Theme.BORDER};")
        layout.addWidget(separator)
        layout.addSpacing(16)
        
        # Menu label
        self.menu_label = QLabel("MENU")
        self.menu_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 11px;
            font-weight: 600;
            color: {Theme.TEXT_LIGHT};
            letter-spacing: 1px;
        """)
        layout.addWidget(self.menu_label)
        layout.addSpacing(8)
        
        # Tabs de navegação
        self.tabs = {}
        tab_items = [
            ("dashboard", "Dashboard", "📊"),
            ("planilha", "Planilha", "📋"),
            ("log", "Log de Execução", "📝"),
            ("historico", "Histórico", "🕐"),
            ("usuario", "Minha Conta", "👤"),
        ]
        
        for tab_id, text, icon in tab_items:
            tab = NavTab2Lock(f"  {icon}  {text}")
            tab.clicked.connect(lambda checked, t=tab_id: self._on_tab_clicked(t))
            self.tabs[tab_id] = tab
            layout.addWidget(tab)
        
        self.tabs["dashboard"].set_active(True)
        
        layout.addStretch()
        
        # Card de estatísticas
        self.stats_card = Card2Lock()
        stats_layout = QVBoxLayout(self.stats_card)
        stats_layout.setContentsMargins(16, 16, 16, 16)
        stats_layout.setSpacing(12)
        
        stats_header = QHBoxLayout()
        self.stats_icon = QLabel("✓")
        self.stats_icon.setStyleSheet(f"""
            background-color: {Theme.SUCCESS};
            color: white;
            border-radius: 15px;
            padding: 5px;
            font-size: 14px;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
        """)
        self.stats_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_header.addWidget(self.stats_icon)
        
        stats_text = QVBoxLayout()
        stats_text.setSpacing(0)
        self.stats_label = QLabel("Taxa de sucesso")
        self.stats_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 12px;
            color: {Theme.TEXT_SECONDARY};
        """)
        stats_text.addWidget(self.stats_label)
        
        self.stats_value = QLabel("98.5%")
        self.stats_value.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 20px;
            font-weight: 700;
            color: {Theme.SUCCESS};
        """)
        stats_text.addWidget(self.stats_value)
        
        stats_header.addLayout(stats_text)
        stats_header.addStretch()
        stats_layout.addLayout(stats_header)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(98)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Theme.BORDER};
                border-radius: 3px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {Theme.SUCCESS};
                border-radius: 3px;
            }}
        """)
        stats_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.stats_card)
        
        # Botão tema
        layout.addSpacing(12)
        self.theme_btn = Button2Lock("☀️  Tema Claro", "ghost")
        self.theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_btn)
    
    def _on_tab_clicked(self, tab_id: str):
        for tid, tab in self.tabs.items():
            tab.set_active(tid == tab_id)
        self.tab_changed.emit(tab_id)
    
    def _toggle_theme(self):
        self._is_dark = not self._is_dark
        self.set_dark_mode(self._is_dark)
        self.parent().set_dark_mode(self._is_dark)
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self._apply_style()
        self.logo.set_dark_mode(is_dark)
        self.stats_card.set_dark_mode(is_dark)
        
        for tab in self.tabs.values():
            tab.set_dark_mode(is_dark)
        
        self.theme_btn.setText("☀️  Tema Claro" if is_dark else "🌙  Tema Escuro")
        self.theme_btn.set_dark_mode(is_dark)
        
        theme = Theme.get_dark_theme() if is_dark else Theme.get_light_theme()
        self.brand_name.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 18px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        self.brand_subtitle.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 12px;
            color: {theme["foreground_secondary"]};
        """)
        self.menu_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 11px;
            font-weight: 600;
            color: {theme["foreground_secondary"]};
            letter-spacing: 1px;
        """)
        self.stats_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 12px;
            color: {theme["foreground_secondary"]};
        """)
    
    def _apply_style(self):
        theme = Theme.get_dark_theme() if self._is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            Sidebar {{
                background-color: {theme["background"]};
                border-right: 1px solid {theme["border"]};
            }}
        """)


# ============== PÁGINAS DE CONTEÚDO ==============

class DashboardPage(QWidget):
    """Página Dashboard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header = QHBoxLayout()
        
        title_section = QVBoxLayout()
        title_section.setSpacing(4)
        
        self.title = QLabel("Dashboard")
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        title_section.addWidget(self.title)
        
        self.subtitle = QLabel("Gerencie suas notas fiscais de serviço eletrônicas")
        self.subtitle.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 14px;
            color: {Theme.TEXT_SECONDARY};
        """)
        title_section.addWidget(self.subtitle)
        
        header.addLayout(title_section)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Upload Card
        self.upload_card = Card2Lock()
        upload_layout = QVBoxLayout(self.upload_card)
        upload_layout.setContentsMargins(32, 32, 32, 32)
        upload_layout.setSpacing(16)
        
        # Área de upload
        self.upload_area = QFrame()
        self.upload_area.setFixedHeight(180)
        self.upload_area.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.GRAY_BG};
                border: 2px dashed {Theme.BORDER};
                border-radius: {Theme.RADIUS_LG};
            }}
            QFrame:hover {{
                border-color: {Theme.BLUE_PRIMARY};
                background-color: {Theme.BLUE_LIGHT};
            }}
        """)
        
        upload_content = QVBoxLayout(self.upload_area)
        upload_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_content.setSpacing(12)
        
        upload_icon = QLabel("📁")
        upload_icon.setStyleSheet("font-size: 48px;")
        upload_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_content.addWidget(upload_icon)
        
        self.upload_text = QLabel("Arraste sua planilha Excel aqui")
        self.upload_text.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 16px;
            font-weight: 600;
            color: {Theme.TEXT_DARK};
        """)
        self.upload_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_content.addWidget(self.upload_text)
        
        self.upload_hint = QLabel("ou clique para selecionar um arquivo")
        self.upload_hint.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 13px;
            color: {Theme.TEXT_SECONDARY};
        """)
        self.upload_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_content.addWidget(self.upload_hint)
        
        upload_layout.addWidget(self.upload_area)
        
        # Arquivo selecionado
        self.file_info = QFrame()
        self.file_info.setVisible(False)
        file_info_layout = QHBoxLayout(self.file_info)
        file_info_layout.setContentsMargins(16, 12, 16, 12)
        
        self.file_icon = QLabel("📄")
        self.file_icon.setStyleSheet("font-size: 24px;")
        file_info_layout.addWidget(self.file_icon)
        
        file_text_layout = QVBoxLayout()
        file_text_layout.setSpacing(2)
        self.file_name = QLabel("arquivo.xlsx")
        self.file_name.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 14px;
            font-weight: 600;
            color: {Theme.TEXT_DARK};
        """)
        file_text_layout.addWidget(self.file_name)
        
        self.file_size = QLabel("2.4 MB")
        self.file_size.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 12px;
            color: {Theme.TEXT_SECONDARY};
        """)
        file_text_layout.addWidget(self.file_size)
        file_info_layout.addLayout(file_text_layout)
        
        file_info_layout.addStretch()
        
        self.remove_file_btn = Button2Lock("✕", "ghost")
        self.remove_file_btn.setFixedSize(32, 32)
        file_info_layout.addWidget(self.remove_file_btn)
        
        upload_layout.addWidget(self.file_info)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.select_btn = Button2Lock("📂  Selecionar Planilha", "outline")
        self.select_btn.clicked.connect(self._select_file)
        btn_layout.addWidget(self.select_btn)
        
        self.process_btn = Button2Lock("⚡  Confirmar e Processar", "primary")
        self.process_btn.clicked.connect(self._process_file)
        btn_layout.addWidget(self.process_btn)
        
        btn_layout.addStretch()
        upload_layout.addLayout(btn_layout)
        
        layout.addWidget(self.upload_card)
        
        # Preview do Log
        self.log_card = Card2Lock()
        log_layout = QVBoxLayout(self.log_card)
        log_layout.setContentsMargins(24, 20, 24, 20)
        log_layout.setSpacing(12)
        
        log_header = QHBoxLayout()
        self.log_title = QLabel("📝  Log de Execução")
        self.log_title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 16px;
            font-weight: 600;
            color: {Theme.TEXT_DARK};
        """)
        log_header.addWidget(self.log_title)
        log_header.addStretch()
        
        self.clear_log_btn = Button2Lock("Limpar", "ghost")
        self.clear_log_btn.clicked.connect(self._clear_log)
        log_header.addWidget(self.clear_log_btn)
        
        log_layout.addLayout(log_header)
        
        self.log_preview = QTextEdit()
        self.log_preview.setReadOnly(True)
        self.log_preview.setFixedHeight(150)
        self.log_preview.setStyleSheet(f"""
            QTextEdit {{
                background-color: #1a1a2e;
                color: #00ff88;
                border: 1px solid {Theme.BORDER};
                border-radius: {Theme.RADIUS};
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }}
        """)
        self._add_log("Interface iniciada com sucesso. Aguardando arquivo...", LogType.INFO)
        log_layout.addWidget(self.log_preview)
        
        layout.addWidget(self.log_card)
        layout.addStretch()
    
    def _select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Planilha Excel", "",
            "Arquivos Excel (*.xlsx *.xls);;Todos os arquivos (*.*)"
        )
        if file_path:
            import os
            file_name = os.path.basename(file_path)
            self.file_name.setText(file_name)
            self.file_info.setVisible(True)
            self._add_log(f"Arquivo selecionado: {file_name}", LogType.SUCCESS)
    
    def _process_file(self):
        self._add_log("Iniciando processamento...", LogType.INFO)
        QTimer.singleShot(500, lambda: self._add_log("Validando dados da planilha...", LogType.INFO))
        QTimer.singleShot(1000, lambda: self._add_log("Processamento concluído com sucesso!", LogType.SUCCESS))
    
    def _clear_log(self):
        self.log_preview.clear()
        self._add_log("Log limpo.", LogType.INFO)
    
    def _add_log(self, message: str, log_type: LogType = LogType.INFO):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            LogType.INFO: "#00bfff",
            LogType.SUCCESS: "#00ff88",
            LogType.WARNING: "#ffaa00",
            LogType.ERROR: "#ff4444",
        }
        color = colors.get(log_type, "#00bfff")
        self.log_preview.append(f'<span style="color: #888;">{timestamp}</span> - <span style="color: {color};">{message}</span>')
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        theme = Theme.get_dark_theme() if is_dark else Theme.get_light_theme()
        
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        self.subtitle.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 14px;
            color: {theme["foreground_secondary"]};
        """)
        self.upload_text.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 16px;
            font-weight: 600;
            color: {theme["foreground"]};
        """)
        self.upload_hint.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 13px;
            color: {theme["foreground_secondary"]};
        """)
        self.log_title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 16px;
            font-weight: 600;
            color: {theme["foreground"]};
        """)
        self.file_name.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 14px;
            font-weight: 600;
            color: {theme["foreground"]};
        """)
        
        self.upload_card.set_dark_mode(is_dark)
        self.log_card.set_dark_mode(is_dark)
        self.select_btn.set_dark_mode(is_dark)
        self.clear_log_btn.set_dark_mode(is_dark)
        self.remove_file_btn.set_dark_mode(is_dark)
        
        # Upload area
        if is_dark:
            self.upload_area.setStyleSheet(f"""
                QFrame {{
                    background-color: {theme["background_secondary"]};
                    border: 2px dashed {theme["border"]};
                    border-radius: {Theme.RADIUS_LG};
                }}
                QFrame:hover {{
                    border-color: {Theme.BLUE_PRIMARY};
                    background-color: {theme["primary_light"]};
                }}
            """)
        else:
            self.upload_area.setStyleSheet(f"""
                QFrame {{
                    background-color: {Theme.GRAY_BG};
                    border: 2px dashed {Theme.BORDER};
                    border-radius: {Theme.RADIUS_LG};
                }}
                QFrame:hover {{
                    border-color: {Theme.BLUE_PRIMARY};
                    background-color: {Theme.BLUE_LIGHT};
                }}
            """)


class SpreadsheetPage(QWidget):
    """Página de visualização da Planilha"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header = QHBoxLayout()
        
        self.title = QLabel("📋  Planilha")
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        header.addWidget(self.title)
        header.addStretch()
        
        self.search_input = InputField2Lock("🔍  Buscar na planilha...")
        self.search_input.setFixedWidth(300)
        header.addWidget(self.search_input)
        
        layout.addLayout(header)
        
        # Tabela
        self.card = Card2Lock()
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Empresa", "CNPJ", "Valor", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self._apply_table_style()
        
        # Dados de exemplo
        sample_data = [
            ("001", "Tech Solutions Ltda", "12.345.678/0001-90", "R$ 15.000,00", "Processado"),
            ("002", "Inovação Digital SA", "98.765.432/0001-10", "R$ 8.500,00", "Pendente"),
            ("003", "Serviços Cloud ME", "11.222.333/0001-44", "R$ 22.750,00", "Processado"),
            ("004", "Consultoria Alfa", "55.666.777/0001-88", "R$ 5.200,00", "Erro"),
            ("005", "Desenvolvimento Beta", "99.888.777/0001-22", "R$ 18.300,00", "Processado"),
        ]
        
        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        
        card_layout.addWidget(self.table)
        layout.addWidget(self.card)
    
    def _apply_table_style(self):
        theme = Theme.get_dark_theme() if self._is_dark else Theme.get_light_theme()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {theme["card"]};
                color: {theme["foreground"]};
                border: none;
                gridline-color: {theme["border"]};
                font-family: {Theme.FONT_FAMILY};
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {theme["border"]};
            }}
            QTableWidget::item:selected {{
                background-color: {Theme.BLUE_LIGHT if not self._is_dark else theme["primary_light"]};
                color: {theme["foreground"]};
            }}
            QHeaderView::section {{
                background-color: {theme["background_secondary"]};
                color: {theme["foreground"]};
                padding: 14px;
                border: none;
                border-bottom: 2px solid {theme["border"]};
                font-weight: 600;
                font-size: 13px;
            }}
        """)
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        theme = Theme.get_dark_theme() if is_dark else Theme.get_light_theme()
        
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        
        self.card.set_dark_mode(is_dark)
        self.search_input.set_dark_mode(is_dark)
        self._apply_table_style()


class LogPage(QWidget):
    """Página de Log completo"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header = QHBoxLayout()
        
        self.title = QLabel("📝  Log de Execução")
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        header.addWidget(self.title)
        header.addStretch()
        
        self.export_btn = Button2Lock("📤  Exportar Log", "outline")
        header.addWidget(self.export_btn)
        
        self.clear_btn = Button2Lock("🗑️  Limpar", "ghost")
        header.addWidget(self.clear_btn)
        
        layout.addLayout(header)
        
        # Log completo
        self.card = Card2Lock()
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0d1117;
                color: #00ff88;
                border: none;
                border-radius: {Theme.RADIUS_LG};
                padding: 20px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.6;
            }}
        """)
        
        # Logs de exemplo
        logs = [
            ("10:30:15", "Sistema inicializado com sucesso", "info"),
            ("10:30:16", "Conexão com servidor estabelecida", "success"),
            ("10:31:02", "Arquivo 'dados_nfse.xlsx' carregado", "info"),
            ("10:31:03", "Validação de dados iniciada...", "info"),
            ("10:31:05", "127 registros encontrados", "info"),
            ("10:31:10", "Processamento em lote iniciado", "info"),
            ("10:32:45", "Registro #45 - Alerta: CNPJ com formato antigo", "warning"),
            ("10:35:20", "Processamento concluído: 126 sucesso, 1 alerta", "success"),
        ]
        
        for time, msg, log_type in logs:
            colors = {"info": "#00bfff", "success": "#00ff88", "warning": "#ffaa00", "error": "#ff4444"}
            color = colors.get(log_type, "#00bfff")
            self.log_text.append(f'<span style="color: #586069;">[{time}]</span> <span style="color: {color};">{msg}</span>')
        
        card_layout.addWidget(self.log_text)
        layout.addWidget(self.card)
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        theme = Theme.get_dark_theme() if is_dark else Theme.get_light_theme()
        
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        
        self.card.set_dark_mode(is_dark)
        self.export_btn.set_dark_mode(is_dark)
        self.clear_btn.set_dark_mode(is_dark)


class HistoryPage(QWidget):
    """Página de Histórico"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header = QHBoxLayout()
        
        self.title = QLabel("🕐  Histórico de Processamentos")
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        header.addWidget(self.title)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Cards de histórico
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)
        
        history_items = [
            ("28/05/2026 10:35", "relatorio_maio.xlsx", 127, "Concluído", "4m 15s"),
            ("27/05/2026 15:20", "nfse_clientes.xlsx", 89, "Concluído", "2m 48s"),
            ("27/05/2026 09:10", "dados_empresa.xlsx", 234, "Concluído", "6m 32s"),
            ("26/05/2026 14:45", "backup_nfse.xlsx", 56, "Erro", "1m 20s"),
            ("25/05/2026 11:00", "lote_mensal.xlsx", 312, "Concluído", "8m 55s"),
        ]
        
        self.history_cards = []
        for date, file, records, status, duration in history_items:
            card = self._create_history_card(date, file, records, status, duration)
            self.history_cards.append(card)
            scroll_layout.addWidget(card)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
    
    def _create_history_card(self, date: str, file: str, records: int, status: str, duration: str) -> Card2Lock:
        card = Card2Lock()
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(20)
        
        # Ícone
        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon)
        
        # Info principal
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        file_label = QLabel(file)
        file_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 15px;
            font-weight: 600;
            color: {Theme.TEXT_DARK};
        """)
        file_label.setProperty("class", "file_label")
        info_layout.addWidget(file_label)
        
        meta_label = QLabel(f"{date}  •  {records} registros  •  {duration}")
        meta_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 13px;
            color: {Theme.TEXT_SECONDARY};
        """)
        meta_label.setProperty("class", "meta_label")
        info_layout.addWidget(meta_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Status badge
        status_type = "success" if status == "Concluído" else "error"
        badge = StatusBadge(status, status_type)
        layout.addWidget(badge)
        
        return card
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        theme = Theme.get_dark_theme() if is_dark else Theme.get_light_theme()
        
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        
        for card in self.history_cards:
            card.set_dark_mode(is_dark)
            for label in card.findChildren(QLabel):
                if label.property("class") == "file_label":
                    label.setStyleSheet(f"""
                        font-family: {Theme.FONT_FAMILY};
                        font-size: 15px;
                        font-weight: 600;
                        color: {theme["foreground"]};
                    """)
                elif label.property("class") == "meta_label":
                    label.setStyleSheet(f"""
                        font-family: {Theme.FONT_FAMILY};
                        font-size: 13px;
                        color: {theme["foreground_secondary"]};
                    """)


class UserPage(QWidget):
    """Página de Usuário / Minha Conta"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        self.title = QLabel("👤  Minha Conta")
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        layout.addWidget(self.title)
        
        # Profile Card
        self.profile_card = Card2Lock()
        profile_layout = QHBoxLayout(self.profile_card)
        profile_layout.setContentsMargins(24, 24, 24, 24)
        profile_layout.setSpacing(20)
        
        # Avatar
        avatar = QLabel("👤")
        avatar.setFixedSize(80, 80)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {Theme.BLUE_LIGHT};
            border-radius: 40px;
            font-size: 36px;
        """)
        profile_layout.addWidget(avatar)
        
        # Info do usuário
        user_info = QVBoxLayout()
        user_info.setSpacing(4)
        
        self.user_name = QLabel("Administrador 2LOCK")
        self.user_name.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 20px;
            font-weight: 700;
            color: {Theme.TEXT_DARK};
        """)
        user_info.addWidget(self.user_name)
        
        self.user_email = QLabel("admin@2lock.com.br")
        self.user_email.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 14px;
            color: {Theme.TEXT_SECONDARY};
        """)
        user_info.addWidget(self.user_email)
        
        self.user_role = StatusBadge("Administrador", "info")
        user_info.addWidget(self.user_role)
        
        profile_layout.addLayout(user_info)
        profile_layout.addStretch()
        
        self.edit_btn = Button2Lock("✏️  Editar Perfil", "outline")
        profile_layout.addWidget(self.edit_btn)
        
        layout.addWidget(self.profile_card)
        
        # Stats Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats_data = [
            ("📊", "Total Processados", "1.247", Theme.BLUE_PRIMARY),
            ("✅", "Taxa de Sucesso", "98.5%", Theme.SUCCESS),
            ("📅", "Este Mês", "127", Theme.WARNING),
        ]
        
        self.stat_cards = []
        for icon, label, value, color in stats_data:
            card = self._create_stat_card(icon, label, value, color)
            self.stat_cards.append(card)
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
    
    def _create_stat_card(self, icon: str, label: str, value: str, color: str) -> Card2Lock:
        card = Card2Lock()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 28px;")
        layout.addWidget(icon_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {color};
        """)
        value_label.setProperty("class", "value_label")
        value_label.setProperty("color", color)
        layout.addWidget(value_label)
        
        text_label = QLabel(label)
        text_label.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 13px;
            color: {Theme.TEXT_SECONDARY};
        """)
        text_label.setProperty("class", "text_label")
        layout.addWidget(text_label)
        
        return card
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        theme = Theme.get_dark_theme() if is_dark else Theme.get_light_theme()
        
        self.title.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        self.user_name.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 20px;
            font-weight: 700;
            color: {theme["foreground"]};
        """)
        self.user_email.setStyleSheet(f"""
            font-family: {Theme.FONT_FAMILY};
            font-size: 14px;
            color: {theme["foreground_secondary"]};
        """)
        
        self.profile_card.set_dark_mode(is_dark)
        self.edit_btn.set_dark_mode(is_dark)
        
        for card in self.stat_cards:
            card.set_dark_mode(is_dark)
            for label in card.findChildren(QLabel):
                if label.property("class") == "text_label":
                    label.setStyleSheet(f"""
                        font-family: {Theme.FONT_FAMILY};
                        font-size: 13px;
                        color: {theme["foreground_secondary"]};
                    """)


# ============== JANELA PRINCIPAL ==============

class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self._is_dark = False
        self.setWindowTitle("2LOCK - Automação NFS-e")
        self.setMinimumSize(1200, 750)
        self.resize(1400, 850)
        
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.tab_changed.connect(self._on_tab_changed)
        main_layout.addWidget(self.sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        
        self.dashboard_page = DashboardPage()
        self.spreadsheet_page = SpreadsheetPage()
        self.log_page = LogPage()
        self.history_page = HistoryPage()
        self.user_page = UserPage()
        
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.spreadsheet_page)
        self.content_stack.addWidget(self.log_page)
        self.content_stack.addWidget(self.history_page)
        self.content_stack.addWidget(self.user_page)
        
        main_layout.addWidget(self.content_stack)
    
    def _on_tab_changed(self, tab_id: str):
        pages = {
            "dashboard": 0,
            "planilha": 1,
            "log": 2,
            "historico": 3,
            "usuario": 4,
        }
        self.content_stack.setCurrentIndex(pages.get(tab_id, 0))
    
    def set_dark_mode(self, is_dark: bool):
        self._is_dark = is_dark
        self._apply_style()
        
        self.dashboard_page.set_dark_mode(is_dark)
        self.spreadsheet_page.set_dark_mode(is_dark)
        self.log_page.set_dark_mode(is_dark)
        self.history_page.set_dark_mode(is_dark)
        self.user_page.set_dark_mode(is_dark)
    
    def _apply_style(self):
        theme = Theme.get_dark_theme() if self._is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme["background_secondary"]};
            }}
            QWidget {{
                font-family: {Theme.FONT_FAMILY};
            }}
        """)


def main():
    app = QApplication(sys.argv)
    
    # Configurar fonte padrão
    font = QFont(Theme.FONT_FAMILY, 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
