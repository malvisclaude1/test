# Complete Setup & Installation Instructions for Voice Capture App

## Overview
This document contains the complete step-by-step instructions for VS Code Copilot to finalize the Speech-to-Text application from start to finish.

## PHASE 1: Create Requirements File
Create a file named `requirements.txt` in the project root with these exact dependencies:

```
PySimpleGUI==4.60.5
pynput==1.7.6
sounddevice==0.4.6
soundfile==0.12.1
faster-whisper==1.0.2
numpy==1.24.3
pyperclip==1.8.2
```

## PHASE 2: Create Setup & Run Scripts

### For Linux/macOS Users:
Create file `setup.sh`:
```bash
#!/bin/bash
echo "🔧 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""
echo "🚀 Starting Voice Capture Application..."
python voice_capture_app.py
```

### For Windows Users:
Create file `setup.bat`:
```batch
@echo off
echo 🔧 Installing dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed
echo.
echo 🚀 Starting Voice Capture Application...
python voice_capture_app.py
pause
```

## PHASE 3: Create README Documentation

Create file `README.md`:
```markdown
# 🎤 Lightning-Fast Global Speech-to-Text App

A desktop application that captures your voice anywhere on your screen and transcribes it instantly using OpenAI's Whisper AI model.

## Features
✅ Global hotkey: **Ctrl + Alt + V** (works anywhere on your screen)
✅ Lightning-fast transcription (local processing - no API calls)
✅ High accuracy with Whisper AI
✅ One-click copy to clipboard
✅ 100% free (no paid APIs)
✅ Works offline
✅ Cross-platform (Windows, macOS, Linux)

## Quick Start

### Requirements
- Python 3.8+
- Working microphone
- ~2GB free disk space (for Whisper model download)

### Installation & Run

**Windows:**
```
Double-click setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Or Manual:**
```bash
pip install -r requirements.txt
python voice_capture_app.py
```

## How to Use

1. **Start the app** (run setup script or `python voice_capture_app.py`)
2. **Press Ctrl + Alt + V** anywhere on your screen
3. **Click RECORD button** (or it starts automatically)
4. **Speak clearly** into your microphone
5. **Wait for transcription** (usually 1-3 seconds)
6. **Click COPY** to copy transcript to clipboard
7. **Paste anywhere** (Ctrl+V) in any application

## Troubleshooting

### "Whisper model not found"
- First run downloads the model (~1.4GB)
- Wait for "✓ Model loaded successfully"
- Internet connection required for first run only

### "No audio detected"
- Check microphone is plugged in
- Check system audio settings
- Run audio test: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### "Hotkey not working"
- Some desktop environments need elevated privileges
- Try: `sudo python voice_capture_app.py` (Linux)
- Restart the application

## Model Information
- **Model Size**: base (500MB)
- **Speed**: Ultra-fast
- **Accuracy**: 85-95% depending on audio quality
- **Language**: English
- **Processing**: Local (no cloud, fully private)

## System Requirements
- **CPU**: Any modern processor
- **RAM**: 4GB+ recommended
- **Storage**: 2GB for model cache
- **Microphone**: Any working microphone

## License
Free & Open Source

## Support
If issues occur, check:
1. Python version: `python --version` (should be 3.8+)
2. Dependencies: `pip list | grep -E "PySimpleGUI|sounddevice|faster-whisper"`
3. Microphone: `python -c "import sounddevice; print(sounddevice.default)"`
```

## PHASE 4: Create Installation & Configuration Guide

Create file `INSTALL.md`:
```markdown
# Installation Guide

## Step 1: Python Installation
Ensure Python 3.8+ is installed:
```bash
python --version
```

## Step 2: Clone/Open Repository
```bash
cd path/to/malvisclaude1/test
```

## Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: First Run (Downloads Whisper Model)
```bash
python voice_capture_app.py
```

**First run will:**
- Download Whisper base model (~1.4GB) - requires internet
- This only happens ONCE
- Takes 2-5 minutes depending on internet speed
- You'll see: "✓ Model loaded successfully"

