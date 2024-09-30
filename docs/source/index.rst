.. MetaSpread documentation master file, created by
   sphinx-quickstart on Mon May 20 15:52:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MetaSpread's documentation!
======================================

You search through the documentation using the user interface at any time by pressing :guilabel:`/`, or by using the search box on the left.

.. contents::
   :depth: 2

Summary
=======

MetaSpread is an open source simulation package and interactive program in Python for tumor growth and metastatic spread, based on a mathematical model by :cite:t:`franssen2019`. This paper proposed a hybrid modeling and computational framework where cellular growth and metastatic spread are described and simulated in a spatially explicit manner, accounting for stochastic individual cell dynamics and deterministic dynamics of abiotic factors. This model incorporates several key processes such as the growth and movement of epithelial and mesenchymal cells, the role of the extracellular matrix, diffusion, haptotaxis, circulation and survival of cancer cells in the vasculature, and seeding and growth in secondary sites. In the software that we develop, these growth and metastatic dynamics are programmed using MESA, a Python Package for Agent-based modeling :cite:p:`python-mesa-2020`.

Installation
============

MetaSpread is available as a official PyPI package. To install, you will need to have PIP installed. Afterwards, run:

.. code-block:: console
   
   pip install metaspread

or:

.. code-block:: console

   python -m pip install metaspread

Manual installation can be done by downloading the repo.

Finally, the program can be run interactively with:


.. code-block:: console

   python -m metaspread

Or it can be run purely through command line arguments, as detailed in the following section.

Usage
=====

The program can be run both interactively through the command line, or with explicit user command line arguments.


.. image:: main_menu.png
When run interactively, starting from the main menu, the following possibilities are offered: 

- **Run a new simulation:** the user can choose the *New Simulation* option to run a new simulation, with the arguments to be specified by the user being the maximal time for the dynamics, and the frequency of saving data (temporal resolution). Any other simulation parameter (see  Table \ref{table} ) will be taken from the *simulation\_configs.csv* file in the main folder. At the end of the simulation the dynamics of the grids, including agents (cells and vasculature points), the vasculature dynamics and the MMP2 and ECM are saved in a properly identified directory, including a *configs.csv* recording the used parameters for this particular simulation. The file *CellsData.csv* in this directory will include all the information of all cells and vasculature points in the simulation, for every time step.

  - The *simulation_configs.csv* file can be modified both in a code editor, or in a spreadsheet processing software, such as Microsoft Excel:

  .. figure:: csv_both.png
  The *simulation_configs.csv* file in Visual Studio Code (left) and in Microsoft Excel (right).
..   .. figure:: csv_code.png
..   The *simulation_configs.csv* file in Visual Studio Code.
  .. figure:: csv_excel.png
..   The *simulation_configs.csv* file in Microsoft Excel.
  
  - In addition, in the ECM and MMP2 folders there will be files containing the values of these factors for each time step, not requiring any postprocessing.
  
  - The vasculature folder will contain several *.json* files with the state of the vasculature at each time step. That is, they will contain a dictionary showing the clusters that were present at each time step. Further information can be extracted by using the **data analysis** option.
  
  - The folder *Time when grids got populated* will have a file that will simply show the time step for which each grid (primary or secondary site) got populated.

  - When running from the commandline, the user can use ``python -m metaspread run max-steps temporal-resolution``. For example, the command `python -m metaspread run 40000 150` would run a simulation for 40000 steps and saving the results every 150 steps.

  - The temporal resolution has to be always less or equal to ``vasculature_time``. If not, it will not be possible to see the dynamics of the vasculature correctly, as the cells can intravasate and extravasate without being recorded.

- **Load an existing simulation** The user can select *Load Simulation* from the main menu, and an existing simulation will be loaded, and can be continued for further time steps with the same parameters in its *configs.csv* file. The only parameters that the user has to select are the new temporal resolution and the maximum extra steps for the simulation to run. When running from the commandline, the user can use ``python -m metaspread load simulation-folder-name additional-steps temporal-resolution``. It is recommended to use the same temporal resolution as used before.

- **Post-process data from a simulation** The generated *CellsData.csv* contains the information of every cancer cell at every time step and every grid of the simulation. In order to facilitate the study of the results, we provide the user with several post-processing options: Data analysis, Graphical analysis and Video generation. 
  
  .. image:: postprocessing_menu.png


