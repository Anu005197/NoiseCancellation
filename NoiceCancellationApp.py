import pyaudio
import numpy as np
import noisereduce as nr
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import soundfile as sf

# Initialize customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Globals
stream = None
p = None
recorded_frames = []
is_recording = False
waveform_buffer = np.array([])

# Device selection
def get_device_list():
    try:
        p_temp = pyaudio.PyAudio()
        devices = [f"{i}: {p_temp.get_device_info_by_index(i)['name']}" for i in range(p_temp.get_device_count())]
        p_temp.terminate()
        return devices
    except Exception as e:
        messagebox.showerror("Error", f"Could not list devices: {e}")
        return ["0: Default"]

# Waveform update
def update_waveform(audio_data):
    global waveform_buffer
    waveform_buffer = np.concatenate([waveform_buffer, audio_data])
    # Show only the last 5000 samples
    if len(waveform_buffer) > 5000:
        waveform_buffer = waveform_buffer[-5000:]
    ax.clear()
    ax.plot(waveform_buffer)
    ax.set_title("Processed Audio Waveform")
    canvas.draw()

# Audio callback
def callback(in_data, frame_count, time_info, status):
    try:
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        n_reduce = float(n_reduce_var.get())
        reduced_noise = nr.reduce_noise(y=audio_data, sr=44100, n_std_thresh_stationary=n_reduce)
        recorded_frames.append(reduced_noise.astype(np.int16))
        update_waveform(reduced_noise)
        return (reduced_noise.tobytes(), pyaudio.paContinue)
    except Exception as e:
        print(f"Error in callback: {e}")
        return (in_data, pyaudio.paContinue)

# Start noise cancellation
def start_noise_cancellation():
    global stream, p, recorded_frames, is_recording
    try:
        recorded_frames = []
        is_recording = True
        input_index = int(input_device_var.get().split(":")[0])
        output_index = int(output_device_var.get().split(":")[0])
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        output=True,
                        input_device_index=input_index,
                        output_device_index=output_index,
                        frames_per_buffer=1024,
                        stream_callback=callback)
        stream.start_stream()
        messagebox.showinfo("Noise Cancellation", "Noise cancellation started!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Stop noise cancellation
def stop_noise_cancellation():
    global stream, p, is_recording
    if stream and stream.is_active():
        stream.stop_stream()
        stream.close()
        p.terminate()
        is_recording = False
        messagebox.showinfo("Noise Cancellation", "Noise cancellation stopped!")

# Save processed audio
def save_audio():
    if recorded_frames:
        audio = np.concatenate(recorded_frames)
        sf.write("processed_audio.wav", audio, 44100)
        messagebox.showinfo("Save Audio", "Processed audio saved as processed_audio.wav")
    else:
        messagebox.showwarning("Save Audio", "No audio to save.")

# GUI setup
root = ctk.CTk()
root.title("Background Noise Cancelling Software")
root.geometry("650x600")

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Background Noise Cancellation", font=("Arial", 18)).pack(pady=10)

# Device selection dropdowns
input_device_var = ctk.StringVar(value="0: Default")
output_device_var = ctk.StringVar(value="0: Default")
input_devices = get_device_list()
output_devices = get_device_list()

ctk.CTkLabel(frame, text="Input Device:").pack()
input_menu = ctk.CTkOptionMenu(frame, variable=input_device_var, values=input_devices)
input_menu.pack()

ctk.CTkLabel(frame, text="Output Device:").pack()
output_menu = ctk.CTkOptionMenu(frame, variable=output_device_var, values=output_devices)
output_menu.pack()

# Noise reduction parameter
ctk.CTkLabel(frame, text="Noise Reduction Level (n_std_thresh_stationary):").pack()
n_reduce_var = ctk.StringVar(value="1")
ctk.CTkEntry(frame, textvariable=n_reduce_var).pack()

# Buttons
ctk.CTkButton(frame, text="Start", command=start_noise_cancellation).pack(pady=10)
ctk.CTkButton(frame, text="Stop", command=stop_noise_cancellation).pack(pady=10)
ctk.CTkButton(frame, text="Save Audio", command=save_audio).pack(pady=10)

# Waveform visualization
fig, ax = plt.subplots(figsize=(6,2))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(pady=10)

# Run the GUI
root.mainloop()
