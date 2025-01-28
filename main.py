# Import required libraries
from config import Config  # Contains sensitive credentials
import requests  # For making HTTP requests to Freshdesk
import re  # Regular expressions for text cleaning
from langdetect import detect, LangDetectException  # Language detection
import ollama  # For AI-generated email responses
from typing import Optional, Dict  # Type hints for better code clarity
from prompt_loader import PromptLoader


class EmailGenerator:
    """Main class that handles the email generation workflow"""

    def __init__(self):
        """Initialize the email generator with configuration and resources"""
        self.prompt_loader = PromptLoader()
        self._validate_config()  # Check if required settings exist
        self.session = self._create_session()  # Create reusable HTTP connection
        self.regex_patterns = self._compile_regex()  # Precompile regex for efficiency

    def _validate_config(self) -> None:
        """Safety check: Ensure required configuration values exist"""
        required = ['FRESHDESK_DOMAIN', 'FRESHDESK_API_KEY']
        for attr in required:
            # Check if each required setting exists and isn't empty
            if not hasattr(Config, attr) or not getattr(Config, attr):
                raise ValueError(f"Missing required Config attribute: {attr}")

    def _create_session(self) -> requests.Session:
        """Create a secure HTTP session with Freshdesk authentication"""
        session = requests.Session()
        session.auth = (Config.FRESHDESK_API_KEY, "X")  # API authentication
        session.headers.update({'Content-Type': 'application/json'})  # Set content type
        return session

    def _compile_regex(self) -> Dict[str, re.Pattern]:
        """Create regex patterns once for better performance"""
        return {
            'url': re.compile(r'https?://\S+'),  # Matches http/https URLs
            'markers': re.compile(r'\{\{\s*\d+\s*\}\}'),  # Matches {{number}} patterns
            'whitespace': re.compile(r'\s+')  # Matches multiple spaces
        }

    def get_customer_content(self, ticket_id: str) -> Optional[str]:
        """Fetch and clean customer ticket data from Freshdesk"""
        url = f"https://{Config.FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}"

        try:
            # Make API request with 15-second timeout
            response = self.session.get(url, timeout=15)
            response.raise_for_status()  # Raise error for bad status codes

            ticket = response.json()  # Convert response to Python dictionary

            # Extract important fields with default values
            subject = ticket.get("subject", "No Subject")
            description = ticket.get("description_text", "")

            return self._format_content(subject, description)

        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            return None
        except KeyError as e:
            print(f"Missing key in response: {str(e)}")
            return None

    def _format_content(self, subject: str, description: str) -> str:
        """Combine and structure ticket subject and description"""
        clean_description = self._clean_text(description)
        return f"Subject: {subject}\n\n{clean_description}"

    def _clean_text(self, text: str) -> str:
        """Remove unwanted patterns and format text consistently"""
        # Step 1: Remove URLs
        text = self.regex_patterns['url'].sub('', text)
        # Step 2: Remove Freshdesk markers like {{5}}
        text = self.regex_patterns['markers'].sub('', text)
        # Step 3: Replace multiple spaces with single space
        text = self.regex_patterns['whitespace'].sub(' ', text).strip()
        return text

    def detect_language(self, text: str) -> str:
        """Identify the language of customer's text with fallback to English"""
        try:
            # Use first 200 characters for faster detection
            return detect(text[:200])
        except LangDetectException:
            return 'en'  # Default to English if detection fails

    def get_employee_response(self) -> str:
        """Collect agent's notes through multi-line input"""
        print("\nEnter response notes (press Enter twice to finish):")
        lines = []
        empty_count = 0  # Track consecutive empty lines

        while empty_count < 2:
            line = input().strip()
            if not line:
                empty_count += 1
            else:
                empty_count = 0  # Reset counter on non-empty line
                lines.append(line)
        return '\n'.join(lines)

    def generate_email(self, customer_content: str, employee_notes: str, language: str = 'en') -> Optional[str]:
        """Generate email using structured JSON prompts"""
        try:
            prompt = self.prompt_loader.get_prompt(
                language=language,
                customer_content=customer_content,
                employee_notes=employee_notes
            )

            response = ollama.generate(
                model='mistral',
                prompt=prompt,
                options={'temperature': 0.5, 'max_tokens': 500}
            )
            return self._postprocess_email(response['response'])

        except Exception as e:
            print(f"Generation Error: {str(e)}")
            return None

    def _postprocess_email(self, text: str) -> str:
        """Clean up any remaining template markers"""
        return text.replace("{customer_name}", "[Naam klant]").strip()

    def _get_prompt_template(self, language: str) -> str:
        """Provide AI instructions in different languages"""
        templates = {
            'en': """[English template...]""",
            'nl': """[Dutch template...]""",
            'fr': """[French template...]""",
            'de': """[German template...]"""
        }
        # Fallback to English if language not supported
        return templates.get(language, templates['en'])

    def process_ticket(self, ticket_id: str) -> Optional[str]:
        """Complete workflow for processing a ticket"""
        # Validate ticket ID format
        if not ticket_id.isdigit():
            print("Error: Ticket ID must be numeric")
            return None

        # Step 1: Get customer message
        if not (customer_content := self.get_customer_content(ticket_id)):
            return None

        # Step 2: Detect language
        language = self.detect_language(customer_content)
        print(f"Detected language: {language.upper()}")

        # Step 3: Get agent input
        if not (employee_notes := self.get_employee_response()):
            print("Error: Empty employee response")
            return None

        # Step 4: Generate and return email
        return self.generate_email(customer_content, employee_notes, language)


if __name__ == "__main__":
    """Main entry point when run directly"""
    try:
        generator = EmailGenerator()
        # Get ticket ID from user input
        ticket_id = input("Enter Freshdesk Ticket ID: ").strip()

        if generated_email := generator.process_ticket(ticket_id):
            print("\n=== Generated Email ===")
            print(generated_email)
        else:
            print("Failed to generate email response.")

    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")