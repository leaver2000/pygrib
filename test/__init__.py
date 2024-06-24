import os


def sample_dir(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), os.pardir, "sampledata", file_name)
