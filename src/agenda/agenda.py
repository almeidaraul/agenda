import argparse
import json
import subprocess
from datetime import datetime
from itertools import starmap
from typing import Dict, List, TextIO


def get_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(prog="simple_schedule",
                                     description="Simple experiment scheduler")

    parser.add_argument("--json", type=str, required=True,
                        help="JSON config filename")
    parser.add_argument("--output", type=str, required=True,
                        help="Output filename")

    return parser.parse_args()


def check_required_keys(d: dict, required_keys: List[str]) -> None:
    """Check that given dict includes required keys"""
    missing_keys = filter(lambda key: key not in d.keys(), required_keys)
    for key in missing_keys:
        raise KeyError(f"Key missing in dictionary: {key}")


def build_cmd_str(cmd_prefix: str, args_dict: Dict[str, any]) -> str:
    """Build bash nohup command for an experiment

    Keyword arguments:
    cmd_prefix -- base command to be executed
    args_dict -- dictionary in the format "arg:value" for command-line args
                 to be used in the command
    """
    for (env_variable, value) in args_dict.pop("env_variables", []):
        cmd_prefix = f"{env_variable}={value} {cmd_prefix}"
    args_strings = starmap(lambda a, v: f"--{a} {v}", args_dict.items())
    cmd_as_list = [cmd_prefix, " ".join(args_strings)]
    return " ".join(cmd_as_list)


def log_line(output: TextIO, *args: str) -> None:
    """Append line to output file"""
    time = datetime.now().strftime("%d/%m/%y %H:%M: ")
    output.write(time + " ".join(args) + "\n")


if __name__ == "__main__":
    opt = get_args()
    schedule = json.load(open(opt.json, 'r'))
    required_keys = schedule.get("required_keys", [])
    output_file = open(opt.output, 'w')

    required_keys = ["cmd_prefix", "cmds"]
    check_required_keys(schedule, required_keys)

    if "log_header" in schedule:
        log_line("\n\n# ", schedule["log_header"], "\n")

    for cmd in schedule["cmds"]:
        check_required_keys(cmd, required_keys)
        cmd_str = build_cmd_str("cmd_prefix", cmd)
        log_line(output_file, "+run", cmd_str)
        subprocess.run(cmd_str, shell=True, check=True)
        log_line(output_file, "%completed\n")
