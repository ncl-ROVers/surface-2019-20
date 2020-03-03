# Simulation

## Setup
Start by opening a terminal and navigating the the desired directory. Start by cloning surface by running:
```
git clone https://github.com/ncl-ROVers/surface
cd surface/
```

Then navigate to the simulation's root directory:
```
cd src
cd simulation
```

Next, you will need to download the source of all the submodules. To do this, run the command:
```
git submodule update --init --recursive
```
It's important that this command finishes successfully, otherwise source files will be missing and you will get an error during compilation.

Afterwards, there are two options. You can either generate a Visual Studio project (mostly for development) or build directly with CMake (recommended if you only want to build the executable).

1. **CMake**: You will need to download and install [CMake](https://cmake.org/). If you are on Windows, make sure that CMake is a part of your PATH. Once this is done, open a terminal in the simulation's root directory (`surface/src/simulation/`). Type `mkdir build`, then `cd build`. Then, run `cmake .. -DCMAKE_BUILD_TYPE=Release` and `cmake --build . --config Release` to build the executable. Now you can execute `.\Release\Simulation` to run to simulation,

2. **Visual Studio**: You will need to download [Premake](https://premake.github.io/). Make sure to download Premake 5 or later. Once you have downloaded Premake, copy the executable to the simulation's root directory (`surface/src/simulation/`). Then, run `./premake.exe vs2017`. This will build a Visual Studio solution. You can then open the solution and run it like usual (press `F5` to build and run). Otherwise, you can specify `gmake` instead of `vs2017` to generate a Makefile.

## Configuration file format
The configuration file uses JSON format. The following is a list of available options:

`scene`: Specify the scene to be loaded. (Format: string)
1. `grid`: A simple scene with just a horizontal grid.
2. `pool`: A scene inside a pool.

`camera`: Specify camera settings. (Format: string/object)
* String: Select from a list of presets.
	1. `firstperson`: First person camera controlled by WASD and the mouse.
	2. `headless`: No output from main camera. Only enable communication with surface. (Not currently supported!)
* Object: Explicitly specify camera properties.
	1. `pos`: Specify the initial camera position. (Format: `[ <x>, <y>, <z> ]`)
	2. `pitch`: Specify the initial pitch of the camera. (Format: `<pitch>`)
	3. `yaw`: Specify the initial yaw of the camera. (Format: `<yaw>`)
	4. `fov`: Specify the Field Of View of the camera in degrees. (Format: `<fov>`)
	5. `allowMovement`: Enable or disable camera movement. (Format: `true` / `false`)
	6. `allowLooking`: Enable or disable camera rotation. (Format: `true` / `false`)

`cache`: Specify cache settings. (Format: string/boolean)
* String: Specify the cache directory. (Format: `<cache_dir>`)
* Boolean: Enable or disable the cache. (Format: `true` / `false`)

`rov_setup`: Specify the properties of the ROV (Format: object). The following is a list of all possible fields:

* `mass`: Specify the mass of the ROV in kilograms. (Format: `<mass>`)

* `pos`: Specify the initial offset of the ROV from the origin in meters. (Format: `[ <x>, <y>, <z> ]`)

* `rot`: Specify the initial rotation of the ROV around the 3 axes. Each angle is in degrees. (Format: `[ <x_angle>, <y_angle>, <z_angle> ]`)

* `thrusters`: Specify properties of the ROV's thrusters (Format: Object of obje-cts). Each field's name is the index of the thruster and its value is an object with all the properties of the thruster:

	* A thruster index is made out of three characters:
		1. `s` or `v`: `h` for horizontal (down). `v` for vertical (up).
		2. `a` or`f`: `a` for aft (backward). `f` for fore (forward).
		3. `h` or `p`: `s` for starboard (right). `p` for port (left).
	* Properties of a thruster:
		1. `pos`: The object-space position of the thruster (Format: `[ <x>, <y>, <z> ]`).
		2. `rot`: The object-space rotation of the thruster around the 3 axes. Each angle is in degrees. (Format: `[ <x_angle>, <y_angle>, <z_angle> ]`)
		3. `force`: The initial force of the thruster, in Newtons. (Format: `<force>`) (Deprecated, to be removed).

* `cameras`: Specify properties of the ROV's virtual cameras (Format: Array of objects). Each element is an object with all the properties of an individual camera:

	* Properties of a camera:
		1. `pos`: The object-space position of the camera (Format: `[ <x>, <y>, <z> ]`).
		2. `rot`: The object-space rotation of the camera around the 3 axes. Each angle is in degrees. (Format: `[ <x_angle>, 	<y_angle>, <z_angle> ]`)
		3. `resolution`: The resolution of the camera (Format: `[ <width> <height> ]`).
        4. `fov`: The Field Of View angle of the camera (in degrees).
		5. `port`: The port the camera's video stream will available on.
		6. `quality`: An integer between 1 and 100 (inclusive) indicating the compression quality of the produced stream.
	
* `center_of_mass`: The object-space position of center of mass of the ROV.

* `max_thruster_force`: The maximum amount of force, in Newtons, that can be produced by a single thruster.

* `server_port`: The port number the ROV control server will be assigned to.

# Configuration examples

## Example 1

The following JSON code will result in a grid scene with the ROV of mass `50kg` at position `(1.0, 1.5, -5.0)`. The camera is in first person mode and caching is enabled.

    {
        "scene": "grid",
        "rov_setup": {
            "mass": 50.0,
            "pos": [ 1.0, 1.5, -5.0 ],
            "rot": [ 0.0, 0.0, 0.0 ],
            "thrusters": {
                "hfs": { "pos": [ 2.53743958, 0.61925888, -0.2160422 ], "rot": [ 90.00063771, 135.00360509, -0.16045937 ] },
                "hfp": { "pos": [ 2.53741074, 0.61925465, 0.2437050 ], "rot": [ 89.99990005, 45.00356502, 0.08723358 ] },
                "hap": { "pos": [ 0.97084224, 0.61884141, 0.2436065 ], "rot": [ 89.99938779, 315.00360668, 0.16046865 ] },
                "has": { "pos": [ 0.97087115, 0.61884564, -0.2161406 ], "rot": [ 90.00013911, 225.00360418, -0.08722996 ] },
                "vas": { "pos": [ 2.03029895, 1.34278131, -0.7146270 ], "rot": [ 0.05825762, 86.05404695, -0.03880541 ] },
                "vfs": { "pos": [ 1.39628148, 1.34278500, -0.7145472 ], "rot": [ 0.00000369, 180.00000000, 0.00000717 ] },
                "vfp": { "pos": [ 1.39618969, 1.34277153, 0.7420799 ], "rot": [ 0.00000000, 73.72771384, -0.00000000 ] },
                "vap": { "pos": [ 2.03041458, 1.34276795, 0.7421197 ], "rot": [ 0.00002615, 73.72619753, -0.00001482 ] }
            },
            "max_thruster_force": 5.0,
            "center_of_mass": [ 1.713296175, 0.6190501449999999, 0.01375635 ]
        },
        "camera": "firstperson",
        "cache": true
    }

## Example 2

The following JSON code will result in a grid scene with the ROV of mass `50kg` at position `(1.0, 1.5, -5.0)`. The camera is in custom mode, with an in initial position of `(0.0, 1.0, 3.0)`, an initial pitch if -20 degrees, a Field Of View angle of 70 degrees, and disabled movement. The cache directory has also been set to "../__sin_cache".

    {
        "scene": "grid",
        "rov_setup": {
        "mass": 50.0,
            "pos": [ 1.0, 1.5, -5.0 ],
            "rot": [ 0.0, 0.0, 0.0 ],
            "thrusters": {
                "hfs": { "pos": [ 2.53743958, 0.61925888, -0.2160422 ], "rot": [ 90.00063771, 135.00360509, -0.16045937 ] },
                "hfp": { "pos": [ 2.53741074, 0.61925465, 0.2437050 ], "rot": [ 89.99990005, 45.00356502, 0.08723358 ] },
                "hap": { "pos": [ 0.97084224, 0.61884141, 0.2436065 ], "rot": [ 89.99938779, 315.00360668, 0.16046865 ] },
                "has": { "pos": [ 0.97087115, 0.61884564, -0.2161406 ], "rot": [ 90.00013911, 225.00360418, -0.08722996 ] },
                "vas": { "pos": [ 2.03029895, 1.34278131, -0.7146270 ], "rot": [ 0.05825762, 86.05404695, -0.03880541 ] },
                "vfs": { "pos": [ 1.39628148, 1.34278500, -0.7145472 ], "rot": [ 0.00000369, 180.00000000, 0.00000717 ] },
                "vfp": { "pos": [ 1.39618969, 1.34277153, 0.7420799 ], "rot": [ 0.00000000, 73.72771384, -0.00000000 ] },
                "vap": { "pos": [ 2.03041458, 1.34276795, 0.7421197 ], "rot": [ 0.00002615, 73.72619753, -0.00001482 ] }
            },
            "max_thruster_force": 5.0,
            "center_of_mass": [ 1.713296175, 0.6190501449999999, 0.01375635 ]
        },
        "camera": {
          "pos": [ 0.0, 1.0, 3.0 ],
          "pitch": -20.0,
          "fov": 70.0,
          "allowMovement": false
        },
        "cache": "../__sim_cache"
    }
