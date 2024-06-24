.. MetaSpread documentation master file, created by
   sphinx-quickstart on Mon May 20 15:52:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MetaSpread's documentation!
======================================

You can open the search user interface at any time by pressing :guilabel:`/`, or by using the search box on the left.

.. contents::
   :depth: 2

Summary
=======

We develop and provide MetaSpread, an open source simulation package and interactive program in Python for tumor growth and metastatic spread, based on a mathematical model by :cite:t:`franssen2019`. This paper proposed a hybrid modeling and computational framework where cellular growth and metastatic spread are described and simulated in a spatially explicit manner, accounting for stochastic individual cell dynamics and deterministic dynamics of abiotic factors. This model incorporates several key processes such as the growth and movement of epithelial and mesenchymal cells, the role of the extracellular matrix, diffusion, haptotaxis, circulation and survival of cancer cells in the vasculature, and seeding and growth in secondary sites. In the software that we develop, these growth and metastatic dynamics are programmed using MESA, a Python Package for Agent-based modeling :cite:p:`python-mesa-2020`.


Cancer growth and spread model
==============================

A 2-dimensional multigrid hybrid spatial model of cancer dynamics is developed in Python (see Figure 1 for a snapshot illustration). Here we combine the stochastic individual based dynamics of single cells with deterministic dynamics of the abiotic factors. The algorithm for dynamic progression at each time step is depicted in Figure 2. In the tumor site we consider two different cancer cell phenotypes: epithelial (epithelial-like) and mesenchymal (mesenchymal-like) cells. The epithelial-like (E) cancer cells reproduce at a higher rate, but diffuse more slowly than mesenchymal (M) cells, which reproduce at a lower rate but diffuse more rapidly. Furthermore, epithelial cells cannot break through the vasculature wall alone, as they require the presence of mesenchymal cells to be able to intravasate into normal vessel entry-points. The exception to this are ruptured vessels, that allow for the intravasation of any type of cancer cell. The cellular growth and movement in space is modeled considering 2 partial differential equations, where random (diffusion) and non-random (haptotaxis) movement are implemented. The model includes two additional equations: one for the spatio-temporal dynamics of matrix metalloproteinase 2 (MMP-2), a chemical that favors the spread of cancer cells, and another for the degradation of the extracellular matrix (ECM), which also favors the haptotactic movement of the cancer cells. 
The dimensionless model, as described by :cite:p:`franssen2019` in Appendix A of their paper, corresponds to 4 PDEs, where the key variables reflect local densities of epithelial cells (:math:`c_E`) and mesenchymal cells (:math:`c_M`), and concentrations of MMP2 (:math:`m`) and extracellular matrix (:math:`w`):

.. math::

  \frac{\partial c_{E}}{\partial t} & =D_{\mathrm{E}} \nabla ^{2} c_{\mathrm{E}} -\Phi _{\mathrm{E}} \nabla \cdot ( c_{\mathrm{E}} \nabla w)\\
  \frac{\partial c_{\mathrm{M}}}{\partial t} & =D_{\mathrm{M}} \nabla ^{2} c_{\mathrm{M}} -\Phi _{\mathrm{M}} \nabla \cdot ( c_{\mathrm{M}} \nabla w)\\
  \frac{\partial m}{\partial t} & =D_{m} \nabla ^{2} m+\Theta c_{\mathrm{M}} -\Lambda m\\
  \frac{\partial w}{\partial t} & =-( \Gamma _{1} c_{\mathrm{M}} +\Gamma _{2} m) w

For the simulation of the spatio-temporal growth dynamics, and metastatic spread, the system of PDE's is discretized, and several 2-dimensional grids are established, representing the primary site and the metastatic sites. Discretizing equations for :math:`c_E` and :math:`c_M` in space and time, we obtain:

