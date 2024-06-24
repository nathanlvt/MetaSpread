.. MetaSpread documentation master file, created by
   sphinx-quickstart on Mon May 20 15:52:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MetaSpread's documentation!
======================================

.. contents::
   :depth: 2
   :caption: Contents:

Summary
=======

We develop and provide MetaSpread, an open source simulation package and interactive program in Python for tumor growth and metastatic spread, based on a mathematical model by :cite:t:`franssen2019`. This paper proposed a hybrid modeling and computational framework where cellular growth and metastatic spread are described and simulated in a spatially explicit manner, accounting for stochastic individual cell dynamics and deterministic dynamics of abiotic factors. This model incorporates several key processes such as the growth and movement of epithelial and mesenchymal cells, the role of the extracellular matrix, diffusion, haptotaxis, circulation and survival of cancer cells in the vasculature, and seeding and growth in secondary sites. In the software that we develop, these growth and metastatic dynamics are programmed using MESA, a Python Package for Agent-based modeling :cite:p:`python-mesa-2020`.


Cancer growth and spread model
==============================

A 2-dimensional multigrid hybrid spatial model of cancer dynamics is developed in Python (see Figure 1 for a snapshot illustration). Here we combine the stochastic individual based dynamics of single cells with deterministic dynamics of the abiotic factors. The algorithm for dynamic progression at each time step is depicted in Figure 2. In the tumor site we consider two different cancer cell phenotypes: epithelial (epithelial-like) and mesenchymal (mesenchymal-like) cells. The epithelial-like (E) cancer cells reproduce at a higher rate, but diffuse more slowly than mesenchymal (M) cells, which reproduce at a lower rate but diffuse more rapidly. Furthermore, epithelial cells cannot break through the vasculature wall alone, as they require the presence of mesenchymal cells to be able to intravasate into normal vessel entry-points. The exception to this are ruptured vessels, that allow for the intravasation of any type of cancer cell. The cellular growth and movement in space is modeled considering 2 partial differential equations, where random (diffusion) and non-random (haptotaxis) movement are implemented. The model includes two additional equations: one for the spatio-temporal dynamics of matrix metalloproteinase 2 (MMP-2), a chemical that favors the spread of cancer cells, and another for the degradation of the extracellular matrix (ECM), which also favors the haptotactic movement of the cancer cells. 
The dimensionless model, as described by [@franssen2019] in Appendix A of their paper, corresponds to 4 PDEs, where the key variables reflect local densities of epithelial cells (:math:`c_E`) and mesenchymal cells (:math:`c_M`), and concentrations of MMP2 (:math:`m`) and extracellular matrix (:math:`w`):

.. math::

  \begin{equation}
  \begin{aligned}
  \frac{\partial c_{E}}{\partial t} & =D_{\mathrm{E}} \nabla ^{2} c_{\mathrm{E}} -\Phi _{\mathrm{E}} \nabla \cdot ( c_{\mathrm{E}} \nabla w)\\
  \frac{\partial c_{\mathrm{M}}}{\partial t} & =D_{\mathrm{M}} \nabla ^{2} c_{\mathrm{M}} -\Phi _{\mathrm{M}} \nabla \cdot ( c_{\mathrm{M}} \nabla w)\\
  \frac{\partial m}{\partial t} & =D_{m} \nabla ^{2} m+\Theta c_{\mathrm{M}} -\Lambda m\\
  \frac{\partial w}{\partial t} & =-( \Gamma _{1} c_{\mathrm{M}} +\Gamma _{2} m) w
  \end{aligned}
  \end{equation}

.. math::
   :label: eqn1

  \begin{equation}
  \begin{aligned}
  \frac{\partial c_{E}}{\partial t} & =D_{\mathrm{E}} \nabla ^{2} c_{\mathrm{E}} -\Phi _{\mathrm{E}} \nabla \cdot ( c_{\mathrm{E}} \nabla w)\\
  \frac{\partial c_{\mathrm{M}}}{\partial t} & =D_{\mathrm{M}} \nabla ^{2} c_{\mathrm{M}} -\Phi _{\mathrm{M}} \nabla \cdot ( c_{\mathrm{M}} \nabla w)\\
  \frac{\partial m}{\partial t} & =D_{m} \nabla ^{2} m+\Theta c_{\mathrm{M}} -\Lambda m\\
  \frac{\partial w}{\partial t} & =-( \Gamma _{1} c_{\mathrm{M}} +\Gamma _{2} m) w
  \end{aligned}
  \end{equation}

Test: :eq:`eqn1`

For the simulation of the spatio-temporal growth dynamics, and metastatic spread, the system of PDE's is discretized, and several 2-dimensional grids are established, representing the primary site and the metastatic sites. Discretizing equations for :math:`c_E` and :math:`c_M` in space and time, we obtain:

