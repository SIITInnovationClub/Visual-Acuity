import pyaudio
import audioop
import matplotlib.pyplot as plt
import numpy as np
import wave
from src.constants import *

class Audio_processing:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_index = None

    def list_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(num_devices):
            device_info = self.p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                print(f"Device ID {i} - {device_info.get('name')}")

    def set_device(self, device_index):
        self.device_index = device_index

    def record_audio(self):
        # Parameters for audio recording
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 35000
        CHUNK = 15000  # The chunk size defines the length of time for each analysis frame.
        THRESHOLD = 3000  # Adjust this threshold to fit your environment and microphone sensitivity.
        SILENCE_LIMIT = 2  # Time in seconds to wait for silence before stopping recording.

        # Open the microphone stream
        stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=CHUNK,
        )

        print("Recording...")
        # playsound_util(playsound_file_path["beep"])
        frames = []
        silence_frames = 0

        while True:
            try:
                data = stream.read(CHUNK)
                frames.append(data)
                rms = audioop.rms(data, 2)  # Calculate the RMS energy of the audio chunk.

                if rms < THRESHOLD:
                    silence_frames += 1
                else:
                    silence_frames = 0  # Reset silence counter if there's audio activity.

                if silence_frames > int(RATE / CHUNK) * SILENCE_LIMIT:
                    print("Silence detected. Stopping recording.")
                    break

            except KeyboardInterrupt:
                print("Recording stopped by user.")
                break

        # Close the audio stream
        stream.stop_stream()
        stream.close()

        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
        return audio_data

    def audio_visualization(self, audio):
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

    def record_audio_from_test(self, output_filename):
        # Parameters for audio recording
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 35000
        CHUNK = 15000  # The chunk size defines the length of time for each analysis frame.
        THRESHOLD = 1500  # Adjust this threshold to fit your environment and microphone sensitivity.
        SILENCE_LIMIT = 2  # Time in seconds to wait for silence before stopping recording.

        # Open the microphone stream
        stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=CHUNK,
        )

        print("Recording...")
        frames = []
        silence_frames = 0

        while True:
            try:
                data = stream.read(CHUNK)
                frames.append(data)
                rms = audioop.rms(data, 2)  # Calculate the RMS energy of the audio chunk.

                if rms < THRESHOLD:
                    silence_frames += 1
                else:
                    silence_frames = 0  # Reset silence counter if there's audio activity.

                if silence_frames > int(RATE / CHUNK) * SILENCE_LIMIT:
                    print("Silence detected. Stopping recording.")
                    break

            except KeyboardInterrupt:
                print("Recording stopped by user.")
                break

        # Close the audio stream
        stream.stop_stream()
        stream.close()

        # Save the recorded audio to a file
        wf = wave.open(output_filename, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
        return audio_data

# Usage example
audio_processor = Audio_processing()
audio_processor.list_devices()
device_id = int(input("Select the device ID to use for recording: "))
audio_processor.set_device(device_id)

# Now you can record audio using the selected device
audio_data = audio_processor.record_audio()
audio_processor.audio_visualization(audio_data)

# To record audio to a file
output_filename = "output.wav"
audio_processor.record_audio_from_test(output_filename)