# AI-Conversation-Flow

Program for dialogue between the user and the voice assistant AI assistant.
Implemented in Python using the grpc library.

## About

The program realizes a [conversation flow](https://www.acrwebsite.org/volumes/7030/volumes/v11/NA-11) with openAI-engine and telephony. 

It is implemented in the form of a script based on the [Tinkoff STT](https://tinkoff.ru/developer/speechkit/) and [Tinkoff TTS](https://tinkoff.ru/developer/speechkit/) services.

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

## Performance

The program is designed to work with the Tinkoff SpeechKit service.

## Optional Dependencies

- [PyAudio](https://pypi.org/project/PyAudio/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
