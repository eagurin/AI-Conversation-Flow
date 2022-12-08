import re
from abc import ABC, abstractmethod

import grpc
import pyaudio
from decouple import config

from auth import authorization_metadata
from tinkoff.cloud.stt.v1 import stt_pb2, stt_pb2_grpc
from tinkoff.cloud.tts.v1 import tts_pb2, tts_pb2_grpc

ENDPOINT = "stt.tinkoff.ru:443"
API_KEY = config("VOICEKIT_API_KEY")
SECRET_KEY = config("VOICEKIT_SECRET_KEY")
SAMPLE_RATE = 48000


class SpeechCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class TTS(SpeechCommand):
    """
    Text To Speech
    """

    def __init__(self, context):
        self.phrase = context.phrase
        if self.phrase:
            self.phrase = self.phrase.split(":")[1]
            self.phrase = self.phrase.replace("!", ",")
        self._ssml = "<speak> " + self.phrase + " </speak>"
        self._text = re.sub(r"\<[^>]*\>", "", self.phrase)
        stub = tts_pb2_grpc.TextToSpeechStub(
            grpc.secure_channel(ENDPOINT, grpc.ssl_channel_credentials())
        )
        metadata = authorization_metadata(API_KEY, SECRET_KEY, "tinkoff.cloud.tts")
        request = tts_pb2.SynthesizeSpeechRequest(
            input=tts_pb2.SynthesisInput(text=self._text, ssml=self._ssml),
            audio_config=tts_pb2.AudioConfig(
                audio_encoding=tts_pb2.LINEAR16,
                speaking_rate=1,
                sample_rate_hertz=SAMPLE_RATE,
            ),
        )
        self._responses = stub.StreamingSynthesize(request, metadata=metadata)

    def execute(self) -> None:
        pyaudio_lib = pyaudio.PyAudio()
        f = pyaudio_lib.open(
            output=True, channels=1, format=pyaudio.paInt16, rate=SAMPLE_RATE
        )
        try:
            for key, value in self._responses.initial_metadata():
                if key == "x-audio-num-samples":
                    break
            for stream_response in self._responses:
                f.write(stream_response.audio_chunk)
        except Exception as e:
            print(e)


class STT(SpeechCommand):
    """
    Speech To Text
    """

    def __init__(self, context):
        self.context = context

    def execute(self) -> None:
        r = stt_pb2.StreamingRecognizeRequest()
        r.streaming_config.config.encoding = stt_pb2.AudioEncoding.LINEAR16  # type: ignore
        r.streaming_config.config.sample_rate_hertz = 16000  # type: ignore
        r.streaming_config.config.num_channels = 1  # type: ignore
        r.streaming_config.config.enable_denormalization = True  # type: ignore
        r.streaming_config.config.enable_automatic_punctuation = True  # type: ignore
        r.streaming_config.config.vad_config.silence_duration_threshold = 1  # type: ignore
        # r.streaming_config.config.max_alternatives = 10  # type: ignore
        r.streaming_config.single_utterance = True  # type: ignore
        metadata = authorization_metadata(API_KEY, SECRET_KEY, "tinkoff.cloud.stt")
        stub = stt_pb2_grpc.SpeechToTextStub(
            grpc.secure_channel(ENDPOINT, grpc.ssl_channel_credentials())
        )
        try:
            responses = stub.StreamingRecognize(self.requests(r), metadata=metadata)
            for response in responses:
                for result in response.results:
                    for alternative in result.recognition_result.alternatives:
                        self.context.set_phrase(alternative.transcript)
                        break
        except Exception as e:
            print(e)

    @staticmethod
    def requests(request):
        try:
            yield request
            pyaudio_lib = pyaudio.PyAudio()
            f = pyaudio_lib.open(
                input=True, channels=1, format=pyaudio.paInt16, rate=16000
            )
            for data in iter(lambda: f.read(800), b""):
                request = stt_pb2.StreamingRecognizeRequest()
                request.audio_content = data  # type: ignore
                yield request
        except Exception as e:
            print("Got exception in generate_requests", e)
            raise


class Invoker:
    _on_speak = None
    _on_listen = None

    def set_on_speak(self, phrase: SpeechCommand):
        self._on_speak = TTS(phrase)

    def set_on_listen(self, context: SpeechCommand):
        self._on_listen = STT(context)

    def do_speak(self):
        if isinstance(self._on_speak, SpeechCommand):
            self._on_speak.execute()

    def do_listen(self):
        if isinstance(self._on_listen, SpeechCommand):
            self._on_listen.execute()


def say(phrase):
    invoker = Invoker()
    invoker.set_on_speak(phrase)
    invoker.do_speak()


def listen(context):
    invoker = Invoker()
    invoker.set_on_listen(context)
    invoker.do_listen()
