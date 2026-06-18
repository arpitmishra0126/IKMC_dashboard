import sys
from pathlib import Path
import pandas as pd

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from services.indicators import *

print(get_msncu_nvd_achieved_count())
print(get_msncu_csection_achieved_count())

print(get_msncu_nvd_coverage())
print(get_msncu_csection_coverage())