import os
import pytest
from src.ingestion.document_parser import DocumentParser
from src.ingestion.image_processor import ImageProcessor

def test_parser_initialization():
    """
    Checks if DocumentParser initializes and creates its output directory.
    """
    output_dir = "tests/test_output_images"
    parser = DocumentParser(image_output_dir=output_dir)
    
    assert parser is not None
    assert os.path.exists(output_dir)
    
    # Cleanup: Remove the test directory after the test
    if os.path.exists(output_dir):
        os.rmdir(output_dir)

def test_image_processor_initialization():
    """
    Checks if ImageProcessor initializes correctly.
    """
    processor = ImageProcessor()
    assert processor is not None

def test_parse_dummy_file():
    """
    Optional: Checks if the processor handles a non-existent file gracefully.
    """
    processor = ImageProcessor()
    result = processor.process_image("non_existent_file.png")
    assert result is None  # It should return None, not crash