<style media="screen,print"> .pb_after { page-break-after: always !important; } </style>

Complex systems / Molecular Dynamics

Federico Williamson / 13938

## Section I

### Part 1: Run results:


#### a - Base run
##### Code params
```
run_steps: 1000
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.378** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 9.8574         |     9.8574     | 9.8574         | 0.0       |     81.51 |
|  1 | Neigh      | 2.0487         |     2.0487     | 2.0487         | 0.0       |     16.94 |
|  2 | Comm       | 0.04139        |     0.04139    | 0.04139        | 0.0       |      0.34 |
|  3 | Output     | 0.00010031     |     0.00010031 | 0.00010031     | 0.0       |      0    |
|  4 | Modify     | 0.1323         |     0.1323     | 0.1323         | 0.0       |      1.09 |
|  5 | Other      |                |     0.01307    |                |           |      0.11 |

Loop time: 12.0929

![Plot a](plot_a.png){ width=100% }

<div class="pb_after"></div>

#### b - 10x steps
##### Code params
```
run_steps: 10000
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.384** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 99.956         |      99.956    | 99.956         | 0.0       |     81.4  |
|  1 | Neigh      | 20.942         |      20.942    | 20.942         | 0.0       |     17.05 |
|  2 | Comm       | 0.40992        |       0.40992  | 0.40992        | 0.0       |      0.33 |
|  3 | Output     | 0.012552       |       0.012552 | 0.012552       | 0.0       |      0.01 |
|  4 | Modify     | 1.331          |       1.331    | 1.331          | 0.0       |      1.08 |
|  5 | Other      |                |       0.1448   |                |           |      0.12 |

Loop time: 122.796

![Plot b](plot_b.png){ width=100% }

<div class="pb_after"></div>

#### c - 8x Box
##### Code params
```
run_steps: 1000
box: (40, 40, 40)
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.371** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 76.481         |    76.481      | 76.481         | 0.0       |     80.63 |
|  1 | Neigh      | 15.935         |    15.935      | 15.935         | 0.0       |     16.8  |
|  2 | Comm       | 0.39647        |     0.39647    | 0.39647        | 0.0       |      0.42 |
|  3 | Output     | 0.00070795     |     0.00070795 | 0.00070795     | 0.0       |      0    |
|  4 | Modify     | 1.6273         |     1.6273     | 1.6273         | 0.0       |      1.72 |
|  5 | Other      |                |     0.4135     |                |           |      0.44 |

Loop time: 94.8545

![Plot c](plot_c.png){ width=100% }

<div class="pb_after"></div>

#### c - 8x Box (Elongated)
##### Code params
```
run_steps: 1000
box: (20, 20, 160)
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.382** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 78.816         |    78.816      | 78.816         | 0.0       |     80.65 |
|  1 | Neigh      | 16.136         |    16.136      | 16.136         | 0.0       |     16.51 |
|  2 | Comm       | 0.6813         |     0.6813     | 0.6813         | 0.0       |      0.7  |
|  3 | Output     | 0.00071879     |     0.00071879 | 0.00071879     | 0.0       |      0    |
|  4 | Modify     | 1.6833         |     1.6833     | 1.6833         | 0.0       |      1.72 |
|  5 | Other      |                |     0.4143     |                |           |      0.42 |

Loop time: 97.7321

![Plot c2](plot_c2.png){ width=100% }

<div class="pb_after"></div>

#### d - 2x Neigh skin
##### Code params
```
run_steps: 1000
neigh_skin: 0.6
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.530** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 14.474         |    14.474      | 14.474         | 0.0       |     85.33 |
|  1 | Neigh      | 2.2878         |     2.2878     | 2.2878         | 0.0       |     13.49 |
|  2 | Comm       | 0.045207       |     0.045207   | 0.045207       | 0.0       |      0.27 |
|  3 | Output     | 0.00010528     |     0.00010528 | 0.00010528     | 0.0       |      0    |
|  4 | Modify     | 0.13921        |     0.13921    | 0.13921        | 0.0       |      0.82 |
|  5 | Other      |                |     0.01594    |                |           |      0.09 |

Loop time: 16.9622

![Plot d](plot_d.png){ width=100% }

<div class="pb_after"></div>

#### f - With dumps
##### Code params
```
run_steps: 1000
do_image_dump: True
do_video_dump: True
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.488** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 9.8829         |       9.8829   | 9.8829         | 0.0       |     63.32 |
|  1 | Neigh      | 2.0568         |       2.0568   | 2.0568         | 0.0       |     13.18 |
|  2 | Comm       | 0.043411       |       0.043411 | 0.043411       | 0.0       |      0.28 |
|  3 | Output     | 3.472          |       3.472    | 3.472          | 0.0       |     22.24 |
|  4 | Modify     | 0.13817        |       0.13817  | 0.13817        | 0.0       |      0.89 |
|  5 | Other      |                |       0.01514  |                |           |      0.1  |

Loop time: 15.6084

![Plot f](plot_f.png){ width=100% }

<div class="pb_after"></div>

#### g - balanced
##### Code params
```
run_steps: 1000
balance: 1.2 shift xz 5 1.1
```
##### Simulation params
```
use_mpi: False
```
##### Result
TPAS ~= **0.378** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 9.8412         |     9.8412     | 9.8412         | 0.0       |     81.43 |
|  1 | Neigh      | 2.0524         |     2.0524     | 2.0524         | 0.0       |     16.98 |
|  2 | Comm       | 0.041288       |     0.041288   | 0.041288       | 0.0       |      0.34 |
|  3 | Output     | 0.00010442     |     0.00010442 | 0.00010442     | 0.0       |      0    |
|  4 | Modify     | 0.13539        |     0.13539    | 0.13539        | 0.0       |      1.12 |
|  5 | Other      |                |     0.01447    |                |           |      0.12 |

