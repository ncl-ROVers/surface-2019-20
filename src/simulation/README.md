# Simulation

## Setup
Start by opening a terminal and navigating the the desired directory. Start by cloning surface by running:
```
git clone https://github.com/ncl-ROVers/surface
cd surface/
```

Then, run the following to switch to the simulation branch and navigate to the simulation's root directory.
```
git checkout simulation
cd src
cd simulation
```

Next, you will need to download the source of all the submodules. To do this, run the command:
```
git submodule update --init --recursive
```
It's important that this command finishes successfully, otherwise source files will be missing and you will get an error during compilation.

Lastly, you will need to download [Premake](https://premake.github.io/). Make sure to download Premake 5 or later. Once you have downloaded Premake, copy the executable to the simulation's root directory (`surface/src/simulation/`). Then, run `./premake.exe vs2017`. This will build a Visual Studio solution. You can then open the solution and run it like usual (press `F5` to build and run). Otherwise, you can specify `gmake` instead of `vs2017` to generate a Makefile.

## Configuration file format
The file is broken into lines. Each line starts with a string that indicates the type of data that follows:

`MASS <m>`: Specify the mass of the ROV in kilograms.

`POS <x> <y> <z>`: Specify the initial offset of the ROV from the origin in meters.

`ROT <x_angle> <y_angle> <z_angle>`: Specify the initial rotation of the ROV around the 3 axes. Each angle is in degrees.

`T_<index> <force>`: Specify the force produced by the specified thruster in Newtons. A thruster index is made out of three characters:
1. `H` or `V`: `H` for horizontal (down). `V` for vertical (up).
2. `A` or`F`: `A` for aft (backward). `F` for fore (forward).
3. `S` or `P`: `S` for starboard (right). `P` for port (left).
