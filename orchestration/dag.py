import os
import subprocess
import luigi
from datetime import datetime

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

VENV_SCRIPTS = os.path.join(PROJECT_ROOT, ".venv", "Scripts")

PYTHON = os.path.join(VENV_SCRIPTS, "python.exe")
DBT = os.path.join(VENV_SCRIPTS, "dbt.exe")

DLT_DIR = os.path.join(PROJECT_ROOT, "dlt_pipeline")
DBT_DIR = os.path.join(PROJECT_ROOT, "walmart_end_to_end_de_project_dbt")

MARKER_DIR = os.path.join(PROJECT_ROOT, "orchestration", "status")

os.makedirs(MARKER_DIR, exist_ok=True)


# =====================================================
# Helper Function
# =====================================================

def run_command(command, cwd):

    print("\nExecuting:")
    print(" ".join(command))
    print("Working Directory:", cwd)

    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Command Failed : {' '.join(command)}")


# =====================================================
# START PIPELINE
# =====================================================

class StartPipeline(luigi.Task):

    def output(self):
        return luigi.LocalTarget(os.path.join(MARKER_DIR, "pipeline_started.txt"))

    def run(self):

        print("=" * 70)
        print("Cleaning Previous Run")
        print("=" * 70)

        for file in os.listdir(MARKER_DIR):
            if file.endswith(".txt"):
                os.remove(os.path.join(MARKER_DIR, file))

        with self.output().open("w") as f:
            f.write(str(datetime.now()))


# =====================================================
# DLT
# =====================================================

class LoadDLT(luigi.Task):

    def requires(self):
        return StartPipeline()

    def output(self):
        return luigi.LocalTarget(os.path.join(MARKER_DIR, "load_complete.txt"))

    def run(self):

        print("=" * 70)
        print("STEP 1 : Running DLT Pipeline")
        print("=" * 70)

        run_command(
            [PYTHON, "load.py"],
            cwd=DLT_DIR
        )

        with self.output().open("w") as f:
            f.write(str(datetime.now()))


# =====================================================
# DBT RUN
# =====================================================

class RunDBT(luigi.Task):

    def requires(self):
        return LoadDLT()

    def output(self):
        return luigi.LocalTarget(os.path.join(MARKER_DIR, "dbt_run_complete.txt"))

    def run(self):

        print("=" * 70)
        print("STEP 2 : Running dbt Models")
        print("=" * 70)

        run_command(
            [DBT, "run"],
            cwd=DBT_DIR
        )

        with self.output().open("w") as f:
            f.write(str(datetime.now()))


# =====================================================
# DBT TEST
# =====================================================

class TestDBT(luigi.Task):

    def requires(self):
        return RunDBT()

    def output(self):
        return luigi.LocalTarget(os.path.join(MARKER_DIR, "dbt_test_complete.txt"))

    def run(self):

        print("=" * 70)
        print("STEP 3 : Running dbt Tests")
        print("=" * 70)

        run_command(
            [DBT, "test"],
            cwd=DBT_DIR
        )

        with self.output().open("w") as f:
            f.write(str(datetime.now()))


# =====================================================
# DBT DOCS
# =====================================================

class GenerateDocs(luigi.Task):

    def requires(self):
        return TestDBT()

    def output(self):
        return luigi.LocalTarget(os.path.join(MARKER_DIR, "docs_complete.txt"))

    def run(self):

        print("=" * 70)
        print("STEP 4 : Generating dbt Docs")
        print("=" * 70)

        run_command(
            [DBT, "docs", "generate"],
            cwd=DBT_DIR
        )

        with self.output().open("w") as f:
            f.write(str(datetime.now()))


# =====================================================
# FINAL TASK
# =====================================================

class WalmartPipeline(luigi.Task):

    def requires(self):
        return GenerateDocs()

    def output(self):
        return luigi.LocalTarget(os.path.join(MARKER_DIR, "pipeline_completed.txt"))

    def run(self):

        print("\n" + "=" * 70)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("Completed At :", datetime.now())
        print("=" * 70)

        with self.output().open("w") as f:
            f.write(str(datetime.now()))


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    luigi.run()