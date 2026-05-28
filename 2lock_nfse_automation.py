#!/usr/bin/env python3
"""
2LOCK - Automação NFS-e
Design moderno com Glassmorphism, Acrylic e Vibrancy
Python 3.13 + PyQt6
"""

import sys
import os
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QFrame, QStackedWidget, QScrollArea, QLineEdit,
    QHeaderView, QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
    QProgressBar, QMessageBox
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QSize,
    pyqtSignal, QParallelAnimationGroup, QSequentialAnimationGroup,
    QAbstractAnimation
)
from PyQt6.QtGui import (
    QColor, QPalette, QFont, QFontDatabase, QIcon, QPainter,
    QBrush, QLinearGradient, QRadialGradient, QPen, QPixmap,
    QPainterPath, QRegion
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


# ============== TEMA E CORES ==============

class Theme:
    """Gerenciador de temas 2LOCK"""
    
    # Cores da marca 2LOCK
    BRAND_BLUE = "#3B82F6"
    BRAND_BLUE_DARK = "#2563EB"
    BRAND_BLUE_LIGHT = "#60A5FA"
    
    @staticmethod
    def get_dark_theme() -> dict:
        return {
            "background": "#0f172a",
            "background_secondary": "#1e293b",
            "card": "rgba(30, 41, 59, 0.6)",
            "card_solid": "#1e293b",
            "foreground": "#f8fafc",
            "foreground_secondary": "#94a3b8",
            "primary": "#3B82F6",
            "primary_hover": "#2563EB",
            "primary_light": "#60A5FA",
            "accent": "#818CF8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444",
            "border": "rgba(71, 85, 105, 0.4)",
            "input": "rgba(15, 23, 42, 0.6)",
            "glass_bg": "rgba(30, 41, 59, 0.4)",
            "glass_border": "rgba(71, 85, 105, 0.3)",
            "glow": "rgba(59, 130, 246, 0.5)",
        }
    
    @staticmethod
    def get_light_theme() -> dict:
        return {
            "background": "#f8fafc",
            "background_secondary": "#e2e8f0",
            "card": "rgba(255, 255, 255, 0.8)",
            "card_solid": "#ffffff",
            "foreground": "#0f172a",
            "foreground_secondary": "#475569",
            "primary": "#2563EB",
            "primary_hover": "#1D4ED8",
            "primary_light": "#3B82F6",
            "accent": "#6366F1",
            "success": "#059669",
            "warning": "#D97706",
            "error": "#DC2626",
            "border": "rgba(203, 213, 225, 0.6)",
            "input": "rgba(241, 245, 249, 0.8)",
            "glass_bg": "rgba(255, 255, 255, 0.6)",
            "glass_border": "rgba(203, 213, 225, 0.4)",
            "glow": "rgba(37, 99, 235, 0.3)",
        }


# ============== COMPONENTES BASE ==============

class GlassCard(QFrame):
    """Card com efeito Glassmorphism"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = True
        self._setup_style()
    
    def _setup_style(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            GlassCard {{
                background-color: {theme['glass_bg']};
                border: 1px solid {theme['glass_border']};
                border-radius: 16px;
            }}
        """)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 80 if self.is_dark else 40))
        self.setGraphicsEffect(shadow)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self._setup_style()


