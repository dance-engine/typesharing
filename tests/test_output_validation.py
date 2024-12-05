import subprocess

def test_python_output():
    """
    Run mypy to validate generated Python types.
    """
    result = subprocess.run(
        ["mypy", "tests/generated/test_types.py"], 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"Python type check failed:\n{result.stdout}\n{result.stderr}"


def test_ts_output():
    """
    Run tsc to validate generated TypeScript types.
    """
    result = subprocess.run(
        ["tsc", "--noEmit", "tests/generated/test_types.ts"], 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"TypeScript type check failed:\n{result.stdout}\n{result.stderr}"
