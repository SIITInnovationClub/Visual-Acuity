import pyaudio
import audioop
import matplotlib.pyplot as plt
import numpy as np
from src.constants import *


class Audio_processing:
    def __init__(self):
        pass

    def record_audio(self):
        # Parameters for audio recording
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 35000
        CHUNK = (
            15000  # The chunk size defines the length of time for each analysis frame.
        )

        THRESHOLD = 3000  # Adjust this threshold to fit your environment and microphone sensitivity.
        SILENCE_LIMIT = (
            2  # Time in seconds to wait for silence before stopping recording.
        )
        p = pyaudio.PyAudio()
        # Open the microphone stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        print("Recording...")
        playsound_util(playsound_file_path["beep"])
        frames = []
        silence_frames = 0

        while True:
            try:
                data = stream.read(CHUNK, True)
                frames.append(data)
                rms = audioop.rms(
                    data, 2
                )  # Calculate the RMS energy of the audio chunk.

                if rms >= THRESHOLD:
                    silence_frames = (
                        0  # Reset silence counter if there's audio activity.
                    )
                else:
                    silence_frames += 1

                if silence_frames > int(RATE / CHUNK) * SILENCE_LIMIT:
                    print("Silence detected. Stopping recording.")
                    break

            except KeyboardInterrupt:
                print("Recording stopped by user.")
                break

        # Close the audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
        return audio_data

    def audio_visualization(audio):
        time = np.arange(len(audio))
        data = audio
        plt.figure(figsize=(10, 6))
        plt.plot(time, data, label="Data")
        plt.xlabel("Time")
        plt.ylabel("Data Value")
        plt.title("Data vs. Time")
        plt.grid(True)
        plt.legend()
        plt.show()
