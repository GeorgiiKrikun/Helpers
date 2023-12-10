#!/usr/bin/env python3

import argparse
import os
from typing import Optional
import environ
import json
import sys
projects_file = os.path.join(os.path.expanduser("~"), "krikun_projects.json")


def directory_path(path_str):
    if os.path.isdir(path_str):
        return path_str
    else:
        raise NotADirectoryError(path_str)

def add_project(name: str, path: str, var: Optional[str]):
    lib = {}
    if os.path.exists(projects_file):
        with open(projects_file, 'r') as f:
            lib = json.load(f)

    if lib.get(name):
        print(f"Project with name {name} already exists")
        sys.exit(1)
    
    if var is None:
        var = name.upper()+"_PROJECT_PATH"
    
    lib[name] = {"path": path, "var": var}
    with open(projects_file, 'w') as f:
        json.dump(lib, f, indent=4)

def delete_project(name: str):
    lib = {}
    if os.path.exists(projects_file):
        with open(projects_file, 'r') as f:
            lib = json.load(f)

    if lib.get(name):
        del lib[name]
        with open(projects_file, 'w') as f:
            json.dump(lib, f, indent=4)
    else:
        print(f"Project with name {name} does not exist")
        sys.exit(1) 


def list_projects():
    lib = {}
    if os.path.exists(projects_file):
        with open(projects_file, 'r') as f:
            lib = json.load(f)

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

    args = parser.parse_args()
    if args.command == 'add':
        add_project(args.name, args.path, args.var)
    elif args.command == 'delete':
        delete_project(args.name)
    elif args.command == 'list':
        list_projects()
    else:
        print("Invalid command")
        sys.exit(1)
        
    # project_var = 

