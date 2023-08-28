import torch

from omegaconf import DictConfig, OmegaConf
import hydra

from rnaglib.kernels import node_sim
from rnaglib.data_loading import rna_dataset, rna_loader
from rnaglib.representations import GraphRepresentation, RingRepresentation
from rnaglib.learning import models, learning_utils, learn

from rnamigos_dock.learning.models import Embedder

@hydra.main(version_base=None, config_path="../conf", config_name="pretrain")
def main(cfg: DictConfig):
    # Choose the data, features and targets to use
    node_features = ['nt_code']

    ###### Unsupervised phase : ######
    # Choose the data and kernel to use for pretraining
    print('Starting to pretrain the network')
    node_simfunc = node_sim.SimFunctionNode(method='R_1', depth=2)
    graph_representation = GraphRepresentation(framework='dgl')
    ring_representation = RingRepresentation(node_simfunc=node_simfunc, max_size_kernel=50)
    unsupervised_dataset = rna_dataset.RNADataset(nt_features=node_features,
                                                  data_path='data/glib/data/annotated/NR_chops_annot',
                                                  representations=[ring_representation, graph_representation])
    train_loader = rna_loader.get_loader(dataset=unsupervised_dataset, split=False, num_workers=4)

    model = Embedder(in_dim=cfg.model.encoder.in_dim,
                     hidden_dim=cfg.model.encoder.hidden_dim,
                     num_hidden_layers=cfg.model.encoder.num_layers,
                      )

    # Then choose the embedder model and pre_train it, we dump a version of this pretrained model
    # embedder_model = models.Embedder(infeatures_dim=unsupervised_dataset.input_dim,
    #                                 dims=[64, 64])

    embedder_model = models.Embedder(infeatures_dim=unsupervised_dataset.input_dim,
                                     dims=[64, 64])
    optimizer = torch.optim.Adam(embedder_model.parameters())
    learn.pretrain_unsupervised(model=embedder_model,
                                optimizer=optimizer,
                                train_loader=train_loader,
                                learning_routine=learning_utils.LearningRoutine(num_epochs=10),
                                rec_params={"similarity": True, "normalize": False, "use_graph": True, "hops": 2})
    torch.save(embedder_model.state_dict(), 'pretrained_model.pth')
 
if __name__ == "__main__":
    main()