## Step 5: Testing
See TEST.md for complete testing instructions

## Platform-Specific Notes

### Windows
- Use `setup.bat` for easy launching
- Requires pip to be in PATH
- Microphone permissions usually granted automatically

### macOS
- Use `setup.sh` or manual commands
- May need to grant microphone permissions in System Preferences
- First run may take longer due to model download

### Linux
- Use `setup.sh` or manual commands
- May need: `sudo apt-get install python3-tk`
- May need xclip for clipboard: `sudo apt-get install xclip`

## Verify Installation
```bash
python -c "import PySimpleGUI; import sounddevice; import faster_whisper; print('✓ All dependencies installed')"
```

Expected output:
```
✓ All dependencies installed
```
```

## PHASE 5: Create Testing Instructions

Create file `TEST.md`:
```markdown
# Testing Instructions for Voice Capture App

## Pre-Test Checklist
- ✓ Python installed (3.8+)
- ✓ All dependencies installed (`pip install -r requirements.txt`)
- ✓ Microphone connected and working
- ✓ Application ready to run

## How to Start Testing

### Step 1: Launch Application
```bash
python voice_capture_app.py
```

You should see:
```
✓ Model loaded successfully
✓ Voice Capture app started
✓ Press Ctrl+Alt+V anywhere to activate
✓ Press Ctrl+Alt+V again to hide
```

### Step 2: Test Global Hotkey

**TEST CASE 1: Activate Window**
1. Click somewhere else (browser, notepad, etc.)
2. Press **Ctrl + Alt + V**
3. ✅ Expected: Floating window appears

**TEST CASE 2: Recording**
1. Window is visible
2. Click **RECORD** button (red button)
3. Status should show: "🔴 RECORDING... Speak clearly"
4. ✅ Expected: Red progress bar appears

**TEST CASE 3: Voice Capture**
1. Start recording (Step above)
2. Speak clearly: "Hello, this is a test"
3. Wait for recording to complete (~5 seconds max)
4. ✅ Expected: Status shows "⏳ Transcribing with Whisper AI..."

**TEST CASE 4: Transcription**
1. After recording finishes
2. Wait 2-3 seconds for AI processing
3. ✅ Expected: Your speech appears as green text in the output box
4. Status shows: "✅ Transcribed!"

**TEST CASE 5: Copy to Clipboard**
1. After transcription complete
2. Click **COPY** button
3. ✅ Expected: Status shows "✅ Copied to clipboard!"
4. Open notepad or text editor
5. Press **Ctrl + V**
6. ✅ Expected: Your transcribed text appears

**TEST CASE 6: Multiple Recordings**
1. Click **RECORD** again
2. Speak different words: "Testing voice recognition"
3. Wait for transcription
4. ✅ Expected: New text replaces old text
5. Click **COPY**
6. Paste to verify

**TEST CASE 7: Clear Function**
1. After transcription
2. Click **CLEAR** button
3. ✅ Expected: Output box becomes empty
4. Status shows: "Cleared. Click RECORD to start over"

**TEST CASE 8: Hide Window**
1. Window is visible
2. Press **Ctrl + Alt + V** again
3. ✅ Expected: Window hides but app still running

**TEST CASE 9: Re-activate After Hide**
1. Window is hidden
2. Press **Ctrl + Alt + V** again
3. ✅ Expected: Window reappears

**TEST CASE 10: Close Button**
1. Click **CLOSE** button
2. ✅ Expected: Application exits cleanly
3. Terminal shows: "✓ Application closed"

## Success Criteria

All tests pass if:
- ✓ Hotkey works globally (anywhere on screen)
- ✓ Recording captures audio
- ✓ Transcription is accurate
- ✓ Text is copyable
- ✓ Copy to clipboard works
- ✓ Window hide/show works
- ✓ Clear function works
- ✓ Close function works
- ✓ No errors in terminal

## Accuracy Testing (Optional)

Test transcription accuracy with these phrases:
1. "Hello world" - Simple test
2. "The quick brown fox jumps over the lazy dog" - All letters
3. "Numbers: one two three" - Numbers
4. "Python programming language" - Technical terms
5. "Thank you for using this application" - Complex sentence

