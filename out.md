<style media="screen,print"> .pb_after { page-break-after: always !important; } </style>

Complex systems / Molecular Dynamics

Federico Williamson / 13938

## Section I

### Part 1: Run results:
<div class="pb_after"></div>

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
TPAS ~= **0.377946875** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 9.8565         |      9.8565    | 9.8565         | 0.0       |     81.5  |
|  1 | Neigh      | 2.05           |      2.05      | 2.05           | 0.0       |     16.95 |
|  2 | Comm       | 0.041086       |      0.041086  | 0.041086       | 0.0       |      0.34 |
|  3 | Output     | 0.0001057      |      0.0001057 | 0.0001057      | 0.0       |      0    |
|  4 | Modify     | 0.13222        |      0.13222   | 0.13222        | 0.0       |      1.09 |
|  5 | Other      |                |      0.01433   |                |           |      0.12 |

Loop time: 12.0943

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
TPAS ~= **0.38472812500000003** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 100.18         |     100.18     | 100.18         | 0.0       |     81.37 |
|  1 | Neigh      | 21.026         |      21.026    | 21.026         | 0.0       |     17.08 |
|  2 | Comm       | 0.41014        |       0.41014  | 0.41014        | 0.0       |      0.33 |
|  3 | Output     | 0.012508       |       0.012508 | 0.012508       | 0.0       |      0.01 |
|  4 | Modify     | 1.3445         |       1.3445   | 1.3445         | 0.0       |      1.09 |
|  5 | Other      |                |       0.1441   |                |           |      0.12 |

Loop time: 123.113

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
TPAS ~= **0.3797671875** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 78.395         |    78.395      | 78.395         | 0.0       |     80.64 |
|  1 | Neigh      | 16.221         |    16.221      | 16.221         | 0.0       |     16.69 |
|  2 | Comm       | 0.37107        |     0.37107    | 0.37107        | 0.0       |      0.38 |
|  3 | Output     | 0.00070402     |     0.00070402 | 0.00070402     | 0.0       |      0    |
|  4 | Modify     | 1.8181         |     1.8181     | 1.8181         | 0.0       |      1.87 |
|  5 | Other      |                |     0.4146     |                |           |      0.43 |

Loop time: 97.2204

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
TPAS ~= **0.381780078125** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 78.876         |    78.876      | 78.876         | 0.0       |     80.7  |
|  1 | Neigh      | 16.141         |    16.141      | 16.141         | 0.0       |     16.52 |
|  2 | Comm       | 0.59847        |     0.59847    | 0.59847        | 0.0       |      0.61 |
|  3 | Output     | 0.00071662     |     0.00071662 | 0.00071662     | 0.0       |      0    |
|  4 | Modify     | 1.7053         |     1.7053     | 1.7053         | 0.0       |      1.74 |
|  5 | Other      |                |     0.4141     |                |           |      0.42 |

Loop time: 97.7357

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
TPAS ~= **0.527115625** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 14.401         |    14.401      | 14.401         | 0.0       |     85.38 |
|  1 | Neigh      | 2.2757         |     2.2757     | 2.2757         | 0.0       |     13.49 |
|  2 | Comm       | 0.041579       |     0.041579   | 0.041579       | 0.0       |      0.25 |
|  3 | Output     | 0.00010436     |     0.00010436 | 0.00010436     | 0.0       |      0    |
|  4 | Modify     | 0.13449        |     0.13449    | 0.13449        | 0.0       |      0.8  |
|  5 | Other      |                |     0.01441    |                |           |      0.09 |

Loop time: 16.8677

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
TPAS ~= **0.4909562499999999** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 9.9407         |       9.9407   | 9.9407         | 0.0       |     63.27 |
|  1 | Neigh      | 2.0629         |       2.0629   | 2.0629         | 0.0       |     13.13 |
|  2 | Comm       | 0.042966       |       0.042966 | 0.042966       | 0.0       |      0.27 |
|  3 | Output     | 3.5107         |       3.5107   | 3.5107         | 0.0       |     22.35 |
|  4 | Modify     | 0.13888        |       0.13888  | 0.13888        | 0.0       |      0.88 |
|  5 | Other      |                |       0.01449  |                |           |      0.09 |

Loop time: 15.7106

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
TPAS ~= **0.380215625** microseconds/atom/step/core

|    | Section    |   min time     |     avg time   |   max time     | %varavg   |    %total |
|---:|:-----------|:---------------|---------------:|:---------------|:----------|----------:|
|  0 | Pair       | 9.9159         |     9.9159     | 9.9159         | 0.0       |     81.5  |
|  1 | Neigh      | 2.0599         |     2.0599     | 2.0599         | 0.0       |     16.93 |
|  2 | Comm       | 0.041267       |     0.041267   | 0.041267       | 0.0       |      0.34 |
|  3 | Output     | 0.00010675     |     0.00010675 | 0.00010675     | 0.0       |      0    |
|  4 | Modify     | 0.13531        |     0.13531    | 0.13531        | 0.0       |      1.11 |
|  5 | Other      |                |     0.01434    |                |           |      0.12 |

Loop time: 12.1669

![Plot g](plot_g.png){ width=100% }

<div class="pb_after"></div>

#### e - Overall system energy

|      |    TotEng a |    TotEng b |    TotEng c |   TotEng c2 |    TotEng d |    TotEng f |    TotEng g |
|:-----|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| mean | -5.27716    | -5.27829    | -5.27729    | -5.27725    | -5.27716    | -5.27716    | -5.27716    |
| std  |  0.00530259 |  0.00421841 |  0.00553594 |  0.00547916 |  0.00530259 |  0.00530259 |  0.00530259 |

![Raw scaling results](scale.png){ width=45% } ![Core count normalized results](scale2.png){ width=45% } ![Base run normalized results](scale3.png){ width=45% } ![Core count base run normalized results](scale4.png){ width=45% }

<div class="pb_after"></div>

a: Base run

b: The simulation cost increases by about 10x, because the number of steps increases by 10x, and we are running on the same number of cores.

c: The simulation cost increases by about 8x, because the box size increases by 8x, and we are running on the same number of cores.

c2: The simulation cost increases by about 8x, because the box size increases by 8x, and we are running on the same number of cores. (There seems to be no performance overhead when running on a single machine)

d: I would expect the neighbor cost to _increase_ by about $4/3 \pi (2r)^3 - r^3$ or about $7r^3$, because the number of steps is the same, but the number of neighbors to check scales with the volume of the sphere of the neighbors. However, due to the very low initial cost of the neighbor check, the skin change barely affects the overall performance.

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
