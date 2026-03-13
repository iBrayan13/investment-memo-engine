import html
import logging
import logging.config

import requests

from src.core.settings import Settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
logger.propagate = False


class TelegramHandler(logging.Handler):
    def __init__(self, settings: Settings) -> None:
        self.token = settings.TELEGRAM_TOKEN
        self.chat_ids = settings.ADMINISTRATOR_IDS
        self.project_flag = settings.PROJECT_FLAG
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        super().__init__()

    def send_message(self, message: str):
        """
        Sends a message to multiple chat IDs.

        Args:
            message (str): The message to be sent.

        Returns:
            None
        """
        try:
            # Ensure the message is a valid string
            if not isinstance(message, str):
                message = str(message)
            
            # Clean the message of characters that might cause issues
            message = message.replace('%', '%%')
            
            project_flag = (
                f"*{self.project_flag}*\n" if hasattr(self, "PROJECT_FLAG") else ""
            )
            
            for chat_id in self.chat_ids:
                # Escape HTML characters after all processing
                safe_text = html.escape(project_flag + message)
                payload = {
                    "chat_id": chat_id,
                    "text": safe_text,
                    "parse_mode": "HTML",
                }
                response = requests.post(self.api_url, data=payload)
                if not response.ok:
                    print(f"Error in Telegram response: {response.text}")
        except Exception as e:
            logger.warning(f"Error sending message to Telegram: {str(e)}")
            # Print the message to console as a fallback
            print(f"Message that could not be sent to Telegram: {message}")

    def emit(self, record):
        try:
            # Pre-process the message and arguments
            if isinstance(record.msg, str):
                if record.args:
                    try:
                        # Safely convert all arguments to string
                        safe_args = tuple(repr(arg) if not isinstance(arg, (str, int, float)) else str(arg) 
                                        for arg in record.args)
                        record.message = record.msg % safe_args
                    except:
                        # If formatting fails, concatenate safely
                        args_str = ', '.join(str(arg) for arg in record.args)
                        record.message = f"{record.msg} - Args: [{args_str}]"
                else:
                    record.message = record.msg
            else:
                # If the message is not a string, convert it safely
                record.message = str(record.msg)

            # Format and send the message
            text = self.format(record)
            self.send_message(text)
        except Exception as e:
            # Fallback with detailed error information
            error_msg = f"Error in TelegramHandler.emit: {str(e)}"
            print(error_msg)
            try:
                # Try a simpler format but with all relevant information
                msg = getattr(record, 'message', str(record.msg))
                args = getattr(record, 'args', ())
                args_str = ', '.join(str(arg) for arg in args) if args else ''
                fallback_msg = f"{record.levelname} - Message: {msg}"
                if args_str:
                    fallback_msg += f" - Args: [{args_str}]"
                print(fallback_msg)
            except Exception as e2:
                print(f"Critical error formatting log message: {str(e2)}")


def init_logger(settings: Settings) -> None:
    """
    Initializes the logger for the application.

    This function sets up the logger with a basic configuration to log messages to the console. The logger is configured with the following settings:
    - Logging level is set to INFO.
    - Log messages are formatted using the standard formatter with the following format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s".
    - A stream handler is added to the logger to send log messages to the console.
    - Logger propagation is disabled to prevent duplicate log messages.

    Parameters:
    None

    Returns:
    None
    """

    standard_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # handler config
    basic_handler = logging.StreamHandler()
    basic_handler.setLevel(logging.INFO)
    basic_handler.setFormatter(standard_formatter)

    # telegram handler
    telegram_handler = TelegramHandler(settings)
    telegram_handler.setLevel(logging.ERROR)
    telegram_handler.setFormatter(standard_formatter)

    # logger config
    app_logger = logging.getLogger()
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(basic_handler)
    app_logger.addHandler(telegram_handler)
    app_logger.propagate = False

    app_logger.info("Logger initialized!")