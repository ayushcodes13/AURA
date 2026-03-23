# AURA — Adaptive Understanding and Response Assistant

**A voice-first assistive AI system designed to help elderly individuals, visually impaired users, and people with low literacy understand their surroundings using natural speech and vision.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white)](LICENSE)

Unlike traditional voice assistants that rely only on verbal commands, AURA allows users to **show instead of explain**, enabling more accurate and accessible assistance in real-world situations.

---

## Demo Video
<div style="text-align: center;">

![AURA Demo](demo_preview.gif)

[📺 Watch Full Demo on YouTube](https://youtu.be/sjE98X0MNao)

*A demonstration of AURA's voice-first and vision-assisted workflow in action.*

</div>

---

## Problem Statement

Many elderly and visually impaired individuals face daily challenges in understanding written information, identifying objects, or interpreting their surroundings.
Most existing digital assistants assume that users can clearly describe what they see or read, which is often not possible.

This leads to:
- 🏥 Dependence on caregivers for simple tasks
- 📝 Difficulty reading labels, notices, or documents
- 🔍 Inability to identify everyday objects confidently
- 😔 Reduced independence and quality of life

**Voice alone is insufficient when the user cannot describe the problem.**

---

## Proposed Solution

AURA is a **voice-first assistive system enhanced with vision**.

Users interact with AURA using natural speech.
When voice is insufficient, AURA uses a camera to understand the user's environment and provide a spoken explanation.

The system is designed to work **without screens**, making it accessible to users with visual or literacy limitations.

---

## Target Users

- 👵 Elderly individuals living independently
- 👁️ Visually impaired users
- 📚 Low-literacy users

---

## Locked Core Use Case

### Understanding Physical Objects and Written Information

AURA helps users understand objects or text they cannot identify or read themselves.

**Example scenarios:**
- 💊 Identifying medicines or household objects
- 🏷️ Reading labels, notices, or short printed text
- 📸 Understanding what is placed in front of the user

This single, well-defined use case addresses multiple societal needs without increasing system complexity.

---

## System Overview

AURA operates as a **session-based, real-time voice system**:

1. 🎤 User activates AURA using a wakeword (once per session)
2. 📝 Speech is captured and transcribed in real time
3. 🤖 The system determines whether visual context is required
4. 📷 If needed, an image is captured using a camera
5. 🗣️ The AI processes the input and responds via speech

The interaction is designed to feel natural and conversational, without requiring repeated wakeword usage.

---

## Key Features

- 🔊 Wakeword-based voice interaction
- ⚡ Real-time speech-to-text processing
- 👁️ Vision-assisted understanding when required
- 🗣️ Spoken responses optimized for clarity
- 🔄 Session-based interaction flow
- 🧩 Modular architecture for future expansion

---

## Why AURA Is Different

- 🎯 Built for users who cannot always describe problems verbally
- 🔐 Vision is used selectively to protect user privacy
- 💬 Supports conversational corrections and interruptions
- 🎯 Focuses on accessibility over feature overload
- ⚡ Designed as a real-time system, not a scripted demo

---

## Societal Relevance

The problem addressed by AURA was identified by observing everyday challenges faced by elderly individuals and users with limited literacy, particularly in understanding visual information independently.

AURA aims to:
- 🤲 Reduce dependence on caregivers
- 💪 Improve confidence in daily activities
- 🌟 Enhance quality of living through assistive AI

---

## Current Project Status

The project has completed approximately **40% of the proposed work**, including:

- ✅ Functional voice interaction
- ✅ Real-time speech recognition
- ✅ Vision-assisted responses
- ✅ Spoken output system
- ✅ Session-based interaction design

### Planned Future Enhancements

- 🧠 Short-term conversational memory
- ⏩ Improved interruption handling
- 🔍 Enhanced vision interpretation

---

## Project Context

This project is developed as part of a **college project exhibition**, aligned with societal needs and assistive technology objectives.
It is designed with real-world constraints, accessibility, and usability in mind.

---

## Technical Architecture

### Core Components

- **Wake Word Engine**: Picovoice Porcupine for "Hey Aura" detection
- **Speech Recognition**: Deepgram Flux real-time API
- **Vision Processing**: OpenCV for image capture
- **AI Processing**: Groq LLM for text and vision understanding
- **Text-to-Speech**: Edge TTS for spoken responses

### Project Structure

```
AURA/
├── main.py                 # Entry point and session management
├── wakeword/               # Wake word detection
├── stt/                    # Speech-to-text processing
├── intent/                 # Intent routing and classification
├── tools/                  # Tool execution and vision capture
├── llm/                    # LLM provider integration
├── tts/                    # Text-to-speech generation
├── chimes/                 # Audio feedback system
├── config/                 # Configuration and environment
└── requirements.txt        # Python dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Camera device
- Microphone
- Speakers
- Internet connection

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AURA
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys in `config/.env`:
   ```env
   DEEPGRAM_API_KEY=your_deepgram_key
   PICOVOICE_ACCESS_KEY=your_picovoice_key
   GROQ_API_KEY=your_groq_key
   ```

4. Run the application:
   ```bash
   python main.py
   ```

---

## Contributing

This project was developed as part of a college project exhibition. Contributions are welcome to help improve accessibility and expand functionality for our target users.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Developed with consideration for elderly and visually impaired individuals
- Focused on real-world accessibility challenges
- Designed with practical impact in mind