.. math::

   c_{Ei,j}^{n+1} = & \mathcal{P}_{0} c^{n}_{Ei-1,j} +\mathcal{P}_{1} c^{n}_{Ei+1,j} +\mathcal{P}_{2} c^{n}_{Ei,j+1} +\mathcal{P}_{3} c^{n}_{Ei,j-1} +\mathcal{P}_{4} c^{n}_{Ei,j}\\
   c_{Mi,j}^{n+1} = & \mathcal{P}_{0} c^{n}_{Mi-1,j} +\mathcal{P}_{1} c^{n}_{Mi+1,j} +\mathcal{P}_{2} c^{n}_{Mi,j+1} +\mathcal{P}_{3} c^{n}_{Mi,j-1} +\mathcal{P}_{4} c^{n}_{Mi,j}\\

Where :math:`n` refers to time point, :math:`(i,j)` refers to the spatial grid point :math:`(i,j)`, and  :math:`\mathcal{P}_0` to :math:`\mathcal{P}_4`:


.. math::
   \mathcal{P}_{0} : & \mathcal{P}_{i-1,j}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} -\frac{\Phi _{k}}{4}\left( w_{i+1,j}^{n} -w_{i-1,j}^{n}\right)\right]\\
   \mathcal{P}_{1} : & \mathcal{P}_{i+1,j}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} +\frac{\Phi _{k}}{4}\left( w_{i+1,j}^{n} -w_{i-1,j}^{n}\right)\right]\\
   \mathcal{P}_{2} : & \mathcal{P}_{i,j+1}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} +\frac{\Phi _{k}}{4}\left( w_{i,j+1}^{n} -w_{i,j-1}^{n}\right)\right]\\
   \mathcal{P}_{3} : & \mathcal{P}_{i,j-1}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} -\frac{\Phi _{k}}{4}\left( w_{i,j+1}^{n} -w_{i,j-1}^{n}\right)\right]\\
   \mathcal{P}_{4} : & \mathcal{P}_{i,j}^{n} :=1-(\mathcal{P}_{0} +\mathcal{P}_{1} +\mathcal{P}_{2} +\mathcal{P}_{3})

represent the probabilities for a cell to move up, down, left, right, or stay in place, and where :math:`k=E,M` can refer to an epithelial-like or mesenchymal-like cell. Each cell on every grid point at location :math:`(x_i,y_j)` is modeled as an individual agent, which obeys probability rules for growth and movement. There is a maximal carrying capacity for each grid point given by :math:`Q,` (assumed equal to 4 in :cite:p:`franssen2019`), to represent competition for space. There exist a doubling time :math:`T_E` and :math:`T_M` for epithelial and mesenchymal cells at which all the cells present in all grids will reproduce, duplicating in place, but never exceeding :math:`Q`.

Only the primary site is seeded with an initial number and distribution of cells. In order for the cells to migrate to another site, they must travel through the vasculature, which they do if they intravasate by one of the several randomly selected points in the grid that represent entrances to the vasculature system. The extravasation to one of the metastatic sites only occurs if they survive, a process that is modeled with net probabilistic rules considering time spent in the vasculature, cluster disaggregation, cell type, and potential biases to different destinations.

For the abiotic factors :math:`m` and :math:`w`, the discretization takes the form (see Appendices in :cite:p:`franssen2019`):


.. math::

   m_{i,j}^{n+1} = & D_{m}\frac{\Delta t_{a}}{( \Delta x_{a})^{2}}\left( m_{i+1,j}^{n} +m_{i-1,j}^{n} +m_{i,j+1}^{n} +m_{i,j-1}^{n}\right)\\
   & +m_{i,j}^{n}\left( 1-4D_{m}\frac{\Delta t_{a}}{( \Delta x_{a})^{2}} -\Delta t\Lambda \right) +\Delta t_{a} \Theta c^{n}_{Mi,j}\\
   w_{i,j}^{n+1} = & w_{i,j}^{n}\left[ 1-\Delta t_{a}\left( \Gamma _{1} c{_{M}^{n}}_{i,j} +\Gamma _{2} m_{i,j}^{n}\right)\right]

