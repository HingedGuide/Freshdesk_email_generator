import json
from pathlib import Path


class PromptLoader:
    def __init__(self):
        self.prompts = self._load_prompts()

    # Read the prompts from the prompts.json file
    def _load_prompts(self):
        try:
            prompts_path = Path(__file__).parent / "prompts.json"
            with open(prompts_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load prompts: {str(e)}")

    # retrieve the prompt so that it can be used
    def get_prompt(self, language: str, customer_content: str, employee_notes: str) -> str:
        lang_data = self.prompts.get(language.lower(), self.prompts['en'])

        return lang_data['template'].format(
            role=lang_data['guidelines']['role'],
            tone="\n- ".join(lang_data['guidelines']['tone']),
            structure="\n".join([f"- {key}: {value}" for key, value in lang_data['guidelines']['structure'].items()]),
            product_rules="\n- ".join(lang_data['guidelines']['product_rules']),
            examples="\n\n".join(
                [f"**{key}**:\n{value}" for key, value in lang_data['guidelines']['examples'].items()]),
            formatting_rules="\n- ".join(lang_data['guidelines']['formatting_rules']),
            closing_advice=lang_data['guidelines']['closing_advice'],  # Add this line
            customer_email=customer_content,
            employee_response=employee_notes
        )