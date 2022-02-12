# Wireless Sensor Networks Simulator

This is a simulator for WSN written in Python. It supports communication from nodes to the Base Station(BS) with the use
of routing algorithms. Currently, there are two algorithms implemented.

1. Direct Communication(DC), in which nodes transmit data directly to Base Station(BS).
2. LEACH, which is cluster based algorithm in which cluster-heads are elected by the BS. Implementation is based on [1]
   paper.

Once simulator is started, network is deployed with nodes localized randomly on a 2D plane. BS is localized in the
center of the field. Next operation of simulation is divided into **rounds**, each **round** consists of three phases:

- **Setup phase**
    - For DC, in this phase each node is informed that they send data to the BS.
    - For LEACH, this phase is described as `advertisement_phase` in[1]. Cluster-heads are elected based on probability
      and then each node finds the nearest cluster_head (distance is calculated based on euclidean distance between
      nodes). Each node has its `next_hop` assigned as their cluster_head, and each cluster_head has its `next_hop`
      assigned as BS.
- **Sensing phase**
    - During sensing phase I assume that each node has data to send. So each alive node has its `contains_data`
      attribute send to True
- **Data transmission phase**
    - Here each node that consists data transmit it further based on `next_hop` attribute. Energy consumed is calculated
      based on energy consumption model described below.

**Energy consumption model**
Based on [2] paper. Energy model adopted in this work is as follows:the radio dissipates 50 nJ/bit (Eelec) to run the
transmitter or receiver circuitry and 100 pJ/bit/m2 (Eamp) for the transmit amplifier. The energy that a node dissipates
for the radio transmission ETx(k, d) of a message of k bits over a distance d is due to running both the transmitter
circuitry ETx-elec(k) and the transmitter amplifier ETx-amp(k, d) and is expressed by the following:
Etx = Eelec * k + Eamp * k * d^2 where Eelec is the transmitter circuitry dissipation per bit—equal to the corresponding
receiver circuitry dissipation per bit—and Eamp is the transmit amplifier dissipation per bit per square meter.
Similarly, the energy dissipated by a node for the reception ERx(k) of a message of k bits is due to running the
receiver circuitry ERx-elec(k) and is expressed by the following equation:
Erx(k) = Eelec * k

Once all three phases are completed, network is restored to initial state.

References:

1. Energy-Efficient Communication Protocol for Wireless Microsensor Networks Wendi Rabiner Heinzelman, Anantha
   Chandrakasan, and Hari Balakrishnan
2. Energy Efficient Routing in Wireless Sensor Networks Through Balanced Clustering Stefanos A. Nikolidakis 1,*,
   Dionisis Kandris 2 , Dimitrios D. Vergados and Christos Douligeris