# Py4MTX
# This repo is in a process of reorganization and adaption to Python 3.11, mtpy-v2 and integrating Jacobian-related functionality. Not fully ready for production use!

This repository currently contains simple scripts useful for EM imaging, modelling, and inversion, partly using mtpy (to be downloaded from https://github.com/MTgeophysics/mtpy-v2). The workflows for reading and processing Jacobians from ModEM outputs has been copied from https://github.com/volkerrath/JacoPyAN, and will be further developed here. 

The repository contains the following subdirectories:


 -	**py4mt/info**
 	Doumentation for the toolbox, and some useful documentation for python, 
 	including the most important extensions, numpy, scipy, and matplotlib 
 	
 -	**py4mt/modules**
 	Contains the modules distortion.py, jacproc.py, mimdas.py, modem.py  mtplots.py,  plot.py,  
	plotrjmcmc.py, and util.py, called from the Python scripts run for different tasks of MT
	interprretation.
 	
 - 	**py4mt/scripts** 
 	Contains the scripts  for preprocessing, visualization, and preparing the inversion of 
 	MT data.   	 
 

- 	**modem**
	Modified and original ModEM source code files including corresponding Makefiles, useful for 
	sensitivity output.  
	
- 	**environment**
	Contains conda environment description files, and some useful helper files for working 
	within the conda environment. The current Py4MT environments contain a lot of packages
	which are not strictly necessary for running aempy, but useful for related geoscientific work.
	


Get your working copy via git from the command line:

_git clone https://github.com/volkerrath/Py4MTX/_

This version will run under Python 3.9+ (3.11 being the current development platform). To install it in an Linux environment (e.g. Ubuntu, SuSE), you need to do the following:

(1) Download the latest Anaconda or Miniconda version  (https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html), and install by running the downloaded bash script.  In order to make updates secure and avoid inconsistencies, copy .condarc to your home directory. As the Miniconda installer is not updated very frequently, it is useful to run the following within the Miniconda base environment:

_conda update conda_

_conda update --all_

Do this regularly to keep everything consistent!

(2) Create an appropriate conda environment (including the necessary prerequisites) from the files Py4MTX.yml or Py4MTX.txt found in the Py4MTX _environment_ directory by:

_conda env create -f Py4MTX.yml_

or:

_conda create --name Py4MTX --file Py4MTX.txt_

This will set up a Python 3.11 environment with all dependencies for aempy. Don't forget to update also Py4MTX regularly, using _conda update --name Py4MTX--all_! 

**Warning: the current versions of mtpy-v2 from conda and pip are not working correctly, please install it from source (https://github.com/MTgeophysics/mtpy-v2)!**

(3) Activate this environment by:

_conda activate Py4MTX_

(4) In order to reproduce the identical behavior of matplotlib, you should copy the included  _matplotlibrc_ file to the appropriate directory. Under Linux (Ubuntu), this should be : _$HOME/.config/matplotlib/matplotlibrc_. Pertinent changes should be made there, or have to be made within the scripts/modules using the _mpl.rcParams[name]=value_ mechanism. 

(6) Currently we have defined two environmental variable, _PY4MTX_ROOT_ and _PY4MTX_DATA_. These need to be set in your .bashrc file pointing to the place where Py4MTX is installed, and where you keep your MT data, respectively. 

Example: 

_export PY4MT_ROOT='${HOME}/Py4MT/'_
	
_export PY4MT_DATA='${HOME}/Py4MT/data/'_

Keeping to this scheme makes life much easier when different persons work on the tools. Never change the sources within the repository, as this may produce conflicts when updating! 
Please keep in mind that this is experimental software, and will contain errors. Use at your own risk! However, we will frequently update the repository correcting bugs, and (re)adding additional functionality.  
 

# On Jacobian-related functionalities including sensitivities

This repository now also contains $\texttt{python}$ tools for manipulating, processing, analysing Jacobians from 3-D magnetotelluric inversion, including 
randomized singular value decompositions (SVD), and other tools related to the Nullspace-Shuttle method [1, 2]. Currently, we have implemented the tools necessary
for using Jacobians generated by $\texttt{ModEM}$ [3, 4]. As of today, the routines for manipulating/sparsifying the full Jacobian, the SVD, and the calculation of sensitivity 
can be used.

**Adapting $\texttt{ModEM}$ for Jacobian output**

The Jacobian  of a data and parameter set is defined as $J_{ij} = \dfrac{\delta d_i}{\delta m_j}$. Before being able to use it for further
action, a  few steps are necessary. $\texttt{ModEM}$ seeks the MAP solution to the usual Bayesian inverse problem [5] defined by:

```math
\Theta  = {({\mathbf{g}}({\mathbf{p}}) - {\mathbf{d}})^T}{\mathbf{C}}_{d}^{-1}({\mathbf{g}}({\mathbf{p}}) - {\mathbf{d}}) + {({\mathbf{p}} - {{\mathbf{p}}_a})^T}{\mathbf{C}}_{p}^{-1}({\mathbf{p}} - {{\mathbf{p}}_a}) =
\left||| {{\mathbf{C}}_{d}^{-1/2}({\mathbf{g}}({\mathbf{p}}) - {\mathbf{d}})} \right|||_2^2 + \left||| {{\mathbf{C}}_{p}^{-1/2}({\mathbf{p}} - {{\mathbf{p}}_a})} \right|||_2^2 
```


Transformig the parameter vector by
```math
{\mathbf{\tilde{p}}}={\mathbf{C}}_{m}^{-1/2} {({\mathbf{p}}-{\mathbf{p}_a})} ,
```
the data by

```math
{\mathbf{\tilde{d}}}={\mathbf{C}_{d}^{-1/2}} {\mathbf{d}},
```

leads to the further transformation

```math
{\mathbf{\tilde{g}}}({\mathbf{\tilde{p}}})={\mathbf{C}_{d}^{-1/2}} {\mathbf{g}} ({\mathbf{C}}_{m}^{1/2} {\mathbf{\tilde{p}}}).
```

From this we havethe simplified objective function

```math
\tilde{\Theta} ({\mathbf{\tilde{p},\tilde{d}}}) = {\left||| {{\mathbf{\tilde d - \tilde g(\tilde p)}}} \right|||_2^2} + \lambda {\left|| {{\mathbf{\tilde p}}} \right||_2^2}.
```
The Jacobian used within $\texttt{ModEM}$ is also calculated in the transformed system:

```math
  {\mathbf{\tilde{J}}} = {\mathbf{C}}_{d}^{-1/2} {\mathbf{J}} {\mathbf{C}}_{m}^{1/2}
```
For this reason, some minor changes in the $\texttt{ModEM}$ source code were made. They do not touch the original functionality, as they are controlled by 
compiler directives. Activating the new code is done by adding $\texttt{-DJAC}$ to the $\texttt{FFLAGS}$ line in the corresponding 
$\texttt{Makefile}$. The adapted code can be found in the $\texttt{modem}$ subdirectory of the  $\texttt{JacoPyAn}$ repository, and 
can be simply copied to the original $\texttt{f90}$ subdirectory in the original source code. 

The changes made in the souce code will only be relevant to the parts used  by the calculation and storage of the Jacobian. In addition to the 
binary file $\texttt{Model.jac}$ containing the physical-space Jacobian (the name is arbitrary), also an ASCII file $`\texttt{Model\_jac.dat}`$ is 
created, which contains data information in the correct sequence and units. 

**Preprocessing the Jacobian**

The generated Jacobians for realistic models  can be large (several tens of Gb). For this reason the first step in working with the Jacobians is
to put them into a format easier to handle by $\texttt{python}$, and, as many of the elements of these matrices are small, reduce their size. This
is done in the script $`\texttt{MT\_jac\_proc.py}`$ .

**Sensitivities**

The use of sensitivities (in a variety of flavours) is comparatively easy, but needs some clarification, as it does not really conform 
to the everyday use of the word. Sensitivities are derived from the final model Jacobian matrix, which often is available from the inversion algorithm 
itself. It needs to be kept in mind that this implies any conclusions drawn are valid in the domain of validity for the Taylor expansion involved only. 
This may be a grave disadvantage in highly non-linear settings, but we believe that it still can be usefull for fast characterization of uncertainty.

Here, the parameter vector $\mathbf{m}$ is the natural logarithm of resistivity. This Jacobian is first normalized with the data error 
to obtain $\mathbf{\tilde{J}}$. While this procedure is uncontroversial, the definition of sensitivity is not unique, and various forms
an be found in the literature. 

$\texttt{Py4MTX}$ calculates "Euclidean" sensitivities, which are the most commonly used form. They are is defined as: 

$S^2_j = \sum_{i=1,n_d} \left||\tilde{J}_{ij}\right||^2=diag\left(\mathbf{\tilde{J}}^T\mathbf{\tilde{J}}\right)$.

The square root of this sensitivity is often preferred, and is implemented in many popular inversion codes. Also availble
is coverage where, the absolute values of the Jacobian are summed: 
$\sum_{i=1,n_d} \left||\tilde{J}_{ij}\right||$
For a definition of a depth of investigation (DoI), or model blanking/shading, forms (2) and (3) can be used. This, however, requires the 
choice of a threshold/scale is required, depending on the form applied. 

When moving from the error-normalised Jacobian, $\mathbf{J}_d$ to sensitivity, there are more choices for further normalisation, depending 
on the understanding and use of this parameter. All mentioned sensitivities are dependent on the underlying mesh. If sensitivity is to be interpreted 
as an approximation to a continuous field over the volume of the model, it seems useful normalize by the cell volume. On the other hand, the effect of 
the volume and its geometry is important when investigating the true role of this cell in the inversion. Given that the raw sensitivities for 
different data types may vary 1-2 orders of magnitude), for some purposes (e.g., comparison of different data (sub)sets or definition of depths of 
investigation) it may be convenient to do a final normalization by the maximum value in the model. All these options are implemented in the $\texttt{Py4MTX}$ toolbox. 

_[1] M. Deal and G. Nolet (1996) “Nullspace shuttles", Geophysical Journal International, 124, 372–380_

_[2] G. Muñoz and V. Rath (2006)
“Beyond smooth inversion: the use of nullspace projection for the exploration of non-uniqueness in MT", Geophysical Journal International, 164, 301–311, 2006, doi:10.1111/j.1365-246X.2005.02825.x_

_[3] G. D. Egbert and A. Kelbert (2012) “Computational recipes for electromagnetic inverse problems”, Geophysical Journal International, 189, 251–267, doi:10.1111/j.1365-246X.2011.05347.x_

_[4] A. Kelbert, N. Meqbel, G. D. Egbert, and K. Tandon (2014) “ModEM: A Modular System for Inversion of Electromagnetic Geophysical Data”, Computers & Geosciences, 66, 440–53, doi:10.1016/j.cageo.2014.01.010_

_[5] A. Tarantola (2005) "Inverse Problem Theory and Methods for Model Parameter Estimation", SIAM, Philadelphia PA, USA_
     
_[6] K. Schwalenberg, V. Rath, and V. Haak (2002) “Sensitivity studies applied to a two-dimensional resistivity model from the Central Andes”, Geophysical Journal International, 150, doi:10.1046/j.1365-246X.2002.01734.x_
  
 
  
 


