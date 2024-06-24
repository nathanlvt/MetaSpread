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
The dimensionless model, as described by [@franssen2019] in Appendix A of their paper, corresponds to 4 PDEs, where the key variables reflect local densities of epithelial cells ($c_E$) and mesenchymal cells ($c_M$), and concentrations of MMP2 ($m$) and extracellular matrix ($w$):

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

  \begin{equation}
  \begin{aligned}
  \frac{\partial c_{E}}{\partial t} & =D_{\mathrm{E}} \nabla ^{2} c_{\mathrm{E}} -\Phi _{\mathrm{E}} \nabla \cdot ( c_{\mathrm{E}} \nabla w)\\
  \frac{\partial c_{\mathrm{M}}}{\partial t} & =D_{\mathrm{M}} \nabla ^{2} c_{\mathrm{M}} -\Phi _{\mathrm{M}} \nabla \cdot ( c_{\mathrm{M}} \nabla w)\\
  \frac{\partial m}{\partial t} & =D_{m} \nabla ^{2} m+\Theta c_{\mathrm{M}} -\Lambda m\\
  \frac{\partial w}{\partial t} & =-( \Gamma _{1} c_{\mathrm{M}} +\Gamma _{2} m) w
  \end{aligned}
  \end{equation}
   :label: eqn1

Test: :eq:`eqn1`
For the simulation of the spatio-temporal growth dynamics, and metastatic spread, the system of PDE's is discretized, and several 2-dimensional grids are established, representing the primary site and the metastatic sites. Discretizing equations for :math:`c_E` and :math:`c_M` in space and time, we obtain:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Bibliography
============

.. bibliography::