\begin{equation}
\begin{aligned}
c_{Ei,j}^{n+1} = & \mathcal{P}_{0} c^{n}_{Ei-1,j} +\mathcal{P}_{1} c^{n}_{Ei+1,j} +\mathcal{P}_{2} c^{n}_{Ei,j+1} +\mathcal{P}_{3} c^{n}_{Ei,j-1} +\mathcal{P}_{4} c^{n}_{Ei,j}\\
c_{Mi,j}^{n+1} = & \mathcal{P}_{0} c^{n}_{Mi-1,j} +\mathcal{P}_{1} c^{n}_{Mi+1,j} +\mathcal{P}_{2} c^{n}_{Mi,j+1} +\mathcal{P}_{3} c^{n}_{Mi,j-1} +\mathcal{P}_{4} c^{n}_{Mi,j}\\
\end{aligned}
\end{equation}

Where :math:`n` refers to time point, :math:`(i,j)` refers to the spatial grid point :math:`(i,j)`, and  :math:`\mathcal{P}_0` to :math:`\mathcal{P}_4`:

\begin{equation}
\begin{aligned}
\mathcal{P}_{0} : & \mathcal{P}_{i-1,j}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} -\frac{\Phi _{k}}{4}\left( w_{i+1,j}^{n} -w_{i-1,j}^{n}\right)\right]\\
\mathcal{P}_{1} : & \mathcal{P}_{i+1,j}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} +\frac{\Phi _{k}}{4}\left( w_{i+1,j}^{n} -w_{i-1,j}^{n}\right)\right]\\
\mathcal{P}_{2} : & \mathcal{P}_{i,j+1}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} +\frac{\Phi _{k}}{4}\left( w_{i,j+1}^{n} -w_{i,j-1}^{n}\right)\right]\\
\mathcal{P}_{3} : & \mathcal{P}_{i,j-1}^{n} :=\frac{\Delta t}{(\Delta x)^{2}}\left[ D_{k} -\frac{\Phi _{k}}{4}\left( w_{i,j+1}^{n} -w_{i,j-1}^{n}\right)\right]\\
\mathcal{P}_{4} : & \mathcal{P}_{i,j}^{n} :=1-(\mathcal{P}_{0} +\mathcal{P}_{1} +\mathcal{P}_{2} +\mathcal{P}_{3})
\end{aligned}
\label{probs}
\end{equation}

represent the probabilities for a cell to move up, down, left, right, or stay in place, and where :math:`k=E,M` can refer to an epithelial-like or mesenchymal-like cell. Each cell on every grid point at location :math:`(x_i,y_j)` is modeled as an individual agent, which obeys probability rules for growth and movement. There is a maximal carrying capacity for each grid point given by :math:`Q,` (assumed equal to 4 in [@franssen2019]), to represent competition for space. There exist a doubling time :math:`T_E` and :math:`T_M` for epithelial and mesenchymal cells at which all the cells present in all grids will reproduce, duplicating in place, but never exceeding :math:`Q`.

Only the primary site is seeded with an initial number and distribution of cells. In order for the cells to migrate to another site, they must travel through the vasculature, which they do if they intravasate by one of the several randomly selected points in the grid that represent entrances to the vasculature system. The extravasation to one of the metastatic sites only occurs if they survive, a process that is modeled with net probabilistic rules considering time spent in the vasculature, cluster disaggregation, cell type, and potential biases to different destinations.

For the abiotic factors :math:`m` and :math:`w`, the discretization takes the form (see Appendices in [@franssen2019]):

\begin{equation}
\begin{aligned}
m_{i,j}^{n+1} = & D_{m}\frac{\Delta t_{a}}{( \Delta x_{a})^{2}}\left( m_{i+1,j}^{n} +m_{i-1,j}^{n} +m_{i,j+1}^{n} +m_{i,j-1}^{n}\right)\\
 & +m_{i,j}^{n}\left( 1-4D_{m}\frac{\Delta t_{a}}{( \Delta x_{a})^{2}} -\Delta t\Lambda \right) +\Delta t_{a} \Theta c^{n}_{Mi,j}\\
w_{i,j}^{n+1} = & w_{i,j}^{n}\left[ 1-\Delta t_{a}\left( \Gamma _{1} c{_{M}^{n}}_{i,j} +\Gamma _{2} m_{i,j}^{n}\right)\right]
\end{aligned}
\end{equation}

where :math:`i,j` reflect the grid point (:math:`i,j`) and :math:`n` the time-point. In this discretization two different time and spatial steps are used for the cell population (E and M cells) and the abiotic factors (ECM and MMP-2), namely :math:`\Delta t` and :math:`\Delta x = \Delta y`, :math:`\Delta t_a` and :math:`\Delta x_a = \Delta y_a` respectively.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Bibliography
============

.. bibliography::