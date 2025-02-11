# /src/processors/llm_processor.py
import logging
from ..code.code_extractor import extract_code_blocks

logger = logging.getLogger(__name__)

def process_llm_output(text: str) -> list:
    """
    Process LLM output text.
    Extract code blocks and simulate a patch response.
    In this beta version, simply prepend a comment to each code block.
    """
    code_blocks = extract_code_blocks(text)
    patched_blocks = []
    for block in code_blocks:
        patched_code = f"# Patched by LLM\n{block['code_block']}"
        patched_blocks.append({
            "language": block["language"],
            "code_block": patched_code
        })
    logger.debug(f"Processed {len(patched_blocks)} patched code blocks from LLM output.")
    return patched_blocks
