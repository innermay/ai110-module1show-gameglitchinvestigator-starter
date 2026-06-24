import os
import sys

# Make the project root importable so tests can `import app`.
# (The pure logic functions currently live in app.py; logic_utils.py is
# still a set of NotImplementedError stubs awaiting the refactor.)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
