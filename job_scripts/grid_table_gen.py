
import os
import glob
from pathlib import Path 
import numpy as np
import pandas as pd
from yaml import safe_load 

# fp_native_grid-true-0.0--1-bce-true-1e-4

if __name__ == "__main__":
    RESULTS_DIR = Path('..', 'results', 'trained_models', 'native_fp')


    # name=migos1_grid2-undirected_${undirected}-migos1_${migos1}-loss_${lossfunc}-lr_${lr}-split_${split}"

    # runs = glob.glob(str(RESULTS_DIR) + '/fp_native_grid2*')
    runs = glob.glob(str(RESULTS_DIR) + '/migos1_grid2*')
    """
    grid_params = ['model.batch_norm', 
                   'model.dropout', 
                   'model.encoder.num_bases',
                   'train.loss',
                   'model.use_pretrained',
                   ]
    """


    grid_params = ['data.undirected', 
                   'train.use_rnamigos1_train', 
                   'train.loss',
                   'train.learning_rate',
                   ]

    results = []
    for run in runs:
        for split in range(10):
            try:
                with open(Path(run, 'config.yaml'), 'r') as f:
                    df = pd.json_normalize(safe_load(f))
                p = Path(run, "ef.csv")
                ef = pd.read_csv(p)
                    
                results.append({
                                'MAR_mean': np.mean(ef['ef']),
                                'MAR_std': np.std(ef['ef']),
                                'split': split,
                                'run': run,
                                **{p.split(".")[-1]: df[p][0] for p in grid_params}
                                }
                               )
            except FileNotFoundError:
                print("missing ", run, split) 

    df = pd.DataFrame(results)
    split_meaned = df.groupby('run').mean().reset_index().drop_duplicates(subset='run').drop(['split', 'run'], axis=1).sort_values(by='MAR_mean')
    print(split_meaned.to_markdown(index=False))
