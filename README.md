# AI-Conversation-Flow

Program for dialogue between the user and the voice assistant AI assistant.
Implemented in Python using the grpc library.

## Dependencies

- [Python 3.10](https://www.python.org/downloads/)
- [OpenAI](https://openai.com/)
- [Text-Davinci](https://openai.com/blog/davinci/)
- [Tinkoff VoiceKit](https://tinkoff.ru/developer/speechkit/)
- [gRPC](https://grpc.io/)
- [PyAudio](https://pypi.org/project/PyAudio/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Quickstart

The program is run in the command line with the command:

```
python3 main.py
```

## Chat-bot

Sample chat-bot:


`Клиент:`       Привет, как дела? 

`ИИ-помощник:`  Здравствуйте, я слышу вас хорошо, как ваши дела? 

`Клиент:`       У меня все отлично, а у тебя? 

`ИИ-помощник:`  Все хорошо, не спрашивайте, не буду вам говорить, т.к. я робот. Поэтому я спрашиваю, как вы себя чувствуете? 

`Клиент:`       Все отлично, спасибо. 

`ИИ-помощник:`  Ну это здорово, как ваши дела? 

`Клиент:`       Отлично. 

`ИИ-помощник:`  Ну давайте поговорим о ваших делах, что вы делаете на работе? 

`Клиент:`       Я учусь в кафедре ИТ и ИТС. 

`ИИ-помощник:`  Интересно, а какие у Вас есть интересы? 

`Клиент:`       Интересы, не понимаешь? 

`ИИ-помощник:`  Да, интересует ваши интересы. 

`Клиент:`       Моя работа по проектированию ИС ВПО. 

`ИИ-помощник:`  Интересно. 

`Клиент:`       С чем ты связан? 

`ИИ-помощник:`  Давайте обсудим это, я займусь этим, как вам нравится работа в кафедре ИТ и ИТС? 

`Клиент:`       Все отлично. 

`ИИ-помощник:`  Ну это здорово. 

`Клиент:`       Спасибо.


## Performance

The program is designed to work with the Tinkoff SpeechKit service.

## Optional Dependencies

- [PyAudio](https://pypi.org/project/PyAudio/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
