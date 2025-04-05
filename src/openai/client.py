import os
import base64
from typing import List, Optional
from utils.logger import logger
from pathlib import Path

from openai import OpenAI
from openai.types.chat import ChatCompletion
from dotenv import load_dotenv


load_dotenv()


class OpenAIClient:
    """
    A class for interacting with the OpenAI API.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI client.

        Args:
            api_key: Optional API key. If not provided, it will be loaded from environment variables.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            )
            raise ValueError("OpenAI API key not found.")

        self.client = OpenAI(api_key=self.api_key)
        logger.info("OpenAI client initialized successfully")

    @staticmethod
    def encode_image(image_path: Path) -> str:
        """
        Encode an image file to base64.

        Returns:
            str: Base64 encoded image.
        """
        if not image_path.exists():
            logger.error(f"Image file not found: {image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")

        logger.debug(
            f"Encoded image {image_path.name} to base64 ({len(encoded)} bytes)"
        )
        return encoded

    def get_raw_response(
        self,
        prompt: str,
        model: str = "gpt-4o",
        images: Optional[List[Path]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[dict] = None,
    ) -> ChatCompletion:
        """
        Generate a response from OpenAI models and return the raw API response.

        Args:
            prompt: The text prompt to send to the model.
            model: The OpenAI model to use.
            images: Optional list of images to include with the prompt.
            temperature: Controls randomness.
            max_tokens: Maximum number of tokens to generate.
            response_format: Optional response format specification.

        Returns:
            ChatCompletion: The raw response from the OpenAI API.

        Raises:
            Exception: For API errors or connectivity issues.
        """
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

        if images:
            try:
                # Only support a single image for now
                image_path = images[0]
                base64_image = self.encode_image(image_path)
                # Include the base64 image in a custom structure
                messages[0]["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    }
                )
            except Exception as e:
                logger.error(f"Failed to prepare image: {str(e)}")
                raise

        params = {
            "model": model,
            "messages": messages,
        }

        if max_tokens:
            params["max_tokens"] = max_tokens

        if temperature:
            params["temperature"] = temperature

        if response_format:
            params["response_format"] = response_format

        # Update tracking params with full info

        logger.info(f"Sending request to OpenAI API with model: {model}")
        response = self.client.chat.completions.create(**params)

        logger.info(
            f"Received response from OpenAI API: {response.usage.total_tokens} tokens used"
        )
        return response

    def get_response(
        self,
        prompt: str,
        model: str = "gpt-4o",
        images: Optional[List[Path]] = None,
        temperature: Optional[float] = 0.3,
        max_tokens: Optional[int] = None,
        response_format: Optional[dict] = None,
    ) -> str:
        """
        Generate a response from OpenAI models and return the text content.

        Args:
            prompt: The text prompt to send to the model.
            model: The OpenAI model to use (default: gpt-4o).
            images: Optional list of images to include with the prompt.
            temperature: Controls randomness (0-1.0).
            max_tokens: Maximum number of tokens to generate.
            response_format: Optional response format specification.

        Returns:
            str: The response text from the OpenAI API.
        """
        params = {
            "prompt": prompt,
            "model": model,
            "images": images,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": response_format,
        }

        response = self.get_raw_response(**params)
        content = response.choices[0].message.content

        if content:
            return content
        else:
            logger.error("No content returned from OpenAI API")
            raise ValueError("No content returned from OpenAI API")
