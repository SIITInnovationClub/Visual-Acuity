import torch  # type: ignore
import torchaudio  # type: ignore
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, Wav2Vec2CTCTokenizer  # type: ignore
from pythainlp import sent_tokenize, word_tokenize  # type: ignore


class Speech_recognition:
    def __init__(self):
        self.model_name = "wannaphong/wav2vec2-large-xlsr-53-th-cv8-deepcut"
        self.tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(self.model_name)
        self.processor = Wav2Vec2Processor.from_pretrained(self.model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name)

    def transcribe_audio(self, audio_np_array, original_sampling_rate=44100):
        audio_input = torch.tensor(audio_np_array, dtype=torch.float32).unsqueeze(0)

        target_sampling_rate = self.processor.feature_extractor.sampling_rate
        if original_sampling_rate != target_sampling_rate:
            resampler = torchaudio.transforms.Resample(
                original_sampling_rate, target_sampling_rate
            )
            audio_input = resampler(audio_input)

        input_signal = self.processor(audio_input, return_tensors="pt").input_values
        input_signal = input_signal.squeeze(0)
        logits = self.model(input_signal).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.tokenizer.batch_decode(predicted_ids)[0]

        return transcription

    def get_text(self, audio_vector) -> str:
        transcription = self.transcribe_audio(audio_vector)
        transcribe_segmented = word_tokenize(transcription, keep_whitespace=False)
        text_sample = " ".join(transcribe_segmented)
        return text_sample
