"""Verify the published Uvicorn constructor boundary without running application code."""

from importlib.metadata import version
from inspect import signature

from uvicorn.supervisors import Multiprocess


def run_server(sockets):
    pass


def verify_binding() -> None:
    expected = {"0.40.0": (True, False), "0.51.0": (False, True)}
    release = version("uvicorn")
    if release not in expected:
        raise SystemExit("Use Uvicorn 0.40.0 or 0.51.0.")

    constructor = signature(Multiprocess)

    observed = []
    for label, keywords in (
        ("with target", {"target": run_server, "sockets": []}),
        ("without target", {"sockets": []}),
    ):
        try:
            constructor.bind(object(), **keywords)
        except TypeError as error:
            observed.append(False)
            print(f"{release} {label}: rejected ({error})")
        else:
            observed.append(True)
            print(f"{release} {label}: accepted")

    if tuple(observed) != expected[release]:
        raise SystemExit(f"Unexpected binding behavior for Uvicorn {release}.")


if __name__ == "__main__":
    verify_binding()
