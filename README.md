# Wireless Sensor Networks Simulator

First simulation is comparison of network lifetime - time(number of rounds) until all nodes in the network are dead.

Communication protocols compared:
    1. Direct Communication(DC), in which nodes transmit data directly to Base Station(BS).
    2. LEACH, in which nodes are divided into clusters, and cluster-heads are elected by the BS.

Once simulator is started, network is deployed with nodes localized randomly on a 2D plane. BS is localized in the center of the field.
Next operation of simulation is divided into phases:
- Setup phase
- Sensing phase
- Data transmission phase


Next step of simulation is setup phase, that in case of LEACH protocol BS elects cluster-heads, and then nodes chooses the nearest cluster-head (distance is calculated with the use of euclidean
distance).






According to Energy-Efficient Communication Protocol for Wireless Microsensor Networks Wendi Rabiner Heinzelman, Anantha Chandrakasan, and Hari Balakrishnan pape



Each node has its coordinates on a 2D plane and therefore energy consumption is calculated based on euclidean distance between nodes.


WIP
- data fusion for LEACH
- 