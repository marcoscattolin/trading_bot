#  Copyright (c) 2024, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import os
import pathlib
import shutil

import click

from src import ROOT_DIR


def initialize_local_default_config() -> pathlib.Path:
    """
    This function should be called once when starting to work on the repo.
    Copies the template file into the base directory.

    Returns: Copy destination
    """

    # gather template path and template filenames
    src_path = os.path.join(ROOT_DIR, "src", "config", "templates")
    src_files = [os.path.join(src_path, f) for f in os.listdir(src_path)]

    # create destination path
    dst_path = os.path.join(ROOT_DIR, "configs")
    os.makedirs(dst_path, exist_ok=True)

    # create destination filenames
    dst_files = [f.replace(".template.", "") for f in os.listdir(src_path)]
    dst_files = [os.path.join(dst_path, f) for f in dst_files]

    # copy
    for src, dst in zip(src_files, dst_files):
        if os.path.isfile(dst):
            raise FileExistsError(dst)
        shutil.copy(src=src, dst=dst)

    return dst_path


@click.group()
def cli():
    """
    Initialize cli
    """


@click.command(name="init")
def init():
    output_path = initialize_local_default_config()
    print(
        "Initialized Config 🥳. You can find a template of the config file in "
        f"`{output_path}` in the project root dir."
    )


cli.add_command(init)
# noinspection PyTypeChecker

if __name__ == "__main__":
    cli()
