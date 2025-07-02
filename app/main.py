"""
Main application entry point for EnergieFixers071 desktop application.
"""
import sys
import os
import logging
import traceback
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    print("Error: ttkbootstrap is not installed. Please run:")
    print("pip install -r requirements.txt")
    sys.exit(1)

# Import application modules
try:
    from config import Config, Colors
    from core.database import initialize_database, close_database
    from ui.root import MainApplication
except ImportError as e:
    print(f"Error importing application modules: {e}")
    print("Please ensure all required files are present and properly configured.")
    sys.exit(1)

def setup_logging():
    """Setup application logging"""
    try:
        # Ensure log directory exists
        Config.LOG_DIR.mkdir(exist_ok=True)
        
        # Configure logging
        log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Reduce noise from external libraries
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
    except Exception as e:
        print(f"Warning: Failed to setup logging: {e}")
        # Fall back to basic console logging
        logging.basicConfig(level=logging.INFO)

def check_environment():
    """Check if the environment is properly configured"""
    issues = []
    
    # Check if .env file exists
    env_file = app_dir.parent / ".env"
    if not env_file.exists():
        issues.append(f"No .env file found. Please copy .env.example to .env and configure your settings.")
    
    # Check database directory
    if not Config.DATA_DIR.exists():
        try:
            Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            issues.append(f"Cannot create data directory: {e}")
    
    # Warn about missing API tokens (non-critical)
    if not Config.KOBO_API_TOKEN and not Config.CALENDLY_API_TOKEN:
        print("Warning: No API tokens configured. Some features will be limited.")
        print("Configure KOBO_API_TOKEN and CALENDLY_API_TOKEN in your .env file.")
    
    if issues:
        print("Configuration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
        
        # Ask user if they want to continue
        response = input("\nDo you want to continue anyway? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            sys.exit(1)

def main():
    """Main application entry point"""
    print(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    
    try:
        # Setup logging first
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
        
        # Check environment
        check_environment()
        
        # Initialize database
        logger.info("Initializing database...")
        if not initialize_database():
            logger.error("Failed to initialize database")
            print("Error: Failed to initialize database. Check logs for details.")
            return 1
        
        logger.info("Database initialized successfully")
        
        # Create and run main application
        logger.info("Creating main application window...")
        app = MainApplication()
        
        logger.info("Starting application main loop...")
        app.run()
        
        logger.info("Application closed normally")
        return 0
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 0
        
    except Exception as e:
        # Log the full traceback for debugging
        error_msg = f"Application crashed: {e}"
        
        if Config.DEBUG:
            error_msg += f"\n{traceback.format_exc()}"
        
        # Try to log the error
        try:
            logger = logging.getLogger(__name__)
            logger.error(error_msg)
        except:
            print(error_msg)
        
        # Show error dialog if possible
        try:
            import tkinter.messagebox as msgbox
            import tkinter as tk
            
            # Create a temporary root window for the error dialog
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            
            msgbox.showerror(
                "Application Error", 
                f"An unexpected error occurred:\n\n{e}\n\nCheck {Config.LOG_FILE} for details."
            )
            
            root.destroy()
            
        except Exception as dialog_error:
            print(f"Error showing dialog: {dialog_error}")
            print(f"Original error: {e}")
        
        return 1
    
    finally:
        # Cleanup
        try:
            close_database()
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")

if __name__ == "__main__":
    # Set the working directory to the app directory
    os.chdir(app_dir)
    
    # Run the application
    exit_code = main()
    sys.exit(exit_code)