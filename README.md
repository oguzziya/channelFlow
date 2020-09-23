This repository contains preCICE test cases for conjugate heat transfer of channel flow, which are extension to the work of Holger Marschall [conjugateHeatFoam](https://bitbucket.org/hmarschall/conjugateheatfoam/src/master/)

# Branch structure
master: buoyantPimpleFoam-laplacianFoam coupling without results and comments
buoyantPimpleFoam-laplacianFoam: buoyantPimpleFoam-laplacianFoam coupling with results
scalarTransportFoam-laplacianFoam: scalarTransportFoam-laplacianFoam coupling with results

# Directory Structure
**conjugateHeatFoam** Copy of the repository: [conjugateHeatFoam](https://bitbucket.org/hmarschall/conjugateheatfoam/src/master/)

conjugateHeatFoam cases:
- **conjugateHeatFoam_Monolithic** Monolithic coupling using conjugateHeatFoam
- **conjugateHeatFoam_Partitioned** Partitioned coupling using conjugateHeatFoam

preCICE cases:
- **preCICE_Case** Contains the fluid and solid side setups as well as the preCICE configuration. Configuration files for different coupling schemes are in `preCICE_Configs` directory. To use different acceleration scheme, copy the respective configuration file into the case directory with name `precice-config.xml`. For example, to test Aitken acceleration:
  
```bash
cp preCICE_Case/precice-config-Aitken.xml preCICE_Case/precice-config.xml
```

All the cases can be directly run by moving in respective directory and executing `./Allrun`.

# preCICE Coupling

## Software Versions
- OpenFOAM (conjugateHeatFoam): foam-extend 4.1
- OpenFOAM (preCICE): 19.12
- preCICE: 2.1.0
- preCICE OpenFOAM Adapter: c49b862aab4845ae79b8b7257a20e15ba5a0019c

## Participant Setup
In order to make the two cases similar to each other as much as possible, `scalarTransportFoam` is used for fluid flow solver. However, OpenFOAM adapter requires solver to access Heat-Flux data, which is not trivial for `scalarTransportFoam`. Therefore it ends up with problems in the flux calculation. In order to resolve the issue, `buoyantPimpleFoam` is also used for fluid participant, which is supported by OpenFOAM Adapter out-of-the box. 

For completeness, we provide both approaches in different branches as:

- buoyantPimpleFoam-laplacianFoam
- scalarTransportFoam-laplacianFoam

You can checkout to individual branch to see the respective case and results. In the master, setup for `buoyantPimpleFoam-laplacianFoam` exists.

All the boundary conditions, physical properties, solver and discretization settings are tried to be hold the same as the main OpenFOAM cases.

Coupling parameters are:
- **Time window size:** 0.01
- **Convergence measure:** Temperature (In OpenFOAM cases heat flux is also used, however the residuals of heat flux in OpenFOAM cases are always zero. Therefore heat flux is not included in the convergence measure.)
- **Relative convergence tolerance:** 1e-5 (Same as OpenFOAM cases)

### Underrelaxation
- **Underrelaxation factor:** 0.5 (Same as OpenFOAM cases)

### Aitken
- **Initial relaxation factor:** 0.5

### Quasi-Newton
- **Quasi-Newton Scheme:** IQN-ILS
- **Initial relaxation factor:** 0.5
- **Maximum used iterations:** 80
- **Reused time windows:** 10
- **Filter:** QR1 with 1e-8