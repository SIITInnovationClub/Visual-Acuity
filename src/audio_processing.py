import pyaudio
import audioop
import matplotlib.pyplot as plt
import numpy as np
from src.constants import *

class Audio_processing():
    def __init__(self):
        pass

    def record_audio(self):
        # Parameters for audio recording
        FORMAT = pyaudio.paInt32
        CHANNELS = 1
        RATE = 48000
        CHUNK = 4096  # Reduced chunk size to reduce overflow risk
        THRESHOLD = 10  # Adjust this threshold to fit your environment and microphone sensitivity.
        SILENCE_LIMIT = 2  # Time in seconds to wait for silence before stopping recording.
        
        p = pyaudio.PyAudio()
        
        # Open the microphone stream with increased input latency
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=None,
                        start=True)
        
        print("Recording...")
        playsound_util(playsound_file_path['beep'])
        frames = []
        silence_frames = 0

        while True:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                rms = audioop.rms(data, 2)  # Calculate the RMS energy of the audio chunk.

                if rms < THRESHOLD:
                    silence_frames += 1
                else:
                    silence_frames = 0  # Reset silence counter if there's audio activity.

                if silence_frames > int(RATE / CHUNK) * SILENCE_LIMIT:
                    print("Silence detected. Stopping recording.")
                    break

            except OSError as e:
                print(f"Error recording audio: {e}")
                break

            except KeyboardInterrupt:
                print("Recording stopped by user.")
                break

        # Close the audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int32)
        return audio_data

    def audio_visualization(self, audio):
        time = np.arange(len(audio))
        data = audio
        plt.figure(figsize=(10, 6))
        plt.plot(time, data, label='Data')
        plt.xlabel('Time')
        plt.ylabel('Data Value')
        plt.title('Data vs. Time')
        plt.grid(True)
        plt.legend()
        plt.show()

AUDIO_processor = Audio_processing()
voice_recorded = AUDIO_processor.record_audio()
AUDIO_processor.audio_visualization(voice_recorded)