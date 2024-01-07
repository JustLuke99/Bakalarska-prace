from abstract.base_parser import BaseParser
import lizard
import os


class LizardParser(BaseParser):
    supported_languages = ["py", "cpp"]  # TODO add "c"

    # TODO delete it
    def __init__(self):
        super().__init__()

    def parse(self, directory_name, file_name):
        data = lizard.analyze_file(os.path.join(directory_name, file_name))
        self.return_data = {
            "ccn": data.CCN,
            "average_cyclomatic_complexity": data.average_cyclomatic_complexity,
            "average_nloc": data.average_nloc,
            "average_token_count": data.average_token_count,
            "nloc": data.nloc,
            "token_count": data.token_count,
            "functions": [
                {
                    "cyclomatic_complexity": func.cyclomatic_complexity,
                    "end_line": func.end_line,
                    "func_name": func.name,
                    "start_line": func.start_line,
                    "nloc": func.nloc,
                    "token_count": func.token_count,
                    "parameters_count": func.parameter_count,
                    "length": func.length,
                }
                for func in data.function_list
            ],
        }

        return self.return_data
