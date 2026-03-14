from subprocess import call
import sys
from typing import Any
from pathlib import Path

COV_FAIL_UNDER = 92

TESTS = Path.cwd() / "src/croniter/tests"
ABS_IMPORT = "from croniter.tests import"
REL_IMPORT = "from . import"
COV_TEST = [
    "coverage",
    "run",
    "-m",
    "--source=croniter",
    "--branch",
    "pytest",
    "-vv",
    "--tb=long",
    "--color=yes",
]
COV_REPORT = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_FAIL_UNDER}",
]


def patch_absolute_imports() -> int:
    ok = patched = 0
    tests = sorted(TESTS.glob("*.py"))
    for test in tests:
        with open(test) as fp:
            test_src = fp.read()

        if ABS_IMPORT in test_src:
            with open(test, "w") as fp:
                fp.write(test_src.replace(ABS_IMPORT, REL_IMPORT))
            print("\n\t- rewrote absolute import in {}".format(test))
            patched += 1
        else:
            print(".", end="")
            ok += 1
    print(f"{patched} patched, {ok} ok", flush=True)
    return 0 if patched else ok


def do(args: list[Any]) -> int:
    args = [*map(str, args)]
    print(">>>", *args)
    return call(args)


if __name__ == "__main__":
    sys.exit(patch_absolute_imports() or do(COV_TEST) or do(COV_REPORT))
