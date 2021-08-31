import os
import re
from pathlib import Path
from typing import Optional, Tuple

density_matcher = re.compile("point density:\s+all returns (\d+\.?\d*) last only (\d+\.?\d*).*")
area_matcher = re.compile("covered area in square meters/kilometers:\s+(\d+)/(\d+\.?\d*)")


def extract_densities(file_path: Path) -> Optional[Tuple[float, float]]:
    with open(file_path, 'r') as f:
        while line := f.readline():
            if m := density_matcher.match(line):
                return float(m.group(1)), float(m.group(2))

    print(file_path)
    print("No point densities found!\n")


def extract_areas(file_path: Path) -> Optional[Tuple[float, float]]:
    with open(file_path, 'r') as f:
        while line := f.readline():
            if m := area_matcher.match(line):
                return int(m.group(1)), float(m.group(2))

    print(file_path)
    print("No area info found!\n")


def main(info_path: Path):
    densities = list(map(extract_densities, info_path.rglob('*.txt')))
    avg_all_returns = sum([g[0] for g in densities]) / (len(densities) + 1e-10)
    avg_last_returns = sum([g[1] for g in densities]) / (len(densities) + 1e-10)

    areas = list(map(extract_areas, info_path.rglob('*.txt')))
    sum_area_m = sum([g[0] for g in areas])
    sum_area_km = sum([g[1] for g in areas])

    print(f'COVERED AREA: {sum_area_m} (m^2) / {round(sum_area_m / 1000./1000., 2)} (km^2)')
    print(f'ALL RETURNS AVG: {round(avg_all_returns, 2)} (per square meter)')
    print(f'LAST RETURNS AVG: {round(avg_last_returns, 2)} (per square meter)')


if __name__ == '__main__':
    info_dir_str = input("Enter path to the directory containing the LASInfoReports .txt files:\n")
    try:
        info_dir = Path(info_dir_str)

        if not info_dir.is_dir():
            print("Provided path must be for a directory location")
            exit(0)

        main(info_dir)

    except RuntimeError:
        print("Error parsing path")
        exit(0)

    # Wait instead of closing program
    input()
