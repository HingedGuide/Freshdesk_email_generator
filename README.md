# AI Email Generator for Freshdesk

Dit project genereert AI-gestuurde e-mailreacties op Freshdesk-supporttickets met behulp van het Mistral-model via Ollama. Het bevat een interactieve GUI en ondersteunt meerdere talen.

## 📌 Functionaliteiten
- Ophalen en verwerken van Freshdesk-tickets
- Automatische taalherkenning
- AI-gegenereerde e-mailantwoorden met Mistral
- Interactieve GUI voor gebruiksgemak
- Ondersteuning voor meertalige e-mails

## 📂 Bestanden
- `email_generator.py` – Hoofdscript dat het e-mailgeneratieproces beheert
- `prompt_loader.py` – Laadt en verwerkt prompt-templates
- `email_gui.py` – Interactieve GUI voor gebruikers
- `prompts.json` – Bevat promptstructuren voor AI-generatie
- `requirements.txt` – Lijst met vereiste afhankelijkheden

## 🛠 Installatie
### 1. Vereisten installeren
Zorg ervoor dat je Python geïnstalleerd hebt (versie 3.8+ aanbevolen).

```sh
pip install -r requirements.txt
```

### 2. Ollama en Mistral installeren
Dit project vereist het **Mistral** model via Ollama. Download eerst Ollama via ollama.com en installeer het als volgt:

```sh
ollama run mistral
```

### 3. Freshdesk-configuratie
Maak een bestand `config.py` en voeg je Freshdesk API-sleutel en domein toe:

```python
class Config:
    FRESHDESK_DOMAIN = "jouw_domein.freshdesk.com"
    FRESHDESK_API_KEY = "jouw_api_sleutel"
```

## 🚀 Gebruik
Om de CLI-versie te gebruiken:

```sh
python email_generator.py
```

Voor de GUI-versie:

```sh
python email_gui.py
```

## 📌 Opmerkingen
- Zorg ervoor dat je Freshdesk API-sleutel correct is ingesteld.
- Het project ondersteunt meerdere talen; zorg ervoor dat `prompts.json` correct geconfigureerd is.
- Lees het gegenereerde e-mailantwoord voordat je het verzendt.

## 📜 Licentie
Dit project wordt uitgebracht onder de GPLv3 licentie. Zie LICENSE voor meer details.