class GlowButton(QPushButton):
    """Botão com efeito de glow"""
    
    def __init__(self, text: str, primary: bool = True, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.is_dark = True
        self._setup_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _setup_style(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        
        if self.primary:
            self.setStyleSheet(f"""
                GlowButton {{
                    background-color: {theme['primary']};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }}
                GlowButton:hover {{
                    background-color: {theme['primary_hover']};
                }}
                GlowButton:pressed {{
                    background-color: {theme['primary']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                GlowButton {{
                    background-color: {theme['glass_bg']};
                    color: {theme['foreground']};
                    border: 1px solid {theme['border']};
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 500;
                }}
                GlowButton:hover {{
                    background-color: {theme['card']};
                    border-color: {theme['primary']};
                }}
            """)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self._setup_style()


class IconButton(QPushButton):
    """Botão de ícone circular"""
    
    def __init__(self, icon_char: str, parent=None):
        super().__init__(icon_char, parent)
        self.is_dark = True
        self.setFixedSize(40, 40)
        self._setup_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _setup_style(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            IconButton {{
                background-color: {theme['glass_bg']};
                color: {theme['foreground']};
                border: 1px solid {theme['border']};
                border-radius: 20px;
                font-size: 16px;
            }}
            IconButton:hover {{
                background-color: {theme['card']};
                border-color: {theme['primary']};
            }}
        """)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self._setup_style()


class ModernLineEdit(QLineEdit):
    """Input moderno com estilo glass"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.is_dark = True
        self._setup_style()
    
    def _setup_style(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.setStyleSheet(f"""
            ModernLineEdit {{
                background-color: {theme['input']};
                color: {theme['foreground']};
                border: 1px solid {theme['border']};
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 14px;
            }}
            ModernLineEdit:focus {{
                border-color: {theme['primary']};
            }}
            ModernLineEdit::placeholder {{
                color: {theme['foreground_secondary']};
            }}
        """)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self._setup_style()


class TabButton(QPushButton):
    """Botão de aba na sidebar"""
    
    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(parent)
        self.icon_char = icon
        self.text_label = text
        self.is_active = False
        self.is_dark = True
        self.setText(f"  {icon}  {text}")
        self.setFixedHeight(48)
        self._setup_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _setup_style(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        
        if self.is_active:
            self.setStyleSheet(f"""
                TabButton {{
                    background-color: {theme['primary']};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 0 16px;
                    font-size: 14px;
                    font-weight: 600;
                    text-align: left;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                TabButton {{
                    background-color: transparent;
                    color: {theme['foreground_secondary']};
                    border: none;
                    border-radius: 12px;
                    padding: 0 16px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
                TabButton:hover {{
                    background-color: {theme['glass_bg']};
                    color: {theme['foreground']};
                }}
            """)
    
    def set_active(self, active: bool):
        self.is_active = active
        self._setup_style()
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self._setup_style()


class StatusBadge(QLabel):
    """Badge de status"""
    
    def __init__(self, text: str, status: str = "info", parent=None):
        super().__init__(text, parent)
        self.status = status
        self.is_dark = True
        self._setup_style()
    
    def _setup_style(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        
        colors = {
            "success": (theme['success'], "rgba(16, 185, 129, 0.2)"),
            "error": (theme['error'], "rgba(239, 68, 68, 0.2)"),
            "warning": (theme['warning'], "rgba(245, 158, 11, 0.2)"),
            "info": (theme['primary'], "rgba(59, 130, 246, 0.2)"),
        }
        
        fg, bg = colors.get(self.status, colors["info"])
        
        self.setStyleSheet(f"""
            StatusBadge {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {fg};
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: 600;
            }}
        """)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self._setup_style()


# ============== WIDGETS DE CONTEÚDO ==============

class DashboardWidget(QWidget):
    """Widget do Dashboard principal"""
    
    file_selected = pyqtSignal(str)
    process_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = True
        self.selected_file: Optional[str] = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Área de upload
        self.upload_card = GlassCard()
        upload_layout = QVBoxLayout(self.upload_card)
        upload_layout.setContentsMargins(32, 32, 32, 32)
        upload_layout.setSpacing(16)
        
        # Ícone de upload
        upload_icon = QLabel("📁")
        upload_icon.setStyleSheet("font-size: 48px;")
        upload_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Texto
        self.upload_text = QLabel("Arraste uma planilha Excel aqui ou clique para selecionar")
        self.upload_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Botão selecionar
        self.select_btn = GlowButton("Selecionar Planilha Excel")
        self.select_btn.clicked.connect(self._select_file)
        
        upload_layout.addWidget(upload_icon)
        upload_layout.addWidget(self.upload_text)
        upload_layout.addWidget(self.select_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Card de arquivo selecionado
        self.file_card = GlassCard()
        self.file_card.setVisible(False)
        file_layout = QHBoxLayout(self.file_card)
        file_layout.setContentsMargins(20, 16, 20, 16)
        
        file_icon = QLabel("📄")
        file_icon.setStyleSheet("font-size: 24px;")
        
        self.file_name_label = QLabel("")
        self.file_size_label = QLabel("")
        
        file_info_layout = QVBoxLayout()
        file_info_layout.addWidget(self.file_name_label)
        file_info_layout.addWidget(self.file_size_label)
        
        remove_btn = IconButton("✕")
        remove_btn.clicked.connect(self._remove_file)
        
        file_layout.addWidget(file_icon)
        file_layout.addLayout(file_info_layout)
        file_layout.addStretch()
        file_layout.addWidget(remove_btn)
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(16)
        
        self.process_btn = GlowButton("Confirmar e Processar")
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self._process)
        
        self.clear_btn = GlowButton("Limpar", primary=False)
        self.clear_btn.clicked.connect(self._remove_file)
        
        actions_layout.addStretch()
        actions_layout.addWidget(self.clear_btn)
        actions_layout.addWidget(self.process_btn)
        
        layout.addWidget(self.upload_card)
        layout.addWidget(self.file_card)
        layout.addStretch()
        layout.addLayout(actions_layout)
        
        self._update_styles()
    
    def _update_styles(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.upload_text.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 14px;")
        self.file_name_label.setStyleSheet(f"color: {theme['foreground']}; font-size: 14px; font-weight: 600;")
        self.file_size_label.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 12px;")
    
    def _select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Planilha Excel",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            self.file_name_label.setText(file_name)
            self.file_size_label.setText(f"{file_size / 1024:.1f} KB")
            
            self.upload_card.setVisible(False)
            self.file_card.setVisible(True)
            self.process_btn.setEnabled(True)
            
            self.file_selected.emit(file_path)
    
    def _remove_file(self):
        self.selected_file = None
        self.upload_card.setVisible(True)
        self.file_card.setVisible(False)
        self.process_btn.setEnabled(False)
    
    def _process(self):
        self.process_clicked.emit()
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self.upload_card.set_theme(is_dark)
        self.file_card.set_theme(is_dark)
        self.select_btn.set_theme(is_dark)
        self.process_btn.set_theme(is_dark)
        self.clear_btn.set_theme(is_dark)
        self._update_styles()


class SpreadsheetWidget(QWidget):
    """Widget de visualização da planilha"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = True
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Header com busca
        header_layout = QHBoxLayout()
        
        self.search_input = ModernLineEdit("Buscar na planilha...")
        self.search_input.setMaximumWidth(300)
        
        self.export_btn = GlowButton("Exportar", primary=False)
        
        header_layout.addWidget(self.search_input)
        header_layout.addStretch()
        header_layout.addWidget(self.export_btn)
        
        # Tabela
        self.table_card = GlassCard()
        table_layout = QVBoxLayout(self.table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Empresa", "CNPJ", "Valor", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        
        table_layout.addWidget(self.table)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.table_card)
        
        self._update_styles()
        self._load_sample_data()
    
    def _update_styles(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: transparent;
                color: {theme['foreground']};
                border: none;
                gridline-color: {theme['border']};
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {theme['border']};
            }}
            QTableWidget::item:selected {{
                background-color: {theme['primary']};
                color: white;
            }}
            QTableWidget::item:alternate {{
                background-color: {theme['glass_bg']};
            }}
            QHeaderView::section {{
                background-color: {theme['card_solid']};
                color: {theme['foreground']};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {theme['primary']};
                font-weight: 600;
            }}
        """)
    
    def _load_sample_data(self):
        sample_data = [
            ("1", "Empresa ABC Ltda", "12.345.678/0001-90", "R$ 1.500,00", "Processado"),
            ("2", "Comércio XYZ ME", "98.765.432/0001-10", "R$ 2.300,00", "Processado"),
            ("3", "Indústria 123 S/A", "11.222.333/0001-44", "R$ 5.000,00", "Pendente"),
            ("4", "Serviços Tech Ltda", "55.666.777/0001-88", "R$ 800,00", "Erro"),
            ("5", "Consultoria Plus", "99.888.777/0001-66", "R$ 3.200,00", "Processado"),
        ]
        
        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self.table_card.set_theme(is_dark)
        self.search_input.set_theme(is_dark)
        self.export_btn.set_theme(is_dark)
        self._update_styles()


class LogWidget(QWidget):
    """Widget de Log de execução"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = True
        self.logs: list[LogEntry] = []
        self._setup_ui()
        self._add_initial_log()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Log de Execução")
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        
        self.clear_btn = GlowButton("Limpar Log", primary=False)
        self.clear_btn.clicked.connect(self.clear_logs)
        
        self.export_btn = GlowButton("Exportar", primary=False)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_btn)
        header_layout.addWidget(self.export_btn)
        
        # Área de log
        self.log_card = GlassCard()
        log_layout = QVBoxLayout(self.log_card)
        log_layout.setContentsMargins(16, 16, 16, 16)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(400)
        
        log_layout.addWidget(self.log_text)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.log_card)
        
        self._update_styles()
    
    def _update_styles(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme['input']};
                color: {theme['foreground']};
                border: 1px solid {theme['border']};
                border-radius: 12px;
                padding: 16px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }}
        """)
    
    def _add_initial_log(self):
        self.add_log("Interface iniciada com sucesso. Aguardando arquivo...", LogType.INFO)
    
    def add_log(self, message: str, log_type: LogType = LogType.INFO):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = LogEntry(timestamp, message, log_type)
        self.logs.append(entry)
        self._update_log_display()
    
    def _update_log_display(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        
        colors = {
            LogType.INFO: theme['primary'],
            LogType.SUCCESS: theme['success'],
            LogType.WARNING: theme['warning'],
            LogType.ERROR: theme['error'],
        }
        
        icons = {
            LogType.INFO: "ℹ️",
            LogType.SUCCESS: "✅",
            LogType.WARNING: "⚠️",
            LogType.ERROR: "❌",
        }
        
        html = ""
        for log in self.logs:
            color = colors.get(log.type, theme['foreground'])
            icon = icons.get(log.type, "•")
            html += f'<p style="color: {color}; margin: 4px 0;">'
            html += f'<span style="color: {theme["foreground_secondary"]}">[{log.timestamp}]</span> '
            html += f'{icon} {log.message}</p>'
        
        self.log_text.setHtml(html)
        # Scroll para o final
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def clear_logs(self):
        self.logs.clear()
        self.log_text.clear()
        self._add_initial_log()
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self.log_card.set_theme(is_dark)
        self.clear_btn.set_theme(is_dark)
        self.export_btn.set_theme(is_dark)
        self._update_styles()
        self._update_log_display()


class HistoryWidget(QWidget):
    """Widget de Histórico de processamentos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = True
        self.history: list[HistoryEntry] = []
        self._setup_ui()
        self._load_sample_history()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Histórico de Processamentos")
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        
        self.search_input = ModernLineEdit("Buscar no histórico...")
        self.search_input.setMaximumWidth(300)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_input)
        
        # Tabela
        self.table_card = GlassCard()
        table_layout = QVBoxLayout(self.table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Data/Hora", "Arquivo", "Registros", "Status", "Duração"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        
        table_layout.addWidget(self.table)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.table_card)
        
        self._update_styles()
    
    def _update_styles(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: transparent;
                color: {theme['foreground']};
                border: none;
                gridline-color: {theme['border']};
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {theme['border']};
            }}
            QTableWidget::item:selected {{
                background-color: {theme['primary']};
                color: white;
            }}
            QTableWidget::item:alternate {{
                background-color: {theme['glass_bg']};
            }}
            QHeaderView::section {{
                background-color: {theme['card_solid']};
                color: {theme['foreground']};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {theme['primary']};
                font-weight: 600;
            }}
        """)
    
    def _load_sample_history(self):
        sample = [
            ("1", "28/05/2026 14:32", "notas_maio.xlsx", "150", "Sucesso", "2m 34s"),
            ("2", "27/05/2026 09:15", "clientes_abril.xlsx", "89", "Sucesso", "1m 12s"),
            ("3", "26/05/2026 16:45", "servicos_q2.xlsx", "234", "Erro Parcial", "4m 56s"),
            ("4", "25/05/2026 11:20", "faturamento.xlsx", "67", "Sucesso", "0m 45s"),
        ]
        
        self.table.setRowCount(len(sample))
        for row, data in enumerate(sample):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
    
    def add_entry(self, file_name: str, records: int, status: str, duration: str):
        entry = HistoryEntry(
            id=len(self.history) + 1,
            date=datetime.now().strftime("%d/%m/%Y %H:%M"),
            file=file_name,
            records=records,
            status=status,
            duration=duration
        )
        self.history.append(entry)
        
        row = self.table.rowCount()
        self.table.insertRow(row)
        data = (str(entry.id), entry.date, entry.file, str(entry.records), entry.status, entry.duration)
        for col, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, col, item)
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self.table_card.set_theme(is_dark)
        self.search_input.set_theme(is_dark)
        self._update_styles()


class UserWidget(QWidget):
    """Widget de perfil do usuário"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = True
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Card do perfil
        profile_card = GlassCard()
        self.profile_card = profile_card
        profile_layout = QHBoxLayout(profile_card)
        profile_layout.setContentsMargins(32, 32, 32, 32)
        profile_layout.setSpacing(24)
        
        # Avatar
        avatar = QLabel("👤")
        avatar.setStyleSheet("""
            font-size: 64px;
            background-color: rgba(59, 130, 246, 0.2);
            border-radius: 40px;
            padding: 16px;
        """)
        avatar.setFixedSize(96, 96)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Info do usuário
        info_layout = QVBoxLayout()
        
        self.name_label = QLabel("Usuário 2LOCK")
        self.email_label = QLabel("usuario@2lock.com.br")
        self.role_label = QLabel("Administrador")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.email_label)
        info_layout.addWidget(self.role_label)
        info_layout.addStretch()
        
        # Botão editar
        edit_btn = GlowButton("Editar Perfil", primary=False)
        self.edit_btn = edit_btn
        
        profile_layout.addWidget(avatar)
        profile_layout.addLayout(info_layout)
        profile_layout.addStretch()
        profile_layout.addWidget(edit_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Cards de estatísticas
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.stat_cards = []
        stats = [
            ("📊", "Total Processados", "1.234"),
            ("✅", "Taxa de Sucesso", "98.5%"),
            ("📅", "Último Acesso", "Hoje, 14:32"),
        ]
        
        for icon, title, value in stats:
            card = GlassCard()
            self.stat_cards.append(card)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 24, 24, 24)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")
            
            title_label = QLabel(title)
            title_label.setObjectName("stat_title")
            
            value_label = QLabel(value)
            value_label.setObjectName("stat_value")
            
            card_layout.addWidget(icon_label)
            card_layout.addWidget(title_label)
            card_layout.addWidget(value_label)
            
            stats_layout.addWidget(card)
        
        layout.addWidget(profile_card)
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        self._update_styles()
    
    def _update_styles(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        
        self.name_label.setStyleSheet(f"color: {theme['foreground']}; font-size: 24px; font-weight: 700;")
        self.email_label.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 14px;")
        self.role_label.setStyleSheet(f"""
            color: {theme['primary']};
            background-color: rgba(59, 130, 246, 0.2);
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
        """)
        
        for card in self.stat_cards:
            for child in card.findChildren(QLabel):
                if child.objectName() == "stat_title":
                    child.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 13px;")
                elif child.objectName() == "stat_value":
                    child.setStyleSheet(f"color: {theme['foreground']}; font-size: 28px; font-weight: 700;")
    
    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        self.profile_card.set_theme(is_dark)
        self.edit_btn.set_theme(is_dark)
        for card in self.stat_cards:
            card.set_theme(is_dark)
        self._update_styles()


# ============== JANELA PRINCIPAL ==============

class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.is_dark = True
        self.current_tab = "dashboard"
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
    
    def _setup_window(self):
        self.setWindowTitle("2LOCK - Automação NFS-e")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Remover borda padrão do Windows (opcional)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    
    def _setup_ui(self):
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # ===== SIDEBAR =====
        self.sidebar = GlassCard()
        self.sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(8)
        
        # Logo
        logo_layout = QHBoxLayout()
        
        logo_icon = QLabel("🔒")
        logo_icon.setStyleSheet("font-size: 28px;")
        
        logo_text = QLabel("2LOCK")
        self.logo_text = logo_text
        
        # Indicador online
        status_dot = QLabel("●")
        self.status_dot = status_dot
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addWidget(status_dot)
        logo_layout.addStretch()
        
        sidebar_layout.addLayout(logo_layout)
        sidebar_layout.addSpacing(32)
        
        # Navegação
        nav_label = QLabel("NAVEGAÇÃO")
        self.nav_label = nav_label
        sidebar_layout.addWidget(nav_label)
        sidebar_layout.addSpacing(8)
        
        # Botões de aba
        self.tab_buttons: dict[str, TabButton] = {}
        tabs = [
            ("dashboard", "📊", "Dashboard"),
            ("spreadsheet", "📋", "Planilha"),
            ("log", "📝", "Log"),
            ("history", "🕐", "Histórico"),
            ("user", "👤", "Usuário"),
        ]
        
        for tab_id, icon, label in tabs:
            btn = TabButton(icon, label)
            btn.clicked.connect(lambda checked, t=tab_id: self._switch_tab(t))
            self.tab_buttons[tab_id] = btn
            sidebar_layout.addWidget(btn)
        
        self.tab_buttons["dashboard"].set_active(True)
        
        sidebar_layout.addStretch()
        
        # Card de estatísticas na sidebar
        stats_card = GlassCard()
        self.sidebar_stats_card = stats_card
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(16, 16, 16, 16)
        
        stats_icon = QLabel("✅")
        stats_icon.setStyleSheet("font-size: 24px;")
        
        stats_title = QLabel("Taxa de sucesso")
        self.stats_title = stats_title
        
        stats_value = QLabel("98.5%")
        self.stats_value = stats_value
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(98)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        
        stats_layout.addWidget(stats_icon)
        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(stats_value)
        stats_layout.addWidget(self.progress_bar)
        
        sidebar_layout.addWidget(stats_card)
        
        # ===== CONTEÚDO PRINCIPAL =====
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.page_title = QLabel("Dashboard")
        self.page_subtitle = QLabel("Gerencie suas automações de NFS-e")
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(self.page_title)
        title_layout.addWidget(self.page_subtitle)
        
        # Botões do header
        self.theme_btn = IconButton("🌙")
        self.theme_btn.clicked.connect(self._toggle_theme)
        
        self.close_btn = IconButton("✕")
        self.close_btn.clicked.connect(self.close)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        header_layout.addWidget(self.close_btn)
        
        # Stack de conteúdo
        self.content_stack = QStackedWidget()
        
        self.dashboard_widget = DashboardWidget()
        self.spreadsheet_widget = SpreadsheetWidget()
        self.log_widget = LogWidget()
        self.history_widget = HistoryWidget()
        self.user_widget = UserWidget()
        
        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.spreadsheet_widget)
        self.content_stack.addWidget(self.log_widget)
        self.content_stack.addWidget(self.history_widget)
        self.content_stack.addWidget(self.user_widget)
        
        content_layout.addWidget(header)
        content_layout.addWidget(self.content_stack)
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_area)
        
        self._update_theme()
    
    def _connect_signals(self):
        self.dashboard_widget.file_selected.connect(self._on_file_selected)
        self.dashboard_widget.process_clicked.connect(self._on_process)
    
    def _switch_tab(self, tab_id: str):
        # Atualizar botões
        for tid, btn in self.tab_buttons.items():
            btn.set_active(tid == tab_id)
        
        # Atualizar conteúdo
        tab_indices = {
            "dashboard": 0,
            "spreadsheet": 1,
            "log": 2,
            "history": 3,
            "user": 4,
        }
        
        tab_titles = {
            "dashboard": ("Dashboard", "Gerencie suas automações de NFS-e"),
            "spreadsheet": ("Planilha", "Visualize os dados da planilha importada"),
            "log": ("Log de Execução", "Acompanhe o processamento em tempo real"),
            "history": ("Histórico", "Veja todos os processamentos realizados"),
            "user": ("Meu Perfil", "Gerencie suas informações de usuário"),
        }
        
        self.content_stack.setCurrentIndex(tab_indices[tab_id])
        title, subtitle = tab_titles[tab_id]
        self.page_title.setText(title)
        self.page_subtitle.setText(subtitle)
        self.current_tab = tab_id
    
    def _toggle_theme(self):
        self.is_dark = not self.is_dark
        self.theme_btn.setText("☀️" if self.is_dark else "🌙")
        self._update_theme()
    
    def _update_theme(self):
        theme = Theme.get_dark_theme() if self.is_dark else Theme.get_light_theme()
        
        # Estilo global
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {theme['background']},
                    stop: 0.5 {theme['background_secondary']},
                    stop: 1 {theme['background']}
                );
            }}
            QWidget {{
                color: {theme['foreground']};
            }}
        """)
        
        # Sidebar
        self.sidebar.set_theme(self.is_dark)
        self.logo_text.setStyleSheet(f"color: {theme['foreground']}; font-size: 24px; font-weight: 700;")
        self.status_dot.setStyleSheet(f"color: {theme['success']}; font-size: 10px;")
        self.nav_label.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 11px; font-weight: 600;")
        
        # Sidebar stats
        self.sidebar_stats_card.set_theme(self.is_dark)
        self.stats_title.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 13px;")
        self.stats_value.setStyleSheet(f"color: {theme['success']}; font-size: 24px; font-weight: 700;")
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {theme['glass_bg']};
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {theme['success']},
                    stop: 1 {theme['primary']}
                );
                border-radius: 4px;
            }}
        """)
        
        # Header
        self.page_title.setStyleSheet(f"color: {theme['foreground']}; font-size: 28px; font-weight: 700;")
        self.page_subtitle.setStyleSheet(f"color: {theme['foreground_secondary']}; font-size: 14px;")
        
        # Botões
        for btn in self.tab_buttons.values():
            btn.set_theme(self.is_dark)
        
        self.theme_btn.set_theme(self.is_dark)
        self.close_btn.set_theme(self.is_dark)
        
        # Widgets de conteúdo
        self.dashboard_widget.set_theme(self.is_dark)
        self.spreadsheet_widget.set_theme(self.is_dark)
        self.log_widget.set_theme(self.is_dark)
        self.history_widget.set_theme(self.is_dark)
        self.user_widget.set_theme(self.is_dark)
    
    def _on_file_selected(self, file_path: str):
        file_name = os.path.basename(file_path)
        self.log_widget.add_log(f"Arquivo selecionado: {file_name}", LogType.INFO)
    
    def _on_process(self):
        if not self.dashboard_widget.selected_file:
            return
        
        file_name = os.path.basename(self.dashboard_widget.selected_file)
        self.log_widget.add_log(f"Iniciando processamento de: {file_name}", LogType.INFO)
        
        # Simular processamento
        QTimer.singleShot(500, lambda: self.log_widget.add_log("Lendo arquivo Excel...", LogType.INFO))
        QTimer.singleShot(1000, lambda: self.log_widget.add_log("Validando dados...", LogType.INFO))
        QTimer.singleShot(1500, lambda: self.log_widget.add_log("Processando 150 registros...", LogType.INFO))
        QTimer.singleShot(2500, lambda: self._finish_processing(file_name))
    
    def _finish_processing(self, file_name: str):
        self.log_widget.add_log("Processamento concluído com sucesso!", LogType.SUCCESS)
        self.history_widget.add_entry(file_name, 150, "Sucesso", "2m 34s")
        
        QMessageBox.information(
            self,
            "Processamento Concluído",
            f"O arquivo {file_name} foi processado com sucesso!\n\n"
            "150 registros processados em 2m 34s."
        )


# ============== MAIN ==============

def main():
    # Habilitar DPI alto
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Configurar fonte padrão
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Criar e mostrar janela
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
