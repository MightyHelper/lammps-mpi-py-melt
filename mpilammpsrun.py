import re
from io import StringIO

import pandas as pd

from sims.mpilammpswrapper import MpiLammpsWrapper


class MpiLammpsRun:
    def __init__(self, title: str, code_params: dict, sim_params: dict):
        self.title = title
        self.code_params = code_params
        self.sim_params = sim_params
        self.output = MpiLammpsWrapper.gen_and_sim(code_params, sim_params)
        self.tpas, self.loop_time = self.calculate_tpas()
        self.timings = self.parse_timings()
        self.thermo_logs = self.get_thermo_logs()


    def calculate_tpas(self):
        lines = self.output.split("\n")
        pattern = r'Loop time of (\d+\.\d+) on (\d+) procs for (\d+) steps with (\d+) atoms'
        for line in lines:
            if line.startswith("Loop time of "):
                if match := re.match(pattern, line):
                    loop_time = float(match.group(1))
                    procs = int(match.group(2))
                    steps = int(match.group(3))
                    atoms = int(match.group(4))
                    tpas = (procs * loop_time) / (steps * atoms)
                    return tpas, loop_time
        return None, None

    def extract_section(self, req: str):
        sections = self.output.split("\n\n")
        for section in sections:
            if section.startswith(req):
                return section

    def parse_timings(self) -> pd.DataFrame: # TODO: No longer returns .to_markdown()
        timings = self.extract_section("MPI task timing breakdown:\n")
        lines = timings.split("\n")[1:]
        header = lines[0].replace("|", ",")
        csv = header + "\n" + "\n".join(lines[2:]).replace("|", ",")
        df = pd.read_csv(StringIO(csv), header=0)
        return df

    def get_thermo_logs(self):
        section = self.extract_section("Generated ")
        if section is None: section = self.output.split("\n\n")[0]
        for i, line in enumerate(section.split("\n")):
            if line.startswith("Per MPI rank memory allocation"):
                section = "\n".join(section.split("\n")[i + 1:-1])
                break
        df = pd.read_fwf(StringIO(section)).drop(columns=['E_mol']).rename(columns={'Unnamed: 3': 'E_mol'})
        df.index = df["Step"]
        df = df.drop(columns=["Step"])
        return df
