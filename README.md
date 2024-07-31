# Live Music Transcription with Fast Fourier Transforms

Flutter based cross-platform app for live music transcription from mic input using Fast Fourier Transforms (FFT) to detect dominant frequencies and their corresponding notes, octave, and pitch. Written in Python using [Flet](https://flet.dev/) for Flutter and [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio input. Supports desktop, android, iOS and web.

![notes](https://github.com/user-attachments/assets/43d132db-71ac-41a0-aef5-58c4b542b1d8)

## Usage

Install required packages with pip or poetry and run the app for desktop with:

```bash
flet run
```

Testing on android, iOS, web (respectively):

```bash
flet run --android
flet run -p ios
flet run -p web
```

## Build

See platform specific build instructions in [Flet documentation](https://flet.dev/docs/publish).
