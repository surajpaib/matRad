import pymedphys
import numpy as np
from pathlib import Path
import SimpleITK as sitk

def calculate_gamma(dose1, dose2, params):
    z = np.arange(0, dose1.shape[0])
    y = np.arange(0, dose1.shape[1])
    x = np.arange(0, dose1.shape[2])

    coords = (z, y, x)

    gamma = pymedphys.gamma(coords, dose1, coords, dose2,
                            **params)

    valid_gamma = gamma[~np.isnan(gamma)]
    passing_rate = 100 * np.round(np.sum(valid_gamma <= 1) / len(valid_gamma), 4)

    return valid_gamma, passing_rate


def main(args):
    dataset_path = args.dataset_path.resolve()

    gamma_options = {
        'dose_percent_threshold': 3,
        'distance_mm_threshold': 3,
        'lower_percent_dose_cutoff': 20,
        'interp_fraction': 10,
        'max_gamma': 2,
        'random_subset': None,
        'local_gamma': True,
        'ram_available': 2**29,  # 1/2 GB
        'quiet': True
    }

    for folder in dataset_path.iterdir():
        if folder.is_dir():
            CT_path = folder / "deformed.nrrd"
            CBCT_path = folder / "target.nrrd"
            sCT_path = folder / "translated.nrrd"

            if not (CT_path.exists() and CBCT_path.exists() and sCT_path.exists()):
                print(f"Skipping patient {folder}")
                continue
                    
            CT = sitk.ReadImage(str(CT_path))
            CBCT = sitk.ReadImage(str(CBCT_path))
            sCT = sitk.ReadImage(str(sCT_path))

            CT = sitk.GetArrayFromImage(CT)
            CBCT = sitk.GetArrayFromImage(CBCT)
            sCT = sitk.GetArrayFromImage(sCT)

            _, passing_rate_CBCT = calculate_gamma(CT, CBCT, gamma_options)
            _, passing_rate_sCT = calculate_gamma(CT, sCT, gamma_options)

            print(f"Original passing rate: {passing_rate_CBCT} \n" \
                f"Translated passing rate: {passing_rate_sCT}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        "Gamma distribution comparison between two CBCT-CT and sCT-CT")

    parser.add_argument("dataset_path", help="Path to dataset", type=Path)

    # Output dir to store dose maps and gamma index maps
    parser.add_argument("--output_dir",
                        help="Path where the output will be stored",
                        default="out",
                        type=Path)

    args = parser.parse_args()

    main(args)
