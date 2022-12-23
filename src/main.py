"""
Date Created: 2023-01-78

Description:
    Main application entry point
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import pydantic as pyd
from my_shared_module import shared_function

APP_VERSION = "v0.0.1"

################################################################
# Section Title
################################################################


class AppConfig(pyd.BaseModel):
    exe_file_dir: Path

    @staticmethod
    def init() -> AppConfig:
        if getattr(sys, "frozen", False):
            # we are running in a an executable
            exe_file_dir = Path(os.path.dirname(sys.executable))
        else:
            # we are running in a normal Python environment
            exe_file_dir = Path(os.path.dirname(__file__))

        # Initialize My logger

        # Silence All Other loggers
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if log_name != __name__:
                log_obj.disabled = True  # type: ignore

        logger = logging.getLogger(__name__)
        logger.info(f"App Version: {APP_VERSION}")
        return AppConfig(exe_file_dir=exe_file_dir)


def main() -> None:  # pylint: disable=missing-function-docstring
    app_config = AppConfig.init()
    print("Application Configured")
    shared_function()
    # Exit and Clean Up


if __name__ == "__main__":
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        logging.exception("Exception caught at the main handler")
