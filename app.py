"""
DMS Flask Application

Independent HTTP service for DMS management.
"""

import sys
import logging
import os
from pathlib import Path

# Add parent directory to Python path so 'dms' can be imported as a package
# This allows relative imports like 'from ..sources' to work
_project_root = Path(__file__).parent
_parent_dir = _project_root.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from dms.web.api import bp as api_bp, set_dms_instance
from dms.core.config import load_config

# Load environment variables
load_dotenv()

# Reduce Werkzeug access log verbosity
# Werkzeug uses its own logger named 'werkzeug' (not 'dms')
# Note: Errors will still be logged (WARNING level), but normal requests won't
logging.getLogger('werkzeug').setLevel(logging.INFO)

# Application logger
logger = logging.getLogger(__name__)

# Global DMS instance
_dms_instance = None

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(24).hex()

# Initialize CORS
CORS(app, supports_credentials=True)

# Register API Blueprint
app.register_blueprint(api_bp, url_prefix='/api/dms')

# Static files
static_dir = Path(__file__).parent / "web" / "static"
if static_dir.exists():
    app.static_folder = str(static_dir)
    app.static_url_path = '/static'


@app.route("/")
def index():
    """Serve main page"""
    index_file = static_dir / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>DMS Service</h1><p>Web interface not available</p>"


# Initialize DMS on startup (before first request)
def startup():
    """Initialize DMS on startup"""
    global _dms_instance
    try:
        logger.info("Starting DMS Service...")
        
        # Load configuration
        from dms.core.config import load_config
        config = load_config()
        
        # Initialize DMS instance (this will trigger database health check)
        from dms.core.dms import DMS
        dms = DMS(config)
        dms.start()
        _dms_instance = dms
        set_dms_instance(dms)
        
        logger.info("DMS service started successfully")
    except Exception as e:
        logger.error(f"ERROR: Failed to start DMS service: {e}", exc_info=True)
        raise  # Re-raise to prevent service from starting with errors

# Call startup immediately
startup()


if __name__ == "__main__":
    # Load config to get port
    try:
        from dms.core.config import load_config
        config = load_config()
        port = config.service.port
        host = config.service.host
    except Exception:
        port = 11183
        host = "0.0.0.0"
    
    app.run(host=host, port=port, debug=False)
