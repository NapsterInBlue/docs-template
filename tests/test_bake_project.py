'''
These unit tests are based off of the tests found here
https://github.com/audreyr/cookiecutter-pypackage/blob/master/tests/test_bake_project.py

Breaks if there isn't a {{}} directory that references
the Cookiecutter namespace
'''

from contextlib import contextmanager
import os
import sys
import unittest
import shlex
import subprocess
import datetime

from cookiecutter.utils import rmtree

if sys.version_info > (3, 0):
    import importlib
else:
    import imp


### Utility functions used to run tests

@contextmanager
def inside_dir(dirpath):
    '''
    Execute code from inside the given directory

    Parameters
    ----------
    dirpath: str
        Path of the directory the command is being run
    '''
    oldPath = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(oldPath)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    '''
    Delete temporary directory that is created when executing tests

    Parameters
    ----------
    cookies: pytest_cookies.Cookies
        Cookie to be baked and its temporal files will be removed
    '''
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def project_info(result):
    '''
    Get toplevel dir, project_slug, and project dir from baked cookies
    '''
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status

    Parameters
    ----------
    command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


### Our unit tests

def test_bake_with_defaults(cookies):
    '''
    Ensure that building with cookiecutter returns the appropriate
    files we want to template and doesn't fail
    '''
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]

        assert '.circleci' in found_toplevel_files
        assert '.github' in found_toplevel_files
        assert '.gitignore' in found_toplevel_files
        assert 'Makefile' in found_toplevel_files
        assert 'README.rst' in found_toplevel_files

def test_year_compute_in_conf(cookies):
    with bake_in_temp_dir(cookies) as result:
        projectPath = str(result.project)
        projectName = os.path.split(projectPath)[-1]
        pathToConf = result.project.join('conf.py')
        now = datetime.datetime.now()
        assert str(now.year) in pathToConf.read()


def test_valid_sphinx_build(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert run_inside_dir('make html', str(result.project)) == 0
