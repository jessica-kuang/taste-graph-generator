import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

STAGES = [
    "embedder.py",
    "profiler.py",
    "palette.py",
    "substack.py",
    "brands.py",
    "generator.py",
]


class PipelineError(Exception):
    def __init__(self, stage: str, stderr: str):
        super().__init__(f"{stage} failed:\n{stderr}")
        self.stage = stage
        self.stderr = stderr


def run_pipeline(on_progress=None) -> None:
    """Runs the same 6 scripts the README has the user run by hand, in order,
    each as its own subprocess so nothing about embedder.py through
    generator.py needs to change to become importable.
    """
    for stage in STAGES:
        if on_progress:
            on_progress(stage, "started", None)
        result = subprocess.run(
            [sys.executable, f"src/{stage}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if on_progress:
            on_progress(stage, result.stdout, result.returncode)
        if result.returncode != 0:
            raise PipelineError(stage, result.stderr)


if __name__ == "__main__":
    def log(stage, output, returncode):
        if returncode is None:
            print(f"→ running {stage}...")
        else:
            print(output)
            print(f"✓ {stage} done")

    run_pipeline(on_progress=log)
    print("\npipeline complete, run app.py to view the graph")
