import numpy as np
import pyaudio
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class LiveAudioWaveform:
    def __init__(self, sample_rate=44100, chunk_size=1024):
        """
        Initialize live audio waveform visualization.
        
        Args:
            sample_rate (int): Audio sampling rate
            chunk_size (int): Number of audio frames per buffer
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        
        # PyAudio configuration
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        # Data storage
        self.audio_buffer = np.zeros(self.chunk_size)
        
        # Setup matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.line, = self.ax.plot(self.audio_buffer)
        
        # Axis setup
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, self.chunk_size)
        self.ax.set_title('Live Audio Waveform')
        self.ax.set_xlabel('Sample')
        self.ax.set_ylabel('Amplitude')
        
        # Threading for audio capture
        self.is_recording = True
        self.audio_thread = threading.Thread(target=self.capture_audio)
        self.audio_thread.start()

    def capture_audio(self):
        """
        Continuously capture audio from microphone.
        Runs in a separate thread to prevent blocking.
        """
        while self.is_recording:
            try:
                data = np.frombuffer(
                    self.stream.read(self.chunk_size), 
                    dtype=np.float32
                )
                self.audio_buffer = data
            except Exception as e:
                print(f"Audio capture error: {e}")

    def update_plot(self, frame):
        """
        Update the plot with latest audio data.
        
        Args:
            frame (int): Animation frame number
        """
        self.line.set_ydata(self.audio_buffer)
        return self.line,

    def start_visualization(self):
        """
        Start the live audio waveform visualization.
        """
        # Create animation
        self.ani = FuncAnimation(
            self.fig, 
            self.update_plot, 
            interval=30,  # 30ms update interval
            blit=True
        )
        plt.show()

    def stop(self):
        """
        Stop audio stream and recording.
        """
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.audio_thread.join()

def main():
    try:
        waveform = LiveAudioWaveform()
        waveform.start_visualization()
    except KeyboardInterrupt:
        print("\nStopping audio visualization...")
    finally:
        waveform.stop()

if __name__ == "__main__":
    main()