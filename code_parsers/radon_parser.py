import os

import radon.complexity as radon_complexity
import radon.raw as radon_raw
from radon.metrics import (
    h_visit,
    h_visit_ast,
    mi_visit,
    mi_parameters,
    mi_compute,
)

from code_parsers.lizard_parser import BaseParser


class RadonParser(BaseParser):
    supported_languages = ["py"]

    def __init__(self):
        super().__init__()
        self.loc = 0

    def parse(self, directory_name, file_name):
        try:
            f = open(os.path.join(directory_name, file_name), "r", encoding='utf-8', errors='replace')
        except UnicodeDecodeError as e:
            print(e)
            return

        source_code = f.read()
        raw_metrics = radon_raw.analyze(source_code)
        results = radon_complexity.cc_visit(source_code)
        visit_h = h_visit(source_code)
        visit_mi = mi_visit(source_code, 2)
        visit_ast = h_visit_ast(visit_h)
        parameters = mi_parameters(source_code)
        mi_computed = mi_compute(
            parameters[0], parameters[1], parameters[2], parameters[3]
        )

        self.loc += int(raw_metrics.loc)
        self.return_data: dict = {
            "loc": raw_metrics.loc,
            "lloc": raw_metrics.lloc,
            "sloc": raw_metrics.sloc,
            "comments": raw_metrics.comments,
            "multi": raw_metrics.multi,
            "single_comments": raw_metrics.single_comments,
            "blank": raw_metrics.blank,
            "h_visit": visit_h,
            "mi_visit": visit_mi,
            "h_visit_ast": visit_ast,
            "mi_parameters": parameters,
            "mi_compute": mi_computed,
            "complexity": [
                {"func_name": func.fullname, "complexity": func.complexity}
                for func in results
            ],
        }

        return self.return_data