- **Data analysis:** several results will be summarized in *.csv* files, such as the vasculature and tumor dynamics. 
  
  - The files that account for total number of cells, Vasculature dynamics (total numbers of CTCs and clusters, cells and phenotypes), and tumor radius (the maximum of all cell distances from the centroid of mass) and diameter (maximum of all cell-to-cell distances) evolution, consist of columns that register the state of a metric in each time step along the simulation. These easily allows plotting graphs of dynamics later on.
  
  - The tumor growth files for each time point consist of 8 rows: the first 2 rows correspond to x and y coordinates of mesenchymal cells. The second 2 rows correspond to the x and y coordinates of epithelial cells, the next 2 rows correspond to x and y coordinates of regular vasculature points, and the final 2 rows correspond to the coordinates of ruptured vessels. These allow for easily plotting the positions of the agents, and thus, the state of the tumor, at each time step.
  
  - The histogram files summarize the spatial distribution of cells for each time point. Each file consists of two columns: one for the bins, and one for the frequency. The bins represent the possible number of cells in each grid point, from 0 to :math:`Q`, and the frequency the number of grid points that have that amount cells.

  - When running from the commandline, the user can use ``python -m metaspread postprocess data simulation-folder-name``

- **Graphical analysis:** in order to run this step, it is necessary to run the data analysis option first. When selected, the used will be prompted to introduce the number of figures to describe the snapshot of the dynamics at equally spaced intervals between 0 and the final time of the simulation. Then, plots of the tumor distribution, ECM, MMP-2 for each grid. Furthermore, it will also produce other plots such as the dynamics of the cells in the vasculature, histograms of the cell number distribution over grid points, radius and diameter of the tumor over time, and total size of the tumor in each grid. When running from the commandline, the user can use ``python -m metaspread postprocess graphics simulation-folder-name amount-of-figures``.

- **Video generation:** The user can choose the Videos option to generate animations from the figures generated in the *graphical analysis* step. When selected, the user will be prompted to introduce the framerate at which the videos should be saved. When running from the commandline, the user can use ``python -m metaspread postprocess videos simulation-folder-name frame-rate``.

- **Run all:** The user can run all the aforementioned steps in order with this option. When running from the commandline, the user can use ``python -m metaspread postprocess all simulation-folder-name amount-of-figures frame-rate``.

Cancer growth and spread model
==============================

.. _figure-example-sim:

.. figure:: Figure_1.png
   :align: center

   **Early snapshot of our simulations for cancer cell spread in the primary tumour (grid 1) after approximately 5 days.** Parameters as in Table \ref{table} with initial distribution centered around (1 mm, 1 mm) with radius of about ~0.1 mm, and total initial size = 388 cells. The blue color denotes mesenchymal cells, the orange color denotes epithelial cells. The intensity of the color represents the number of cells (from 0 to Q = 4) in that particular grid point. The red grid points represent entry-points to the vasculature, with circles intact vessels and crosses representing ruptured vessels.

A 2-dimensional multigrid hybrid spatial model of cancer dynamics is developed in Python (see :numref:`figure-example-sim` for a snapshot illustration). Here we combine the stochastic individual based dynamics of single cells with deterministic dynamics of the abiotic factors. The algorithm for dynamic progression at each time step is depicted in :numref:`figure-flowchart`. In the tumor site we consider two different cancer cell phenotypes: epithelial (epithelial-like) and mesenchymal (mesenchymal-like) cells. The epithelial-like (E) cancer cells reproduce at a higher rate, but diffuse more slowly than mesenchymal (M) cells, which reproduce at a lower rate but diffuse more rapidly. Furthermore, epithelial cells cannot break through the vasculature wall alone, as they require the presence of mesenchymal cells to be able to intravasate into normal vessel entry-points. The exception to this are ruptured vessels, that allow for the intravasation of any type of cancer cell. The cellular growth and movement in space is modeled considering 2 partial differential equations, where random (diffusion) and non-random (haptotaxis) movement are implemented. The model includes two additional equations: one for the spatio-temporal dynamics of matrix metalloproteinase 2 (MMP-2), a chemical that favors the spread of cancer cells, and another for the degradation of the extracellular matrix (ECM), which also favors the haptotactic movement of the cancer cells. 
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

