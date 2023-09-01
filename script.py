import subprocess, re, numpy as np, pandas as pd
from io import StringIO

def get_code(box=(20,20,20), init_vel=1.0, neigh_skin=0.3, dump_pos_freq=1000, thermo_log_freq=50, run_steps=1000, do_image_dump=False, do_video_dump=False, balance=None):
    image_dump = """
dump		2 all image 25 image.*.jpg type type &
		axes yes 0.8 0.02 view 60 -30
dump_modify	2 pad 3
"""
    video_dump = """
dump		3 all movie 25 movie.mpg type type &
		axes yes 0.8 0.02 view 60 -30
dump_modify	3 pad 3
"""
    return f"""
# 3d Lennard-Jones melt
units		lj
atom_style	atomic # / full
newton off

lattice		fcc 0.8442               # Face center cubic / density
region		box block 0 {box[0]} 0 {box[1]} 0 {box[2]} # repeat box 
create_box	 1 box
create_atoms 1 box # attoms of type 1
mass		 1 1.0 # set mass of atoms of type 1 to 1.0
{'balance ' + balance if balance is not None else ''}

velocity	 all create {init_vel} 87287 loop geom # Assign velocity with energy 3.0 and seed 87...

pair_style	lj/cut 2.5 # LJ params
pair_coeff	1 1 1.0 1.0 2.5

neighbor	 {neigh_skin} bin # Skin [R_j]
neigh_modify every 20 delay 0 check no # checks expected neighbors

fix	         1 all nve # How to update velocity

dump         id all atom {dump_pos_freq} dump.melt.*
{image_dump if do_image_dump else ''}
{video_dump if do_video_dump else ''}
thermo	    {thermo_log_freq} # How often to log temperature
run		    {run_steps} # Run for N steps
"""

def simulate(inputFile="in.melt", useGPU=True, useMPI=False, mpiHWThreads=False, mpiNThreads=1, inTOKO=False):
    gpu = "-sf gpu -pk gpu 1" if useGPU else ""
    mpi = f"mpirun -n {mpiNThreads} {'--use-hwthread-cpus' if mpiHWThreads else ''} " if useMPI else ""
    if not inTOKO:
        try:
            return subprocess.check_output(f'{mpi} ../lmp_cuda {gpu} -in {inputFile}'.strip().replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" "))
        except subprocess.CalledProcessError as e:
            print("Error occurred", e, f"{inputFile=}", f"{useGPU=} {useMPI=} {mpiHWThreads=} {mpiNThreads=} {inTOKO=}")
            raise e
    return print("TODO: TOKO not implemented yet :c")


def gen_and_sim(codeParams=None, simParams=None):
    codeParams = {} if codeParams is None else codeParams
    simParams = {} if simParams is None else simParams
    code = get_code(**codeParams)
    fileToUse = '/tmp/in.melt'
    with open(fileToUse, 'w') as f:
        f.write(code)
    result = simulate(inputFile=fileToUse, **simParams)
    return result.decode('utf-8')

def calculate_tpas(result: str):
    lines = result.split("\n")
    for line in lines:
        if line.startswith("Loop time of "):
            return parse_tpas_line(line)

def parse_tpas_line(line: str):
    pattern = r'Loop time of (\d+\.\d+) on (\d+) procs for (\d+) steps with (\d+) atoms'
    match = re.match(pattern, line)
    
    if match:
        loop_time = float(match.group(1))
        procs = int(match.group(2))
        steps = int(match.group(3))
        atoms = int(match.group(4))
        
        tpas = (loop_time / (procs * steps)) / atoms
        return tpas, loop_time
    else:
        return None

def extract_section(result: str, req: str):
    sections = result.split("\n\n")
    for section in sections:
        if section.startswith(req):
            return section

def parse_timings(result: str):
    timings = extract_section(result, "MPI task timing breakdown:\n")
    lines = timings.split("\n")[1:]
    header = lines[0].replace("|",",")
    csv = header + "\n" + "\n".join(lines[2:]).replace("|",",")
    df = pd.read_csv(StringIO(csv), header=0)
    return df.to_markdown()

