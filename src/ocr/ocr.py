from pathlib import Path
from typing import List
from src.openai.client import OpenAIClient
from utils.logger import logger


class OCR:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        logger.info("OCR processor initialized")

    def extract_text(self, image_paths: List[Path]) -> str:
        """
        Extract text from images using OpenAI's vision capabilities.

        Args:
            image_paths: List of paths to images to process

        Returns:
            Extracted text content as a string
        """
        logger.info(f"Starting OCR text extraction for {len(image_paths)} images")

        response = self.openai_client.get_response(
            prompt="Extract all text visible in this image. \
                Respond ONLY with the exact text content from the image, nothing more. \
                No explanations, no additional context, no formatting instructions.",
            images=image_paths,
            model="gpt-4o",
        )

        logger.info(f"OCR extraction completed, extracted {len(response)} characters")

        return response
