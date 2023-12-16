import os
import importlib
import sys
from datetime import datetime


class CodeParserManager:
    """
    Manages a collection of code parsers and facilitates parsing of code files in a directory.

    Attributes:
    - parsers_directory (str): The directory containing code parsers.
    - parsers (list): A list of dictionaries, each containing a parser class and its supported languages.
    - supported_languages (list): A list of all supported programming languages by the loaded parsers.
    """

    def __init__(self):
        """
        Initializes a new instance of the CodeParserManager class.

        Parameters:
        - None
        """
        self.parsers_directory = "code_parsers"
        self.parsers = []
        self.supported_languages = []
        self.data = []

    def load_parsers(self) -> None:
        """
        Loads code parsers from the specified directory and updates supported_languages.

        Parameters:
        - None

        Returns:
        - None
        """
        parser_files = [
            f
            for f in os.listdir(self.parsers_directory)
            if f.endswith(".py") and not f.startswith("__")
        ]

        for parser_file in parser_files:
            module_name = os.path.splitext(parser_file)[0]
            module_path = f"{self.parsers_directory}.{module_name}"

            try:
                module = importlib.import_module(module_path)
                parser_class = getattr(
                    module, module_name.split("_")[0].capitalize() + "Parser"
                )
                supported_languages = parser_class().get_languages()
                for language in supported_languages:
                    if language not in self.supported_languages:
                        self.supported_languages.append(language)

                self.parsers.append(
                    {
                        "class": parser_class(),
                        "supported_languages": parser_class().get_languages(),
                    }
                )

            except (ImportError, AttributeError) as e:
                print(f"Failed to load parser from {parser_file}: {e}")

    def parse(self, root_directory: str, ignore_files=[], ignore_folders=[]) -> None:
        """
        Parses code files in the specified root directory using loaded parsers.

        Parameters:
        - root_directory (str): The root directory to start parsing from.
        - ignore_files (list): A list of file names to ignore during parsing.
        - ignore_folders (list): A list of folder names to ignore during parsing.

        Returns:
        - None
        """
        sd, sd2 = 0, 0
        for directory_name, _, files in os.walk(root_directory):
            if any(x in directory_name for x in ignore_folders):
                continue

            for file in files:
                if not (
                    any(file.endswith(ext) for ext in self.supported_languages)
                    or any(x in file for x in ignore_files)
                    or not "." in file
                ):
                    continue

                for code_parser in self.parsers:
                    if not any(
                        file.endswith(ext) for ext in code_parser["supported_languages"]
                    ):
                        continue

                    try:
                        _ = file.rsplit(".")[1]
                        data = code_parser["class"].parse(
                            directory_name=directory_name, file_name=file
                        )
                    except Exception as e:
                        print(f"File: {os.path.join(directory_name, file)}: {e}")
                        continue

                    self.data.append(
                        {
                            "file_path": os.path.join(directory_name, file),
                            "file_type": file.rsplit(".")[1],
                            "data": data,
                        }
                    )


if __name__ == "__main__":
    start_time = datetime.now()
    IGNORE_FOLDERS = ["venv", "idea"]
    IGNORE_FILES = []
    files = 0
    parserdasda = 0
    # FOLDER = "test_files"
    FOLDER = "/home/luke/PycharmProjects/You-are-Pythonista"
    parser = CodeParserManager()
    parser.load_parsers()
    fiLES = parser.parse(
        FOLDER, ignore_files=IGNORE_FILES, ignore_folders=IGNORE_FOLDERS
    )
    print("Size of data: ", sys.getsizeof(parser.data))
    print("Time taken: ", datetime.now() - start_time)
    print(fiLES)
