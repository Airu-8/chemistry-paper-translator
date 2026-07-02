import os
from typing import Optional
import openai

class Translator:
    """Handle translation of text using AI APIs"""
    
    def __init__(self):
        self.api_provider = os.getenv("TRANSLATION_API_PROVIDER", "openai")
        self.api_key = os.getenv("TRANSLATION_API_KEY")
        
        if not self.api_key:
            raise ValueError("TRANSLATION_API_KEY not set in environment variables")
    
    async def translate(self, text: str, target_language: str = "Japanese") -> str:
        """Translate text to target language with context awareness"""
        
        if self.api_provider == "openai":
            return await self._translate_with_openai(text, target_language)
        elif self.api_provider == "claude":
            return await self._translate_with_claude(text, target_language)
        else:
            raise ValueError(f"Unknown API provider: {self.api_provider}")
    
    async def _translate_with_openai(self, text: str, target_language: str) -> str:
        """Translate using OpenAI API"""
        try:
            openai.api_key = self.api_key
            
            prompt = f"""You are an expert translator specializing in chemistry and scientific papers.
            
Translate the following chemistry research paper to {target_language}.
Preserve:
- All chemical formulas and notation
- Scientific terminology with proper translation
- Document structure and formatting
- References and citations
- Table and figure captions

Provide only the translated text without additional commentary.

Text to translate:
{text}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert scientific translator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"OpenAI translation failed: {str(e)}")
    
    async def _translate_with_claude(self, text: str, target_language: str) -> str:
        """Translate using Anthropic Claude API"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            prompt = f"""You are an expert translator specializing in chemistry and scientific papers.
            
Translate the following chemistry research paper to {target_language}.
Preserve:
- All chemical formulas and notation
- Scientific terminology with proper translation
- Document structure and formatting
- References and citations
- Table and figure captions

Provide only the translated text without additional commentary.

Text to translate:
{text}"""
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        
        except Exception as e:
            raise Exception(f"Claude translation failed: {str(e)}")
