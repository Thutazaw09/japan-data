import re
from pathlib import Path
from typing import Union, Tuple, Dict, Optional
import pandas as pd

# float matcher: 1, -2.3, 4.5e-3, etc.
_FLOAT_RE = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")


def parse_iad_output_txt(path: Union[str, Path]) -> pd.DataFrame:
    """
    Python 3.9 compatible parser for Scott Prahl IAD output (*.txt).

    Extracts the final numeric table regardless of:
      - optional leading row index column
      - trailing '*' convergence marker
      - extra whitespace/text

    Returns columns:
      wave_nm, M_R, R_fit, M_T, T_fit, mu_a, mu_s_p, g
    """
    path = Path(path)
    rows = []

    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.endswith("*"):
            s = s[:-1].strip()

        nums = [float(x) for x in _FLOAT_RE.findall(s)]
        if len(nums) < 8:
            continue

        # Take the last 8 numeric values as the standard IAD columns
        wave, M_R, R_fit, M_T, T_fit, mu_a, mu_s_p, g = nums[-8:]

        rows.append({
            "wave_nm": wave,
            "M_R": M_R,
            "R_fit": R_fit,
            "M_T": M_T,
            "T_fit": T_fit,
            "mu_a": mu_a,
            "mu_s_p": mu_s_p,
            "g": g,
        })

    if not rows:
        raise ValueError(
            "No IAD table rows found. Confirm you're parsing the iad.exe output file.")

    return pd.DataFrame(rows).sort_values("wave_nm").reset_index(drop=True)


# ---- example usage ----
if __name__ == "__main__":
    df = parse_iad_output_txt("my_data\sample.txt")  # change path
    print(df.head())
    df.to_csv("iad_parsed.csv", index=False)
    print("Saved iad_parsed.csv")
