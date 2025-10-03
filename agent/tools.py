import pathlib
import subprocess
from typing import Tuple, Optional
import re
import hashlib

from langchain_core.tools import tool

# Base directory for all projects
PROJECTS_BASE = pathlib.Path.cwd() / "generated_projects"

class ProjectContext:
    """Manages the current project context."""
    _current_project: Optional[pathlib.Path] = None
    
    @classmethod
    def set_project(cls, project_name: str) -> pathlib.Path:
        """Sets the current project root."""
        # Sanitize project name to be filesystem-safe
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', project_name)
        safe_name = safe_name.strip()[:50]  # Limit length
        
        cls._current_project = PROJECTS_BASE / safe_name
        cls._current_project.mkdir(parents=True, exist_ok=True)
        return cls._current_project
    
    @classmethod
    def get_project(cls) -> pathlib.Path:
        """Gets the current project root."""
        if cls._current_project is None:
            raise ValueError("No project initialized. Call init_project_root(project_name) first.")
        return cls._current_project
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Check if a project is initialized."""
        return cls._current_project is not None


def safe_path_for_project(path: str) -> pathlib.Path:
    project_root = ProjectContext.get_project()
    p = (project_root / path).resolve()
    if project_root.resolve() not in p.parents and project_root.resolve() != p.parent and project_root.resolve() != p:
        raise ValueError(f"Attempt to write outside project root: {p}")
    return p


@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(ProjectContext.get_project())


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    project_root = ProjectContext.get_project()
    files = [str(f.relative_to(project_root)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    project_root = ProjectContext.get_project()
    cwd_dir = safe_path_for_project(cwd) if cwd else project_root
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def generate_project_name(user_prompt: str) -> str:
    """Generate a project name from user prompt."""
    # Take first few words and clean them
    words = user_prompt.lower().split()[:3]
    name = "_".join(words)
    # Remove special characters
    name = re.sub(r'[^a-z0-9_]', '', name)
    # Add hash for uniqueness
    hash_suffix = hashlib.md5(user_prompt.encode()).hexdigest()[:6]
    return f"{name}_{hash_suffix}"


def init_project_root(project_name: str) -> str:
    """Initializes a new project root with the given project name."""
    PROJECTS_BASE.mkdir(parents=True, exist_ok=True)
    project_path = ProjectContext.set_project(project_name)
    print(f"✓ Initialized project: {project_path}")
    return str(project_path)


def list_projects() -> list:
    """Lists all existing projects."""
    if not PROJECTS_BASE.exists():
        return []
    return [d.name for d in PROJECTS_BASE.iterdir() if d.is_dir()]


def get_current_project_name() -> Optional[str]:
    """Returns the name of the current project."""
    if ProjectContext.is_initialized():
        return ProjectContext.get_project().name
    return None