from cx_Freeze import setup, Executable

setup(
    name = "jf-copy-cut",
    version = "1.0",
    description = "1c db copy-cut",
    executables = [Executable("run.py")]
)