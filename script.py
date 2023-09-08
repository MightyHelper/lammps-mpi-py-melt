import numpy as np
import pandas as pd

from mpilammpsrun import MpiLammpsRun


def output_tp_result(title, code_params=None, sim_params=None):
    lammps_run = MpiLammpsRun(title, code_params, sim_params)
    merge = lambda x: "<default>" if len(x) == 0 else "\n".join(x)
    output = f"""
#### {title}
##### Code params
```
{merge([f'{k}: {v}' for k, v in lammps_run.code_params.items()])}
```
##### Simulation params
```
{merge([f'{k}: {v}' for k, v in lammps_run.sim_params.items()])}
```
##### Result
TPAS ~= **{lammps_run.tpas * 1_000_000}** microseconds/atom/step/core

{lammps_run.timings.to_markdown()}

Loop time: {lammps_run.loop_time}
"""
    print(f"Finished job '{title}' in {lammps_run.loop_time} seconds")
    return output, lammps_run


def output_scaling_test_results(scaling_run_results):
    weak = []
    strong = []
    for i, (md, lammps_run) in scaling_run_results.items():
        if 'strong' in i:
            strong.append(lammps_run.loop_time)
        if 'weak' in i:
            weak.append(lammps_run.loop_time)
    df = pd.DataFrame(data=np.array([weak, strong]).transpose(), columns=['weak', 'strong'], index=[2, 4, 8, 16, 32])
    df.plot(title="Raw scaling test results").get_figure().savefig(f"scale.png")
    df['strong_norm_core'] = df['strong'] * df.index
    df['weak_norm_core'] = df['weak'] / df.index
    df['strong_norm'] = df['strong'] / df['strong'][2]  # TODO: Consider using iloc
    df['weak_norm'] = df['weak'] / df['weak'][2]
    core_norm_df = df.drop(columns=['strong_norm', 'weak_norm', 'strong', 'weak'])
    initial_norm_df = df.drop(columns=['strong_norm_core', 'weak_norm_core', 'strong', 'weak'])
    core_norm_df.plot(title="Core count normalized scaling results").get_figure().savefig(f"scale2.png")
    core_initial_norm_df = core_norm_df / core_norm_df.iloc[0]
    initial_norm_df.plot(title="Base run normalized scaling results").get_figure().savefig(f"scale3.png")
    core_initial_norm_df.plot(title="Core count base run normalized scaling results").get_figure().savefig(
        f"scale4.png")
    print("Scaling test results: ", strong, weak)
    return ("\n" +
            f"![Raw scaling results](scale.png){{ width=45% }} " +
            f"![Core count normalized results](scale2.png){{ width=45% }} " +
            f"![Base run normalized results](scale3.png){{ width=45% }} " +
            f"![Core count base run normalized results](scale4.png){{ width=45% }}\n\n"
            )


def output_main_tp_results(run_results):
    computed_thermos = pd.DataFrame()
    output_md = ""
    for i, (md, lammps_run) in run_results.items():
        df2 = lammps_run.thermo_logs.drop(columns=["Temp", "E_pair", "E_mol", "Press"])
        df2.plot(title=f"Simulation {i}").get_figure().savefig(f"plot_{i}.png")
        output_md += md + "\n" + f"![Plot {i}](plot_{i}.png){{ width=100% }}\n"
        computed_thermos = pd.concat([
            computed_thermos,
            df2.agg(['mean', 'std']).rename(columns={'TotEng': f"TotEng {i}"})
        ], axis=1)
        output_md += f"\n{page_break()}\n"
    return computed_thermos, output_md


def do_long_running_test():
    return output_tp_result(
        title=f"long_running",
        code_params={'run_steps': 10000, 'thermo_log_freq': 5000, 'dump_pos_freq': 100, 'init_vel': 1.0},
        sim_params={'use_gpu': True, 'use_mpi': False}
    )


def perform_scaling_tests(gpu):
    scaling_run_results = {}
    gpu_cfg = {'use_gpu': gpu} if gpu else {}
    for i in [2, 4, 8, 16]:
        scaling_run_results[f'2. strong {i}x'] = output_tp_result(
            title=f"2. strong {i}x",
            code_params={'run_steps': 1000, },
            sim_params={**gpu_cfg, 'use_mpi': True, 'mpi_n_threads': i}
        )
    scaling_run_results[f'2. strong 32x - hw'] = output_tp_result(
        title=f"2. strong 32x - hw",
        code_params={'run_steps': 1000, },
        sim_params={**gpu_cfg, 'use_mpi': True, 'mpi_hw_threads': True, 'mpi_n_threads': 32}
    )
    for i, (a, b, c) in enumerate([(2, 1, 1), (2, 2, 1), (2, 2, 2), (2, 4, 2), (4, 4, 2)]):
        scaling_run_results[f'2. weak {a * b * c}x'] = output_tp_result(
            title=f"2. weak {a * b * c}x",
            code_params={'run_steps': 1000, 'box': (20 * a, 20 * b, 20 * c)},
            sim_params={**gpu_cfg, 'use_mpi': True, 'mpi_n_threads': 16 if not gpu else 1}
        )
    return scaling_run_results


