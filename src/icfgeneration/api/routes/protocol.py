from fastapi import APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
import os
import tempfile
import traceback
from icfgeneration.logger.logger_setup import loguru_setup
from icfgeneration.utils.constants import env_path
from icfgeneration.utils.Parser import Parser
from icfgeneration.models.protocol import (
    Protocol,
    ProtocolSection,
)

load_dotenv(env_path)

logger = loguru_setup()

router = APIRouter(prefix="/protocol", tags=["protocol"])


@router.post("/parse")
async def parse_protocol(file: UploadFile = File(...)):
    try:
        logger.info(f"Parsing protocol {file.filename}")

        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Create a temporary file to store the uploaded content
        file_extension = (
            os.path.splitext(file.filename)[1] or ".pdf"
        )  # Default to .pdf if no extension
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=file_extension
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            parser = Parser()
            sections, breadcrumbs, parsed_data = parser.process_file(temp_file_path)
            sections = [
                ProtocolSection(
                    text=section.page_content,
                )
                for section in sections
            ]
            return Protocol(
                sections=sections,
                breadcrumbs=breadcrumbs,
                parsed_data=parsed_data,
            )
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file {temp_file_path}")
    except Exception as e:
        logger.error(
            f"Error processing protocol file: {str(e)}\n{traceback.format_exc()}"
        )
        raise
