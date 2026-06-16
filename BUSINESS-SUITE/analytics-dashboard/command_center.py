#!/usr/bin/env python3
"""Command Center — Unified Business Dashboard.

A polished local command center for the Titus Banks business suite.
It connects to the shared API at http://127.0.0.1:19200 and shows CRM,
content, academy, and system status in one desktop cockpit.
"""
import ctypes
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
except Exception:
    pass

API = os.getenv("BUSINESS_SUITE_API", "http://127.0.0.1:19200")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKSPACE_ROOT = os.path.abspath(os.path.join(ROOT, ".."))
GATEWAY_SCRIPT = os.path.join(WORKSPACE_ROOT, "run_gateway.py")
DOCFLOW_EXE = os.path.join(WORKSPACE_ROOT, "DOCFLOW", "dist", "DocFlow", "DocFlow.exe")
AI_OS_BRAIN_URL = os.getenv("AI_OS_BRAIN_URL", "http://127.0.0.1:8765")
AI_TUTOR_SCRIPT = os.path.join(WORKSPACE_ROOT, "FLOATING-AI-TUTOR", "src", "main.py")
TELEGRAM_BOT_URL = os.getenv("TELEGRAM_BOT_URL", "https://t.me/Bankshez_bot")


def api_get(path: str) -> dict:
    try:
        with urllib.request.urlopen(f"{API}{path}", timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return {}


class CommandCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Titus Command Center")
        self.setMinimumSize(1180, 760)
        self.stat_widgets = {}
        self.service_widgets = {}
        self.setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(5000)
        self.refresh()

    def setup_ui(self):
        self.setStyleSheet(STYLES)
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self.build_sidebar())

        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(24, 22, 24, 18)
        main_layout.setSpacing(16)
        root.addWidget(main, 1)

        main_layout.addLayout(self.build_header())
        main_layout.addWidget(self.build_mission_panel())
        main_layout.addLayout(self.build_stats_grid())
        main_layout.addLayout(self.build_service_strip())
        main_layout.addWidget(self.build_tables())
        main_layout.addLayout(self.build_controls())

    def build_sidebar(self) -> QWidget:
        side = QFrame()
        side.setObjectName("sidebar")
        side.setFixedWidth(230)
        layout = QVBoxLayout(side)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(14)

        logo = QLabel("TB")
        logo.setObjectName("logo")
        logo.setFixedSize(48, 48)
        brand = QLabel("Titus OS")
        brand.setObjectName("brand")
        sub = QLabel("Command Center")
        sub.setObjectName("muted")

        layout.addWidget(logo)
        layout.addWidget(brand)
        layout.addWidget(sub)
        layout.addSpacing(14)

        nav_items = [
            "▣ Overview",
            "◎ CRM Pipeline",
            "✦ Content Ops",
            "◈ Academy",
            "⚙ System",
        ]
        for item in nav_items:
            label = QLabel(item)
            label.setObjectName("navItem")
            layout.addWidget(label)

        layout.addStretch()
        self.api_badge = QLabel("API: checking…")
        self.api_badge.setObjectName("apiBadge")
        layout.addWidget(self.api_badge)
        return side

    def build_header(self) -> QHBoxLayout:
        hdr = QHBoxLayout()
        title_wrap = QVBoxLayout()
        title = QLabel("Business Command Center")
        title.setObjectName("pageTitle")
        subtitle = QLabel("One cockpit for pipeline, content, learning, and system health.")
        subtitle.setObjectName("pageSubtitle")
        title_wrap.addWidget(title)
        title_wrap.addWidget(subtitle)
        hdr.addLayout(title_wrap)
        hdr.addStretch()

        self.clock_label = QLabel()
        self.clock_label.setObjectName("clock")
        hdr.addWidget(self.clock_label)
        return hdr

    def build_mission_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("missionPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(16)

        copy = QVBoxLayout()
        headline = QLabel("Today’s operating picture")
        headline.setObjectName("missionTitle")
        self.mission_text = QLabel("Waiting for the shared API server…")
        self.mission_text.setObjectName("missionText")
        self.mission_text.setWordWrap(True)
        copy.addWidget(headline)
        copy.addWidget(self.mission_text)
        layout.addLayout(copy, 1)

        self.status_label = QLabel("Checking connection")
        self.status_label.setObjectName("statusPill")
        layout.addWidget(self.status_label)
        return panel

    def build_stats_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(12)
        stats = [
            ("contacts", "Contacts", "👤", "CRM reach"),
            ("pipeline_value", "Pipeline", "💰", "Open deal value"),
            ("scheduled_content", "Content", "📝", "Scheduled posts"),
            ("active_courses", "Academy", "🎓", "Active courses"),
        ]
        for col, (key, label, icon, detail) in enumerate(stats):
            card, number = self.make_stat_card(icon, label, detail)
            grid.addWidget(card, 0, col)
            self.stat_widgets[key] = number
        return grid

    def make_stat_card(self, icon: str, label: str, detail: str):
        card = QFrame()
        card.setObjectName("statCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        top = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")
        name = QLabel(label)
        name.setObjectName("statName")
        top.addWidget(icon_label)
        top.addWidget(name)
        top.addStretch()
        number = QLabel("--")
        number.setObjectName("statNumber")
        caption = QLabel(detail)
        caption.setObjectName("muted")
        layout.addLayout(top)
        layout.addWidget(number)
        layout.addWidget(caption)
        return card, number

    def build_service_strip(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(10)
        services = [
            ("api", "Shared API"),
            ("crm", "CRM"),
            ("content", "Content"),
            ("academy", "Academy"),
            ("automation", "Automation"),
        ]
        for key, label in services:
            pill = QLabel(f"● {label}: checking")
            pill.setObjectName("servicePill")
            row.addWidget(pill)
            self.service_widgets[key] = pill
        row.addStretch()
        return row

    def build_tables(self) -> QWidget:
        split = QSplitter(Qt.Horizontal)
        split.setObjectName("tableSplit")

        activity_card = self.make_panel("Recent Activity")
        activity_layout = activity_card.layout()
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(3)
        self.activity_table.setHorizontalHeaderLabels(["Time", "Action", "Detail"])
        self.activity_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setAlternatingRowColors(True)
        activity_layout.addWidget(self.activity_table)
        split.addWidget(activity_card)

        pipeline_card = self.make_panel("Pipeline Breakdown")
        pipeline_layout = pipeline_card.layout()
        self.pipeline_table = QTableWidget()
        self.pipeline_table.setColumnCount(3)
        self.pipeline_table.setHorizontalHeaderLabels(["Stage", "Deals", "Value"])
        self.pipeline_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.pipeline_table.verticalHeader().setVisible(False)
        self.pipeline_table.setAlternatingRowColors(True)
        pipeline_layout.addWidget(self.pipeline_table)
        split.addWidget(pipeline_card)

        split.setSizes([680, 420])
        return split

    def make_panel(self, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("panel")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 14)
        heading = QLabel(title)
        heading.setObjectName("panelTitle")
        layout.addWidget(heading)
        return card

    def build_controls(self) -> QHBoxLayout:
        ctrl = QHBoxLayout()
        ctrl.setSpacing(10)
        buttons = [
            ("Refresh Now", self.refresh, "primary"),
            ("Start Gateway", self.start_gateway, "primary"),
            ("Stop Gateway", self.stop_gateway, ""),
            ("Open Telegram Bot", self.open_telegram_bot, ""),
            ("Open DocFlow", self.open_docflow, ""),
            ("Open AI OS Brain", self.open_ai_os_brain, "primary"),
            ("Open AI Tutor", self.open_ai_tutor, "primary"),
            ("Open Pipeline CRM", self.open_crm, ""),
            ("Open API", self.open_api, ""),
        ]
        for text, handler, obj in buttons:
            btn = QPushButton(text)
            if obj:
                btn.setObjectName(obj)
            btn.clicked.connect(handler)
            ctrl.addWidget(btn)
        ctrl.addStretch()
        self.last_refresh = QLabel("Not refreshed yet")
        self.last_refresh.setObjectName("muted")
        ctrl.addWidget(self.last_refresh)
        return ctrl

    def refresh(self):
        self.clock_label.setText(datetime.now().strftime("%a %I:%M %p"))
        data = api_get("/dashboard")
        now = datetime.now().strftime("%H:%M:%S")
        self.last_refresh.setText(f"Last refresh: {now}")

        if not data:
            self.status_label.setText("API offline")
            self.status_label.setProperty("state", "warn")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
            self.api_badge.setText("API: offline")
            self.mission_text.setText(
                f"Start the shared API server at {API}, then refresh. The dashboard shell is ready."
            )
            self.set_services(False, {})
            return

        activities = data.get("recent_activities", [])
        pipeline_value = data.get("pipeline_value", 0)
        self.status_label.setText("Live")
        self.status_label.setProperty("state", "ok")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.api_badge.setText("API: live")
        self.mission_text.setText(
            f"{len(activities)} recent activities tracked. Pipeline value is ${pipeline_value:,.0f}. "
            "Use this dashboard to decide the next business action."
        )
        self.set_services(True, data)
        self.update_stats(data)
        self.update_activity(activities)
        self.update_pipeline(data.get("pipeline_breakdown", []))

    def set_services(self, api_ok: bool, data: dict):
        states = {
            "api": api_ok,
            "crm": api_ok and data.get("contacts", 0) >= 0,
            "content": api_ok and data.get("scheduled_content", 0) >= 0,
            "academy": api_ok and data.get("active_courses", 0) >= 0,
            "automation": api_ok,
        }
        for key, ok in states.items():
            label = self.service_widgets[key]
            name = label.text().split(":")[0].replace("● ", "")
            label.setText(f"{'●' if ok else '○'} {name}: {'online' if ok else 'offline'}")
            label.setProperty("state", "ok" if ok else "warn")
            label.style().unpolish(label)
            label.style().polish(label)

    def update_stats(self, data: dict):
        self.stat_widgets["contacts"].setText(str(data.get("contacts", 0)))
        val = data.get("pipeline_value", 0)
        self.stat_widgets["pipeline_value"].setText(f"${val:,.0f}" if val else "$0")
        self.stat_widgets["scheduled_content"].setText(str(data.get("scheduled_content", 0)))
        self.stat_widgets["active_courses"].setText(str(data.get("active_courses", 0)))

    def update_activity(self, activities):
        self.activity_table.setRowCount(len(activities))
        for row, act in enumerate(activities):
            ts = act.get("created_at", "")
            time_text = ts[11:19] if ts else "--"
            self.activity_table.setItem(row, 0, QTableWidgetItem(time_text))
            self.activity_table.setItem(row, 1, QTableWidgetItem(act.get("action", "")))
            self.activity_table.setItem(row, 2, QTableWidgetItem(act.get("detail", "")[:90]))

    def update_pipeline(self, pipeline):
        self.pipeline_table.setRowCount(len(pipeline))
        for row, stage in enumerate(pipeline):
            self.pipeline_table.setItem(row, 0, QTableWidgetItem(stage.get("stage", "")))
            self.pipeline_table.setItem(row, 1, QTableWidgetItem(str(stage.get("count", 0))))
            self.pipeline_table.setItem(row, 2, QTableWidgetItem(f"${stage.get('value', 0):,.0f}"))

    def seed_data(self):
        result = api_get("/seed")
        if result.get("status") == "seeded":
            QMessageBox.information(
                self,
                "Seeded",
                f"Added {result.get('contacts', 0)} contacts and {result.get('content', 0)} content items.",
            )
            self.refresh()
        else:
            QMessageBox.warning(self, "API offline", "Could not seed data. Start the shared API server first.")

    def start_gateway(self):
        if not os.path.exists(GATEWAY_SCRIPT):
            QMessageBox.warning(self, "Gateway not found", f"Could not find:\n{GATEWAY_SCRIPT}")
            return
        try:
            subprocess.Popen(
                ["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", f"python '{GATEWAY_SCRIPT}'"],
                cwd=WORKSPACE_ROOT,
            )
            QMessageBox.information(self, "Gateway", "Gateway start command launched in a new PowerShell window.")
        except Exception as exc:
            QMessageBox.warning(self, "Gateway launch failed", str(exc))

    def stop_gateway(self):
        confirm = QMessageBox.question(
            self,
            "Stop Gateway",
            "Stop Python processes whose command line contains run_gateway.py or hermes_cli gateway?",
        )
        if confirm != QMessageBox.Yes:
            return
        command = (
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.CommandLine -match 'run_gateway.py|hermes_cli.*gateway' } | "
            "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        )
        try:
            subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command], check=False)
            QMessageBox.information(self, "Gateway", "Gateway stop command sent.")
        except Exception as exc:
            QMessageBox.warning(self, "Gateway stop failed", str(exc))

    def open_telegram_bot(self):
        QDesktopServices.openUrl(QUrl(TELEGRAM_BOT_URL))

    def open_docflow(self):
        if os.path.exists(DOCFLOW_EXE):
            try:
                subprocess.Popen([DOCFLOW_EXE], cwd=os.path.dirname(DOCFLOW_EXE))
                return
            except Exception as exc:
                QMessageBox.warning(self, "DocFlow launch failed", str(exc))
                return
        QMessageBox.warning(self, "DocFlow not found", f"Could not find:\n{DOCFLOW_EXE}")

    def open_crm(self):
        crm_path = os.path.join(ROOT, "crm", "pipeline_crm.py")
        if os.path.exists(crm_path):
            try:
                subprocess.Popen([sys.executable, crm_path], cwd=os.path.dirname(crm_path))
                return
            except Exception as exc:
                QMessageBox.warning(self, "CRM launch failed", str(exc))
                return
        QMessageBox.information(self, "Pipeline CRM", "CRM launcher not found. Open the Pipeline CRM shortcut manually.")

    def open_ai_os_brain(self):
        QDesktopServices.openUrl(QUrl(AI_OS_BRAIN_URL))

    def open_ai_tutor(self):
        if os.path.exists(AI_TUTOR_SCRIPT):
            try:
                subprocess.Popen([sys.executable, AI_TUTOR_SCRIPT], cwd=os.path.dirname(AI_TUTOR_SCRIPT))
                return
            except Exception as exc:
                QMessageBox.warning(self, "AI Tutor launch failed", str(exc))
                return
        QMessageBox.information(self, "AI Tutor", f"AI Tutor script not found at:\n{AI_TUTOR_SCRIPT}\n\nRun it manually from the FLOATING-AI-TUTOR folder.")

    def open_api(self):
        QDesktopServices.openUrl(QUrl(API))


