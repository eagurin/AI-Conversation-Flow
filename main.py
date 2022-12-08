from __future__ import annotations

import sys
from abc import ABC, abstractmethod

import openai
from decouple import config

from voicekit import say, listen

sys.path.append("..")

openai.api_key = config("OPENAI_API_KEY")
endpoint = config("VOICEKIT_ENDPOINT", default="api.tinkoff.ai:443")
api_key = config("VOICEKIT_API_KEY")
secret_key = config("VOICEKIT_SECRET_KEY")


class Context:
    _phrase: str = ""
    _history: list = []

    def __init__(self, user, robot) -> None:
        self.user = user
        self.robot = robot
        self.speakers = [self.robot, self.user]
        self.title = "Далее следует разговор с " + self.robot.name + "-помощником. "
        self.title += "Помощник услужливый, творческий, умный и очень дружелюбный.\n\n"
        self.title += self.user.name + ":\n"

    @property
    def prompt(self):
        return self.title + "".join(self._history[-6:]) + "\n" + self.robot.name + ":"

    @property
    def phrase(self):
        return self._phrase

    def set_phrase(self, text):
        print(text, end="")
        self._phrase += text or " "

    def add_history(self):
        self._history.append(self._phrase)
        self._phrase = ""

    def conversation_to(self, speaker: Dialog):
        self._speaker = speaker
        self._speaker.context = self

    def request(self):
        for speaker in self.speakers:
            self.conversation_to(speaker)
            self.set_phrase("\n" + speaker.name + ": ")
            self._speaker.handle()
            self.add_history()


class Dialog(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle(self) -> None:
        pass


class OpenAI(Dialog):
    """Класс OpenAI делает запрос и отдает ответ ИИ-помощника для диалога с Клиентом."""

    def handle(self):
        phrase = self.get_request()
        phrase = self.clear_text(phrase)
        self.context.set_phrase(phrase)
        say(self.context)

    def get_request(self):
        try:
            return openai.Completion.create(
                model="text-davinci-003",
                prompt=self.context.prompt,
                temperature=0.9,
                max_tokens=250,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[self.context.user.name, self.context.robot.name],
            )["choices"][0]["text"]  # type: ignore
        except Exception as e:
            print(e)

    @staticmethod
    def clear_text(text):
        while text and not text[:1].isalpha():
            text = text[1::]
        while text and text[-1:] not in [".", "?", "!", ""]:
            text = text[:-1]
        if not text:
            return
        return text.replace("\n", "")


class SpeechToText(Dialog):
    def handle(self):
        listen(self.context)
        phrase = self.context.phrase.split(":")[1].replace(" ", "")
        if not phrase:
            self.handle()


class User(SpeechToText):
    """Класс User хранит информацию о пользователе"""

    def __init__(self, name):
        self.name = name


class Robot(OpenAI):
    """Класс Robot хранит информацию о голосовом ассистенте ИИ-помощнике."""

    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    user = User("Клиент")
    robot = Robot("ИИ-помощник")
    context = Context(user, robot)
    while True:
        context.request()
