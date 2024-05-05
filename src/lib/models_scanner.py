import venusian


def scan_models():
    from src.modules.core import models as core_models

    scanner = venusian.Scanner()

    scanner.scan(core_models)
