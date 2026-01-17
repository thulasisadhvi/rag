import os
from typing import List, Dict, Any
from unstructured.partition.pdf import partition_pdf

class DocumentParser:
    def __init__(self, image_output_dir: str = "src/assets/extracted_images"):
        """
        Initializes the parser.
        :param image_output_dir: Directory to save images extracted from PDFs.
        """
        self.image_output_dir = image_output_dir
        os.makedirs(self.image_output_dir, exist_ok=True)

    def parse_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parses a PDF file to extract text, tables, and images.
        """
        print(f"Processing PDF: {file_path}...")
        
        # partition_pdf is the magic function that splits the PDF into elements
        # strategy="hi_res" is needed for table and image extraction
        elements = partition_pdf(
            filename=file_path,
            strategy="hi_res", 
            extract_images_in_pdf=True,
            image_output_dir_path=self.image_output_dir,
            infer_table_structure=True,
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
        )

        extracted_data = []

        for element in elements:
            # Common metadata for all elements
            metadata = {
                "source": file_path,
                "page_number": element.metadata.page_number,
                "filename": os.path.basename(file_path)
            }

            # Handle Tables specifically to preserve structure
            if "Table" in str(type(element)):
                extracted_data.append({
                    "type": "table",
                    "content": element.metadata.text_as_html, # Keep HTML for structure
                    "text_summary": str(element), # Plain text for searching
                    "metadata": metadata
                })
            
            # Handle Images (The element text will often be empty, but metadata has image info)
            elif "Image" in str(type(element)):
                # Note: 'partition_pdf' saves the image to disk automatically.
                # We need to link the text chunk to that image file.
                image_path = element.metadata.image_path
                extracted_data.append({
                    "type": "image",
                    "content": "Image extracted from page.",
                    "image_path": image_path,
                    "metadata": metadata
                })

            # Handle Regular Text
            else:
                extracted_data.append({
                    "type": "text",
                    "content": str(element),
                    "metadata": metadata
                })

        return extracted_data

if __name__ == "__main__":
    # Simple test to verify it works
    parser = DocumentParser()
    # Ensure you have a test PDF in sample_documents to run this
    # data = parser.parse_pdf("sample_documents/test.pdf")
    # print(f"Extracted {len(data)} elements.")