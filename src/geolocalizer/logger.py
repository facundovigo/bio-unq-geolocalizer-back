from pathlib import Path
import logging


class Logger:
    def __init__(self, folder_name):
        self.__logger = logging.getLogger("Geolocalizer")
        self.__output = str(Path(f"{folder_name}/logfile.txt").absolute())
        self.__configure_logger(self.__logger, self.__output)

    def log(self, module, msg):
        self.__logger.info(f"{module} - {msg}")

    def warn(self, module, msg):
        self.__logger.warning(f"{module} - {msg}")

    def err(self, module, msg):
        self.__logger.error(f"{module} - {msg}")

    def __configure_logger(self, logger, output_file):
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(output_file)
        logger.setLevel(logging.INFO)
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        c_format = logging.Formatter("%(levelname)s - %(message)s")
        f_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
