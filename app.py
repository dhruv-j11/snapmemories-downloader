# for main ui

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QProgressBar, QFileDialog,
                             QMessageBox, QFrame)
from PyQt6.QtCore import QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, Qt, QTimer
from PyQt6.QtGui import QFont
from controller import run

# Color theme
NEON_YELLOW = "#ffd9fc"
DARK_BG = "#1a1a1a"
DARKER_BG = "#0f0f0f"
LIGHT_TEXT = "#ffffff"
MEDIUM_TEXT = "#b0b0b0"
ACCENT_HOVER = "#FFD700"

# Font configuration - change this to your preferred font
# Popular options: "SF Pro Display", "Helvetica Neue", "Arial", "Segoe UI", "Roboto"
APP_FONT_FAMILY = "Helvetica Neue"  # macOS default, falls back to system default if not available

class ToastMessage(QLabel):
    """Toast notification widget with fade animation"""
    def __init__(self, message, parent=None):
        super().__init__(message, parent)
        self.setStyleSheet(f"""
            background-color: {NEON_YELLOW};
            color: {DARK_BG};
            padding: 12px 20px;
            border-radius: 8px;
            font-family: "{APP_FONT_FAMILY}";
            font-weight: bold;
            font-size: 14px;
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(50)
        
        # Fade in animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def showEvent(self, event):
        super().showEvent(event)
        self.fade_animation.start()

class DownloadThread(QThread):
    progress_updated = pyqtSignal(int, int)
    finished_signal = pyqtSignal()
    
    def __init__(self, json_file, output_dir):
        super().__init__()
        self.json_file = json_file
        self.output_dir = output_dir
    
    def run(self):
        def progress_cb(done, total):
            self.progress_updated.emit(done, total)
        run(self.json_file, self.output_dir, progress_cb)
        self.finished_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snapchat Memory Downloader")
        self.setGeometry(100, 100, 600, 400)
        
        # Apply dark theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {DARK_BG};
                font-family: "{APP_FONT_FAMILY}";
            }}
            QLabel {{
                color: {LIGHT_TEXT};
                font-size: 13px;
            }}
            QLineEdit {{
                background-color: {DARKER_BG};
                color: {LIGHT_TEXT};
                border: 2px solid #333333;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 2px solid {NEON_YELLOW};
            }}
            QPushButton {{
                background-color: {NEON_YELLOW};
                color: {DARK_BG};
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #CCB800;
            }}
            QPushButton:disabled {{
                background-color: #666666;
                color: #999999;
            }}
            QProgressBar {{
                border: 2px solid #333333;
                border-radius: 8px;
                text-align: center;
                background-color: {DARKER_BG};
                color: {LIGHT_TEXT};
                font-weight: bold;
                font-size: 12px;
                height: 30px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {NEON_YELLOW}, stop:1 {ACCENT_HOVER});
                border-radius: 6px;
            }}
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Snapchat Memory Downloader")
        title_font = QFont(APP_FONT_FAMILY, 32, QFont.Weight.Bold)
        title_font.setStyleHint(QFont.StyleHint.SansSerif)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {NEON_YELLOW}; margin-bottom: 10px; font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: #333333; max-height: 1px;")
        main_layout.addWidget(separator)
        
        # JSON file selection
        json_label = QLabel("📄 Snapchat JSON File:")
        json_label.setStyleSheet(f"color: {LIGHT_TEXT}; font-weight: bold; font-size: 14px;")
        main_layout.addWidget(json_label)
        
        json_layout = QHBoxLayout()
        json_layout.setSpacing(10)
        self.json_entry = QLineEdit()
        self.json_entry.setPlaceholderText("Select your Snapchat JSON export file...")
        json_layout.addWidget(self.json_entry, 3)
        
        self.json_btn = QPushButton("Browse")
        self.json_btn.clicked.connect(self.pick_json)
        json_layout.addWidget(self.json_btn, 1)
        main_layout.addLayout(json_layout)
        
        # Output folder selection
        output_label = QLabel("📁 Output Folder:")
        output_label.setStyleSheet(f"color: {LIGHT_TEXT}; font-weight: bold; font-size: 14px;")
        main_layout.addWidget(output_label)
        
        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)
        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("Select where to save your memories...")
        output_layout.addWidget(self.output_entry, 3)
        
        self.output_btn = QPushButton("Browse")
        self.output_btn.clicked.connect(self.pick_output)
        output_layout.addWidget(self.output_btn, 1)
        main_layout.addLayout(output_layout)
        
        # Progress bar
        self.progress_label = QLabel("Ready to download")
        self.progress_label.setStyleSheet(f"color: {MEDIUM_TEXT}; font-size: 12px;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.progress_label)
        
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFormat("%p%")
        main_layout.addWidget(self.progress)
        
        # Start button
        self.start_btn = QPushButton("Begin Download")
        self.start_btn.clicked.connect(self.start_download)
        self.start_btn.setMinimumHeight(50)
        main_layout.addWidget(self.start_btn)
        
        main_layout.addStretch()
        
        self.download_thread = None
        
        # Button hover animations
        self.setup_button_animations()
        
        # Fade in window animation
        self.setWindowOpacity(0.0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(400)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        QTimer.singleShot(50, self.fade_in_animation.start)
    
    def setup_button_animations(self):
        """Add subtle scale animation on button hover"""
        for btn in [self.json_btn, self.output_btn, self.start_btn]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def pick_json(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Snapchat JSON", "", "JSON Files (*.json)")
        if filename:
            self.json_entry.setText(filename)
            self.show_toast("JSON file selected!")
    
    def pick_output(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if directory:
            self.output_entry.setText(directory)
            self.show_toast("Output folder selected!")
    
    def show_toast(self, message):
        """Show a toast notification"""
        toast = ToastMessage(message, self)
        toast.setFixedWidth(350)
        
        # Position toast at bottom center
        def position_toast():
            parent_geometry = self.geometry()
            toast_x = parent_geometry.x() + (parent_geometry.width() - 350) // 2
            toast_y = parent_geometry.y() + parent_geometry.height() - 80
            toast.move(toast_x, toast_y)
            toast.raise_()
            toast.show()
        
        # Position after layout is complete
        QTimer.singleShot(10, position_toast)
        QTimer.singleShot(2000, lambda: self.fade_out_toast(toast))
    
    def fade_out_toast(self, toast):
        """Fade out toast before removing"""
        fade_out = QPropertyAnimation(toast, b"windowOpacity")
        fade_out.setDuration(300)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.finished.connect(toast.deleteLater)
        fade_out.start()
    
    def start_download(self):
        json_file = self.json_entry.text()
        output_dir = self.output_entry.text()
        
        if not json_file or not output_dir:
            QMessageBox.warning(self, "Missing Information", 
                              "Please select both a JSON file and an output folder.")
            return
        
        self.start_btn.setEnabled(False)
        self.json_btn.setEnabled(False)
        self.output_btn.setEnabled(False)
        self.progress.setValue(0)
        self.progress_label.setText("Downloading memories...")
        self.show_toast("Download started! 🎉")
        
        self.download_thread = DownloadThread(json_file, output_dir)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_complete)
        self.download_thread.start()
    
    def update_progress(self, done, total):
        if total > 0:
            percent = int((done / total) * 100)
            self.progress.setValue(percent)
            self.progress_label.setText(f"Downloading... {done}/{total} files ({percent}%)")
    
    def download_complete(self):
        self.start_btn.setEnabled(True)
        self.json_btn.setEnabled(True)
        self.output_btn.setEnabled(True)
        self.progress_label.setText("Download complete! ✅")
        
        # Show completion message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Download Complete!")
        msg.setText("Your Memories Have Been Uploaded Into The Directed File.\n\nPlease review the report (CSV file generated) to ensure all files were successfully uploaded.")
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {DARK_BG};
                color: {LIGHT_TEXT};
                font-family: "{APP_FONT_FAMILY}";
            }}
            QMessageBox QLabel {{
                color: {LIGHT_TEXT};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {NEON_YELLOW};
                color: {DARK_BG};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_HOVER};
            }}
        """)
        msg.exec()
        self.show_toast("All done! 🎊")

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Apply custom font to entire application
    app_font = QFont(APP_FONT_FAMILY)
    app_font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(app_font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
