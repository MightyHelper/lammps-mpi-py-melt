import subprocess


class MpiLammpsWrapper:
    @staticmethod
    def _get_code(box=(20, 20, 20), init_vel=1.0, neigh_skin=0.3, dump_pos_freq=10000, thermo_log_freq=5000,
                  run_steps=1000,
                  do_image_dump=False, do_video_dump=False, balance=None, timestep=0.0001, newton="on"):
        image_dump = """
dump             2 all image 25 image.*.jpg type type &
                 axes yes 0.8 0.02 view 60 -30
dump_modify      2 pad 3
"""
        video_dump = """
dump             3 all movie 25 movie.mpg type type &
                 axes yes 0.8 0.02 view 60 -30
dump_modify      3 pad 3
"""
        return f"""
                                                                        # 3d Lennard-Jones melt
units            lj
atom_style       atomic                                                 # / full
newton           {newton}

timestep         {timestep}
lattice          fcc 0.8442                                             # Face center cubic / density
region           box block 0 {box[0]} 0 {box[1]} 0 {box[2]}             # repeat box 
create_box       1 box
create_atoms     1 box                                                  # atoms of type 1
mass             1 1.0                                                  # set mass of atoms of type 1 to 1.0
                 {'balance ' + balance if balance is not None else ''}

velocity         all create {init_vel} 87287 loop geom                  # Assign velocity with energy 3.0 and seed 87...

pair_style       lj/cut 2.5                                             # LJ params
pair_coeff       1 1 1.0 1.0 2.5

neighbor         {neigh_skin} bin                                       # Skin [R_j]
neigh_modify     every 20 delay 0 check no                              # checks expected neighbors

fix              1 all nve                                              # How to update velocity

dump             id all atom {dump_pos_freq} dump.melt.*
{image_dump if do_image_dump else ''}
{video_dump if do_video_dump else ''}
thermo           {thermo_log_freq}                                      # How often to log temperature
run              {run_steps}                                            # Run for N steps
    """

    @staticmethod
    def _simulate(input_file="in.melt", use_gpu=False, use_mpi=False, mpi_hw_threads=False, mpi_n_threads=1,
                  in_toko=False, cwd='./lammps_output', lammps_executable='../../lmp_cuda'):
        gpu = "-sf gpu -pk gpu 1" if use_gpu else ""
        mpi = f"mpirun -n {mpi_n_threads} {'--use-hwthread-cpus' if mpi_hw_threads else ''} " if use_mpi else ""
        if not in_toko:
            try:
                return subprocess.check_output(
                    f'{mpi} {lammps_executable} {gpu} -in {input_file}'
                    .strip()
                    .replace("  ", " ")
                    .replace("  ", " ")
                    .replace("  ", " ")
                    .split(" "),
                    cwd=cwd
                )
            except subprocess.CalledProcessError as e:
                print("Error occurred", e, f"{input_file=}",
                      f"{use_gpu=} {use_mpi=} {mpi_hw_threads=} {mpi_n_threads=} {in_toko=}")
                raise e
        return print("TODO: TOKO not implemented yet :c")

    @staticmethod
    def gen_and_sim(code_params=None, sim_params=None):
        code_params = {} if code_params is None else code_params
        sim_params = {} if sim_params is None else sim_params
        code = MpiLammpsWrapper._get_code(**code_params)
        file_to_use = '/tmp/in.melt'
        with open(file_to_use, 'w') as f:
            f.write(code)
        result = MpiLammpsWrapper._simulate(input_file=file_to_use, **sim_params)
        return result.decode('utf-8')
