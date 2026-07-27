import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, 
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QComboBox, QFormLayout, QGroupBox,
    QCheckBox, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Content Publisher Pro v2.0")
        self.resize(1100, 750)
        
        self.apply_theme()
        self.init_ui()

    def apply_theme(self):
        self.setStyleSheet('''
            QMainWindow, QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 13px;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
                background: #1e293b;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #1e293b;
                color: #94a3b8;
                padding: 10px 22px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #0284c7;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                font-weight: bold;
                border: none;
                padding: 10px 18px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0369a1;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px;
                color: #f8fafc;
            }
            QGroupBox {
                border: 1px solid #334155;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #38bdf8;
            }
        ''')

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self.create_generator_tab(), "🤖 Генерация Контента")
        self.tabs.addTab(self.create_publisher_tab(), "🚀 Публикация & Мультипостинг")
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Настройки & API")
        self.tabs.addTab(self.create_logs_tab(), "📋 Монитор Логов")

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Система готова к работе")

    def create_generator_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        form = QFormLayout()
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Например: Лучшие стратегии арбитража трафика 2026")
        
        self.ai_model_select = QComboBox()
        self.ai_model_select.addItems(["Google Gemini Pro", "OpenAI GPT-4o", "Claude 3.5 Sonnet"])
        
        self.content_type = QComboBox()
        self.content_type.addItems(["SEO Статья (Longread)", "Пост для Telegram", "Статья VC.ru / Medium / Teletype"])

        form.addRow("Тема / Ключевые слова:", self.topic_input)
        form.addRow("ИИ Модель:", self.ai_model_select)
        form.addRow("Формат контента:", self.content_type)
        layout.addLayout(form)

        layout.addWidget(QLabel("Предпросмотр и редактор контента:"))
        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText("Здесь появится сгенерированный текст...")
        layout.addWidget(self.result_text)

        btn_generate = QPushButton("✨ Сгенерировать контент")
        btn_generate.clicked.connect(self.on_generate)
        layout.addWidget(btn_generate)

        return tab

    def create_publisher_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Выбор площадок для автопостинга")
        g_layout = QVBoxLayout(group)

        self.chk_tg = QCheckBox("Telegram Канал")
        self.chk_blogger = QCheckBox("Blogger.com")
        self.chk_wp = QCheckBox("WordPress Сайт")
        self.chk_medium = QCheckBox("Medium / VC.ru / Teletype")

        g_layout.addWidget(self.chk_tg)
        g_layout.addWidget(self.chk_blogger)
        g_layout.addWidget(self.chk_wp)
        g_layout.addWidget(self.chk_medium)

        layout.addWidget(group)

        btn_publish = QPushButton("🚀 Опубликовать во все выбранные каналы")
        btn_publish.clicked.connect(self.on_publish)
        layout.addWidget(btn_publish)

        layout.addStretch()
        return tab

    def create_settings_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)

        self.api_gemini = QLineEdit()
        self.api_gemini.setEchoMode(QLineEdit.EchoMode.Password)

        self.tg_bot_token = QLineEdit()
        self.tg_bot_token.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Gemini API Key:", self.api_gemini)
        layout.addRow("Telegram Bot Token:", self.tg_bot_token)

        btn_save = QPushButton("💾 Сохранить конфигурацию")
        btn_save.clicked.connect(lambda: QMessageBox.information(self, "Успех", "Настройки сохранены!"))
        layout.addRow(btn_save)

        return tab

    def create_logs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.append("[INFO] Система успешно инициализирована.")

        layout.addWidget(self.log_output)
        return tab

    def on_generate(self):
        topic = self.topic_input.text()
        if not topic:
            QMessageBox.warning(self, "Ошибка", "Введите тему!")
            return
        self.statusBar.showMessage("Генерация...")
        self.result_text.setText(f"# {topic}\n\n[Сгенерированный текст будет отображен здесь...]")
        self.statusBar.showMessage("Завершено", 5000)

    def on_publish(self):
        QMessageBox.information(self, "Публикация", "Запрос на публикацию отправлен!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
