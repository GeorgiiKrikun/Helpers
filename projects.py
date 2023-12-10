#!/usr/bin/env python3

import argparse
import os
from typing import List, Optional
import json
import sys

PROJECTS_FILE = os.path.join(os.path.expanduser("~"), "krikun_projects.json")
HELPERS_DIR = os.path.dirname(os.path.realpath(__file__))
BASHRC_INIT_FILE = os.path.join(os.path.expanduser("~"), "krikun-bash-init")
BASHRC_FILE = os.path.join(os.path.expanduser("~"), ".bashrc")

def directory_path(path_str):
    if os.path.isdir(path_str):
        return path_str
    else:
        raise NotADirectoryError(path_str)

def get_init_file_line(name:str, path:str, var:str) -> str:
    return f"export {var}={path}"
    
def get_bashrc_line() -> str:
    return f"source {BASHRC_INIT_FILE}"

def commit_bashrc():
    lines = []
    with open(BASHRC_FILE, 'r') as f:
        lines = f.readlines()
    
    add_line = get_bashrc_line()
    if add_line not in lines:
        lines.append(add_line)
    
    with open(BASHRC_FILE, 'w') as f:
        f.write("".join(lines))

def get_projects_dict() -> dict:
    lib = {}
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            lib = json.load(f)
    return lib

def commit_init_file():
    lib = get_projects_dict()
    lines = []
    PATH_var = "$PATH"
    for name, project in lib.items():
        line = get_init_file_line(name, project['path'], project['var'])
        lines.append(line)
        PATH_var += ":$"+project['var']

    with open(BASHRC_INIT_FILE, 'w') as f:
        f.write("\n".join(lines))
        f.write("\n")
        f.write(f"export PATH={PATH_var}")

def add_project(name: str, path: str, var: Optional[str]):
    lib = get_projects_dict()

    if lib.get(name):
        print(f"Project with name {name} already exists")
        sys.exit(1)
    
    if var is None:
        var = name.upper()+"_PROJECT_PATH"
    
    lib[name] = {"path": path, "var": var}
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(lib, f, indent=4)

    commit_init_file()

    print(f"Added project {name} with path {path} and variable {var}")

def delete_project(name: str):
    lib = get_projects_dict()

    if lib.get(name):
        del lib[name]
        with open(PROJECTS_FILE, 'w') as f:
            json.dump(lib, f, indent=4)
    else:
        print(f"Project with name {name} does not exist")
        sys.exit(1) 

    commit_init_file()

def list_projects():
    lib = get_projects_dict()

    if len(lib) == 0:
        print("No projects exist")
        return

    for name, project in lib.items():
        print(f"{name}: path: {project['path']} var: {project['var']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Add parser
    add_parser = subparsers.add_parser('add', help='Add project')
    add_parser.add_argument('-n','--name', help="No spaces allowed", type=str, required=True)
    add_parser.add_argument('-p','--path', type=directory_path, required=True)
    add_parser.add_argument('-v','--var', type=str, required=False)

    # Delete parser
    delete_parser = subparsers.add_parser('delete', help='Delete project')
    delete_parser.add_argument('-n', '--name', help="No spaces allowed", type=str)

    # List parser
    list_parser = subparsers.add_parser('list', help='List projects')

    change_bashrc_parser = subparsers.add_parser('init', help='Change bashrc file with current config')


    args = parser.parse_args()
    if args.command == 'add':
        add_project(args.name, args.path, args.var)
    elif args.command == 'delete':
        delete_project(args.name)
    elif args.command == 'list':
        list_projects()
    elif args.command == 'init':
        commit_bashrc()
    else:
        print("Invalid command")
        sys.exit(1)
        
    # project_var = 

