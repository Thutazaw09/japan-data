import re
import argparse
from pathlib import Path
from typing import Union
import pandas as pd
import matplotlib.pyplot as plt

# float matcher
_FLOAT_RE = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")


def parse_iad_output_txt(path: Union[str, Path]) -> pd.DataFrame:
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
        raise ValueError("No IAD table rows found in the file.")

    return pd.DataFrame(rows).sort_values("wave_nm").reset_index(drop=True)


def plot_iad_results(df: pd.DataFrame, prefix: str, show: bool = False) -> None:
    # Reflectance
    plt.figure()
    plt.plot(df["wave_nm"], df["M_R"], label="Measured R")
    plt.plot(df["wave_nm"], df["R_fit"], label="Fit R")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Reflectance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{prefix}_R.png", dpi=300)

    # Transmittance
    plt.figure()
    plt.plot(df["wave_nm"], df["M_T"], label="Measured T")
    plt.plot(df["wave_nm"], df["T_fit"], label="Fit T")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Transmittance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{prefix}_T.png", dpi=300)

    # Absorption
    plt.figure()
    plt.plot(df["wave_nm"], df["mu_a"])
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("μa (1/mm)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{prefix}_mua.png", dpi=300)

    # Reduced scattering
    plt.figure()
    plt.plot(df["wave_nm"], df["mu_s_p"])
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("μs' (1/mm)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{prefix}_mus_p.png", dpi=300)

    if show:
        plt.show()
    else:
        plt.close("all")


def main():
    parser = argparse.ArgumentParser(
        description="Parse Scott Prahl IAD output and generate CSV + plots"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="IAD output text file (e.g. sample.txt)"
    )

    parser.add_argument(
        "-o", "--output",
        default="iad_result",
        help="Output file prefix (default: iad_result)"
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Display plots on screen"
    )

    args = parser.parse_args()

    df = parse_iad_output_txt(args.input)

    csv_name = f"{args.output}.csv"
    df.to_csv(csv_name, index=False)

    plot_iad_results(df, prefix=args.output, show=args.show)

    print("=== IAD parsing complete ===")
    print(f"Input file : {args.input}")
    print(f"CSV output : {csv_name}")
    print(f"Plots saved: {args.output}_*.png")


if __name__ == "__main__":
    main()
