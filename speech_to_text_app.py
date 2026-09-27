#!/usr/bin/env python3
"""
Speech-to-Text Desktop Application
Activate with Ctrl+Alt+V globally, records audio, and transcribes using OpenAI's Whisper
"""

import threading
import queue
import os
import sys
import json
from pathlib import Path
from datetime import datetime

import PySimpleGUI as sg
from pynput import keyboard
import sounddevice as sd
import soundfile as sf
import numpy as np
from openai import OpenAI

# Configuration
CONFIG_FILE = Path.home() / ".stt_config.json"
RECORDINGS_DIR = Path.home() / ".stt_recordings"
RECORDINGS_DIR.mkdir(exist_ok=True)

# Initialize OpenAI client (uses OPENAI_API_KEY environment variable)
try:
    client = OpenAI()
except Exception as e:
    print(f"Error: OPENAI_API_KEY not set. Please set your OpenAI API key.")
    sys.exit(1)

# Theme
sg.theme('DarkBlue3')

class SpeechToTextApp:
    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.hotkey_listener = None
        self.window = None
        self.recording_thread = None
        self.transcription_queue = queue.Queue()
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                self.config = json.load(f)
        else:
            self.config = {"api_key": "", "language": "en"}
            
    def save_config(self):
        """Save configuration to file"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)
    
    def setup_hotkey_listener(self):
        """Setup global hotkey listener for Ctrl+Alt+V"""
        def on_press(key):
            try:
                # Check for Ctrl+Alt+V
                if hasattr(key, 'char'):
                    pass
            except AttributeError:
                pass
        
        def on_release(key):
            try:
                if (hasattr(key, 'vk') or True):  # Catch the combination
                    pass
            except AttributeError:
                pass
        
        # Use hotkey detection - simpler approach
        from pynput.keyboard import Key, Controller, Listener
        
        self.ctrl_pressed = False
        self.alt_pressed = False
        
        def on_key_press(key):
            try:
                if key == Key.ctrl_l or key == Key.ctrl_r:
                    self.ctrl_pressed = True
                elif key == Key.alt_l or key == Key.alt_r:
                    self.alt_pressed = True
                elif hasattr(key, 'char') and key.char == 'v':
                    if self.ctrl_pressed and self.alt_pressed:
                        self.activate_recording()
            except:
                pass
        
        def on_key_release(key):
            try:
                if key == Key.ctrl_l or key == Key.ctrl_r:
                    self.ctrl_pressed = False
                elif key == Key.alt_l or key == Key.alt_r:
                    self.alt_pressed = False
            except:
                pass
        
        self.hotkey_listener = keyboard.Listener(
            on_press=on_key_press,
            on_release=on_key_release
        )
        self.hotkey_listener.start()
    
    def activate_recording(self):
        """Activate recording when hotkey is pressed"""
        if not self.is_recording:
            self.is_recording = True
            if self.window:
                self.window.write_event_value('-RECORDING_START-', None)
    
    def record_audio(self, duration=10):
        """Record audio from microphone"""
        print(f"Recording for up to {duration} seconds... (press Ctrl+Alt+V again to stop)")
        try:
            audio = sd.rec(int(duration * self.sample_rate), 
                          samplerate=self.sample_rate, 
                          channels=1, 
                          dtype='float32',
                          blocking=False)
            
            # Wait for recording to complete or be stopped
            for i in range(duration * 10):
                if not self.is_recording:
                    break
                sd.wait(timeout=0.1)
            
            sd.wait()  # Ensure all audio is recorded
            return audio
        except Exception as e:
            print(f"Recording error: {e}")
            return None
    
    def transcribe_audio(self, audio_file_path):
        """Transcribe audio using OpenAI's Whisper"""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            return transcript.text
        except Exception as e:
            return f"Transcription error: {str(e)}"
    
    def create_main_window(self):
        """Create the main recording window"""
        layout = [
            [sg.Text("🎤 Speech-to-Text Recorder", font=("Helvetica", 16, "bold"))],
            [sg.Text("Press Ctrl+Alt+V to start recording", font=("Helvetica", 10))],
            [sg.Text("", key="-STATUS-", font=("Helvetica", 12, "italic"), text_color="yellow")],
            [sg.Multiline(size=(60, 10), key="-OUTPUT-", 
                         disabled=True, background_color="#1a1a1a", 
                         text_color="#00FF00", font=("Courier", 10))],
            [sg.Button("Copy to Clipboard", key="-COPY-"), 
             sg.Button("Clear", key="-CLEAR-"), 
             sg.Button("Exit", key="-EXIT-")],
            [sg.ProgressBar(100, orientation='h', size=(40, 20), 
                           key='-PROGRESS-', visible=False)]
        ]
        
        return sg.Window("Speech-to-Text", layout, 
                        finalize=True, 
                        keep_on_top=True,
                        size=(700, 400))
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            import subprocess
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                      stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        except:
            # Fallback for Windows/Mac
            try:
                import pyperclip
                pyperclip.copy(text)
            except:
                # Fallback using tkinter
                try:
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()
                    root.clipboard_clear()
                    root.clipboard_append(text)
                    root.update()
                    root.destroy()
                except:
                    pass
    
    def run(self):
        """Main application loop"""
        self.setup_hotkey_listener()
        self.window = self.create_main_window()
        
        current_transcript = ""
        
        # Start a thread for recording
        def recording_worker():
            while True:
                try:
                    if self.is_recording:
                        # Record audio
                        audio = sd.rec(int(10 * self.sample_rate), 
                                      samplerate=self.sample_rate, 
                                      channels=1, 
                                      dtype='float32')
                        sd.wait()
                        
                        # Save to file
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        audio_file = RECORDINGS_DIR / f"recording_{timestamp}.wav"
                        sf.write(audio_file, audio, self.sample_rate)
                        
                        # Transcribe
                        self.window.write_event_value('-TRANSCRIBING-', audio_file)
                        self.is_recording = False
                        
                except Exception as e:
                    print(f"Recording worker error: {e}")
        
        recording_thread = threading.Thread(target=recording_worker, daemon=True)
        recording_thread.start()
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break
            
            elif event == "-RECORDING_START-":
                self.window["-STATUS-"].update("🔴 Recording... Press Ctrl+Alt+V to stop")
                self.window["-PROGRESS-"].update_bar(50)
                self.window["-PROGRESS-"].set_visible(True)
            
            elif event == "-TRANSCRIBING-":
                audio_file = values[event]
                self.window["-STATUS-"].update("⏳ Transcribing audio...")
                
                # Transcribe in background
                def transcribe_worker(audio_path):
                    result = self.transcribe_audio(str(audio_path))
                    self.window.write_event_value('-TRANSCRIBED-', result)
                    # Clean up
                    try:
                        audio_path.unlink()
                    except:
                        pass
                
                transcribe_thread = threading.Thread(
                    target=transcribe_worker, 
                    args=(audio_file,), 
                    daemon=True
                )
                transcribe_thread.start()
            
            elif event == "-TRANSCRIBED-":
                transcript = values[event]
                current_transcript = transcript
                self.window["-OUTPUT-"].update(transcript)
                self.window["-STATUS-"].update("✅ Ready! Press Ctrl+Alt+V to record again")
                self.window["-PROGRESS-"].set_visible(False)
            
            elif event == "-COPY-":
                if current_transcript:
                    self.copy_to_clipboard(current_transcript)
                    self.window["-STATUS-"].update("📋 Copied to clipboard!")
            
            elif event == "-CLEAR-":
                self.window["-OUTPUT-"].update("")
                current_transcript = ""
                self.window["-STATUS-"].update("Cleared. Press Ctrl+Alt+V to start")
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        
        self.window.close()


if __name__ == "__main__":
    app = SpeechToTextApp()
    app.run()