Loop time: 12.0849

![Plot g](plot_g.png){ width=100% }

<div class="pb_after"></div>

#### e - Overall system energy

|      |    TotEng a |    TotEng b |    TotEng c |   TotEng c2 |    TotEng d |    TotEng f |    TotEng g |
|:-----|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| mean | -5.27716    | -5.27829    | -5.27729    | -5.27725    | -5.27716    | -5.27716    | -5.27716    |
| std  |  0.00530259 |  0.00421841 |  0.00553594 |  0.00547916 |  0.00530259 |  0.00530259 |  0.00530259 |

<div class="pb_after"></div>


![Weak speedup](weak_speedup.png){ width=100% }
![Weak efficiency](weak_efficiency.png){ width=100% }
![Strong speedup](strong_speedup.png){ width=100% }
![Strong efficiency](strong_efficiency.png){ width=100% }
![Speedup](speedup.png){ width=100% } ![Logarithmic speedup](speedup_log.png){ width=100% }
![Efficiency](efficiency.png){ width=100% }



a: Base run

b: The simulation cost increases by about 10x, because the number of steps increases by 10x, and we are running on the same number of cores.

c: The simulation cost increases by about 8x, because the box size increases by 8x, and we are running on the same number of cores.

c2: The simulation cost increases by about 8x, because the box size increases by 8x, and we are running on the same number of cores. (There seems to be no performance overhead when running on a single machine)

d: I would expect the neighbor cost to _increase_ by about $4/3 \pi (2r)^3 - r^3$ or about $7r^3$, because the number of steps is the same, but the number of neighbors to check scales with the volume of the sphere of the neighbors.
In our example, with relation to the base run this amounts to about a 33% increase in wall time. 

e: They are very similar, this is to be expected as the number of steps is the same, and the number of atoms is the same.

f: The simulation cost increases slightly (~3s), this might be influenced by the fact that my SSD is very fast.

g: The simulation cost decreases by about 10%, this is to be expected as the load is balanced between the cores.


### Part 2

#### a: Strong scaling

strong 2x: The simulation cost decreases by about 2x, this is to be expected as the number of atoms is the same, but the number of cores is 2x.

strong 4x: The simulation cost decreases by about 4x, this is to be expected as the number of atoms is the same, but the number of cores is 4x.

strong 8x: The simulation cost decreases by slightly less than 8x

strong 16x: The simulation cost decreases by slightly less than 16x

strong 32x - hw: The simulation cost increases by about 3x with respect to 2. strong 16x, this is to be expected as the number of steps is the same, but the number of cores is 32x, and my machine only has 16 physical cores.


### b: Weak scaling

> All the weak scaling tests are run on 16 cores

weak 2x: The simulation cost increases by about 2x, this is to be expected as the number of atoms is the 2x, but the number of cores is the same.

weak 4x: The simulation cost increases by about 4x, this is to be expected as the number of atoms is the 4x, but the number of cores is the same.

weak 8x: The simulation cost increases by about 8x, this is to be expected as the number of atoms is the 8x, but the number of cores is the same.

weak 16x: The simulation cost increases by about 16x, this is to be expected as the number of atoms is the 16x, but the number of cores is the same.

weak 32x: The simulation cost increases by about 32x, this is to be expected as the number of atoms is the 32x, but the number of cores is the same.


### b-2: Memory constraints

#### GPU

Max atom count simulatable on my *gpu* [180 * 100 * 100] * 4 = 7.2M (No swapping)

Higher values yield `ERROR on proc 0: Insufficient memory on accelerator (src/GPU/pair_lj_cut_gpu.cpp:110)`

It refused to do 200 * 200 * 100 * 4 = 16M

#### CPU

Max atom count simulatable on my *cpu* [300 * 200 * 200] * 4 = 48_000_000 = 48M (1 timestep ~= 37s)

Above this, eg [300, 210, 200] lammps starts computing (Prints the initial TotEng, Pressure, E_pair, etcc) but fails with NZEC and no error in any log, but the memory usage does not reach 100%, so this doesn't seem to be the issue either.

## Section II: Ovito
 
### a: Solid or Liquid?

To check if the sample has a solid or liquid structure, we can check the coordination's radial distribution of the atoms. If the sample is solid, then the distribution function will appear near discrete.

Results: At the start of the simulation, the sample is solid, as the distribution function has very pronounced spikes due to the shape of FCC.

At the end of the simulation, the sample is liquid, as the distribution function is much smoother, however it still retains some of the spikes.

If this were not the case, then the sample would be considered a gas.

![Radial distribution at start](radial_distrib_start.png){ width=100% }

![Radial distribution at end](radial_distrib_end.png){ width=100% }

### b

We have FCC, if we tell ovito to ignore PBC, then the attoms at the boundry would not be detected as fcc conformant,

An expectable proportion would be arrount 1/6, but for some reason its closer to 1/7 in practice.

![Initial FCC with PBC](fcc initial.png){ width=100% }

![Initial FCC without PBC](fcc no pbc ptm.png){ width=100% }

### c

![Coordination at start](Coordination_start.png){ width=100% }

![Coordination at end](Coordination_end.png){ width=100% }

![Voronoi polyhedra](voronoi_polyhedra.png){ width=100% }

### d

I. 

![Displacement vectors at end](displacement_end.png){ width=100% }

II. Drastic changes to the mean value usually indicate a phase change, this is not the case here.

III. The displacements along xyz are very similar, this is to be expected as we have PBC and the sample is homogeneous.

## Section III

Definitely!
