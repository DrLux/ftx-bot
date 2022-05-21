import yaml
from pathlib import Path

params = {
    "prm_dict" : {
        'prova' : 1,
        "sub1": "secondo"
    },
    "sec_dict" : {
        'prova' : 2,
        "sub1": "secondo"
    }
}

path = Path("../../parameters/default.yaml")

with path.open('w') as fp:
    yaml.dump(params, fp)
