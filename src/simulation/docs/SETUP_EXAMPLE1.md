## Setup file example 1

The following JSON code will result in a grid scene with the ROV of mass `50kg` at position `(1.0, 1.5, -5.0)`. The camera is in first person mode and caching is enabled.

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
        "camera": "firstperson",
        "cache": true
    }