.. _figure-flowchart:

.. figure::flowchart.png
   :align: center

   **Diagram summarizing the key algorithmic steps**


Simulation parameters
=====================


+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
|                               | Variable name                     | Description                                                                   | Value                     |
+===============================+===================================+===============================================================================+===========================+
| :math:`\Delta t`              | ``th``                            | Time step                                                                     | :math:`1\times 10^{-3}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Delta x`              | ``xh``                            | Space step                                                                    | :math:`5\times 10^{-3}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Delta t_a`            | ``tha``                           | Abiotic time step                                                             | :math:`1\times 10^{-3}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Delta x_a`            | ``xha``                           | Abiotic space step                                                            | :math:`5\times 10^{-3}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`D_{M}`                 | ``dM``                            | Mesenchymal-like cancercell diffusion coefficient                             | :math:`1\times 10^{-4}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`D_{E}`                 | ``dE``                            | Epithelial-like cancer cell diffusion coefficient                             | :math:`5\times 10^{-5}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Phi _{M}`             | ``phiM``                          | Mesenchymal haptotactic sensitivity coefficient                               | :math:`5\times 10^{-4}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Phi _{E}`             | ``phiE``                          | Epithelial haptotactic sensitivity coefficient                                | :math:`5\times 10^{-4}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`D_{m}`                 | ``dmmp``                          | MMP-2 diffusion coefficient                                                   | :math:`1\times 10^{-3}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Theta`                | ``theta``                         | MMP-2 production rate                                                         | :math:`0.195`             |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Lambda`               | ``Lambda``                        | MMP-2 decay rate                                                              | :math:`0.1`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Gamma _{1}`           | ``gamma1``                        | ECM degradation rate by MT1-MMP                                               | :math:`1`                 |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\Gamma _{2}`           | ``gamma2``                        | ECM degradation rate by MMP-2                                                 | :math:`1`                 |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`T_{V}`                 | ``vasculature_time``              | Steps CTCs spend in the vasculature                                           | :math:`180`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`T_{E}`                 | ``doublingTimeE``                 | Epithelial doubling time                                                      | :math:`3000`              |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`T_{M}`                 | ``doublingTimeM``                 | Mesenchymal doubling time                                                     | :math:`2000`              |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\mathcal{P}_{s}`       | ``single_cell_survival``          | Single CTC survival probability                                               | :math:`5\times 10^{-4}`   |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\mathcal{P}_{C}`       | ``cluster_survival``              | CTC cluster survival probability                                              | :math:`2.5\times 10^{-2}` |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\mathcal{E}_{1,...,n}` | ``extravasation_probs``           | Extravasation probabilities                                                   | :math:`[0.75, 0.25]`      |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`\mathcal{P}_{d}`       | ``disaggregation_prob``           | Individual cancer cell dissagregation probability                             | :math:`0.5`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`Q`                     | ``carrying_capacity``             | Maximum amount of cells per grid point                                        | :math:`4`                 |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`U_P`                   | ``normal_vessels_primary``        | Nr. of normal vessels present on the primary grid                             | :math:`2`                 |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`V_P`                   | ``ruptured_vessels_primary``      | Nr. of ruptured vessels present on the primary grid                           | :math:`8`                 |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`U_{2,...,n}`           | ``secondary_sites_vessels``       | Nr. of vessels present on the secondary sites                                 | :math:`[10, 10]`          |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     | ``n_center_points_for_tumor``     | | Nr. of center-most grid points where the                                    | :math:`97`                |
|                               |                                   | | primary cells are going to be seeded                                        |                           |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     |``n_center_points_for_vessels``    | | Nr. of center-most grid points where the                                    | :math:`200`               |
|                               |                                   | | vessels will not be able to spawn                                           |                           |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     | ``gridsize``                      | Length in gridpoints of the grid's side                                       | :math:`201`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     | ``grids_number``                  | Nr. of grids, including the primary site                                      | :math:`3`                 |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     | ``mesenchymal_proportion``        | Initial proportion of M cells in grid 1                                       | :math:`0.6`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     | ``epithelial_proportion``         | Initial proportion of E cells in grid 1                                       | :math:`0.4`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+
| :math:`-`                     | ``number_of_initial_cells``       | Initial nr. of total cells                                                    | :math:`388`               |
+-------------------------------+-----------------------------------+-------------------------------------------------------------------------------+---------------------------+

The biological parameters of the model and the simulation values are summarized in Table \ref{table}, tailored to breast cancer progression and early-stage dynamics prior to any treatment and in a pre-angiogenic phase (less than 0.2 cm in diameter). We provide the default values used by :cite:p:`franssen2019`, as informed by biological and empirical considerations (see also Table \ref{table} and references therein in :cite:p:`franssen2019`). The dynamics represent a two-dimensional cross-section of a small avascular tumor and run on a 2-dimensional discrete grid (spatial domain :math:`[0,1] \times [0,1]` corresponding to physical domain of size :math:`[0,0.2]\text{ cm} \times [0,0.2]\text{ cm}`), where each grid element corresponds to a spatial unit of dimension :math:`(\Delta x,\Delta y)`, and where position :math:`x_i,y_j` corresponds to :math:`i \Delta x` and :math:`j \Delta y`. Cancer cells are modeled as discrete agents whose growth and migration dynamics follow probabilistic rules, whereas the abiotic factors MMP2 and extracellular matrix dynamics follow the deterministic PDE evolution, discretized by an explicit five-point central difference discretization scheme together with zero-flux boundary conditions. The challenge of the simulation lies in coupling deterministic and agent-based stochastic dynamics, and in formulating the interface between the primary tumor Grid 1 and the metastatic sites (Grids 2,... :math:`k`). Each grid shares the same parameters, but there can be biases in connectivity parameters between grids (:math:`\mathcal{E}_{k}` parameters).

Cell proliferation is implemented in place by generating a new cell when the doubling time is completed, for each cell in each grid point. But if the carrying capacity gets surpassed, then there is no generation of a new cell. The movement of the cells is implemented through the probabilities in Equations \ref{probs}, which are computed at each time point and for each cell and contain the contribution of the random diffusion process and non-random haptotactic movement. If a cell lands in a grid point that contains a vasculature entry point, it is typically removed from the main grid and added to the vasculature. But there are details regarding the type of cells (E or M) and vasculature entry points (normal or ruptured) further described by :cite:p:`franssen2019`.

The vasculature is the structure connecting the primary and secondary sites, and it represents a separate compartment in the simulation framework. Single cells or clusters of cells, denominated as circulating tumor cells (CTCs), can enter the vasculature either through a ruptured or normal vessel, and they can remain there for a fixed number of time :math:`T_V`, representing the average time a cancer cell spends in the blood system. Each cell belonging to a cluster in the vasculature can disaggregate with some probability. At the end of the residence time in the vasculature, each cell's survival is determined randomly with probabilities that are different for single and cluster cells, and the surviving cells are randomly distributed on the secondary sites. To implement this vasculature dynamics in the algorithm, the vasculature is represented as a dictionary where the keys refer to the time-step in which there are clusters ready to extravasate. Intravasation at time :math:`t` corresponds to saving the cells into the dictionary with the associated exit time :math:`t+T_V`.  It is important to note that this parameter on the configuration file must be in time steps units.

Extravasation rules follow the setup in the original paper :cite:p:`franssen2019`, ensuring arriving cells do not violate the carrying capacity. Metastatic growth after extravasation follows the same rules as in the original grid. 

The default parameters are:

+--------------------------+--------------------------------------------------------------------------+
|        Variable          |     Dimensional Value                                                    |
+==========================+==========================================================================+
| :math:`\Delta t`         | :math:`40` s                                                             |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Delta x`         | :math:`1\times 10^{-3}` cm                                               |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Delta t_a`       | :math:`40` s                                                             |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Delta x_a`       | :math:`1\times 10^{-3}` cm                                               |
+--------------------------+--------------------------------------------------------------------------+
| :math:`D_{M}`            | :math:`1\times 10^{-10}` cm :math:`^{2}` s :math:`^{-1}`                 |
+--------------------------+--------------------------------------------------------------------------+
| :math:`D_{E}`            | :math:`5\times 10^{-11}` cm :math:`^{2}` s :math:`^{-}` :math:`^{1}`     |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Phi _{M}`        | :math:`2.6\times 10^{3}` cm :math:`^{2}` M :math:`^{-1}` s :math:`^{-1}` |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Phi _{E}`        | :math:`2.6\times 10^{3}` cm :math:`^{2}` M :math:`^{-1}` s :math:`^{-1}` |
+--------------------------+--------------------------------------------------------------------------+
| :math:`D_{m}`            | :math:`1\times 10^{-9}` cm :math:`^{2}` s :math:`^{-1}`                  |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Theta`           | :math:`4.875\times 10^{-6}` M :math:`^{-1}` s :math:`^{-1}`              |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Lambda`          | :math:`2.5\times 10^{-6}` s :math:`^{-1}`                                |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Gamma _{1}`      | :math:`1\times 10^{-4}` s :math:`^{-1}`                                  |
+--------------------------+--------------------------------------------------------------------------+
| :math:`\Gamma _{2}`      | :math:`1\times 10^{-4}` M :math:`^{-1}` s :math:`^{-1}`                  |
+--------------------------+--------------------------------------------------------------------------+
| :math:`T_{V}`            | :math:`7.2\times 10^{3}` s                                               |
+--------------------------+--------------------------------------------------------------------------+
| :math:`T_{M}`            | :math:`1.2\times 10^{5}` s                                               |
+--------------------------+--------------------------------------------------------------------------+
| :math:`T_{E}`            | :math:`8\times 10^{4}` s                                                 |
+--------------------------+--------------------------------------------------------------------------+

Examples
=======

With the default values, the following output was obtained:

.. _figure-6-images:

.. figure:: 6_images.png
   :align: center

   **Later snapshot of our simulations for cancer cell spread and ECM and MMP2 evolution in the primary and secondary metastatic site, grid 1 (left) and grid 2 (right) after approximately 12.78 days.** Parameters as in Table \ref{table} with initial distribution centered around (1 mm,1 mm) and total initial size = 388 cells. In the top row, the blue color denotes mesenchymal cells, the orange color denotes epithelial cells. The intensity of the color represents the number of cells (from 0 to Q) in that particular grid point. The red grid points represent entry-points to the vasculature, with circles intact vessels and crosses representing ruptured vessels. In the middle row, we plot the corresponding evolution of the density of the extracellular matrix at the same time points. In the last row we plot the spatial distribution of MMP2:

.. _figure-dynamics:

.. figure:: dynamics.png
   :align: center

   **Dynamics of total cell counts over time up to 12.78 days.** Top panels: In the primary (left) and secondary (right) tumor grid. Here we illustrate the functionality of the package to yield summaries of the spatiotemporal evolution of the cancer dynamics in the primary and in the metastatic site(s), namely total count of epithelial (E) and mesenchymal (M) cells. Middle panels: Dynamics in the vasculature, showing the amount of E and M cells (left), and the amount clusters (right). Cells can persist as single cells (CTC) or as multicellular clusters. As it can be seen, the majority of cells in the vasculature circulate in the form of clusters (green line) with only a minority being single CTCs (the difference between the red and the green line). Bottom panels: (left) radius and diameter of the spatio-temporal spread Radius is defined as the maximum of all cell distances from the centroid of mass, and diameter as the maximum of all cell-to-cell distances. (Right) distribution histogram of the cells over spatial grid points in the primary grid. The figure is obtained from the simulations corresponding to :numref:`figure-6-images`:


.. .. raw:: html

..     <div style="margin-bottom: 2em; position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
..         <iframe src="https://youtube.com/embed/Tc81GKmZDCs" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
..     </div>

`Video of the default tumor dynamics <https://www.youtube.com/watch?v=Tc81GKmZDCs>`_


| `Video of the tumor dynamics of the haptotactic tumor <https://www.youtube.com/watch?v=UIGS2FAuN9A>`_

.. .. raw:: html

..     <div style="margin-bottom: 2em; position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
..         <iframe src="https://youtube.com/embed/UIGS2FAuN9A" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
..     </div>

How to contribute
=======

How to cite
=======

**Cite MetaSpread:**


**The original mathematical model:**
Franssen, L.C., Lorenzi, T., Burgess, A.E.F. *et al*. A Mathematical Framework for Modelling the Metastatic Spread of Cancer. *Bull Math Biol* **81**, 1965–2010 (2019). https://doi.org/10.1007/s11538-019-00597-x

Indices
=======

* :ref:`genindex`
* :ref:`modindex`


Bibliography
============

.. bibliography::