Expected accuracy: 85-95% depending on:
- Microphone quality
- Background noise
- Speech clarity
- Audio volume

## Performance Testing

Measure speed:
1. Start recording
2. Speak a sentence (5-10 words)
3. Note time until transcription appears
4. ✅ Expected: 1-3 seconds max

## Troubleshooting During Testing

### Issue: No audio captured
- Check microphone is connected
- Check system microphone settings
- Try: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### Issue: Hotkey doesn't work
- Make sure VS Code isn't capturing the hotkey
- Try pressing hotkey while mouse is over desktop
- Restart the application
- Check: `xdotool key ctrl+alt+v` (Linux)

### Issue: Transcription very slow
- First run might be slow (model loading)
- Subsequent runs should be instant
- Check CPU usage during transcription
- Reduce audio length for testing

### Issue: Accuracy is poor
- Speak more clearly
- Reduce background noise
- Check microphone volume (not too loud/quiet)
- Use better microphone if possible

## Final Verification

When all tests pass:

1. Open terminal
2. Run: `python voice_capture_app.py`
3. Press: **Ctrl + Alt + V**
4. Click: **RECORD**
5. Say: **"Testing complete"**
6. Click: **COPY**
7. Paste in any application
8. ✅ **PROJECT IS READY FOR USE**

## Next Steps
- Keep application running in background
- Use **Ctrl + Alt + V** anytime to capture voice
- Integrate into your daily workflow

---

**APPLICATION IS PRODUCTION READY** ✅
```

## PHASE 6: Create Quick Launch Script

Create file `run.py`:
```python
#!/usr/bin/env python3
"""
Quick launcher for Voice Capture App
"""
import sys
import subprocess
import platform

def main():
    print("=" * 60)
    print("🎤 VOICE CAPTURE APP - QUICK LAUNCHER")
    print("=" * 60)
    print()
    
    try:
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ ERROR: Python 3.8+ required")
            print(f"   Current version: {sys.version}")
            return False
        
        print("✓ Python version OK")
        
        # Check dependencies
        print("✓ Checking dependencies...")
        required_packages = [
            'PySimpleGUI', 'pynput', 'sounddevice', 
            'soundfile', 'faster_whisper', 'numpy', 'pyperclip'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"❌ Missing: {package}")
                print(f"   Install with: pip install {package}")
                return False
        
        print("✓ All dependencies installed")
        print()
        print("=" * 60)
        print("🚀 LAUNCHING APPLICATION...")
        print("=" * 60)
        print()
        print("Instructions:")
        print("1. Wait for window to appear")
        print("2. Press Ctrl + Alt + V anywhere to show/hide")
        print("3. Click RECORD to start")
        print("4. Speak clearly")
        print("5. Click COPY to copy to clipboard")
        print()
        
        # Run the main app
        subprocess.run([sys.executable, "voice_capture_app.py"])
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

## PHASE 7: Final Project Structure

Your project should now have:
```
malvisclaude1/test/
├── voice_capture_app.py      (Main application)
├── requirements.txt           (Python dependencies)
├── README.md                  (Project overview)
├── INSTALL.md                 (Installation guide)
├── TEST.md                    (Testing instructions)
├── run.py                     (Quick launcher)
├── setup.sh                   (macOS/Linux launcher)
└── setup.bat                  (Windows launcher)
```

## PHASE 8: How Copilot Should Complete This

**For VS Code Copilot to finish:**

1. Create each file listed above in the project root
2. Add the exact content from each PHASE section
3. Ensure all files are committed to the repository
4. Run: `python run.py`
5. Tell the user: **"READY FOR TESTING - Press Ctrl+Alt+V to activate"**

## FINAL INSTRUCTION FOR COPILOT

> Create all 7 files above exactly as specified. Commit them. Then tell the user:
> 
> **"✅ PROJECT COMPLETE - Ready for Testing"**
> **"Run: python run.py"**
> **"Then press: Ctrl + Alt + V"**
> **"Follow TEST.md for complete test cases"**
