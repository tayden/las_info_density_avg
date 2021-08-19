import os
import re
from pathlib import Path
from typing import Optional, Tuple

matcher = re.compile("point density: all returns (\d+\.?\d*) last only (\d+\.?\d*).*")


def extract_densities(file_path: Path) -> Optional[Tuple[float, float]]:
    print(file_path)

    with open(file_path, 'r') as f:
        while line := f.readline():
            if m := matcher.match(line):
                print(m.group(0), '\n')
                return float(m.group(1)), float(m.group(2))

    print("No point densities found!\n")


def main(info_path: Path):
    densities = list(map(extract_densities, info_path.rglob('*.txt')))
    avg_all_returns = sum([g[0] for g in densities]) / (len(densities) + 1e-10)
    avg_last_returns = sum([g[1] for g in densities]) / (len(densities) + 1e-10)

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
