#!/usr/bin/env python3
"""
Lightning-Fast Global Speech-to-Text Application
Press Ctrl+Alt+V anywhere on your screen to activate
"""

import os
import sys
import threading
import queue
import time
from pathlib import Path
from datetime import datetime

import PySimpleGUI as sg
import numpy as np
import sounddevice as sd
import soundfile as sf
from pynput.keyboard import GlobalHotKeys
from faster_whisper import WhisperModel


# ----------------------------
# Configuration
# ----------------------------
AUDIO_DIR = Path.home() / ".voice_hotkey_audio"
AUDIO_DIR.mkdir(exist_ok=True)

# Model size: "tiny" (fastest), "base", "small", "medium", "large"
# For maximum speed + accuracy: "base" or "small"
MODEL_SIZE = "base"

SAMPLE_RATE = 16000
CHANNELS = 1
MAX_RECORD_DURATION = 15  # seconds


# ----------------------------
# Load Whisper Model (Faster-Whisper - fastest + accurate)
# ----------------------------
def load_model():
    """Load the Whisper model with optimal settings for speed"""
    try:
        print(f"Loading {MODEL_SIZE} Whisper model...")
        model = WhisperModel(
            MODEL_SIZE,
            device="cpu",  # Change to "cuda" if you have NVIDIA GPU
            compute_type="int8"  # int8 for CPU speed, float16 for GPU
        )
        print("✓ Model loaded successfully")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


MODEL = load_model()
TRANSCRIPTION_QUEUE = queue.Queue()


