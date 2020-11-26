import argparse
import subprocess
import os

PRECICE_CONFIG="""<?xml version="1.0"?>

<precice-configuration>

    <log>
        <sink filter="%Severity% > debug and %Rank% = 0" format="---[precice] %ColorizedSeverity% %Message%" enabled="true"/>
    </log>

    <solver-interface dimensions="3">

    <data:scalar name="Temperature"/>
    <data:scalar name="Heat-Flux"/>

    <mesh name="Fluid-Mesh">
        <use-data name="Temperature"/>
        <use-data name="Heat-Flux"/>
    </mesh>

    <mesh name="Solid-Mesh">
        <use-data name="Temperature"/>
        <use-data name="Heat-Flux"/>
    </mesh>

    <participant name="{participant:}">
        <use-mesh name="Fluid-Mesh" provide="yes"/>
        <use-mesh name="Solid-Mesh" from="Solid"/>
        <read-data name="Heat-Flux" mesh="Fluid-Mesh"/>
        <write-data name="Temperature" mesh="Fluid-Mesh"/>
        <mapping:nearest-neighbor direction="read" from="Solid-Mesh" to="Fluid-Mesh" constraint="consistent"/>
    </participant>

    <participant name="Solid">
        <use-mesh name="Fluid-Mesh" from="{participant:}"/>
        <use-mesh name="Solid-Mesh" provide="yes"/>
        <read-data name="Temperature" mesh="Solid-Mesh"/>
        <write-data name="Heat-Flux" mesh="Solid-Mesh"/>
        <mapping:nearest-neighbor direction="read" from="Fluid-Mesh" to="Solid-Mesh" constraint="consistent"/>
    </participant>

    <m2n:sockets from="{participant:}" to="Solid"/>

    {coupling_scheme:}
    {acceleration_scheme:}

    </solver-interface>

</precice-configuration>
"""

CONFIG_FILE_NAME="precice-config.xml"

EXPLICIT_COUPLING="""
    <coupling-scheme:serial-explicit>
        <max-time value="10"/>
	<time-window-size value="0.01"/>
        <participants first="{participant:}" second="Solid"/>
        <exchange data="Temperature" mesh="Fluid-Mesh" from="{participant:}" to="Solid"/>
        <exchange data="Heat-Flux" mesh="Solid-Mesh" from="Solid" to="{participant:}"/>
    </coupling-scheme:serial-explicit>
"""

IMPLICIT_COUPLING="""
    <coupling-scheme:serial-implicit>
        <time-window-size value="0.01"/>
        <max-time value="10"/>
        <participants first="{participant}" second="Solid"/>
        <exchange data="Temperature" mesh="Fluid-Mesh" from="{participant:}" to="Solid"/>
        <exchange data="Heat-Flux" mesh="Solid-Mesh" from="Solid" to="{participant:}"/>
        <max-iterations value="100"/>
        <relative-convergence-measure limit="1.0e-5" data="Temperature" mesh="Fluid-Mesh"/>
	<relative-convergence-measure limit="1.0e-5" data="Heat-Flux" mesh="Solid-Mesh"/>
"""

UNDERRELAXATION="""
	<acceleration:constant>
            <relaxation value="0.5"/>
        </acceleration:constant>
    </coupling-scheme:serial-implicit>
"""

AITKEN="""
	<acceleration:aitken>
	    <data name="Heat-Flux" mesh="Solid-Mesh"/>
            <initial-relaxation value="0.5"/>
        </acceleration:aitken>
    </coupling-scheme:serial-implicit>
"""

IQN_ILS="""
	<acceleration:IQN-ILS>
            <data name="Heat-Flux" mesh="Solid-Mesh"/>
	    <preconditioner type="residual-sum"/>
	    <filter type="QR2" limit="1e-3"/>
	    <initial-relaxation value="0.1"/>
	    <max-used-iterations value="100"/>
	    <time-windows-reused value="20"/>
        </acceleration:IQN-ILS>
    </coupling-scheme:serial-implicit>
"""


def main():

    CASE = None
    config_file = None

    parser = argparse.ArgumentParser("Build preCICE case with different coupling and acceleration schemes")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e",
                        "--explicit",
                        action="store_true"
                        )
    group.add_argument("-u",
                        "--underrelaxation",
                        action="store_true"
                        )
    group.add_argument("-a",
                        "--aitken",
                        action="store_true"
                        )
    group.add_argument("-i",
                        "--iqn",
                        action="store_true"
                        )
    parser.add_argument("-s",
                        "--scalar",
                        action="store_true"
                        )
    parser.add_argument("-b",
                        "--buoyant",
                        action="store_true"
                        )

    args = parser.parse_args().__dict__

    if args["explicit"]:
        coupling_scheme = EXPLICIT_COUPLING
        acceleration_scheme = ""
    elif args["underrelaxation"]:
        coupling_scheme = IMPLICIT_COUPLING
        acceleration_scheme = UNDERRELAXATION
    elif args["aitken"]:
        coupling_scheme = IMPLICIT_COUPLING
        acceleration_scheme = AITKEN
    elif args["iqn"]:
        coupling_scheme = IMPLICIT_COUPLING
        acceleration_scheme = IQN_ILS
    else:
        parser.print_help()
        exit(1)

    if args["buoyant"]:
        CASE = "1"
        participant="Fluid-buoyantPimpleFoam"
    elif args["scalar"]:
        CASE = "2"
        participant="Fluid-scalarTransportFoam"
    else:
        parser.print_help()
        exit(1)

    coupling_scheme = coupling_scheme.format(participant=participant)
    config_file = PRECICE_CONFIG.format(coupling_scheme=coupling_scheme,
                                        acceleration_scheme=acceleration_scheme,
                                        participant=participant)

    if CASE is not None and config_file is not None:
        with open(CONFIG_FILE_NAME, "w") as f:
            f.write(config_file)

        subprocess.call(["./Allrun", CASE])

    else:
        print("Cannot run.")
        exit(1)

if __name__ == "__main__":
    main()