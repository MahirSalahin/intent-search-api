import logging
import socket
import sys
import os

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
    
    # Setup Loki with detailed formatting for better Grafana visualization
    try:
        import logging_loki
        
        # Use docker service name if running in container, otherwise localhost
        loki_url = os.environ.get("LOKI_URL", "http://localhost:3100/loki/api/v1/push")
        
        # Create a more detailed formatter for Loki logs
        loki_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configure Loki handler with additional labels for better querying
        loki_handler = logging_loki.LokiHandler(
            url=loki_url,
            tags={
                "service": "ecommerce-api", 
                "host": socket.gethostname()
            },
            version="1",
            # Add these labels to make filtering by log level easier in Grafana
            additional_labels={
                "level": "%(levelname)s",
                "module": "%(module)s"
            }
        )
        
        # Use the detailed formatter
        loki_handler.setFormatter(loki_formatter)
        
        # IMPORTANT: Set level to DEBUG to capture all logs including ERROR
        loki_handler.setLevel(logging.DEBUG)
        
        logger.addHandler(loki_handler)
        logger.info("✅ Loki logging configured successfully")
        logger.error("❌ Loki logging configured successfully")
    except Exception as e:
        # Make sure error is visible in console
        print(f"❌ Failed to configure Loki: {str(e)}")
        logger.warning(f"Failed to configure Loki logging: {str(e)}")
    
    return logger