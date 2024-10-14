import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, 
                             QFileDialog, QComboBox, QLabel, QGroupBox, QGridLayout, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt

from utils.sevenzip import SevenZip

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("7-Zip GUI")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.sevenzip = SevenZip()

    def setup_ui(self):
        # File/Directory selection
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select file or directory")
        self.file_button = QPushButton("Browse File")
        self.file_button.clicked.connect(self.browse_file)
        self.dir_button = QPushButton("Browse Directory")
        self.dir_button.clicked.connect(self.browse_directory)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.dir_button)
        self.layout.addLayout(file_layout)

        # Options
        options_group = QGroupBox("Compression Options")
        options_layout = QGridLayout()
        options_group.setLayout(options_layout)

        # Archive format
        options_layout.addWidget(QLabel("Archive format:"), 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["7z", "zip", "gzip", "bzip2", "tar"])
        options_layout.addWidget(self.format_combo, 0, 1)

        # Compression level
        options_layout.addWidget(QLabel("Compression level:"), 1, 0)
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Store", "Fastest", "Fast", "Normal", "Maximum", "Ultra"])
        options_layout.addWidget(self.level_combo, 1, 1)

        # Compression method
        options_layout.addWidget(QLabel("Compression method:"), 2, 0)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["LZMA2", "LZMA", "PPMd", "BZip2"])
        options_layout.addWidget(self.method_combo, 2, 1)

        # Dictionary size
        options_layout.addWidget(QLabel("Dictionary size:"), 3, 0)
        self.dict_combo = QComboBox()
        self.dict_combo.addItems(["64 KB", "1 MB", "2 MB", "4 MB", "8 MB", "16 MB", "32 MB", "64 MB"])
        options_layout.addWidget(self.dict_combo, 3, 1)

        # Word size
        options_layout.addWidget(QLabel("Word size:"), 4, 0)
        self.word_combo = QComboBox()
        self.word_combo.addItems(["8", "12", "16", "24", "32", "48", "64", "96", "128", "192", "256"])
        options_layout.addWidget(self.word_combo, 4, 1)

        # Solid Block size
        options_layout.addWidget(QLabel("Solid Block size:"), 5, 0)
        self.solid_combo = QComboBox()
        self.solid_combo.addItems(["Non-solid", "2 MB", "4 MB", "8 MB", "16 MB", "32 MB", "64 MB", "128 MB", "256 MB", "512 MB", "1 GB", "2 GB", "4 GB", "8 GB", "16 GB", "32 GB", "64 GB"])
        options_layout.addWidget(self.solid_combo, 5, 1)

        # CPU threads
        options_layout.addWidget(QLabel("CPU threads:"), 6, 0)
        self.cpu_combo = QComboBox()
        max_threads = os.cpu_count() or 1
        self.cpu_combo.addItems([str(i) for i in range(1, max_threads + 1)])
        options_layout.addWidget(self.cpu_combo, 6, 1)

        # Password field
        options_layout.addWidget(QLabel("Password:"), 7, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Start with password hidden
        options_layout.addWidget(self.password_input, 7, 1)

        # Encrypt file names
        self.encrypt_names = QCheckBox("Encrypt file names")
        options_layout.addWidget(self.encrypt_names, 8, 0, 1, 2)

        # Show password checkbox
        self.show_password = QCheckBox("Show password")
        self.show_password.stateChanged.connect(self.toggle_password_visibility)
        options_layout.addWidget(self.show_password, 9, 0, 1, 2)

        self.layout.addWidget(options_group)

        # Compress and Extract buttons
        button_layout = QHBoxLayout()
        self.compress_button = QPushButton("Add to archive")
        self.compress_button.clicked.connect(self.compress)
        self.extract_button = QPushButton("Extract")
        self.extract_button.clicked.connect(self.extract)
        button_layout.addWidget(self.compress_button)
        button_layout.addWidget(self.extract_button)
        self.layout.addLayout(button_layout)

        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Archive files (*.7z *.zip *.rar *.tar *.gz *.bz2 *.xz);;All files (*)")
        if file_name:
            self.file_input.setText(file_name)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.file_input.setText(directory)

    def compress(self):
        input_path = self.file_input.text()
        if input_path:
            output_path, _ = QFileDialog.getSaveFileName(self, "Save Compressed File", "", "Archive files (*.7z *.zip *.gz *.bz2 *.tar)")
            if output_path:
                options = {
                    "format": self.format_combo.currentText(),
                    "level": self.level_combo.currentText(),
                    "password": self.password_input.text(),
                }
                result = self.sevenzip.compress(input_path, output_path, options)
                if result.startswith("Error:"):
                    QMessageBox.critical(self, "Compression Failed", result)
                else:
                    QMessageBox.information(self, "Compression Complete", "File has been successfully compressed.")
                self.output_text.setText(result)
        else:
            self.output_text.setText("Please select a file or directory to compress.")

    def extract(self):
        input_path = self.file_input.text()
        if input_path:
            valid_extensions = ('.7z', '.zip', '.rar', '.tar', '.gz', '.bz2', '.xz')
            if not input_path.lower().endswith(valid_extensions):
                QMessageBox.warning(self, "Invalid File", "Please select a valid archive file (.7z, .zip, .rar, .tar, .gz, .bz2, .xz)")
                return

            output_dir = QFileDialog.getExistingDirectory(self, "Select Extract Directory")
            if output_dir:
                password = self.password_input.text()
                result = self.sevenzip.extract(input_path, output_dir, password)
                if "Wrong password" in result:
                    QMessageBox.critical(self, "Extraction Failed", "Wrong password. Please try again.")
                elif result.startswith("Error:"):
                    QMessageBox.critical(self, "Extraction Failed", result)
                else:
                    QMessageBox.information(self, "Extraction Complete", "Files have been successfully extracted.")
                self.output_text.setText(result)
        else:
            self.output_text.setText("Please select an archive file to extract.")

    # Add this method to your MainWindow class
    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
