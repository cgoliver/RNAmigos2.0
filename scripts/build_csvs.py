import pickle

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem
from tqdm import tqdm

interactions_csv_original = '../data/rnamigos2_dataset_consolidated.csv'
interactions_csv_migos1 = '../data/rnamigos_1_data/rnamigos1_dataset.csv'

interactions_csv_dock = '../data/csvs/docking_data.csv'
interactions_csv_fp = '../data/csvs/fp_data.csv'
interactions_csv_binary = '../data/csvs/binary_data.csv'

systems = pd.read_csv(interactions_csv_original)
systems = systems.rename({'TYPE': 'SPLIT'}, axis='columns')

# Get PDB, SMILES for fp predictions
natives = systems.loc[systems['IS_NATIVE'] == 'YES']
systems_fp = natives[['PDB_ID_POCKET', 'LIGAND_SMILES', 'SPLIT']]

# PARSE RNAMIGOS_1 systems to get consistent splits
systems_migos_1 = pd.read_csv(interactions_csv_migos1)
old_splits = {}
for i, row in systems_migos_1.iterrows():
    row_id = f"{row['pdbid'].upper()}_{row['chain']}_{row['ligand_id']}_{row['ligand_resnum']}"
    row_splits = row.values[-10:]
    old_splits[row_id] = row_splits

migos_1_splits = []
for i, row in systems_fp.iterrows():
    pocket_id = row['PDB_ID_POCKET']
    if pocket_id in old_splits:
        migos_1_splits.append([1] + list(old_splits[pocket_id]))
    else:
        migos_1_splits.append(np.zeros((11,)))
migos_1_splits = np.asarray(migos_1_splits)
columns = ['IN_MIGOS_1'] + [f'split_test_{i}' for i in range(10)]
new_block = pd.DataFrame(migos_1_splits,
                         index=systems_fp.index,
                         columns=columns)
systems_fp = pd.concat([systems_fp, new_block], axis=1)
systems_fp.to_csv(interactions_csv_fp)

# Get PDB, SMILES, SCORE
systems_dock = systems[['PDB_ID_POCKET', 'LIGAND_SMILES', 'TOTAL', 'SPLIT']]
systems_dock.to_csv(interactions_csv_dock)

# Get PDB, SMILES, 0/1
systems_binary = systems[['PDB_ID_POCKET', 'LIGAND_SMILES', 'IS_NATIVE', 'SPLIT']]
systems_binary['IS_NATIVE'] = systems_binary['IS_NATIVE'].apply(lambda x: 1 if x == 'YES' else 0)
systems_binary.to_csv(interactions_csv_binary)

ligands = set(systems['LIGAND_SMILES'].unique())
morgan_map = {}
maccs_map = {}
morgan_path = '../data/ligands/morgan.p'
maccs_path = '../data/ligands/maccs.p'
failed = 0
for sm in tqdm(ligands):
    try:
        mol = Chem.MolFromSmiles(sm)
    except:
        failed += 1
        print('failed to parse smiles', sm, failed)
        continue
    try:
        # for some reason RDKit maccs is 167 bits
        maccs = (list(map(int, MACCSkeys.GenMACCSKeys(mol).ToBitString()))[1:])
    except:
        maccs = [0] * 166
    try:
        morgan = list(map(int, AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024).ToBitString()))
    except:
        morgan = [0] * 1024
    morgan = np.asarray(morgan, dtype=bool)
    maccs = np.asarray(maccs, dtype=bool)
    morgan_map[sm] = morgan
    maccs_map[sm] = maccs

pickle.dump(morgan_map, open(morgan_path, 'wb'))
pickle.dump(maccs_map, open(maccs_path, 'wb'))
