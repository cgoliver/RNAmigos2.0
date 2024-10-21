import os
import sys
from pathlib import Path

import pandas as pd
from yaml import safe_load

import hydra
from omegaconf import DictConfig, OmegaConf
import torch

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from rnamigos.learning.dataset import get_systems_from_cfg
from rnamigos.learning.dataloader import get_vs_loader
from rnamigos.learning.models import get_model_from_dirpath
from rnamigos.utils.virtual_screen import get_results_dfs

torch.multiprocessing.set_sharing_strategy('file_system')
torch.set_num_threads(1)


@hydra.main(version_base=None, config_path="conf", config_name="evaluate")
def main(cfg: DictConfig):
    # Setup hardware, cpu is fastest for inference
    torch.multiprocessing.set_sharing_strategy('file_system')

    # Load params from file
    print(OmegaConf.to_yaml(cfg))
    print('Done importing')
    with open(Path(cfg.saved_model_dir, 'config.yaml'), 'r') as f:
        params = safe_load(f)
        print(params['train'])
        if cfg.custom_dir:
            params['data']['pocket_path'] = cfg.data.pocket_graphs
        cfg_load = OmegaConf.create(params)

    # Get model
    model = get_model_from_dirpath(cfg.saved_model_dir)

    # Setup data
    if cfg.custom_dir:
        test_systems = pd.DataFrame({'PDB_ID_POCKET': [Path(g).stem for g in os.listdir(cfg.data.pocket_graphs)]})
    else:
        test_systems = get_systems_from_cfg(cfg=cfg_load, return_test=True)

    # Run VS
    decoys = ['chembl', 'pdb', 'pdb_chembl', 'decoy_finder'] if cfg.decoys == 'all' else [cfg.decoys]
    ef_dfs, raw_dfs = [], []
    for decoy_mode in decoys:
        dataloader = get_vs_loader(systems=test_systems, decoy_mode=decoy_mode, cfg=cfg_load, rognan=cfg.rognan)
        decoy_efs, decoys_raw = get_results_dfs(model=model,
                                                dataloader=dataloader,
                                                decoy_mode=decoy_mode,
                                                cfg=cfg,
                                                verbose=True)
        ef_dfs += decoy_efs
        raw_dfs += decoys_raw

    # Make it a df
    ef_df = pd.concat(ef_dfs)
    df_raw = pd.DataFrame(raw_dfs)

    # Dump csvs
    d = Path(cfg.result_dir, parents=True, exist_ok=True)
    base_name = Path(cfg.csv_name).stem
    ef_df.to_csv(d / (base_name + '.csv'))
    df_raw.to_csv(d / (base_name + "_raw.csv"))


if __name__ == "__main__":
    main()
