# /src/validators/removal_validator.py
import json
import logging

logger = logging.getLogger(__name__)

def validate_removal_instructions(instructions: str) -> bool:
    """
    Validate removal instructions provided as JSON.
    Returns True if valid, False otherwise.
    """
    try:
        data = json.loads(instructions)
        if "targets" in data and isinstance(data["targets"], list):
            logger.debug("Removal instructions validated successfully.")
            return True
        else:
            logger.error("Removal instructions missing 'targets' list.")
            return False
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in removal instructions: {e}")
        return False
