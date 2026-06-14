#!/usr/bin/env python3
"""Whisper My Idea Pro v2 — Entry Point"""
import sys
import ctypes
from pathlib import Path

# Keep PC awake
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("Whisper My Idea Pro")
    app.setApplicationVersion("2.0")
    
    # Load Inter font if available
    from PySide6.QtGui import QFontDatabase
    QFontDatabase.addApplicationFont("C:/Windows/Fonts/segui.ttf")
    
    win = MainWindow()
    win.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()