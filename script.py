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
            sim_params={'use_gpu': gpu, 'use_mpi': True, 'mpi_hw_threads': True,
                        'mpi_n_threads': 32 if not gpu else 1, 'in_toko': False}
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
    with open('out.md', 'w') as f:
        f.write(output_md)


solve_tp1(scaling_tests=True, main_tp_tests=False)