def output_tp_result(title, codeParams={}, simParams={}):
    output = ""
    output += "## " + title + "\n"
    output += "### Code params\n```\n"
    for k,v in codeParams.items(): output += f"{k}: {v}\n"
    if len(codeParams.items()) == 0: output += "<Default>\n"
    output += "```\n### Simulation params\n```\n"
    for k,v in simParams.items(): output += f"{k}: {v}\n"
    if len(simParams.items()) == 0: output += "<Default>\n"
    
    output += "```\n### Result\n"
    result = gen_and_sim(codeParams=codeParams, simParams=simParams)
    tpas, loop_time = calculate_tpas(result)
    tpas *= 1_000_000
    thermo = get_thermo_logs(result)
    output += f"TPAS ≈ **{tpas}** microseconds/atom/step\n"
    output += parse_timings(result) + "\n"
    print(f"Finished job '{title}' in {loop_time} seconds")
    return output, result, tpas, thermo, loop_time

def get_thermo_logs(result: str):
    section = extract_section(result, "Generated ")
    if section is None: section = result.split("\n\n")[0]
    for i, line in enumerate(section.split("\n")):
        if line.startswith("Per MPI rank memory allocation"):
            section = "\n".join(section.split("\n")[i+1:-1])
            break
    df = pd.read_fwf(StringIO(section)).drop(columns=['E_mol']).rename(columns={'Unnamed: 3':'E_mol'})
    df.index = df["Step"]
    df = df.drop(columns=["Step"])
    return df

def solve_tp1():
    gpu = False
    run_results = {
        'a': output_tp_result(title="a - Base run",
            codeParams={
                'run_steps':1000,
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        ),
        'b': output_tp_result(title="b - 10x steps",
            codeParams={
                'run_steps':10000,
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        ),
        'c': output_tp_result(title="c - 8x Box",
            codeParams={
                'run_steps':1000,
                'box': (40, 40, 40)
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        ),
        'c2': output_tp_result(title="c - 8x Box (Elongated)",
            codeParams={
                'run_steps':1000,
                'box': (20, 20, 8*20)
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        ),
        'd': output_tp_result(title="d - 2x Neigh skin",
            codeParams={
                'run_steps':1000,
                'neigh_skin': 0.6
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        ),
        'f': output_tp_result(title="f - With dumps",
            codeParams={
                'run_steps':1000,
                'do_image_dump': True,
                'do_video_dump': True
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        ),
        'g': output_tp_result(title="g - balanced",
            codeParams={
                'run_steps':1000,
                'balance':'1.2 shift xz 5 1.1'
            }, simParams={
                'useGPU':gpu,
                'useMPI':False,
                'inTOKO':False
            }
        )
    }
    for i in [2, 4, 8, 16]:
        run_results[f'2. strong {i}x']= output_tp_result(title=f"2. strong {i}x",
                codeParams={
                    'run_steps':1000,
                }, simParams={
                    'useGPU':gpu,
                    'useMPI':True,
                    'mpiNThreads':i,
                    'inTOKO':False
                }
            )
    run_results[f'2. strong 32x[hw]']= output_tp_result(title=f"2. strong 32x[hw]",
                codeParams={
                    'run_steps':1000,
                }, simParams={
                    'useGPU':gpu,
                    'useMPI':True,
                    'mpiHWThreads':True,
                    'mpiNThreads':32,
                    'inTOKO':False
                }
            )
    for i,(a,b,c) in enumerate([(2,1,1), (2,2,1), (2,2,2), (2,4,2)]):
        run_results[f'2. weak {a*b*c}x']= output_tp_result(title=f"2. weak {a*b*c}x",
                codeParams={
                    'run_steps':1000,
                    'box':(20*a,20*b,20*c)
                }, simParams={
                    'useGPU':gpu,
                    'useMPI':True,
                    'mpiHWThreads':True,
                    'mpiNThreads':32 if not gpu else 1,
                    'inTOKO':False
                }
            )
    run_results['long_running'] = output_tp_result(title=f"long_running",
        codeParams={
            'run_steps':10000,
            'thermo_log_freq': 5000,
            'dump_pos_freq': 100,
            'init_vel': 1.0
        }, simParams={
            'useGPU':True,
            'useMPI':False,
            'inTOKO':False
        }
    )
    computed_thermos = pd.DataFrame()
    output_md = ""
    for i, (md, output, tpas, thermos, runtime) in run_results.items():
        df2 = thermos.drop(columns=["Temp", "E_pair", "E_mol", "Press"])
        df2.plot(title=f"Simulation {i}").get_figure().savefig(f"plot_{i}.png")
        output_md += md + "\n" + f"![Plot {i}](plot_{i}.png)\n"
        computed_thermos = pd.concat([computed_thermos, df2.agg(['mean','std']).rename(columns={'TotEng':f"TotEng {i}"})], axis=1)
    output_md += "## e - Overall system energy\n" + computed_thermos.to_markdown()
    with open('out.md', 'w') as f:
        f.write(output_md)
solve_tp1()


