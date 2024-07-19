import pyaudio  # type: ignore
import audioop
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from src.constants import *


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
        CHUNK = (
            15000  # The chunk size defines the length of time for each analysis frame.
        )

        THRESHOLD = 500  # Adjust this threshold to fit your environment and microphone sensitivity.
        SILENCE_LIMIT = (
            5  # Time in seconds to wait for silence before stopping recording.
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
        numberInput = 0
        speech_text = ""
        hyp_text = ""

        while True:
            try:
                if numberInput < self.arrayNum:
                    data = stream.read(CHUNK, False)
                    frames.append(data)
                    rms = audioop.rms(
                        data, 2
                    )  # Calculate the RMS energy of the audio chunk.

                    if rms >= THRESHOLD:
                        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
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

                        if hyp_text.split(" ")[numberInput - 1] == "":
                            numberInput -= 1
                            silence_frames = (
                                0  # Reset silence counter if there's audio activity.
                            )
                            continue

                        print("Input: ", array_hyp_text)
                        print("NO.input: %d" % numberInput)
                        silence_frames = (
                            0  # Reset silence counter if there's audio activity.
                        )
                    else:
                        silence_frames += 1

                    if silence_frames > int(RATE / CHUNK) * SILENCE_LIMIT:
                        print("Silence detected. Stopping recording.")
                        break

                else:
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
