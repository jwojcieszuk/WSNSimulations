# Wireless Sensor Networks Simulator

First simulation is comparison of network lifetime - time(number of rounds) until all nodes in the network are dead.

Communication protocols compared:

1. Direct Communication(DC), in which nodes transmit data directly to Base Station(BS).
2. LEACH, in which nodes are divided into clusters, and cluster-heads are elected by the BS.

Once simulator is started, network is deployed with nodes localized randomly on a 2D plane. BS is localized in the
center of the field. Next operation of simulation is divided into rounds, each round consists of three phases:

- **Setup phase**
    - For DC, in this phase each node has its `next_hop` attribute assigned as BS.
    - For LEACH, this phase is described as `advertisement_phase` in[1]. Cluster-heads are elected based on probability
      and then each node finds the nearest cluster_head (distance is calculated based on euclidean distance between
      nodes). Each node has its `next_hop` assigned as their cluster_head, and each cluster_head has its `next_hop`
      assigned as BS.
- **Sensing phase**
    - During sensing phase, events in the environment are simulated in a very simple way - random nodes are chosen (5%
      of the number of all nodes), and they sense data, which means that their `contains_data` attribute is set to True.
- **Data transmission phase**
    - Here each node that consists some data transmit it further based on `next_hop`. Energy consumed is calculated
      based on euclidean distance between node that consists data and destination node.

Once all three phases are completed, network is refreshed to initial state.

Network continue to operate until all nodes in the network are dead and counts how many rounds were performed.


**TODO**
- data fusion for LEACH
- energy consumption based on euclidean distance
- sleep scheduling(?)


References:

1. Energy-Efficient Communication Protocol for Wireless Microsensor Networks Wendi Rabiner Heinzelman, Anantha
   Chandrakasan, and Hari Balakrishnan