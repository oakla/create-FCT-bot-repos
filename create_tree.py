from octk import pytree, uniquify
from pathlib import Path

tree_exclude_dirs = [
    "__pycache__",
    "build",
    "develop-eggs",
    "dist",
    "downloads",
    "eggs",
    ".eggs",
    "lib",
    "lib64",
    "parts",
    "sdist",
    "var",
    "wheels",
    "share/python-wheels",
    ".egg-info",
    ".en",
    ".ven",
    "env",
    "venv",
    "ENV",
    "env.bak",
    "venv.bak",
    ".ipynb_checkpoints",
]

tree_exclude_file_extensions = [
    ".pyc",
    ".pyo",
    ".pyd",
    ".db",
    ".egg",
    ".sqlite3",
    ".sqlite",
    ".sqlite3-journal",
    ".sqlite-journal",
    ".bak",
    ".swp",
    ".swo",
    ".swn",
    ".swo",
    ".swn",
    ".swm",
    ".swl",
    ".swx",
    ".swpx",
    ".ipynb_checkpoints",
]

source_folder = r"."

output_dir = uniquify("test/outputs/output")

full_parent_name = str(Path(source_folder).absolute())

tree_str = full_parent_name + str(pytree.FileTree(
    source_folder, 
    diminishing_branches_mode=True, 
    max_item_per_level=512, 
    show_exclusion_message=True,
    exclude_dirs=tree_exclude_dirs,
    exclude_extensions=tree_exclude_file_extensions,
    ))

output_dir.mkdir(parents=True, exist_ok=True)
with open(output_dir / "file_tree.txt", "w", encoding="utf-8") as f:
    f.write(tree_str)