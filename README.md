# 📸 Snapchat Memory Downloader

A beautiful, professional desktop application that helps you recover and organize your Snapchat Memories by converting Snapchat's JSON data export into a permanent, organized local media library.

## 🎯 What Does This Do?

Snapchat provides users with their data as a JSON file containing metadata and temporary signed URLs. This application:

- **Parses** your Snapchat JSON export file
- **Downloads** all your memories (photos and videos) from temporary URLs
- **Organizes** files by year in clean folder structures
- **Names** files using their original timestamps (YYYY-MM-DD_HH-MM-SS format)
- **Validates** downloads to ensure file integrity
- **Generates** a comprehensive CSV report of all download attempts

Your data belongs to you — this app makes it permanent and accessible.

---

## ✨ Key Features

- 🖥️ **Modern GUI** — Beautiful dark-themed interface with neon yellow accents and smooth animations
- 📁 **Automatic Organization** — Files automatically organized into year-based folders
- 🔄 **Reliable Downloads** — Automatic retry mechanism for failed downloads
- 📊 **Progress Tracking** — Real-time progress bar with download status
- 📝 **Detailed Reports** — CSV report showing which files downloaded successfully
- 🎨 **Sleek Design** — Professional UI with toast notifications and completion dialogs
- 🔒 **Error Handling** — Handles expiring links, partial downloads, and network issues gracefully

---

## 🛠️ Requirements

- **Python 3.7+** (Python 3.13 recommended)
- **macOS, Windows, or Linux**
- A **Snapchat data export** (JSON file) — Request your data from Snapchat's privacy settings

### Dependencies

- `PyQt6` — Modern GUI framework
- `tqdm` — Progress bar utilities

---

## 📦 Installation

### Quick Setup (Recommended)

1. **Clone or download** this repository:
   ```bash
   cd snapchat_downloader
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This will:
   - Create a Python virtual environment
   - Install all required dependencies
   - Prepare the application for use

### Manual Setup

If you prefer to set up manually:

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### Getting Your Snapchat Data

1. Open Snapchat app → Settings → Privacy → My Data
2. Request your data export (this may take a few days)
3. Download the ZIP file from Snapchat
4. Extract the ZIP file
5. Locate the JSON file (usually named something like `memories_history.json`)

### Running the Application

1. **Activate the virtual environment** (if not already active):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate  # Windows
   ```

2. **Launch the application**:
   ```bash
   python3 app.py
   ```

3. **In the application window**:
   - Click **"Browse"** next to "Snapchat JSON" and select your JSON file
   - Click **"Browse"** next to "Output Folder" and choose where to save your memories
   - Click **"Start Download"** to begin

4. **Wait for completion**:
   - Watch the progress bar as files download
   - Receive toast notifications for status updates
   - A completion dialog will appear when finished

5. **Review the results**:
   - Your memories will be organized in the output folder by year
   - Check `report.csv` in the output folder to see which files downloaded successfully

### Example Output Structure

```
output_folder/
├── 2020/
│   ├── 2020-05-15_14-30-22.jpg
│   ├── 2020-06-20_09-15-45.mp4
│   └── ...
├── 2021/
│   ├── 2021-01-10_18-45-30.jpg
│   └── ...
└── report.csv
```

---

## 📁 Project Structure

```
snapchat_downloader/
├── app.py              # Main GUI application (PyQt6)
├── controller.py       # Orchestrates the download process
├── snapchat_parser.py  # Parses Snapchat JSON export
├── downloader.py       # Handles file downloads with retries
├── file_manager.py     # Organizes files and manages paths
├── report.py           # Generates CSV reports
├── requirements.txt    # Python dependencies
├── setup.sh            # Setup script for quick installation
└── README.md           # This file
```

Each module has a single, clear responsibility — following professional software design principles.

---

## 🔧 How It Works

The application follows a clean pipeline:

```
Snapchat JSON → Parser → Job Builder → Downloader → Validator → File Organizer → Report
```

1. **snapchat_parser.py** — Extracts memory URLs, dates, and types from JSON
2. **controller.py** — Coordinates the entire download process
3. **downloader.py** — Downloads files with automatic retry (3 attempts)
4. **file_manager.py** — Creates organized folder structure and meaningful filenames
5. **report.py** — Logs all download attempts to CSV for review

---

## 💡 Technical Highlights

- **Modular Architecture** — Clean separation of concerns
- **Error Resilience** — Handles expiring links, network failures, and corrupted files
- **User-Friendly** — No command line needed, beautiful GUI
- **Thread-Safe** — Downloads run in background thread to keep UI responsive
- **Modern UI** — PyQt6 with custom styling, animations, and notifications

---

## 📝 Notes

- **Download Speed**: Download speed depends on your internet connection and Snapchat's servers
- **File Names**: Files are named using their original timestamp (YYYY-MM-DD_HH-MM-SS format)
- **Report**: Always check `report.csv` after completion to verify all files downloaded successfully
- **Temporary URLs**: Snapchat URLs may expire. Download your data as soon as possible after receiving it

---

## 🎨 Customization

### Changing the Font

Edit `APP_FONT_FAMILY` in `app.py` (line 21):
```python
APP_FONT_FAMILY = "Helvetica Neue"  # Change to your preferred font
```

### Changing Colors

Edit the color constants in `app.py` (lines 12-17):
```python
NEON_YELLOW = "#ffd9fc"  # Accent color
DARK_BG = "#1a1a1a"      # Background color
# ... etc
```

---

## 🐛 Troubleshooting

**Application won't start?**
- Ensure you've activated the virtual environment
- Verify PyQt6 is installed: `pip list | grep PyQt6`

**Downloads failing?**
- Check your internet connection
- Verify the JSON file is valid
- Check if Snapchat URLs have expired (request a fresh data export)

**Import errors?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version (3.7+)

---

## 📄 License

This project is provided as-is for personal use.

---

## 🙏 Acknowledgments

Built to help users take ownership of their personal data and preserve their digital memories.

---

**Enjoy preserving your Snapchat memories! 📸✨**