STYLES = """
QMainWindow { background: #070a12; }
QWidget { color: #eef4ff; font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; }
#sidebar { background: #0b1020; border-right: 1px solid rgba(255,255,255,0.07); }
#logo {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #7c3aed, stop:0.5 #06b6d4, stop:1 #22c55e);
    border-radius: 14px; font-weight: 900; font-size: 18px; qproperty-alignment: AlignCenter;
}
#brand { font-size: 20px; font-weight: 800; letter-spacing: -0.4px; }
#pageTitle { font-size: 28px; font-weight: 850; letter-spacing: -0.8px; }
#pageSubtitle, #muted, .muted { color: #8792a8; }
#muted { color: #8792a8; }
#navItem { color: #b8c2d8; padding: 10px 12px; border-radius: 10px; background: rgba(255,255,255,0.025); }
#navItem:hover { background: rgba(99,102,241,0.18); color: #ffffff; }
#apiBadge, #clock { color: #9fb0cf; padding: 8px 10px; background: rgba(255,255,255,0.04); border-radius: 10px; }
#missionPanel, #statCard, #panel {
    background: rgba(15, 23, 42, 0.86);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 18px;
}
#missionPanel { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 rgba(30,41,59,0.95), stop:1 rgba(15,23,42,0.92)); }
#missionTitle { font-size: 16px; font-weight: 750; }
#missionText { color: #c7d2fe; line-height: 1.35; }
#statusPill, #servicePill {
    padding: 8px 12px; border-radius: 12px; background: rgba(148,163,184,0.08); color: #cbd5e1;
    border: 1px solid rgba(148,163,184,0.16);
}
#statusPill[state="ok"], #servicePill[state="ok"] { color: #86efac; border-color: rgba(34,197,94,0.35); background: rgba(22,163,74,0.10); }
#statusPill[state="warn"], #servicePill[state="warn"] { color: #fde68a; border-color: rgba(245,158,11,0.35); background: rgba(245,158,11,0.10); }
#statIcon { font-size: 18px; }
#statName { color: #aeb9cf; font-weight: 650; }
#statNumber { font-size: 34px; font-weight: 900; color: #93c5fd; letter-spacing: -1px; }
#panelTitle { font-size: 14px; font-weight: 800; color: #e2e8f0; padding-bottom: 6px; }
QTableWidget {
    background: #0a0f1d; border: 1px solid rgba(148,163,184,0.10); border-radius: 12px;
    gridline-color: rgba(148,163,184,0.08); alternate-background-color: rgba(255,255,255,0.018);
    selection-background-color: rgba(99,102,241,0.35);
}
QHeaderView::section { background: #111827; color: #93a4bd; padding: 9px; border: none; font-weight: 750; }
QPushButton {
    background: rgba(30,41,59,0.92); border: 1px solid rgba(148,163,184,0.18); border-radius: 12px;
    padding: 10px 16px; color: #dbeafe; font-weight: 700;
}
QPushButton:hover { background: rgba(51,65,85,0.95); border-color: #60a5fa; }
QPushButton#primary { background: #4f46e5; border-color: #6366f1; color: white; }
QSplitter::handle { background: transparent; width: 10px; }
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = CommandCenter()
    win.show()
    sys.exit(app.exec())
