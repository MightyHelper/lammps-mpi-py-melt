<style media="screen,print"> .pb_after { page-break-after: always !important; } </style>

Complex systems / Molecular Dynamics

Federico Williamson / 13938

## Section I

### Part 1: Run results:

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

