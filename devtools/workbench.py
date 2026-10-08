#!/usr/bin/env python3
"""A workbench for choosing what becomes a 3D model, without the game.

    python devtools/workbench.py            then open http://localhost:8765

(Windows Python; the maps' pictures come from devtools/workbench_prepare.py,
run once in WSL.) Pick a map, drag over the cells of a thing, say what kind of
model it should be - a card, a dome, a box - and:

  * Preview builds that one model with the real generator (in WSL, some 15 s)
    and shows it from several angles, beside its drawing;
  * Save request writes it to devtools/model_requests.json, with a picture of
    the cells in devtools/model_requests/, for whoever turns requests into
    specs of scripts/voxel_building_specs.py.

Nothing here changes the game's build: a request is a note until it is made a
spec.
"""
import base64
import json
import os
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BENCH = os.path.join(REPO, "build", "workbench")
REQUESTS = os.path.join(REPO, "devtools", "model_requests.json")
PICTURES = os.path.join(REPO, "devtools", "model_requests")
PORT = 8765
NAME = re.compile(r"^[a-z0-9_]{1,40}$")
LAYOUT = re.compile(r"^LAYOUT_[A-Z0-9_]{1,60}$")


def mnt(path):
    path = os.path.abspath(path).replace("\\", "/")
    return "/mnt/" + path[0].lower() + path[2:]


def load_requests():
    if os.path.exists(REQUESTS):
        return json.load(open(REQUESTS, encoding="utf-8"))
    return []


def save_requests(items):
    with open(REQUESTS, "w", encoding="utf-8", newline="\n") as f:
        json.dump(items, f, indent=1)
        f.write("\n")


def clean(d):
    """A request as the page sent it, checked: only what a spec is made of."""
    if not NAME.match(str(d.get("name", ""))) or not LAYOUT.match(str(d.get("layout", ""))):
        raise ValueError("a name of a-z, 0-9 and _, and a layout")
    rect = [int(v) for v in d["rect"]]
    if len(rect) != 4 or min(rect) < 0 or rect[2] < 1 or rect[3] < 1 or rect[2] > 16 or rect[3] > 16:
        raise ValueError("a rectangle of 1 to 16 cells a side")
    colours = [c for c in d.get("clear", []) if re.match(r"^[0-9a-f]{6}$", c)][:16]
    return {"name": d["name"], "layout": d["layout"], "map": str(d.get("map", ""))[:60], "rect": rect,
            "kind": d.get("kind") if d.get("kind") in ("card", "dome", "box") else "card",
            "ground": int(d.get("ground", 1)), "clear": colours, "drop": bool(d.get("drop")),
            "height": max(1, min(int(d.get("height", 16)), 255)),
            "note": str(d.get("note", ""))[:400]}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body, kind="application/json", code=200):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def file(self, root, name, kind):
        path = os.path.join(root, os.path.basename(name))
        if not os.path.exists(path):
            return self.send({"error": "not found"}, code=404)
        self.send(open(path, "rb").read(), kind)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            return self.send(open(os.path.join(REPO, "devtools", "workbench.html"), "rb").read(),
                             "text/html; charset=utf-8")
        if path == "/index.json":
            return self.file(BENCH, "index.json", "application/json")
        if path == "/requests":
            return self.send(load_requests())
        if path.startswith("/layouts/"):
            return self.file(os.path.join(BENCH, "layouts"), path,
                             "image/png" if path.endswith(".png") else "application/json")
        if path.startswith("/preview/"):
            return self.file(os.path.join(REPO, "build", "previews"), path, "image/png")
        if path.startswith("/pictures/"):
            return self.file(PICTURES, path, "image/png")
        self.send({"error": "not found"}, code=404)

    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))) or b"{}")
            if self.path == "/save":
                item = clean(data)
                item["status"] = "requested"
                picture = str(data.get("picture", ""))
                if picture.startswith("data:image/png;base64,"):
                    os.makedirs(PICTURES, exist_ok=True)
                    with open(os.path.join(PICTURES, item["name"] + ".png"), "wb") as f:
                        f.write(base64.b64decode(picture.split(",", 1)[1]))
                items = [r for r in load_requests() if r["name"] != item["name"]] + [item]
                save_requests(items)
                return self.send({"ok": True, "requests": items})
            if self.path == "/delete":
                items = [r for r in load_requests() if r["name"] != data.get("name")]
                save_requests(items)
                return self.send({"ok": True, "requests": items})
            if self.path == "/preview":
                item = clean(data)
                item["name"] = "draft_" + item["name"]
                os.makedirs(BENCH, exist_ok=True)
                draft = os.path.join(BENCH, "draft.json")
                json.dump([item], open(draft, "w", encoding="utf-8"))
                command = "cd '%s' && VOXEL_DRAFT='%s' bash devtools/model_view.sh %s %s" % (
                    mnt(REPO), mnt(draft), item["name"], item["layout"])
                run = subprocess.run(["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-lc", command],
                                     capture_output=True, text=True, timeout=400)
                sheet = os.path.join(REPO, "build", "previews", item["name"] + "_sheet.png")
                return self.send({"ok": os.path.exists(sheet) and run.returncode == 0,
                                  "log": (run.stdout + run.stderr)[-1500:],
                                  "image": "/preview/%s_sheet.png" % item["name"]})
            self.send({"error": "not found"}, code=404)
        except Exception as error:      # said to the page, not a dead server
            self.send({"ok": False, "log": "%s: %s" % (type(error).__name__, error)}, code=400)


def main():
    if not os.path.exists(os.path.join(BENCH, "index.json")):
        sys.exit("no maps yet: run `python3 devtools/workbench_prepare.py` in WSL first")
    print("workbench: http://localhost:%d   (Ctrl+C to stop)" % PORT)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
