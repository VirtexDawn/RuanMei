import os
import sys

from dotenv import load_dotenv
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    CardWidget,
    ComboBox,
    FluentIcon,
    IconWidget,
    NavigationInterface,
    NavigationItemPosition,
    PrimaryPushButton,
    SettingCard,
    SettingCardGroup,
    SmoothScrollArea,
    SubtitleLabel,
    SwitchSettingCard,
    Theme,
    TitleLabel,
    TransparentToolButton,
    setTheme,
)

load_dotenv()
AppName = os.getenv("APPNAME", "RuanMei App")


class AnimatedHoverCard(CardWidget):
    """A premium mockup card with soft glow"""

    def __init__(self, accent="#7ad8ff", radius=18):
        super().__init__()
        self.accent = accent
        self.radius = radius
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: rgba(15, 18, 24, 0.80);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: {radius}px;
            }}
            """
        )

        self.glow_layer = QFrame(self)
        self.glow_layer.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.glow_layer.setStyleSheet(
            f"""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 rgba(255,255,255,0.18),
                stop: 0.25 rgba({self._to_rgba(accent, 0.32)}),
                stop: 1 rgba({self._to_rgba(accent, 0.04)})
            );
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: {radius}px;
            """
        )
        self.glow_layer.lower()

        self.glow_effect = QGraphicsOpacityEffect(self.glow_layer)
        self.glow_layer.setGraphicsEffect(self.glow_effect)
        self.glow_effect.setOpacity(0.12)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(12)
        self.shadow.setColor(QColor(0, 0, 0, 110))
        self.setGraphicsEffect(self.shadow)

        self.animation = QPropertyAnimation(self.glow_effect, b"opacity")
        self.animation.setDuration(220)

    @staticmethod
    def _to_rgba(hex_color: str, alpha: float) -> str:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(ch * 2 for ch in hex_color)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b},{int(alpha * 255)}"

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.glow_layer.resize(self.size())

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.glow_effect.opacity())
        self.animation.setEndValue(0.38)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.glow_effect.opacity())
        self.animation.setEndValue(0.12)
        self.animation.start()
        super().leaveEvent(event)


class MockHeroWidget(QWidget):
    def __init__(self, title: str, subtitle: str):
        super().__init__()
        self.setFixedHeight(176)
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(118, 165, 255, 0.16),
                    stop: 0.46 rgba(129, 121, 255, 0.09),
                    stop: 1 rgba(255, 255, 255, 0.03)
                );
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 28px;
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)

        top = QHBoxLayout()
        badge = QLabel("LIVE MOCKUP")
        badge.setStyleSheet(
            """
            color: #7ad8ff;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.6px;
            background: rgba(122, 216, 255, 0.10);
            border: 1px solid rgba(122, 216, 255, 0.25);
            border-radius: 999px;
            padding: 7px 12px;
            """
        )
        top.addWidget(badge)
        top.addStretch(1)
        top.addWidget(QLabel("Ambient preview"))
        layout.addLayout(top)

        title_label = TitleLabel(title)
        title_label.setStyleSheet("font-size: 26px; color: #f4f8ff;")
        layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            "color: rgba(230, 235, 245, 0.74); font-size: 12px;"
        )
        layout.addWidget(subtitle_label)

        pills = QHBoxLayout()
        for text, accent in [("Signals", "#7ad8ff"), ("Latency", "#7ef0b0"), ("Sync", "#ffcb6b")]:
            chip = QLabel(text)
            chip.setStyleSheet(
                f"""
                color: {accent};
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 999px;
                padding: 6px 10px;
                font-size: 10px;
                font-weight: 600;
                """
            )
            pills.addWidget(chip)
        pills.addStretch(1)
        layout.addLayout(pills)


class MockStatCard(AnimatedHoverCard):
    def __init__(self, label_text: str, value: str, accent="#7ad8ff"):
        super().__init__(accent=accent)
        self.setFixedHeight(120)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        label = SubtitleLabel(label_text)
        label.setStyleSheet("color: rgba(226, 231, 239, 0.78); font-size: 12px;")
        value_label = TitleLabel(value)
        value_label.setStyleSheet(f"color: {accent}; font-size: 30px;")

        layout.addWidget(label)
        layout.addWidget(value_label)
        layout.addStretch(1)


class MockServerCard(AnimatedHoverCard):
    def __init__(self, server_name: str, status: str):
        super().__init__(accent="#7ef0b0" if status == "Running" else "#ff7b7b")
        self.setFixedHeight(128)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 12)

        title = SubtitleLabel(server_name)
        title.setStyleSheet("font-size: 17px;")
        layout.addWidget(title)

        status_color = "#7ef0b0" if status == "Running" else "#ff7b7b"
        status_label = QLabel(f"Status: {status}")
        status_label.setStyleSheet(f"color: {status_color}; font-size: 12px; font-weight: 600;")
        layout.addWidget(status_label)

        button_layout = QHBoxLayout()
        for icon in (FluentIcon.PLAY, FluentIcon.SETTING, FluentIcon.DELETE):
            btn = TransparentToolButton(icon, self)
            btn.setStyleSheet(
                """
                TransparentToolButton {
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 10px;
                    min-width: 34px;
                    min-height: 34px;
                }
                """
            )
            button_layout.addWidget(btn)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(13, 17, 22, 0.96),
                    stop: 1 rgba(20, 24, 32, 0.96)
                );
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(22)

        layout.addWidget(MockHeroWidget("Home Overview", "Live system telemetry and service readiness preview"))

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(18)
        for label_text, val, accent in [
            ("Active Servers", "12", "#7ad8ff"),
            ("Total Requests", "1,420", "#8de7c9"),
            ("System Load", "34%", "#ffca6d"),
        ]:
            stats_layout.addWidget(MockStatCard(label_text, val, accent))
        layout.addLayout(stats_layout)

        content_card = AnimatedHoverCard(accent="#8e9dff")
        content_card.setFixedHeight(220)
        content_layout = QVBoxLayout(content_card)
        content_layout.setContentsMargins(18, 18, 18, 18)
        content_layout.setSpacing(10)
        content_layout.addWidget(SubtitleLabel("Recent Activity Log (Mockup)"))
        content_layout.addWidget(QLabel("[INFO] Server #1 initialized successfully."))
        content_layout.addWidget(QLabel("[INFO] Database sync completed without errors."))
        content_layout.addWidget(QLabel("[WARN] High latency detected on Node 3."))
        layout.addWidget(content_card)
        layout.addStretch(1)


class CreatePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(14, 17, 22, 0.96),
                    stop: 1 rgba(22, 24, 31, 0.96)
                );
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(22)
        layout.addWidget(MockHeroWidget("Create New Instance", "Prototype creation flow with ambient visual cues"))

        card = AnimatedHoverCard(accent="#7ad8ff")
        card.setFixedHeight(324)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)
        card_layout.addWidget(SubtitleLabel("Server Details"))

        for label_text in ["Server Name:", "Target Environment / Port:"]:
            label = QLabel(label_text)
            label.setStyleSheet("color: rgba(232,235,240,0.80); font-size: 12px;")
            card_layout.addWidget(label)
            field = QLineEdit()
            field.setStyleSheet(
                """
                QLineEdit {
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px;
                    padding: 10px 12px;
                    color: #f1f5ff;
                }
                """
            )
            card_layout.addWidget(field)

        btn_create = PrimaryPushButton("Create Server")
        btn_create.setStyleSheet(
            """
            PrimaryPushButton {
                background-color: rgba(122, 216, 255, 0.18);
                border: 1px solid rgba(122, 216, 255, 0.40);
                border-radius: 12px;
                min-height: 36px;
            }
            """
        )
        card_layout.addWidget(btn_create, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(card)
        layout.addStretch(1)


class DatabasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(12, 16, 21, 0.96),
                    stop: 1 rgba(20, 24, 31, 0.96)
                );
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(22)
        layout.addWidget(MockHeroWidget("Database Overview", "Preview of records, storage capacity and sync health"))

        card = AnimatedHoverCard(accent="#8de7c9")
        card.setFixedHeight(220)
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(18, 18, 18, 18)
        c_layout.setSpacing(10)
        c_layout.addWidget(SubtitleLabel("Records & Storage (Mockup)"))
        c_layout.addWidget(QLabel("Tabel data SQLite / Database Record placeholder."))
        c_layout.addWidget(QLabel("• total_users: 2,491 records\n• app_logs: 18,302 records\n• session_cache: Active"))
        layout.addWidget(card)
        layout.addStretch(1)


class ConfigurationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(16, 17, 25, 0.96),
                    stop: 1 rgba(21, 23, 31, 0.96)
                );
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(22)
        layout.addWidget(MockHeroWidget("Global Configurations", "Environment layout mockup for backend runtime settings"))

        card = AnimatedHoverCard(accent="#ffca6d")
        card.setFixedHeight(220)
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(18, 18, 18, 18)
        c_layout.addWidget(SubtitleLabel("Environment Variables (Mockup)"))
        c_layout.addWidget(QLabel("Pengaturan global runtime environment dan API endpoints."))
        layout.addWidget(card)
        layout.addStretch(1)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(13, 15, 20, 0.97),
                    stop: 1 rgba(23, 27, 34, 0.97)
                );
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)

        scroll = SmoothScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        c_layout = QVBoxLayout(container)
        c_layout.setSpacing(18)
        c_layout.setContentsMargins(0, 0, 0, 0)

        c_layout.addWidget(MockHeroWidget("Settings", "Appearance and system preferences mock preview"))

        group_app = SettingCardGroup("Application Settings", container)
        group_app.setStyleSheet(
            """
            SettingCardGroup {
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                background: rgba(255,255,255,0.02);
            }
            """
        )

        dark_mode_card = SwitchSettingCard(
            FluentIcon.BRUSH,
            "Dark Theme",
            "Use a refined dark mode with a polished Windows-inspired finish",
            parent=group_app,
        )
        dark_mode_card.setChecked(True)
        dark_mode_card.setStyleSheet("SwitchSettingCard { background: transparent; }")

        telemetry_card = SwitchSettingCard(
            FluentIcon.INFO,
            "Anonymous Telemetry",
            "Share anonymous diagnostics to help tune the experience",
            parent=group_app,
        )
        telemetry_card.setStyleSheet("SwitchSettingCard { background: transparent; }")

        group_app.addSettingCard(dark_mode_card)
        group_app.addSettingCard(telemetry_card)
        c_layout.addWidget(group_app)

        group_net = SettingCardGroup("Network & Storage", container)
        port_card = SettingCard(
            icon=FluentIcon.GLOBE,
            title="Default Listening Port",
            content="Choose the default backend service port",
            parent=group_net,
        )
        self.port_combo = ComboBox(port_card)
        self.port_combo.addItems(["80", "8080", "3000", "8501"])
        self.port_combo.setCurrentIndex(0)
        self.port_combo.setStyleSheet(
            """
            ComboBox {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 10px;
                padding: 4px 8px;
                min-width: 110px;
            }
            """
        )
        port_card.hBoxLayout.addWidget(self.port_combo, 0)
        port_card.hBoxLayout.addSpacing(16)
        group_net.addSettingCard(port_card)
        c_layout.addWidget(group_net)
        c_layout.addStretch(1)

        scroll.setWidget(container)
        layout.addWidget(scroll)


class UICoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(str(AppName))
        self.resize(1150, 720)
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #090b10,
                    stop: 0.5 #12161d,
                    stop: 1 #0d1118
                );
            }
            """
        )

        setTheme(Theme.DARK)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(16)

        top_bar = QFrame()
        top_bar.setFixedHeight(72)
        top_bar.setStyleSheet(
            """
            QFrame {
                background: rgba(20, 23, 30, 0.82);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
            }
            """
        )

        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(22, 0, 22, 0)

        logo_icon = IconWidget(FluentIcon.CODE)
        logo_icon.setFixedSize(22, 22)
        app_title = SubtitleLabel(str(AppName))
        app_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f2f7ff;")

        top_bar_layout.addWidget(logo_icon)
        top_bar_layout.addWidget(app_title)
        top_bar_layout.addStretch(1)

        root_layout.addWidget(top_bar)

        body_widget = QWidget()
        body_widget.setStyleSheet(
            """
            QWidget {
                background: rgba(255,255,255,0.025);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 26px;
            }
            """
        )
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(16)

        self.left_nav = NavigationInterface(self, showMenuButton=False, showReturnButton=False)
        self.left_nav.setFixedWidth(212)
        self.left_nav.setStyleSheet(
            """
            NavigationInterface {
                background: rgba(17, 20, 26, 0.90);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
            }
            """
        )

        self.stack_widget = QStackedWidget()
        self.stack_widget.setStyleSheet("background: transparent;")

        self.page_home = HomePage()
        self.page_create = CreatePage()
        self.page_db = DatabasePage()
        self.page_config = ConfigurationsPage()
        self.page_settings = SettingsPage()

        self.stack_widget.addWidget(self.page_home)
        self.stack_widget.addWidget(self.page_create)
        self.stack_widget.addWidget(self.page_db)
        self.stack_widget.addWidget(self.page_config)
        self.stack_widget.addWidget(self.page_settings)

        self.left_nav.addItem(
            routeKey="home",
            icon=FluentIcon.HOME,
            text="Home",
            onClick=lambda: self.stack_widget.setCurrentWidget(self.page_home),
        )
        self.left_nav.addItem(
            routeKey="create",
            icon=FluentIcon.ADD,
            text="Create",
            onClick=lambda: self.stack_widget.setCurrentWidget(self.page_create),
        )
        self.left_nav.addItem(
            routeKey="database",
            icon=FluentIcon.FOLDER,
            text="Database",
            onClick=lambda: self.stack_widget.setCurrentWidget(self.page_db),
        )
        self.left_nav.addItem(
            routeKey="configurations",
            icon=FluentIcon.DEVELOPER_TOOLS,
            text="Configurations",
            onClick=lambda: self.stack_widget.setCurrentWidget(self.page_config),
        )
        self.left_nav.addItem(
            routeKey="settings",
            icon=FluentIcon.SETTING,
            text="Settings",
            onClick=lambda: self.stack_widget.setCurrentWidget(self.page_settings),
            position=NavigationItemPosition.BOTTOM,
        )

        body_layout.addWidget(self.left_nav)

        center_widget = QWidget()
        center_widget.setStyleSheet(
            """
            QWidget {
                background: rgba(17, 21, 28, 0.82);
                border: 1px solid rgba(255,255,255,0.04);
                border-radius: 22px;
            }
            """
        )
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(10, 10, 10, 10)
        center_layout.setSpacing(0)

        controls_bar = QHBoxLayout()
        controls_bar.setContentsMargins(10, 6, 10, 6)
        self.btn_toggle_left = TransparentToolButton(FluentIcon.CHEVRON_RIGHT, self)
        self.btn_toggle_left.clicked.connect(self.toggle_left_sidebar)
        self.btn_toggle_right = TransparentToolButton(FluentIcon.CHEVRON_RIGHT, self)
        self.btn_toggle_right.clicked.connect(self.toggle_right_sidebar)

        controls_bar.addWidget(self.btn_toggle_left)
        controls_bar.addStretch(1)
        controls_bar.addWidget(self.btn_toggle_right)

        center_layout.addLayout(controls_bar)
        center_layout.addWidget(self.stack_widget, stretch=1)
        body_layout.addWidget(center_widget, stretch=1)

        self.right_sidebar = QFrame()
        self.right_sidebar.setFixedWidth(310)
        self.right_sidebar.setStyleSheet(
            """
            QFrame {
                background: rgba(20, 23, 30, 0.90);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 22px;
            }
            """
        )

        right_layout = QVBoxLayout(self.right_sidebar)
        right_layout.setContentsMargins(14, 14, 14, 14)
        right_layout.setSpacing(14)

        sidebar_title = SubtitleLabel("Servers")
        sidebar_title.setStyleSheet("font-size: 18px; font-weight: 700;")
        right_layout.addWidget(sidebar_title)

        right_scroll = SmoothScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setStyleSheet("border: none; background: transparent;")

        right_scroll_content = QWidget()
        right_scroll_content.setStyleSheet("background: transparent;")
        right_scroll_layout = QVBoxLayout(right_scroll_content)
        right_scroll_layout.setContentsMargins(0, 0, 0, 0)
        right_scroll_layout.setSpacing(12)
        right_scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for i in range(1, 6):
            server_card = MockServerCard(
                server_name=f"Server #{i}",
                status="Running" if i % 2 != 0 else "Stopped",
            )
            right_scroll_layout.addWidget(server_card)

        right_scroll.setWidget(right_scroll_content)
        right_layout.addWidget(right_scroll)

        body_layout.addWidget(self.right_sidebar)
        root_layout.addWidget(body_widget)

    def toggle_left_sidebar(self):
        is_visible = self.left_nav.isVisible()
        self.left_nav.setVisible(not is_visible)
        self.btn_toggle_left.setIcon(
            FluentIcon.CHEVRON_RIGHT if is_visible else FluentIcon.CHEVRON_RIGHT_MED
        )

    def toggle_right_sidebar(self):
        is_visible = self.right_sidebar.isVisible()
        self.right_sidebar.setVisible(not is_visible)
        self.btn_toggle_right.setIcon(
            FluentIcon.CHEVRON_RIGHT_MED if is_visible else FluentIcon.CHEVRON_RIGHT
        )


def CreateApp():
    app = QApplication(sys.argv)
    window = UICoreWindow()
    window.show()
    sys.exit(app.exec())
