# **Noise Cancellation App**

A real-time background noise cancellation application built with Python, PyAudio, noisereduce, and customtkinter. This app was inspired by the “Noise Reduction in Open-Plan Offices” project from Engineering Strategies and Practice II at the University of Toronto. The prototype was further developed independently to refine its functionality.

## Features

Captures live audio input and reduces background noise in real-time.
Simple GUI with Start and Stop buttons using customtkinter.
Built for Windows/Linux/Mac (requires Python and dependencies).

## Technologies Used

- Python – Core programming language
- PyAudio – Real-time audio streaming
- NumPy – Audio data processing
- noisereduce – Noise reduction algorithm
- customtkinter – Modern GUI

## Usage

1. Install dependencies:
```bash
pip install pyaudio numpy noisereduce customtkinter
```
2. Run the app

```bash
python noise_cancellation_app.py
```
3. Click Start to begin noise cancellation, Stop to end.
   
## Skills Demonstrated

- Audio signal processing
- Real-time streaming and data handling
- GUI development
- Independent project development

## Future Improvements

- Improve algorithm efficiency for low-latency performance
- Add volume and sensitivity controls
- Cross-platform packaging
