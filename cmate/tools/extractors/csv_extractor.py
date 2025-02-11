# /src/extractors/csv_extractor.py
import os
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def extract_metrics_to_csv(file_paths: list, output_file: str) -> None:
    """
    Extract simple metrics (e.g., file path and file size) from the given file paths
    and save the data to a CSV file.
    """
    data = []
    for file_path in file_paths:
        try:
            path = Path(file_path)
            size = path.stat().st_size
            data.append({
                "Path": str(path),
                "Size": size
            })
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"CSV metrics saved to {output_file}")
