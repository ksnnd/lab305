| Per-class results: |  |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Object Class | AP | ATE | ASE | AOE | AVE | AAE |
| car | 0.494 | 0.541 | 0.160 | 0.115 | 1.366 | 0.246 |
| truck | 0.215 | 0.687 | 0.219 | 0.109 | 1.656 | 0.419 |
| bus | 0.329 | 0.672 | 0.192 | 0.113 | 2.226 | 0.456 |
| trailer | 0.053 | 0.965 | 0.238 | 0.495 | 1.686 | 0.300 |
| construction_vehicle | 0.026 | 1.076 | 0.530 | 1.127 | 0.203 | 0.367 |
| pedestrian | 0.332 | 0.699 | 0.298 | 1.410 | 0.937 | 0.665 |
| motorcycle | 0.254 | 0.645 | 0.255 | 0.568 | 2.493 | 0.105 |
| bicycle | 0.193 | 0.579 | 0.259 | 0.652 | 0.520 | 0.112 |
| traffic_cone | 0.508 | 0.501 | 0.400 | nan | nan | nan |
| barrier | 0.336 | 0.567 | 0.333 | 0.214 | nan | nan |



| Per-class results: |  |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Object Class | AP | ATE | ASE | AOE | AVE | AAE |
| car | 0.504 | 0.617 | 0.154 | 0.121 | 1.088 | 0.237 |
| truck | 0.276 | 0.848 | 0.226 | 0.219 | 0.911 | 0.257 |
| bus | 0.341 | 0.865 | 0.216 | 0.148 | 2.314 | 0.392 |
| trailer | 0.112 | 1.199 | 0.255 | 0.663 | 0.398 | 0.089 |
| construction_vehicle | 0.063 | 1.108 | 0.525 | 1.160 | 0.126 | 0.383 |
| pedestrian | 0.419 | 0.733 | 0.294 | 1.026 | 0.834 | 0.574 |
| motorcycle | 0.308 | 0.794 | 0.259 | 0.905 | 1.618 | 0.106 |
| bicycle | 0.280 | 0.728 | 0.269 | 1.247 | 0.574 | 0.029 |
| traffic_cone | 0.515 | 0.602 | 0.317 | nan | nan | nan |
| barrier | 0.420 | 0.778 | 0.278 | 0.192 | nan | nan | 

| results: |  |
| :--- | :--- |
| mAP: | 0.6319 |
| mATE: | 0.2823 |
| mASE: | 0.2550 |
| mAOE: | 0.3663 |
| mAVE: | 0.2808 |
| mAAE: | 0.1862 |
| NDS: | 0.6789 |

| results: |  |
| :--- | :--- |
| mAP: | 0.4974 |
| mATE: | 0.3126 |
| mASE: | 0.2710 |
| mAOE: | 0.3823 |
| mAVE: | 0.3973 |
| mAAE: | 0.1970 |
| NDS: | 0.5972 |

| Per-class results: |  |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0bject Class | AP | ATE | ASE | AOE | AVE | AAE |
| car | 0.866 | 0.173 | 0.152 | 0.094 | 0.286 | 0.187 |
| truck | 0.589 | 0.336 | 0.183 | 0.085 | 0.249 | 0.229 |
| bus | 0.709 | 0.342 | 0.190 | 0.083 | 0.479 | 0.234 |
| trailer | 0.429 | 0.489 | 0.207 | 0.820 | 0.202 | 0.189 |
| construction_vehicle | 0.261 | 0.674 | 0.432 | 0.937 | 0.125 | 0.307 |
| pedestrian | 0.856 | 0.136 | 0.280 | 0.369 | 0.220 | 0.094 |
| motorcycle | 0.676 | 0.196 | 0.248 | 0.341 | 0.457 | 0.242 |
| bicycle | 0.517 | 0.155 | 0.257 | 0.511 | 0.227 | 0.009 |
| traffic_cone | 0.727 | 0.132 | 0.314 | nan | nan | nan |
| barrier | 0.690 | 0.191 | 0.287 | 0.057 | nan | nan |




| Parameter               | nuScenes (7DoF)                          | Suscape (9DoF)                                  |
|--------------------------|------------------------------------------|------------------------------------------------|
| Position                | (x, y, z)                                | (x, y, z)                                      |
| Size                    | (Length, Width, Height)                 | (Length, Width, Height)                      |
| Orientation             | yaw (Rotation around Y-axis)             | yaw + pitch + roll (Rotations around Y/X/Z-axes) |
| Applicable Scenario     | Flat ground (e.g., urban roads)          | Complex terrains (e.g., slopes, uneven roads) |

