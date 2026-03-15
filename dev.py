#!/usr/bin/env python3
"""
dev.py — Development server with auto-rebuild and live reload

Usage: python3 dev.py [port]
Default port: 8000

Watches content/, templates/, static/ for changes.
Rebuilds site and triggers browser refresh automatically.
"""

import sys
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

ROOT = Path(__file__).parent
WATCH_DIRS = ["content", "templates", "static"]


class RebuildHandler(FileSystemEventHandler):
    """Debounced rebuild on file changes."""

    def __init__(self, rebuild_fn, reload_server=None):
        self.rebuild_fn = rebuild_fn
        self.reload_server = reload_server
        self._timer = None
        self._lock = threading.Lock()

    def on_any_event(self, event):
        if event.is_directory:
            return
        # Ignore hidden files and __pycache__
        if any(part.startswith(".") or part == "__pycache__"
               for part in Path(event.src_path).parts):
            return
        self._schedule_rebuild()

    def _schedule_rebuild(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(0.5, self._do_rebuild)
            self._timer.start()

    def _do_rebuild(self):
        print("\n--- Change detected, rebuilding... ---")
        try:
            self.rebuild_fn()
            print("--- Rebuild complete ---\n")
            if self.reload_server:
                # Touch a file to trigger livereload
                marker = ROOT / "site" / ".reload"
                marker.write_text(str(time.time()))
        except Exception as e:
            print(f"--- Rebuild failed: {e} ---\n")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    # Import build function
    from build import build

    # Initial build
    print("Initial build...")
    build()

    # Try livereload, fall back to simple HTTP server
    try:
        import livereload
        server = livereload.Server()
        for d in WATCH_DIRS:
            watch_path = str(ROOT / d)
            server.watch(watch_path, build)
        print(f"\nDev server (livereload): http://localhost:{port}")
        server.serve(root=str(ROOT / "site"), port=port, open_url_delay=None)
    except ImportError:
        print("livereload not installed, using watchdog + http.server")
        print(f"Install for auto-refresh: pip install livereload\n")

        # Start file watcher
        handler = RebuildHandler(build)
        observer = Observer()
        for d in WATCH_DIRS:
            watch_path = ROOT / d
            if watch_path.exists():
                observer.schedule(handler, str(watch_path), recursive=True)
        observer.start()

        # Start HTTP server
        import http.server
        import os
        os.chdir(ROOT / "site")
        httpd = http.server.HTTPServer(
            ("", port),
            http.server.SimpleHTTPRequestHandler
        )
        print(f"Dev server: http://localhost:{port}")
        print("Watching for changes... (Ctrl+C to stop)\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    main()