where :math:`i,j` reflect the grid point (:math:`i,j`) and :math:`n` the time-point. In this discretization two different time and spatial steps are used for the cell population (E and M cells) and the abiotic factors (ECM and MMP-2), namely :math:`\Delta t` and :math:`\Delta x = \Delta y`, :math:`\Delta t_a` and :math:`\Delta x_a = \Delta y_a` respectively.


Simulation parameters
=====================


+-----------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
|                       | **Variable name**                 | ** Description **                                                             | **Value**                 |
+=======================+===================================+===============================================================================+===========================+
| :math:`\Delta t`      | `th`                              | Time step                                                                     | :math:`1\times 10^{-3}`   |
| :math:`\Delta x`      | `xh`                              | Space step                                                                    | :math:`5\times 10^{-3}`   |
| :math:`\Delta t_a`    | `tha`                             | Abiotic time step                                                             | :math:`1\times 10^{-3}`   |
| :math:`\Delta x_a`    | `xha`                             | Abiotic space step                                                            | :math:`5\times 10^{-3}`   |
| :math:`D_{M}`         | `dM`                              | Mesenchymal-like cancercell diffusion coefficient                             | :math:`1\times 10^{-4}`   |
| :math:`D_{E}`          |`dE`                              | Epithelial-like cancer cell diffusion coefficient                             | :math:`5\times 10^{-5}`   |
| :math:`\Phi _{M}`     | `phiM`                            | Mesenchymal haptotactic sensitivity coefficient                               | :math:`5\times 10^{-4}`   |
| :math:`\Phi _{E}`     | `phiE`                            | Epithelial haptotactic sensitivity coefficient                                | :math:`5\times 10^{-4}`   |
| :math:`D_{m}`         | `dmmp`                            | MMP-2 diffusion coefficient                                                   | :math:`1\times 10^{-3}`   |
| :math:`\Theta`        | `theta`                           | MMP-2 production rate                                                         | :math:`0.195`             |
| :math:`\Lambda`       | `Lambda`                          | MMP-2 decay rate                                                              | :math:`0.1`               |
| :math:`\Gamma _{1}`   | `gamma1`                          | ECM degradation rate by MT1-MMP                                               | :math:`1`                 |
| :math:`\Gamma _{2}`    |`gamma2`                          | ECM degradation rate by MMP-2                                                 | :math:`1`                 |
| :math:`T_{V}`         | `vasculature\_time`               | Steps CTCs spend in the vasculature                                           | :math:`180`               |
| :math:`T_{E}`         | `doublingTimeE`                   | Epithelial doubling time                                                      | :math:`3000`                 |
| :math:`T_{M}`         | `doublingTimeM`                   | Mesenchymal doubling time                                                     | :math:`2000`                 |
| :math:`\mathcal{P}_{s}`       | `single\_cell\_survival`          | Single CTC survival probability                                               | :math:`5\times 10^{-4}`   |
| :math:`\mathcal{P}_{C}`       | `cluster\_survival`               | CTC cluster survival probability                                              | :math:`2.5\times 10^{-2}` |
| :math:`\mathcal{E}_{1,...,n}` | `extravasation_probs`                              | Extravasation probabilities                                                   | :math:`[0.75, 0.25]`       |
| :math:`\mathcal{P}_{d}`       | `disaggregation\_prob`            | Individual cancer cell dissagregation probability                             | :math:`0.5`               |
| :math:`Q`             | `carrying\_capacity`              | Maximum amount of cells per grid point                                        | :math:`4`                 |
| :math:`U_P`           | `normal\_vessels\_primary`        | Nr. of normal vessels present on the primary grid                             | :math:`2`                 |
| :math:`V_P`           | `ruptured\_vessels\_primary`      | Nr. of ruptured vessels present on the primary grid                           | :math:`8`                 |
| :math:`U_{2,...,n}`   | `secondary\_sites\_vessels`       | Nr. of vessels present on the secondary sites                                 | :math:`[10, 10]`          |
| :math:`-`             | `n\_center\_points\_for\_tumor`   | Nr. of center-most grid points where the primary cells are going to be seeded | :math:`97`                |
| :math:`-`             | `n\_center\_points\_for\_vessels` | Nr. of center-most grid points where the vessels will not be able to spawn    | :math:`200`               |
| :math:`-`             | `gridsize`                        | Length in gridpoints of the grid's side                                       | :math:`201`                   |
| :math:`-`             | `grids\_number`                   | Nr. of grids, including the primary site                                      | :math:`3`                 |
| :math:`-`             | `mesenchymal\_proportion`         | Initial proportion of M cells in grid 1                                       | :math:`0.6`               |
| :math:`-`             | `epithelial\_proportion`          | Initial proportion of E cells in grid 1                                       | :math:`0.4`               |
| :math:`-`             | `number\_of\_initial\_cells`      | Initial nr. of total cells                                                    | :math:`388`               |

