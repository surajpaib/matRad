import sys

sys.path.append('.')

from pyrad.matrad_dose_calc_wrapper import MatRadDoseCalcWrapper

def main():

    masks = {
        "TARGET": {
            'CTV': '/home/suraj/Repositories/data/matRad_test/CTVcervixFull.nrrd'
            },
        "OAR": {
            'BLADDER': '/home/suraj/Repositories/data/matRad_test/BLADDER.nrrd',
            'BOWELAREA': '/home/suraj/Repositories/data/matRad_test/BOWELAREA.nrrd',

        },
        "OTHER": {
            'BODY': '/home/suraj/Repositories/data/matRad_test/Masks/BODY.nrrd'
        }
    }
    dose_calc = MatRadDoseCalcWrapper(".", "./pyrad/plan_config.yaml")
    dose_calc("/home/suraj/Repositories/data/matRad_test/deformed.nrrd", masks)

if __name__ == "__main__":
    main()
