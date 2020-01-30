## Setup file example 2

The following JSON code will result in a grid scene with the ROV of mass `50kg` at position `(1.0, 1.5, -5.0)`. The camera is in custom mode, with an in initial position of `(0.0, 1.0, 3.0)`, an initial pitch if -20 degrees, a Field Of View angle of 70 degrees, and disabled movement. The cache directory has also been set to "../__sin_cache".

    {
      "scene": "grid",
      "mass": 50.0,
      "pos": [ 1.0, 1.5, -5.0 ],
      "rot": [ 0.0, 0.0, 0.0 ],
      "thrusters": {
        "has": 0.01,
        "vas": 0.01,
        "vfp": 0.01,
        "hfp": -0.01
      },
      "camera": {
        "pos": [ 0.0, 1.0, 3.0 ],
        "pitch": -20.0,
        "fov": 70.0,
        "allowMovement": false
      },
      "cache": "../__sim_cache"
    }