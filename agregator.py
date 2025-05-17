from enum import StrEnum
from pathlib import Path
from typing import Final
import re

class Severity(StrEnum):
    TRACE = 'TRACE'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'

LOG_PATTERN: Final = re.compile(
    f"^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}T[0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}}Z ({'|'.join(sev.value for sev in Severity)})(?: |$)"
)

def aggregate_logs(file: Path) -> dict[str, int]:
    result = {}
    try:
        with file.open("r") as f:
            for line in f:
                match = LOG_PATTERN.match(line)
                if match:
                    severity = match.group(1)
                    result[severity] = result.get(severity, 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError(f"Log file not found: {file}")
        
    return result

severity_totals = aggregate_logs(Path('application.log'))
print("{ " + ", ".join(f'"{sev}": {count}' for sev, count in severity_totals.items()) + " }")
