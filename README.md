This repository contains preCICE test cases for conjugate heat transfer of channel flow, which are extension to the work of Holger Marschall [conjugateHeatFoam](https://bitbucket.org/hmarschall/conjugateheatfoam/src/master/)

# How to get the cases
```bash
git clone --recursive https://github.com/oguzziya/channelFlow.git
```

# How to run the cases
The installation and tutuinstructions of OpenFOAM solver `conjugateHeatFoam` can be found in: [conjugateHeatFoam](https://bitbucket.org/hmarschall/conjugateheatfoam/src/master/)

For the preCICE cases, several options are possible to run the cases:

## 1- Using Python script
Using the script `run.py`, one can produce the preCICE configuration file and run the cases automatically. This script takes two arguments: 

- OpenFOAM solver for the fluid participant: 
	- `--scalar, -s`: scalarTransportFoam
	- `--buoyant, -b`: buoyantPimpleFoam
- Coupling scheme:
	- `--explicit, -e`: Explicit coupling
	- `--underrelaxation, -u`: Implicit coupling with constant underrelaxation
	- `--aitken, -a`: Implicit coupling with dynamic Aitken underrelaxation
	- `--iqn, -i`: Implicit coupling with IQN-ILS acceleration
	
## 2- Using Allrun or runFluid&runSolid
`Allrun` and `runSolid` script takes one argument, which corresponds to the type of the fluid participant solver:
- `./Allrun 1`: buoyantPimpleFoam
- `./Allrun 2`: scalarTransportFoam

The important point is that, with this approach user needs to modify the corresponding preCICE configuration file. Therefore, using the Python script is highly encouraged.

# preCICE Coupling

## Software Versions
- OpenFOAM (conjugateHeatFoam): foam-extend 4.1
- OpenFOAM (preCICE): 20.06
- preCICE: 2.1.0
- preCICE OpenFOAM Adapter: c49b862aab4845ae79b8b7257a20e15ba5a0019c

## Participant Setup
In order to make the two cases similar to each other as much as possible, `scalarTransportFoam` is used for fluid flow solver. However, OpenFOAM adapter requires solver to access Heat-Flux data, which is not trivial for `scalarTransportFoam`. Therefore it ends up with problems in the flux calculation. In order to resolve the issue, `buoyantPimpleFoam` is also used for fluid participant, which is supported by OpenFOAM Adapter out-of-the box. 

All the boundary conditions, physical properties, solver and discretization settings are tried to be hold the same as the main OpenFOAM cases.

Coupling parameters are:
- **Time window size:** 0.01
- **Convergence measure:** Temperature and Heat-Flux
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
