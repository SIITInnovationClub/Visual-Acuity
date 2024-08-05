import pyaudio  # type: ignore
import audioop
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from src.constants import *
from src.utils import *
import noisereduce as nr  # type: ignore


class Audio_processing:
    def __init__(self, arrayNum, speechRec, type):
        self.arrayNum = arrayNum
        self.speechRec = speechRec
        self.type = type

    def record_audio(self, TEXT_processor):
        # Parameters for audio recording
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 35000
        CHUNK = 15000  # Length of each chunk
        THRESHOLD = 100  # RMS threshold for detecting sound
        SILENCE_LIMIT = 5  # Time in seconds to wait for silence before stopping

        p = pyaudio.PyAudio()
        # Open the microphone stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        frames = []
        silence_frames = 0
        numberInput = 0
        speech_text = ""
        hyp_text = ""

        if self.type == "open":
            data = stream.read(CHUNK, False)
            frames.append(data)
            audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
            audio_data = nr.reduce_noise(y=audio_data, sr=RATE)
            speech_text = self.speechRec.get_text(audio_data)
            print("Audio set up competed.")
            return

        print("Recording...")
        playsound_util(playsound_file_path["beep"])

        while True:
            try:
                if numberInput < self.arrayNum:
                    data = stream.read(CHUNK, False)
                    frames.append(data)
                    rms = audioop.rms(
                        data, 2
                    )  # Calculate the RMS energy of the audio chunk

                    if rms >= THRESHOLD:
                        print("Detect Sound...")
                        # Convert raw data to numpy array
                        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)

                        # Noise reduction
                        audio_data = nr.reduce_noise(y=audio_data, sr=RATE)

                        # Process audio data with speech recognition
                        speech_text = self.speechRec.get_text(audio_data)
                        print("Pure text: ", speech_text.split(" "))

                        if self.type == "user":
                            hyp_text = TEXT_processor.process_user_respond(speech_text)
                            print("Translate to user response: %s" % hyp_text)
                        elif self.type == "number":
                            hyp_text = TEXT_processor.process_text(speech_text)
                            print("Translate to number: %s" % hyp_text)

                        array_hyp_text = hyp_text.split(" ")
                        numberInput = len(array_hyp_text)

                        # Keep increasing silence until approve sound
                        silence_frames += 1

                        if hyp_text.split(" ")[numberInput - 1] == "":
                            numberInput -= 1
                            continue

                        print("* Approve Sound *")
                        silence_frames = (
                            0  # Reset silence counter if there's audio activity
                        )
                        print("Input: ", array_hyp_text)
                        print("NO.input: %d" % numberInput)

                        if numberInput >= self.arrayNum:
                            if numberInput > self.arrayNum:
                                array_hyp_text.pop()
                                hyp_text = " ".join(array_hyp_text)
                            print("Done. Stopping recording.")
                            break
                    else:
                        print("Detect Silence...")
                        silence_frames += 1

                    if silence_frames > int(RATE / CHUNK) * SILENCE_LIMIT:
                        print("Silence detected. Stopping recording.")
                        break

                else:
                    if numberInput > self.arrayNum:
                        array_hyp_text.pop()
                        hyp_text = " ".join(array_hyp_text)
                    print("Done. Stopping recording.")
                    break

            except KeyboardInterrupt:
                print("Recording stopped by user.")
                break

        # Close the audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        return hyp_text

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
