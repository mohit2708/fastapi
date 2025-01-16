import os
import logging
from datetime import datetime

def configure_logging():
    # Generate the current date
    current_date = datetime.now().strftime("%d_%m_%Y")

    # Define the log folder and file name
    log_folder = "logs"
    log_file_name = f"app_{current_date}.log"

    # Create the log folder if it doesn't exist
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Create the full path to the log file
    log_file_path = os.path.join(log_folder, log_file_name)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),  # Output logs to the specified file
            logging.StreamHandler()              # Output logs to the console
        ]
    )

# Call the function to configure logging
configure_logging()

# Get the logger
logger = logging.getLogger(__name__)