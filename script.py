import numpy as np
import pandas as pd

from mpilammpsrun import MpiLammpsRun


def output_tp_result(title, code_params=None, sim_params=None):
    lammps_run = MpiLammpsRun(title, code_params, sim_params)
    merge = lambda x: "<default>" if len(x) == 0 else "\n".join(x)
    output = f"""
## {title}
### Code params
```
{merge([f'{k}: {v}' for k, v in lammps_run.code_params.items()])}
```
### Simulation params
```
{merge([f'{k}: {v}' for k, v in lammps_run.sim_params.items()])}
```
### Result
TPAS ≈ **{lammps_run.tpas * 1_000_000}** microseconds/atom/step/core

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
    df.plot(title="Scaling test").get_figure().savefig(f"fig.png")
    print("Scaling test results: ", weak, strong)


def output_main_tp_results(run_results):
    computed_thermos = pd.DataFrame()
    output_md = ""
    for i, (md, lammps_run) in run_results.items():
        df2 = lammps_run.thermo_logs.drop(columns=["Temp", "E_pair", "E_mol", "Press"])
        df2.plot(title=f"Simulation {i}").get_figure().savefig(f"plot_{i}.png")
        output_md += md + "\n" + f"![Plot {i}](plot_{i}.png)\n"
        computed_thermos = pd.concat([
            computed_thermos,
            df2.agg(['mean', 'std']).rename(columns={'TotEng': f"TotEng {i}"})
        ], axis=1)
    return computed_thermos, output_md


def do_long_running_test():
    return output_tp_result(
        title=f"long_running",
        code_params={'run_steps': 10000, 'thermo_log_freq': 5000, 'dump_pos_freq': 100, 'init_vel': 1.0},
        sim_params={'use_gpu': True, 'use_mpi': False, 'in_toko': False}
    )


def perform_scaling_tests(gpu):
    scaling_run_results = {}
    for i in [2, 4, 8, 16]:
        scaling_run_results[f'2. strong {i}x'] = output_tp_result(
            title=f"2. strong {i}x",
            code_params={'run_steps': 1000, },
            sim_params={'use_gpu': gpu, 'use_mpi': True, 'mpi_n_threads': i, 'in_toko': False}
        )
    scaling_run_results[f'2. strong 32x - hw'] = output_tp_result(
        title=f"2. strong 32x - hw",
        code_params={'run_steps': 1000, },
        sim_params={'use_gpu': gpu, 'use_mpi': True, 'mpi_hw_threads': True, 'mpi_n_threads': 32, 'in_toko': False}
    )
    for i, (a, b, c) in enumerate([(2, 1, 1), (2, 2, 1), (2, 2, 2), (2, 4, 2), (4, 4, 2)]):
        scaling_run_results[f'2. weak {a * b * c}x'] = output_tp_result(
            title=f"2. weak {a * b * c}x",
            code_params={'run_steps': 1000, 'box': (20 * a, 20 * b, 20 * c)},
            sim_params={'use_gpu': gpu, 'use_mpi': True, 'mpi_n_threads': 16 if not gpu else 1, 'in_toko': False}
        )
    return scaling_run_results


def calculate_main_tp(gpu):
    return {
        'a': output_tp_result(
            title="a - Base run",
            code_params={'run_steps': 1000},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        ),
        'b': output_tp_result(
            title="b - 10x steps",
            code_params={'run_steps': 10000},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        ),
        'c': output_tp_result(
            title="c - 8x Box",
            code_params={'run_steps': 1000, 'box': (40, 40, 40)},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        ),
        'c2': output_tp_result(
            title="c - 8x Box (Elongated)",
            code_params={'run_steps': 1000, 'box': (20, 20, 8 * 20)},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        ),
        'd': output_tp_result(
            title="d - 2x Neigh skin",
            code_params={'run_steps': 1000, 'neigh_skin': 0.6},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        ),
        'f': output_tp_result(
            title="f - With dumps",
            code_params={'run_steps': 1000, 'do_image_dump': True, 'do_video_dump': True},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        ),
        'g': output_tp_result(
            title="g - balanced",
            code_params={'run_steps': 1000, 'balance': '1.2 shift xz 5 1.1'},
            sim_params={'use_gpu': gpu, 'use_mpi': False, 'in_toko': False}
        )
    }


def solve_tp1(use_gpu=False, scaling_tests=True, main_tp_tests=True, long_running_test=True):
    run_results = {}
    output_md = ""
    if main_tp_tests:
        run_results = calculate_main_tp(use_gpu)
        computed_thermos, output_md = output_main_tp_results(run_results)
        output_md += "## e - Overall system energy\n" + computed_thermos.to_markdown()
    if scaling_tests:
        scaling_run_results = perform_scaling_tests(use_gpu)
        output_scaling_test_results(scaling_run_results)
    if long_running_test: run_results['long_running'] = do_long_running_test()
    output_md += """

