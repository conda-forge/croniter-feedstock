import os
import sys
from glob import glob
from os.path import join

import pytest


TESTS = join(os.getcwd(), "src", "src", "croniter", "tests")
ABS_IMPORT = "from croniter.tests import"
COV_THRESHOLD = "94"
TEST_ARGS = [TESTS, "-vv", "--cov", "croniter", "--cov-fail-under", COV_THRESHOLD]


def patch_absolute_imports():
    for test in glob(join(TESTS, "*.py")):
        with open(test) as fp:
            test_src = fp.read()

        if ABS_IMPORT in test_src:
            with open(test, "w") as fp:
                fp.write(test_src.replace(ABS_IMPORT, "from . import"))
            print("rewrote absolute import in {}".format(test))


def run_tests():
    return pytest.main(TEST_ARGS)



if __name__ == "__main__":
    patch_absolute_imports()
    sys.exit(run_tests())
