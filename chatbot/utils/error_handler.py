import time
import logging
from typing import Any, Callable, Dict


# Set up logging
logging.basicConfig(
    level = logging.INFO,
    format = '[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class RetryConfig:
    """
    Config for retrying operations.
    """
    def __init__(
            self,
            max_attempts: int = 3,
            initial_delay: float = 1.0,
            backoff_multiplier: float = 2.0,
            max_delay: float = 10.0
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.backoff_multiplier = backoff_multiplier
        self.max_delay = max_delay

def retry_with_backoff(
        func: Callable,
        config: RetryConfig = None,
        tool_name: str = "unknown_tool",
):
    """
    Execute func with exponential backoff retry logic.

    Args:
        func: function to execute
        config: RetryConfig instance
        tool_name: name of the tool (for logging)

    Returns:
        Result of func() if successful.

    Raises:
        Exception from func() if all retries fail.
    """
    if config is None:
        config = RetryConfig()

    last_exception = None
    delay = config.initial_delay

    for attempt in range(1, config.max_attempts + 1):
        try:
            logger.info(f"Executing tool '{tool_name}', attempt {attempt}...")
            result = func()
            logger.info(f"Tool '{tool_name}' succeeded on attempt {attempt}.")
            return result
        
        except Exception as e:
            last_exception = e
            logger.warning(
                f"Tool '{tool_name}' failed on attempt {attempt}: {e}")
            if attempt < config.max_attempts:
                logger.info(
                    f"Retrying tool '{tool_name}' in {delay:.2f} seconds...")
                time.sleep(delay)
                delay = min(delay * config.backoff_multiplier, config.max_delay)
            else:
                logger.error(
                    f"Tool '{tool_name}' failed after {config.max_attempts} attempts.")
    raise last_exception
    

def format_user_friendly_error(error: Exception, tool_name: str) -> str:
    """
    Convert technical error into user-friendly message.

    Args:
        tool_name: name of the tool that caused the error
        error: original exception
        
    Returns:
        User-friendly error message string.
    """
    error_type = type(error).__name__
    error_msg = str(error)

    # map technical errors to friendly messages
    friendly_messages = {
        "ConnectionError": "I'm having trouble connecting to the service right now.",
        "TimeoutError": "The service is taking too long to respond.",
        "ValueError": "There was an issue with the input provided.",
        "Timeout": "The operation timed out. Please try again later.",
        "KeyError": "A required value was missing.",
        "ZeroDivisionError": "An unexpected calculation error occurred.",
        "FileNotFoundError": "A required file was not found.",
        "PermissionError": "I don't have permission to access that resource.",
    }

    friendly_msg = friendly_messages.get(error_type, "An unexpected error occurred.")

    # build full message
    if tool_name:
        full_msg = f"{friendly_msg} while using the '{tool_name}' tool."

    else:
        full_msg = friendly_msg

    hints = {
        "ConnectionError": "Please check your internet connection or try again later.",
        "TimeoutError": "You might want to try again after some time.",
        "ValueError": "Please verify the input format and try again.",
        "KeyError": "Please ensure all required parameters is provided.",
        "FileNotFoundError": "Please check if the file path is correct.",
        "PermissionError": "Please check your access rights for the resource.",
        "ZeroDivisionError": "Division by 0 isn't mathematically possible.",
    } 

    if error_type in hints:
        full_msg += " " + hints[error_type]

    return full_msg + "."


def create_error_result(error:Exception, tool_name: str=None) -> Dict[str,Any]:
    """
    Create a standardized error result dict.

    Args:
        error: original exception
        tool_name: name of the tool that caused the error

    Returns:
        Error result dict
    """

    return{
        "error": format_user_friendly_error(error, tool_name),
        "type": type(error).__name__,
        "details": str(error),
        "success": False
    }