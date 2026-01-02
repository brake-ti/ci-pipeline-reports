import logging
import sys
import datetime
from pythonjsonlogger import json
from src.core.config import settings

class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        if not log_record.get('time'):
            now = datetime.datetime.now(datetime.timezone.utc)
            log_record['time'] = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
        if log_record.get('level'):
            log_record['level'] = log_record['level'].lower()
        else:
            log_record['level'] = record.levelname.lower()

def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    
    formatter = CustomJsonFormatter(
        '%(time)s %(level)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Also write to file as requested
    try:
        file_handler = logging.FileHandler("/var/log/app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, FileNotFoundError):
        # Ignore file logging if permission denied (common in CI/Tests)
        pass
    
    logger.setLevel(settings.LOG_LEVEL)
    
    # Mute noisy libraries
    logging.getLogger("uvicorn.access").disabled = True

logger = logging.getLogger(__name__)
