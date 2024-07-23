import warnings
import os
import sys


warnings.filterwarnings("ignore", message=".*'cached_download' is the legacy way to download files from the HF hub.*", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Creating a tensor from a list of numpy.ndarrays is extremely slow.*", category=UserWarning)

class SuppressOutput:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr