import os
import sys

import itertools
import time

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import random
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
import scipy.stats as ss
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import MACCSkeys

# Rdkit can cause segfaults
use_rdkit_plotting = True
if use_rdkit_plotting:
    from rdkit.Chem import Draw

    options = Draw.DrawingOptions()
    options.bgColor = None  # Set background color to None for transparency

import seaborn as sns

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from scripts_fig.plot_utils import *

positions = ["top_right", "middle_right", "bottom_right", "top_left", "middle_left", "bottom_left", "bottom_middle"]

draw_mols = [
    {"idx": 113, "pos": "top_right"},
    {"idx": 6159, "pos": "middle_right"},
    {"idx": 21818, "pos": "bottom_right"},
    {"idx": 10613, "pos": "top_left"},
    {"idx": 45, "pos": "middle_left"},
    {"idx": 16224, "pos": "bottom_left"},
    {"idx": 3648, "pos": "bottom_middle"},
]

mols_only = False
do_draw_mols = True


class MolImage:
    mol_zones = {
        "top_left": (-125, 100),
        "middle_left": (-135, 10),
        "bottom_left": (-125, -100),
        "top_right": (90, 100),
        "middle_right": (100, 0),
        "bottom_right": (80, -100),
        "bottom_middle": (40, -130),
    }
    smiles_to_ind = pickle.load(open("smiles_to_ind.p", "rb"))
    ind_to_smiles = {i: sm for sm, i in smiles_to_ind.items()}
    X = np.load("x_tsne.npy")

    def __init__(self, idx, loc, size=50):
        self.idx = idx
        self.loc = loc
        self.pos = self.mol_zones[loc]
        self.mol = Chem.MolFromSmiles(self.ind_to_smiles[self.idx])

        self.mol_x = self.mol_zones[self.loc][0]
        self.mol_y = self.mol_zones[self.loc][1]

        self.point_x = self.X[self.idx][0]
        self.point_y = self.X[self.idx][1]

        self.size = size

        self.compute_corners()

        pass

    def compute_corners(self):
        self.bottom_left = (self.mol_x + 17.5, self.mol_y)
        self.bottom_right = (self.mol_x + 32.6, self.mol_y)
        pass

    def draw(self, ax):

        # Generate an image of the molecule
        mol_image = Draw.MolToImage(self.mol, size=(800, 800), options=options)

        drawer = Draw.rdMolDraw2D.MolDraw2DSVG(300, 300)
        drawer.DrawMolecule(self.mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        with open(f"figs/mol_{self.idx}.svg", "w") as svg_file:
            svg_file.write(svg)

        mol_array = np.array(mol_image)

        if mol_array.shape[2] == 4:
            mol_array = mol_array[..., :3]

        linewidth = 1
        boxheight = 50
        if "left" in self.loc:
            plt.plot(
                [self.bottom_right[0], self.point_x],
                [self.bottom_right[1], self.point_y],
                color="black",
                linewidth=linewidth,
            )
            plt.plot(
                [self.bottom_right[0], self.point_x],
                [self.bottom_right[1] + boxheight, self.point_y],
                color="black",
                linewidth=linewidth,
            )
        if "right" in self.loc:
            plt.plot(
                [self.bottom_left[0], self.point_x],
                [self.bottom_left[1], self.point_y],
                color="black",
                linewidth=linewidth,
            )
            plt.plot(
                [self.bottom_left[0], self.point_x],
                [self.bottom_left[1] + boxheight, self.point_y],
                color="black",
                linewidth=linewidth,
            )

        inset_ax = ax.inset_axes(
            [self.mol_x, self.mol_y, self.size, self.size], transform=ax.transData
        )  # X, Y, width, height

        inset_ax.set_xticks([])  # Get current axes and set x-ticks to an empty list
        inset_ax.set_yticks([])  #

        # Hide the inset axes
        # inset_ax.axis("off")

        # Display the molecule image in the inset axes
        inset_ax.imshow(mol_array)

        ax.text(self.mol_x, self.mol_y, self.idx)
        ax.text(self.point_x, self.point_y, self.idx)

    pass


if __name__ == "__main__":

    recompute_tsne = False

    robins = [
        "2GDI_Y_TPP_100",
        "5BTP_A_AMZ_106",
        # "2QWY_A_SAM_100",
        "2QWY_B_SAM_300",
        # "3FU2_C_PRF_101",
        "3FU2_A_PRF_101",
    ]
    robin_ids = [
        "TPP",
        "ZTP",
        "SAM_ll",
        "PreQ1",
    ]

    # {smiles} {dock_score} {native_score} {fp_score} {mixed_score}

    big_df = pd.read_csv("outputs/robin/big_df_raw.csv")

    smiles_list = sorted(list(set(big_df["smiles"])))

    if recompute_tsne:
        print("Making fps")
        mols = [Chem.MolFromSmiles(s) for s in smiles_list]
        clean_mols = []
        clean_smiles = []
        for mol, sm in zip(mols, smiles_list):
            if mol is None:
                continue
            clean_mols.append(mol)
            clean_smiles.append(sm)

        smiles_to_ind = {sm: i for i, sm in enumerate(clean_smiles)}
        fps = np.array([MACCSkeys.GenMACCSKeys(m) for m in clean_mols])
        np.save("fps.npy", fps)
        pickle.dump(smiles_to_ind, open("smiles_to_ind.p", "wb"))

    smiles_to_ind = pickle.load(open("smiles_to_ind.p", "rb"))
    ind_to_smiles = {i: sm for i, sm in smiles_to_ind.items()}
    fps = np.load("fps.npy")
    if recompute_tsne:
        print("Tsne")
        X_embedded = TSNE(n_components=2, learning_rate="auto", init="pca").fit_transform(fps)

        np.save("x_tsne.npy", X_embedded)

    X_embedded = np.load("x_tsne.npy")

    fig, ax = plt.subplots(figsize=(12, 8))
    # fig.set_size_inches(15, 5)
    markers = ["^", "P", "D", "*"]
    # colors = ['green', 'blue', 'red', 'orange']
    # colors = sns.color_palette()
    # colors = sns.color_palette("Paired", 4)
    # colors = sns.color_palette(["#149950", "#00c358", "#037938", "#149921"])
    # colors = sns.color_palette(["#33ccff", "#b3ffff", "#3366ff", "#9999ff"])
    # colors = sns.color_palette(["#33ccff", "#00cccc", "#3366ff", "#9999ff"])
    colors = sns.color_palette(["#33ccff", "#00cccc", "#3366ff", "#9999ff"])
    # #77b553, # #027a38     # #00c458     # #149950    # #149921 #446600
    # colors = sns.color_palette(["#3cdd2f", "#446600", "#027a38", "#30a600"])
    # colors = sns.color_palette(["#149950", "#00c358", "#037938", "#149921"])
    # colors = sns.color_palette(["#149950"]*4)
    active_smiles_all = {}
    accs = []
    to_plot = []

    dead_color = "whitesmoke"
    inactive_color = "lightgrey"
    thresh_cutoff = 0.90
    score_to_use = "rnamigos_42"
    # thresh_cutoff = 0.95
    # for plot_decoys in [True, False]:  # cheap hack for putting active points on top
    for i, robin in enumerate(robins):
        actives = big_df.loc[(big_df["pocket_id"] == robin) & (big_df["is_active"] == 1)]
        inactives = big_df.loc[(big_df["pocket_id"] == robin) & (big_df["is_active"] == 0)]

        inds_active = [smiles_to_ind[s] for s in actives["smiles"] if s in smiles_to_ind]
        scores_active = [score for sm, score in zip(actives["smiles"], actives[score_to_use]) if sm in smiles_to_ind]

        inds_inactive = [smiles_to_ind[s] for s in inactives["smiles"] if s in smiles_to_ind]
        scores_inactive = [
            score for sm, score in zip(inactives["smiles"], inactives[score_to_use]) if sm in smiles_to_ind
        ]
        ranks = ss.rankdata(scores_active + scores_inactive)
        ranks_active = ranks[: len(scores_active)]
        ranks_inactive = ranks[len(scores_active) :]
        # plt.hist(ranks_active)
        # plt.show()

        N = len(scores_active) + len(scores_inactive)
        # import numpy as np
        # for cutoff in [0.99, 0.98, 0.95, 0.9, 0.8, 0.7, 0.6]:
        #     n_hits = np.sum([(r / N) > cutoff for r in ranks_active])
        #     print(cutoff, n_hits)
        for active in [False, True]:
            indices = inds_active if active else inds_inactive
            ranks = ranks_active if active else ranks_inactive
            for j in range(len(indices)):
                ind = indices[j]
                pos_x = X_embedded[ind, 0]
                pos_y = X_embedded[ind, 1]
                selected = ranks[j] > thresh_cutoff * N
                color = colors[i]
                to_plot.append((robin, color, pos_x, pos_y, selected, active, ind))
        pass

    # start plotting

    colnames = ["robin", "color", "pos_x", "pos_y", "selected", "active", "idx"]
    df = pd.DataFrame(to_plot, columns=colnames)

    # sns.kdeplot(data=df, x="pos_x", y="pos_y", color="grey", fill=False, bw_adjust=0.5, alpha=0.25)

    fig, ax = plt.subplots(1, 4, figsize=(12, 4))
    for i, robin in enumerate(robins):
        # actives unselected: big empty dot
        df_rob = df.loc[df["robin"] == robin]
        subset = df_rob.loc[(df_rob["selected"] == False) & df_rob["active"] == True]
        sns.kdeplot(
            data=df.loc[(df["robin"] == robin) & (df["active"] == True)],
            x="pos_x",
            y="pos_y",
            cmap="coolwarm",
            fill=False,
            bw_adjust=0.5,
            alpha=0.55,
            ax=ax[i],
        )
        ax[i].scatter(
            subset["pos_x"].values,
            subset["pos_y"].values,
            c=dead_color,
            linewidths=1.2,
            edgecolors=subset["color"],
            # marker=markers[i],
            marker="o",
            s=14,
            alpha=1,
        )

        # actives selected: big solid dot
        subset = df_rob.loc[(df_rob["selected"] == True) & (df_rob["active"] == True)]
        ax[i].scatter(
            subset["pos_x"].values,
            subset["pos_y"].values,
            c=subset["color"],
            linewidths=0.2,
            edgecolors="black",
            # marker=markers[i],
            marker="o",
            s=50,
            alpha=1,
        )

        ax[i].set_title(robin)
        ax[i].axis("off")
    plt.tight_layout()
    plt.savefig(f"kdes_{score_to_use}.pdf", format="pdf")
    plt.show()

    if not mols_only:
        # inactives unselected: grey dot
        """
        subset = df.loc[(df["selected"] == False) & (df["active"] == False)]
        plt.scatter(subset["pos_x"].values, subset["pos_y"].values, c=inactive_color, marker="o", s=0.1, alpha=0.25)
        """

        # inactives selected: small solid
        subset = df.loc[(df["selected"] == True) & (df["active"] == False)]
        plt.scatter(
            subset["pos_x"].values,
            subset["pos_y"].values,
            c=subset["color"],
            # marker=markers[i],
            marker="o",
            s=2,
            alpha=0.4,
        )

    # actives unselected: big empty dot
    subset = df.loc[(df["selected"] == False) & df["active"] == True]
    plt.scatter(
        subset["pos_x"].values,
        subset["pos_y"].values,
        c=dead_color,
        linewidths=1.2,
        edgecolors=subset["color"],
        # marker=markers[i],
        marker="o",
        s=14,
        alpha=1,
    )

    # actives selected: big solid dot
    subset = df.loc[(df["selected"] == True) & (df["active"] == True)]
    plt.scatter(
        subset["pos_x"].values,
        subset["pos_y"].values,
        c=subset["color"],
        linewidths=0.2,
        edgecolors="black",
        # marker=markers[i],
        marker="o",
        s=50,
        alpha=1,
    )
    legend_elements = [
        Line2D([0], [0], linestyle="none", marker="o", color=colors[i], markersize=20, label=f"{r}")
        for i, r in enumerate(robin_ids)
    ]
    fig.legend(handles=legend_elements, ncol=len(robins), loc="lower center")

    # rdkit can cause segfaults
    if not use_rdkit_plotting:
        plt.legend()
        plt.show()
        sys.exit()

    plt.axis("off")
    plt.savefig("figs/robin_tsne_bkg.png", dpi=600, format="png")
    # draw some mols
    if do_draw_mols:
        selected_actives = list(df.loc[(df["selected"] == True) & (df["active"] == True)]["idx"])
        selected_inactives = list(df.loc[(df["selected"] == True) & (df["active"] == False)]["idx"])
        not_selected_actives = list(df.loc[(df["selected"] == False) & (df["active"] == True)]["idx"])
        not_selected_inactives = list(df.loc[(df["selected"] == False) & (df["active"] == False)]["idx"])

        """
        for mol_info in draw_mols:
            # MolImage(mol_info["idx"], mol_info["pos"]).draw(ax)
            MolImage(random.choice(range(len(X_embedded))), mol_info["pos"]).draw(ax)
        """
        local_random = random.Random(15)
        pos_iter = iter(positions)
        for idx in local_random.sample(selected_actives, 3):
            print(idx)
            MolImage(idx, next(pos_iter)).draw(ax)
        for idx in local_random.sample(not_selected_actives, 3):
            print(idx)
            MolImage(idx, next(pos_iter)).draw(ax)

    plt.axis("off")
    plt.savefig("figs/robin_tsne_mols.pdf", format="pdf")
    plt.show()
