<p align="center">
  <img src="site/mark.svg" width="72" height="72" alt="AURA project mark">
</p>
<h1 align="center">AURA — Adaptive Understanding and Response Assistant</h1>
<p align="center">
  <a href="https://www.python.org/downloads/"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-52734D"></a>
  <img alt="Experimental prototype" src="https://img.shields.io/badge/status-experimental-d4a654">
</p>

**AURA is an experimental voice and camera assistant prototype.** It explores spoken questions and optional visual context through a local Python command-line app that connects to speech and AI providers.

> This repository has not been evaluated with its intended users and is not a validated accessibility aid. Model output can be wrong. Do not rely on it for medicines, emergencies, or other safety-critical tasks.

## Project presentation

The static project presentation is deployed at [aura.devayushrout.me](https://aura.devayushrout.me). It is informational only and does not provide the device-backed assistant. The actual prototype runs locally on a configured machine.

![Existing AURA project demo](demo_preview.gif)

*Existing demo animation included in the repository. It is project media, not a fresh capture from this review; the full hardware-backed flow was not re-run.*

[Watch the existing demo video](https://youtu.be/sjE98X0MNao)

## Problem and intended users

The project explores whether voice input and an optional camera request can help someone ask about an object or short printed information hands-free. It was motivated by accessibility needs, but there has been no user research or accessibility evaluation. Treat it as an engineering prototype, not assistive technology for real-world reliance.

## User workflow

1. A local Porcupine wakeword model listens for its configured phrase.
2. The user asks a question; microphone audio is streamed to Deepgram for transcription.
3. Groq routes the transcript. A visual request can capture a still image and send it to Groq for analysis.
4. A response is spoken through the local audio output.

The CLI handles one request per wakeword activation. The vision path has no preview screen: captured images are held in the ignored `.runtime/` directory for the request and deleted when it succeeds or fails.

## Architecture

```text
Local microphone + Porcupine wakeword
                   │
                   ▼
     Deepgram streaming transcription
                   │ transcript
                   ▼
        Groq intent and response
           │               │
           │ visual request│ optional still image
           └──── local camera ───────► Groq vision
                   │
                   ▼
       Local text-to-speech output
```

- **Wakeword:** Picovoice Porcupine, using a platform-specific `.ppn` file that is not included.
- **Speech recognition:** Deepgram Flux streaming API.
- **Intent and vision:** Groq API.
- **Camera access:** OpenCV on the local machine.
- **Speech output:** Edge TTS and local audio playback.

Speech audio is sent to Deepgram. Transcripts and, when the vision path is used, an image are sent to Groq. Check each provider's current privacy and retention terms before use, and get permission before capturing another person's speech or image.

## Run locally

### Requirements

- Python 3.10 or newer (the pinned NumPy 2.2.6 package requires Python 3.10+).
- Microphone and speakers; a camera is needed for visual questions.
- Internet access and API credentials for Deepgram, Groq, and Picovoice.
- A compatible platform-specific Porcupine keyword model. It is intentionally not committed here.
- Audio system libraries or drivers may need platform-specific setup for PyAudio, sounddevice, and simpleaudio.

### Setup

```bash
git clone https://github.com/ayushcodes13/AURA.git
cd AURA
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp config/.env.example config/.env
```

Fill `config/.env` with your own credentials:

```env
GROQ_API_KEY=...
DEEPGRAM_API_KEY=...
PICOVOICE_ACCESS_KEY=...
```

Download the Porcupine keyword model from Picovoice for your platform and place it under `wakeword/` using the filename expected by [`wakeword/aura_wakeword.py`](wakeword/aura_wakeword.py): `hey_aura_new.ppn` on macOS or `hello_aura_rpi.ppn` on other platforms. The expected file is not distributed with this source. Keep credentials private; `config/.env` and keyword files are ignored by Git.

Start the CLI from the repository root:

```bash
python main.py
```

You must supply the physical devices, provider credentials, and keyword model before the complete workflow can run. This review did not exercise a live provider or hardware session.

## Tests and verification

Run the deterministic visual-intent tests:

```bash
python -m unittest discover -v
```

These tests cover phrases that should and should not directly trigger the camera path. They do not exercise microphones, cameras, network APIs, wakeword detection, or speech output. The intent-router and TTS demo scripts are interactive demos, not automated tests.

## Deployment and privacy boundaries

The device-backed CLI is designed to run locally. Vercel cannot provide its microphone, camera, or speaker access, and this project has no serverless application runtime. The static project presentation is hosted at [aura.devayushrout.me](https://aura.devayushrout.me), but remains clearly distinct from the actual local prototype.

The application sends speech audio to Deepgram and transcripts to Groq; a visual request also sends a still image to Groq. AURA is a prototype, not a privacy-preserving or clinically validated product. Do not use it for high-stakes decisions.

## Repository layout

```text
main.py                 CLI orchestration
wakeword/               Local Porcupine wakeword listener
stt/                    Deepgram streaming transcription
intent/                 Intent and visual-request routing
llm/                    Groq provider integration
tools/                  Request executor and camera capture
tts/                    Spoken response output
chimes/                 Audio feedback
config/                 Environment example
site/                   Static project presentation
```

## License

MIT. See [LICENSE](LICENSE).