The biological parameters of the model and the simulation values are summarized in Table \ref{table}, tailored to breast cancer progression and early-stage dynamics prior to any treatment and in a pre-angiogenic phase (less than 0.2 cm in diameter). We provide the default values used by [@franssen2019], as informed by biological and empirical considerations (see also Table \ref{table} and references therein in [@franssen2019]). The dynamics represent a two-dimensional cross-section of a small avascular tumor and run on a 2-dimensional discrete grid (spatial domain :math:`[0,1] \times [0,1]` corresponding to physical domain of size :math:`[0,0.2]\text{ cm} \times [0,0.2]\text{ cm}`), where each grid element corresponds to a spatial unit of dimension :math:`(\Delta x,\Delta y)`, and where position :math:`x_i,y_j` corresponds to :math:`i \Delta x` and :math:`j \Delta y`. Cancer cells are modeled as discrete agents whose growth and migration dynamics follow probabilistic rules, whereas the abiotic factors MMP2 and extracellular matrix dynamics follow the deterministic PDE evolution, discretized by an explicit five-point central difference discretization scheme together with zero-flux boundary conditions. The challenge of the simulation lies in coupling deterministic and agent-based stochastic dynamics, and in formulating the interface between the primary tumor Grid 1 and the metastatic sites (Grids 2,..:math:`k`). Each grid shares the same parameters, but there can be biases in connectivity parameters between grids (:math:`\mathcal{E}_{k}` parameters).

Cell proliferation is implemented in place by generating a new cell when the doubling time is completed, for each cell in each grid point. But if the carrying capacity gets surpassed, then there is no generation of a new cell. The movement of the cells is implemented through the probabilities in Equations \ref{probs}, which are computed at each time point and for each cell and contain the contribution of the random diffusion process and non-random haptotactic movement. If a cell lands in a grid point that contains a vasculature entry point, it is typically removed from the main grid and added to the vasculature. But there are details regarding the type of cells (E or M) and vasculature entry points (normal or ruptured) further described by [@franssen2019].

The vasculature is the structure connecting the primary and secondary sites, and it represents a separate compartment in the simulation framework. Single cells or clusters of cells, denominated as circulating tumor cells (CTCs), can enter the vasculature either through a ruptured or normal vessel, and they can remain there for a fixed number of time :math:`T_V`, representing the average time a cancer cell spends in the blood system. Each cell belonging to a cluster in the vasculature can disaggregate with some probability. At the end of the residence time in the vasculature, each cell's survival is determined randomly with probabilities that are different for single and cluster cells, and the surviving cells are randomly distributed on the secondary sites. To implement this vasculature dynamics in the algorithm, the vasculature is represented as a dictionary where the keys refer to the time-step in which there are clusters ready to extravasate. Intravasation at time :math:`t` corresponds to saving the cells into the dictionary with the associated exit time :math:`t+T_V`.  It is important to note that this parameter on the configuration file must be in time steps units.

Extravasation rules follow the setup in the original paper [@franssen2019], ensuring arriving cells do not violate the carrying capacity. Metastatic growth after extravasation follows the same rules as in the original grid. 


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`rtd_search`


Bibliography
============

.. bibliography::