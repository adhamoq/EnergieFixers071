"""
Main application entry point for EnergieFixers071 desktop application.
"""
import sys
import os
import logging
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def setup_logging():
    """Setup application logging"""
    try:
        from config import Config
        Config.ensure_directories()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
    except Exception as e:
        # Fallback logging setup
        logging.basicConfig(level=logging.INFO)
        logging.error(f"Failed to setup logging: {e}")

def main():
    """Main application entry point"""
    try:
        # Setup logging first
        setup_logging()
        logger = logging.getLogger(__name__)
        
        from config import Config
        logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
        
        # Initialize database
        from core.database import initialize_database
        if not initialize_database():
            logger.error("Failed to initialize database")
            print("Error: Failed to initialize database. Check logs for details.")
            return 1
        
        # Import and run GUI after database is ready
        import ttkbootstrap as ttk
        from ui.root import MainApplication
        
        app = MainApplication()
        app.run()
        
        logger.info("Application closed normally")
        return 0
        
    except Exception as e:
        error_msg = f"Application crashed: {e}"
        logging.error(error_msg)
        print(f"Error: {error_msg}")
        return 1
    
    finally:
        # Cleanup
        try:
            from core.database import close_database
            close_database()
        except:
            pass

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
