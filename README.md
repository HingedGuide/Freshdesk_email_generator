
# AI Email Generator for Freshdesk

This project generates AI-driven email responses to Freshdesk support tickets using the Mistral model via Ollama. It features an interactive GUI and supports multiple languages.

## 📌 Features
- Fetching and processing Freshdesk tickets
- Automatic language detection
- AI-generated email responses with Mistral
- Interactive GUI for ease of use
- Multilingual email support

## 📂 Files
- `email_generator.py` – Main script managing the email generation process
- `prompt_loader.py` – Loads and processes prompt templates
- `email_gui.py` – Interactive GUI for users
- `prompts.json` – Contains prompt structures for AI generation
- `requirements.txt` – List of required dependencies

## 🛠 Installation
### 1. Install Requirements
Ensure you have Python installed (version 3.8+ recommended).

```sh
pip install -r requirements.txt
```

### 2. Install Ollama and Mistral
This project requires the **Mistral** model via Ollama. First, download Ollama from ollama.com and install it as follows:

```sh
ollama run mistral
```

### 3. Freshdesk Configuration
Create a `config.py` file and add your Freshdesk API key and domain:

```python
import os

class Config:
    FRESHDESK_API_KEY = os.getenv('FRESHDESK_API_KEY', 'your_api_key')
    FRESHDESK_DOMAIN = 'yourcompany.freshdesk.com'
```

## 🚀 Usage
To use the CLI version:

```sh
python email_generator.py
```

For the GUI version:

```sh
python email_gui.py
```

## 📌 Notes
- Ensure your Freshdesk API key is set up correctly.
- The project supports multiple languages; make sure `prompts.json` is properly configured.
- Review the generated email response before sending it.

## 📜 License
This project is released under the GPLv3 license. See LICENSE for more details.
