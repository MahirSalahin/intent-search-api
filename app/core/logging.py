import logging
import socket
import sys
from datetime import datetime

def setup_logging():
    """Configure application logging with console and optional Loki output"""
    # Reset root logger configuration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure basic logging to make sure we see everything
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',  # Simplified format
    )

    # Configure our application logger with explicit handler
    logger = logging.getLogger("api")
    
    # Clear any existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Set to DEBUG to capture all levels
    logger.setLevel(logging.DEBUG)
    
    # Create console handler for our logger
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Create simplified formatter that only shows status code (level) and message
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Make sure propagation is disabled to avoid duplicate logs
    logger.propagate = False
    
    # Setup Loki (optional) with the same simplified format
    try:
        import logging_loki
        loki_url = "http://localhost:3100/loki/api/v1/push"
        
        loki_handler = logging_loki.LokiHandler(
            url=loki_url,
            tags={"service": "api-server", "host": socket.gethostname()},
            version="1",
        )
        loki_handler.setFormatter(formatter)  # Use the same simplified formatter
        loki_handler.setLevel(logging.INFO)
        logger.addHandler(loki_handler)
    except Exception as e:
        print(f"Failed to configure Loki: {str(e)}")
    
    return logger