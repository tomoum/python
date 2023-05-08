# ---------------------------------------------------------------------------------
# Copyright (c) John Doe. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.
# ---------------------------------------------------------------------------------
"""
Author     : John Doe
Description:
"""


from __future__ import annotations

import logging
import sys
from pathlib import Path

import pkg_resources
import pydantic as pyd
from logzilla import LogZilla

from .common.my_shared_module import shared_function


class AppConfig(pyd.BaseModel):
    exe_file_dir: Path

    @staticmethod
    def init() -> AppConfig:
        if getattr(sys, "frozen", False):
            # we are running in a an executable
            exe_file_dir = Path(sys.executable).parent.absolute()
        else:
            # we are running in a normal Python environment
            exe_file_dir = Path(__file__).parent.absolute()

        # Initialize My logger
        LogZilla.init_root_logger(output_dir=exe_file_dir, log_file_name_append=exe_file_dir.stem)

        # Silence All Other loggers
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if log_name != __name__:
                log_obj.disabled = True  # type: ignore[disabled]

        logger = logging.getLogger(__name__)
        package_name = __package__
        package_version = pkg_resources.get_distribution(package_name).version
        logger.info(f"{package_name}, version: {package_version}")
        return AppConfig(exe_file_dir=exe_file_dir)


def main() -> None:  # pylint: disable=missing-function-docstring
    app_config = AppConfig.init()
    print("Application Configured")
    shared_function()
    # Exit and Clean Up


if __name__ == "__main__":
    main()
