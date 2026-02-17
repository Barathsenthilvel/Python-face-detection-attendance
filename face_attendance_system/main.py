import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_ui import main

if __name__ == "__main__":
    main()
