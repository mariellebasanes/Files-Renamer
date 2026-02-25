"""
Flask Rename File Application
Lists folder contents and renames files with aligned old/new name display.
"""
import os
from pathlib import Path

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Always use a \"COPY FILES HERE\" (or \"@COPY FILES HERE\") folder next to this script.
# This is relative to the app location, so it works for any user path.
_base_dir = Path(__file__).resolve().parent
for folder_name in ("COPY FILES HERE", "@COPY FILES HERE"):
    _copy_files = _base_dir / folder_name
    if not _copy_files.exists():
        # Create the folder if it does not exist yet
        _copy_files.mkdir(parents=True, exist_ok=True)
    BASE_FOLDER = _copy_files.resolve()
    break


def get_folder_contents(folder_path: str) -> list[dict]:
    """Return list of files in folder: name, full path, is_dir."""
    path = Path(folder_path)
    if not path.exists() or not path.is_dir():
        return []
    items = []
    for p in sorted(path.iterdir()):
        try:
            items.append({
                "name": p.name,
                "path": str(p),
                "is_dir": p.is_dir(),
            })
        except OSError:
            continue
    return items


@app.route("/")
def index():
    return render_template("index.html", base_folder=str(BASE_FOLDER))


@app.route("/api/list", methods=["GET"])
def list_folder():
    """List files in the given folder. Query param: folder (path)."""
    folder = request.args.get("folder", "").strip() or str(BASE_FOLDER)
    path = Path(folder)
    if not path.is_absolute():
        path = BASE_FOLDER / folder
    path = path.resolve()
    # Restrict to under BASE_FOLDER for safety
    try:
        path.resolve().relative_to(BASE_FOLDER)
    except ValueError:
        folder = str(BASE_FOLDER)
        path = BASE_FOLDER
    items = get_folder_contents(str(path))
    return jsonify({
        "folder": str(path),
        "items": items,
    })


@app.route("/api/rename", methods=["POST"])
def rename_file():
    """
    Rename a file. JSON body: folder, old_name, new_name.
    Returns success/error with message.
    """
    data = request.get_json() or {}
    folder = (data.get("folder") or "").strip() or str(BASE_FOLDER)
    old_name = (data.get("old_name") or "").strip()
    new_name = (data.get("new_name") or "").strip()

    if not old_name:
        return jsonify({"ok": False, "error": "Old name is required"}), 400
    if not new_name:
        return jsonify({"ok": False, "error": "New name is required"}), 400
    if old_name == new_name:
        return jsonify({"ok": True, "message": "No change"})

    path = Path(folder)
    if not path.is_absolute():
        path = BASE_FOLDER / folder
    path = path.resolve()
    try:
        path.relative_to(BASE_FOLDER)
    except ValueError:
        return jsonify({"ok": False, "error": "Folder not allowed"}), 403

    old_path = path / old_name
    new_path = path / new_name

    if not old_path.exists():
        return jsonify({"ok": False, "error": f"File not found: {old_name}"}), 404
    if new_path.exists():
        return jsonify({"ok": False, "error": f"Target already exists: {new_name}"}), 409

    try:
        old_path.rename(new_path)
        return jsonify({"ok": True, "message": f"Renamed to {new_name}"})
    except OSError as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    import threading
    import webbrowser

    def _open_browser():
        webbrowser.open("http://127.0.0.1:5000/")

    threading.Timer(1.0, _open_browser).start()
    app.run(debug=True, port=5000, use_reloader=False)
