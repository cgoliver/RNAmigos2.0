import random

from sklearn.manifold import TSNE
from sklearn.manifold import MDS 
import scipy.stats as ss
import pandas as pd
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import MACCSkeys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":

    robins = ['2GDI_Y_TPP_100',
             '2QWY_A_SAM_100',
             '3FU2_C_PRF_101',
             '5BTP_A_AMZ_106']


    actives = pd.read_csv("outputs/robin/2GDI_Y_TPP_100_actives.txt", delimiter=' ')
    actives.columns = ['smiles', 'dock', 'native', 'fp', 'mixed']
    inactives = pd.read_csv("outputs/robin/2GDI_Y_TPP_100_inactives.txt", delimiter=' ')

    #{smiles} {dock_score} {native_score} {fp_score} {mixed_score}
    inactives.columns = ['smiles', 'dock', 'nat', 'fp', 'mixed']

    smiles_list = sorted(list(set(actives['smiles']))) + sorted(list(set(inactives['smiles'])))

    print("Making fps")
    mols = [Chem.MolFromSmiles(s) for s in smiles_list]
    clean_mols = []
    clean_smiles = []
    for mol, sm in zip(mols, smiles_list):
        if mol is None:
            continue
        clean_mols.append(mol)
        clean_smiles.append(sm)

    smiles_to_ind = {sm:i for i,sm in enumerate(clean_smiles)}
    fps = np.array([MACCSkeys.GenMACCSKeys(m) for m in clean_mols])

    print("Tsne")
    X_embedded = TSNE(n_components=2, learning_rate='auto',
                      init='pca').fit_transform(fps)


    
    markers = ["^", "P", "D", "*"]
    colors = ['green', 'blue', 'red', 'orange']
    for i, robin in enumerate(robins):
        actives = pd.read_csv(f"outputs/robin/{robin}_actives.txt", delimiter=' ')
        actives.columns = ['smiles', 'dock', 'native', 'fp', 'mixed']
        actives['docknat'] = actives['dock'] + actives['native']
        inactives = pd.read_csv(f"outputs/robin/{robin}_inactives.txt", delimiter=' ')
        inactives.columns = ['smiles', 'dock', 'native', 'fp', 'mixed']
        inactives['docknat'] = inactives['dock'] + inactives['native']


        inds_active = [smiles_to_ind[s] for s in actives['smiles'] if s in smiles_to_ind]
        scores_active = [score for sm,score in zip(actives['smiles'], actives['docknat']) if sm in smiles_to_ind]

        inds_inactive = [smiles_to_ind[s] for s in inactives['smiles'] if s in smiles_to_ind]
        scores_inactive = [score for sm,score in zip(inactives['smiles'], inactives['docknat']) if sm in smiles_to_ind]

        ranks = ss.rankdata(scores_active + scores_inactive)
        ranks_active = ranks[:len(scores_active)]
        ranks_inactive = ranks[len(scores_active):]

        N = len(scores_active) + len(scores_inactive)

        colors_active = [colors[i] if ((r / N) > 0.9) else 'grey' for r in ranks_active] 
        colors_inactive = [colors[i] if ((r / N) > 0.9) else 'grey' for r in ranks_inactive] 

        plt.scatter(X_embedded[inds_inactive,0], X_embedded[inds_inactive,1], c=colors_inactive, marker='o', s=.5, alpha=.5)
        plt.scatter(X_embedded[inds_active,0], X_embedded[inds_active,1], c=colors_active, linewidths=0.8, edgecolors='black', marker='o', s=50, alpha=1, label=robin)
    
    plt.legend()
    plt.axis("off")
    plt.show()

    pass
