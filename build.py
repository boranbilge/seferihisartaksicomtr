"""Generate the complete Seferihisar Taksi 7/24 website and brand assets."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).parent/'redesign.py'))