def calculate_main_tp(gpu):
    gpu_cfg = {'use_gpu': gpu} if gpu else {}
    return {
        'a': output_tp_result(
            title="a - Base run",
            code_params={'run_steps': 1000},
            sim_params={**gpu_cfg, 'use_mpi': False}
        ),
        'b': output_tp_result(
            title="b - 10x steps",
            code_params={'run_steps': 10000},
            sim_params={**gpu_cfg, 'use_mpi': False}
        ),
        'c': output_tp_result(
            title="c - 8x Box",
            code_params={'run_steps': 1000, 'box': (40, 40, 40)},
            sim_params={**gpu_cfg, 'use_mpi': False}
        ),
        'c2': output_tp_result(
            title="c - 8x Box (Elongated)",
            code_params={'run_steps': 1000, 'box': (20, 20, 8 * 20)},
            sim_params={**gpu_cfg, 'use_mpi': False}
        ),
        'd': output_tp_result(
            title="d - 2x Neigh skin",
            code_params={'run_steps': 1000, 'neigh_skin': 0.6},
            sim_params={**gpu_cfg, 'use_mpi': False}
        ),
        'f': output_tp_result(
            title="f - With dumps",
            code_params={'run_steps': 1000, 'do_image_dump': True, 'do_video_dump': True},
            sim_params={**gpu_cfg, 'use_mpi': False}
        ),
        'g': output_tp_result(
            title="g - balanced",
            code_params={'run_steps': 1000, 'balance': '1.2 shift xz 5 1.1'},
            sim_params={**gpu_cfg, 'use_mpi': False}
        )
    }


def page_break():
    return '<div class="pb_after"></div>'


def solve_tp1(use_gpu=False, scaling_tests=True, main_tp_tests=True, long_running_test=True):
    run_results = {}
    output_md = '<style media="screen,print"> .pb_after { page-break-after: always !important; } </style>'  # Add page break support
    output_md += f"""

Complex systems / Molecular Dynamics

Federico Williamson / 13938

## Section I

### Part 1: Run results:

"""
    if main_tp_tests:
        run_results = calculate_main_tp(use_gpu)
        computed_thermos, md = output_main_tp_results(run_results)
        output_md += md
        output_md += f"\n#### e - Overall system energy\n\n{computed_thermos.to_markdown()}\n\n{page_break()}\n\n"
    if scaling_tests:
        scaling_run_results = perform_scaling_tests(use_gpu)
        output_md += output_scaling_test_results(scaling_run_results)
    if long_running_test: run_results['long_running'] = do_long_running_test()
    output_md += f"""

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

![Radial distribution at start](radial_distrib_start.png){{ width=100% }}

![Radial distribution at end](radial_distrib_end.png){{ width=100% }}

### b

We have FCC, if we tell ovito to ignore PBC, then the attoms at the boundry would not be detected as fcc conformant,

An expectable proportion would be arrount 1/6, but for some reason its closer to 1/7 in practice.

![Initial FCC with PBC](fcc initial.png){{ width=100% }}

![Initial FCC without PBC](fcc no pbc ptm.png){{ width=100% }}

### c

![Coordination at start](Coordination_start.png){{ width=100% }}

![Coordination at end](Coordination_end.png){{ width=100% }}

![Voronoi polyhedra](voronoi_polyhedra.png){{ width=100% }}

### d

I. 

![Displacement vectors at end](displacement_end.png){{ width=100% }}

II. Drastic changes to the mean value usually indicate a phase change, this is not the case here.

III. The displacements along xyz are very similar, this is to be expected as we have PBC and the sample is homogeneous.

## Section III

Definitely!

"""

    with open('out.md', 'w') as f:
        f.write(output_md)


def mem_stress_test():
    # Max atom count simulatable on my pc 200 * 100 * 100 * 4 = 8M
    print(output_tp_result(
        title="maxmem",
        code_params={'run_steps': 1, 'box': (300, 210, 200)},
        sim_params={'use_gpu': False, 'use_mpi': True, 'mpi_n_threads': 16}
    )[1].output)


solve_tp1(scaling_tests=True, main_tp_tests=True)
# mem_stress_test()
# pandoc out.md -f markdown-implicit_figures -o out.pdf
# pandoc out.md -f markdown-implicit_figures --from=markdown -t html+raw_tex --metadata title="TP 1" --pdf-engine-opt='--enable-local-file-access' -o out.pdf
