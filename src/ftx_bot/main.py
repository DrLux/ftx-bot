import hydra
from omegaconf import DictConfig
from hydra.utils import get_original_cwd


@hydra.main(config_path='../../parameters', config_name='default.yaml')
def metodo(cfg: DictConfig):
    print(cfg)

metodo()