```
Run results:
a: Base run
b: The simulation cost increases by about 10x, because the number of steps increases by 10x, and we are running on the same number of cores.
c: The simulation cost increases by about 8x, because the box size increases by 8x, and we are running on the same number of cores.
c2: The simulation cost increases by about 8x, because the box size increases by 8x, and we are running on the same number of cores. (There seems to be no performance overhead when running on a single machine)
d: I would expect the simulation cost to increase by about 2x, because the number of steps is the same, but the number of neighbors to check is 2x.
e: They are very similar, this is to be expected as the number of steps is the same, and the number of atoms is the same.
f: The simulation cost increases slightly (~3s), this might be influenced by the fact that my SSD is very fast.
g: The simulation cost decreases by about 10%, this is to be expected as the load is balanced between the cores.
2. strong 2x: The simulation cost decreases by about 2x, this is to be expected as the number of atoms is the same, but the number of cores is 2x.
2. strong 4x: The simulation cost decreases by about 4x, this is to be expected as the number of atoms is the same, but the number of cores is 4x.
2. strong 8x: The simulation cost decreases by slightly less than 8x
2. strong 16x: The simulation cost decreases by slightly less than 16x
2. strong 32x - hw: The simulation cost increases by about 3x with respect to 2. strong 16x, this is to be expected as the number of steps is the same, but the number of cores is 32x, and my machine only has 16 physical cores.
>All the weak scaling tests are run on 16 cores<
2. weak 2x: The simulation cost increases by about 2x, this is to be expected as the number of atoms is the 2x, but the number of cores is the same.
2. weak 4x: The simulation cost increases by about 4x, this is to be expected as the number of atoms is the 4x, but the number of cores is the same.
2. weak 8x: The simulation cost increases by about 8x, this is to be expected as the number of atoms is the 8x, but the number of cores is the same.
2. weak 16x: The simulation cost increases by about 16x, this is to be expected as the number of atoms is the 16x, but the number of cores is the same.
2. weak 32x: The simulation cost increases by about 32x, this is to be expected as the number of atoms is the 32x, but the number of cores is the same.
Max atom count simulatable on my pc 200 * 100 * 100 * 4 = 8M
It refused to do 200 * 200 * 100 * 4 = 16M
3.a) To check if the sample has a solid or liquid structure, we can check the coordination number of the atoms. If the coordination number is mostly 12, then the sample is solid, otherwise, then the sample is liquid.
Results: Coordination at the start is 12, but at the end it is much more spread out arrout 14
3.b) We have FCC, if we tell ovito to ignore PBC, then the attoms at the boundry would not be detected as fcc conformant,
An expectable proportion would be arrount 1/6, but for some reason its closer to 1/7 in practice.
```
![](fcc initial.png)
![](fcc no pbc ptm.png)
`3.c)`
![Coordination at start](Coordination_start.png) ![Coordination at end](Coordination_end.png) ![Voronoi polyhedra](voronoi_polyhedra.png)
`3.d)`
![Displacement vectors at end](displacement_end.png)
```
II. Drastic changes to the mean value usually indicate a phase change, this is not the case here.
III. The displacements along xyz are very similar, this is to be expected as we have PBC and the sample is homogeneous.
```

"""

    with open('out.md', 'w') as f:
        f.write(output_md)


def mem_stress_test():
    print(output_tp_result(
        title="maxmem",
        code_params={'run_steps': 1000, 'box': (10,10,10)},
        sim_params={'use_gpu': True, 'use_mpi': False, 'in_toko': False}
    )[1].output)

solve_tp1(scaling_tests=True, main_tp_tests=True)