# ----------------------------
# Main Application Class
# ----------------------------
class GlobalVoiceCapture:
    def __init__(self):
        self.recording = False
        self.window_visible = False
        self.current_transcript = ""
        self.hotkey_listener = None
        self.audio_data = None
        self.stream = None
        
        # Setup UI
        sg.theme("DarkBlue3")
        self.window = self.create_window()
        self.setup_hotkey()

    def create_window(self):
        """Create the main floating window"""
        layout = [
            [sg.Text("🎤 VOICE CAPTURE", font=("Helvetica", 16, "bold"), text_color="#FFD966")],
            [sg.Text("Global Hotkey: Ctrl + Alt + V", font=("Helvetica", 10), text_color="#B3E5FC")],
            [sg.Text("", key="-STATUS-", font=("Helvetica", 11, "bold"), text_color="#00FF00")],
            
            # Recording button
            [sg.Button("🔴 RECORD", key="-RECORD-", size=(20, 2), 
                      button_color=("white", "#C62828"), font=("Helvetica", 12, "bold"))],
            
            # Transcription display
            [sg.Multiline(
                key="-OUTPUT-",
                size=(70, 12),
                font=("Courier New", 11),
                autoscroll=True,
                disabled=True,
                no_scrollbar=False,
                background_color="#0D1B2A",
                text_color="#00FF00",
                border_width=2
            )],
            
            # Action buttons
            [
                sg.Button("📋 COPY", key="-COPY-", size=(15, 1), 
                         button_color=("white", "#2E7D32"), font=("Helvetica", 11, "bold")),
                sg.Button("🗑️ CLEAR", key="-CLEAR-", size=(15, 1), font=("Helvetica", 11)),
                sg.Button("❌ CLOSE", key="-CLOSE-", size=(15, 1), font=("Helvetica", 11)),
            ],
            
            [sg.ProgressBar(100, orientation='h', size=(65, 20), 
                           key='-PROGRESS-', visible=False, bar_color=("#00FF00", "#1a1a1a"))]
        ]

        window = sg.Window(
            "Voice Capture - Global Hotkey",
            layout,
            keep_on_top=True,
            finalize=True,
            size=(750, 550),
            element_justification="left",
            use_default_focus=False,
            alpha_channel=0.98
        )
        
        window.hide()
        return window

    def setup_hotkey(self):
        """Setup global Ctrl+Alt+V hotkey"""
        def on_activate():
            self.show_window()

        try:
            self.hotkey_listener = GlobalHotKeys({
                '<ctrl>+<alt>+v': on_activate
            })
            
            listener_thread = threading.Thread(
                target=self.hotkey_listener.start,
                daemon=True
            )
            listener_thread.start()
            print("✓ Global hotkey Ctrl+Alt+V activated")
        except Exception as e:
            print(f"Hotkey setup error: {e}")

    def show_window(self):
        """Show the window and bring to front"""
        if not self.window_visible:
            self.window.un_hide()
            self.window.bring_to_front()
            self.window_visible = True
            self.update_status("🎤 Ready to record - Click RECORD or press space")

    def update_status(self, text):
        """Update status message"""
        self.window["-STATUS-"].update(text)

    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            return
        
        self.recording = True
        self.update_status("🔴 RECORDING... Speak clearly")
        self.window["-RECORD-"].update(disabled=True)
        self.window["-PROGRESS-"].set_visible(True)
        
        # Start recording in background thread
        recording_thread = threading.Thread(
            target=self.record_audio,
            daemon=True
        )
        recording_thread.start()

    def record_audio(self):
        """Capture audio from microphone"""
        try:
            print(f"Recording for up to {MAX_RECORD_DURATION} seconds...")
            
            # Initialize recording
            audio_buffer = []
            
            def audio_callback(indata, frames, time_info, status):
                if status:
                    print(f"Audio status: {status}")
                audio_buffer.append(indata.copy())
            
            # Record audio
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                blocksize=4096,
                callback=audio_callback
            ):
                # Record for duration or until user stops
                for i in range(MAX_RECORD_DURATION * 10):
                    time.sleep(0.1)
                    progress = min(100, (i / (MAX_RECORD_DURATION * 10)) * 100)
                    self.window["-PROGRESS-"].update(int(progress))
                    
                    if not self.recording:
                        break
            
            # Combine audio chunks
            if audio_buffer:
                audio_data = np.concatenate(audio_buffer, axis=0)
                
                # Save audio file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                audio_path = AUDIO_DIR / f"voice_{timestamp}.wav"
                sf.write(str(audio_path), audio_data, SAMPLE_RATE)
                
                print(f"✓ Audio saved: {audio_path}")
                
                # Start transcription
                self.transcribe_async(audio_path)
            else:
                self.update_status("❌ No audio detected")
                self.recording = False
                self.window["-RECORD-"].update(disabled=False)
                self.window["-PROGRESS-"].set_visible(False)
                
        except Exception as e:
            print(f"Recording error: {e}")
            self.update_status(f"❌ Error: {str(e)}")
            self.recording = False
            self.window["-RECORD-"].update(disabled=False)
            self.window["-PROGRESS-"].set_visible(False)

    def transcribe_async(self, audio_path):
        """Transcribe audio asynchronously"""
        def transcribe_worker():
            try:
                self.update_status("⏳ Transcribing with Whisper AI...")
                self.window["-PROGRESS-"].update(50)
                
                # Transcribe using Faster-Whisper
                segments, info = MODEL.transcribe(
                    str(audio_path),
                    language="en",
                    vad_filter=True,  # Remove silence
                    beam_size=5,
                    best_of=1
                )
                
                # Extract text
                text = " ".join([seg.text.strip() for seg in segments if seg.text.strip()])
                
                if not text:
                    text = "[No speech detected]"
                
                self.current_transcript = text
                self.window["-OUTPUT-"].update(text)
                self.update_status(f"✅ Transcribed! ({len(text)} chars) - Click COPY or press Ctrl+C")
                self.window["-PROGRESS-"].update(100)
                
                time.sleep(0.5)
                self.window["-PROGRESS-"].set_visible(False)
                
                # Clean up audio file
                try:
                    audio_path.unlink()
                except:
                    pass
                
            except Exception as e:
                print(f"Transcription error: {e}")
                self.update_status(f"❌ Transcription error: {str(e)}")
                self.window["-PROGRESS-"].set_visible(False)
            
            finally:
                self.recording = False
                self.window["-RECORD-"].update(disabled=False)
        
        transcribe_thread = threading.Thread(target=transcribe_worker, daemon=True)
        transcribe_thread.start()

    def copy_to_clipboard(self, text):
        """Copy text to clipboard (cross-platform)"""
        try:
            import pyperclip
            pyperclip.copy(text)
            self.update_status("✅ Copied to clipboard!")
            return True
        except Exception:
            try:
                # Linux fallback
                import subprocess
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode("utf-8"),
                    check=False
                )
                self.update_status("✅ Copied to clipboard!")
                return True
            except Exception:
                try:
                    # macOS fallback
                    import subprocess
                    subprocess.run(
                        ["pbcopy"],
                        input=text.encode("utf-8"),
                        check=False
                    )
                    self.update_status("✅ Copied to clipboard!")
                    return True
                except Exception as e:
                    print(f"Clipboard error: {e}")
                    self.update_status("❌ Could not copy to clipboard")
                    return False

    def run(self):
        """Main application loop"""
        print("✓ Voice Capture app started")
        print("✓ Press Ctrl+Alt+V anywhere to activate")
        print("✓ Press Ctrl+Alt+V again to hide")
        
        while True:
            event, values = self.window.read(timeout=100)

            # Window closed
            if event == sg.WINDOW_CLOSED or event == "-CLOSE-":
                break

            # Record button clicked
            if event == "-RECORD-":
                self.start_recording()

            # Copy button clicked
            if event == "-COPY-":
                if self.current_transcript.strip():
                    self.copy_to_clipboard(self.current_transcript)
                else:
                    self.update_status("⚠️ Nothing to copy yet")

            # Clear button clicked
            if event == "-CLEAR-":
                self.window["-OUTPUT-"].update("")
                self.current_transcript = ""
                self.update_status("Cleared. Click RECORD to start over")

            # Check for window visibility toggle (hide when losing focus via hotkey)
            if event == '<ctrl>+<alt>+v':
                if self.window_visible:
                    self.window.hide()
                    self.window_visible = False
                    self.recording = False
                    self.window["-RECORD-"].update(disabled=False)
                    self.window["-PROGRESS-"].set_visible(False)

        # Cleanup
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except:
                pass
        
        self.window.close()
        print("✓ Application closed")


# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    try:
        app = GlobalVoiceCapture()
        app.run()
    except KeyboardInterrupt:
        print("\n✓ Application interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
