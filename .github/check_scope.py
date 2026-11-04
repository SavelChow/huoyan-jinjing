"""Scope and artifact checks. Review/branch rules remain the trust boundary."""
import ast
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = {p.name[6:8]: p.as_posix() for p in Path("members").iterdir() if p.is_dir() and re.fullmatch(r"member0[1-7]_.+", p.name)}

def allowed_paths(branch, author, owner, paths):
    if branch.startswith("integration/") and author.casefold() == owner.casefold():
        return True
    match = re.match(r"^member(0[1-7])/.+", branch)
    if not match:
        return False
    prefix = MEMBERS[match.group(1)] + "/"
    return all(path.startswith(prefix) for path in paths)

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")

def main():
    assert len(MEMBERS) == 7, "Seven member directories required"
    for path in MEMBERS.values():
        assert all((Path(path)/f).is_file() for f in ("README.md", "progress.md", "requirements.txt"))
    data = json.loads(Path("shared/catalogue.json").read_text(encoding="utf-8"))
    assert [c["id"] for c in data["classes"]] == list(range(6))
    assert set(data["models"]) == {"baseline1", "baseline2", "baseline3", "final"}
    # Git-tracked files only; local data/venvs must not enter the public repository.
    files = [p for p in git("ls-files", "-z").split("\0") if p]
    forbidden = {".pt", ".pth", ".ckpt", ".onnx", ".engine", ".pkl", ".joblib", ".npy", ".npz", ".jpg", ".jpeg", ".png", ".mp4", ".avi", ".zip", ".7z", ".pdf"}
    for name in files:
        p = Path(name)
        assert not p.is_symlink(), f"Symlink requires explicit review: {name}"
        assert not set(p.parts) & {"sealed_test", "private", "datasets", "weights", "checkpoints"}, name
        assert not p.name.startswith((".env", "ground_truth", "individual_report", "peer_feedback")), name
        assert p.suffix.lower() not in forbidden, f"Use artifact storage: {name}"
        assert p.stat().st_size <= 5*1024*1024, f"File exceeds 5 MiB: {name}"
        if p.suffix == ".py":
            ast.parse(p.read_text(encoding="utf-8"), filename=name)
    branch = os.environ.get("PR_BRANCH", "")
    if branch:
        base = os.environ["BASE_SHA"]
        paths = [p for p in git("diff", "--no-renames", "--name-only", "-z", base, "HEAD").split("\0") if p]
        assert allowed_paths(branch, os.environ["PR_AUTHOR"], os.environ["REPO_OWNER"], paths), "PR must modify only its member directory; owner integration PR required for shared changes"
    print("Framework and scope checks passed")

if __name__ == "__main__":
    main()
