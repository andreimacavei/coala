from subprocess import call as _call
import os
import shutil


def call(command, assert_success=True):
    retval = _call(command, shell=True)
    if assert_success:
        assert retval == 0, ("The command '{cmd}' didn't succeed as "
                             "specified.".format(cmd=command))

    return retval


if __name__ == '__main__':
    # Set up test env
    test_dir = os.path.abspath("tutorial_test")
    shutil.rmtree(test_dir, ignore_errors=True)

    # Begin test
    call("git clone https://github.com/coala-analyzer/coala-tutorial.git "
         + test_dir)
    os.chdir(test_dir)
    call("coala-ci --files=src/*.c --bears=SpaceConsistencyBear --save -S "
         "use_spaces=True", assert_success=False)
    with open(os.path.join(test_dir, ".coafile")) as file:
        lines = file.readlines()
        assert lines == ['[Default]\n',
                         'bears = SpaceConsistencyBear\n',
                         'files = src/*.c\n',
                         'use_spaces = True\n']

    # Remove all files again
    os.chdir(os.path.join(test_dir, os.pardir))
    shutil.rmtree(test_dir, ignore_errors=True)
