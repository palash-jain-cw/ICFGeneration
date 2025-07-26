import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from icfgeneration.logger.logger_setup import loguru_setup
from typing import Literal
from icfgeneration.utils.utils import fix_markdown_for_streamlit

logger = loguru_setup()


class Parser:
    def __init__(self):
        """
        Initializes a new instance of the `parser` class.

        This class provides functionality for parsing word files to markdown and splitting their content by headers.
        """
        logger.info("Initializing parser...")
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
        ]  # Define a list of header patterns to split the content by
        self.splitter = MarkdownHeaderTextSplitter(
            self.headers_to_split_on
        )  # Create an instance of the `MarkdownHeaderTextSplitter` class to split the content by headers
        self.headers_syntax = {
            "Header 1": "#",
            "Header 2": "##",
            "Header 3": "###",
            "Header 4": "####",
        }  # Define a dictionary mapping header names to their corresponding Markdown syntax

    def parse_to_markdown(self, path_to_file):
        """
        Parses a Markdown file and returns its HTML representation.

        Args:
            path_to_file (str): The path to the Markdown file to be parsed.

        Returns:
            str: The HTML representation of the Markdown file.
        """
        logger.info(f"Parsing {path_to_file} to markdown...")
        return pymupdf4llm.to_markdown(
            path_to_file
        )  # Convert the PDF file to Markdown using the `pymupdf4llm` instance

    def split_markdown_by_headers(self, markdown_text):
        """
        Splits the content of a Markdown file by its headers and returns a list of sections.

        Args:
            markdown_text (str): The content of the Markdown file to be split.

        Returns:
            List[str]: A list of sections obtained by splitting the content by headers.
        """
        logger.info("Splitting markdown content by headers...")
        return self.splitter.split_text(
            markdown_text
        )  # Split the content by headers using the `MarkdownHeaderTextSplitter` instance

    def process_document(self, document_split_by_sections):
        logger.info("Processing document split by sections...")
        return [self.process_section(section) for section in document_split_by_sections]

    def process_section(self, section):
        logger.info(f"Processing section {list(section.metadata.values())}...")
        section_dict = section.metadata
        breadcrumb = list(section_dict.values())
        section_dict["section_content"] = section.page_content
        for k, v in section_dict.items():
            if k in self.headers_syntax:
                section_dict[k] = f"{self.headers_syntax[k]} {v}"
        section_dict["section_content"] = "\n ".join(section_dict.values())
        document = Document(
            page_content=section_dict["section_content"],
            metadata={"sectionName": " -> ".join(breadcrumb)},
        )
        return document

    def process_file(self, file_path):
        logger.info(f"Processing file {file_path}...")
        process_dict = {}
        process_dict["parsed_data"] = self.parse_to_markdown(file_path)
        process_dict["parsed_data"] = fix_markdown_for_streamlit(
            process_dict["parsed_data"]
        )
        sections = self.split_markdown_by_headers(
            process_dict["parsed_data"],
        )
        process_dict["sections"] = self.process_document(sections)
        process_dict["breadcrumbs"] = [
            section.metadata["sectionName"] for section in process_dict["sections"]
        ]
        return (
            process_dict["sections"],
            process_dict["breadcrumbs"],
            process_dict["parsed_data"],
        )
