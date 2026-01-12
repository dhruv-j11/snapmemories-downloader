# logic for the app


import os
from snapchat_parser import load_memories
from file_manager import build_path
from downloader import download
from report import Report

def run(json_file, output_dir, progress_cb):
    memories = load_memories(json_file)
    report = Report(output_dir)

    total = len(memories)
    done = 0

    for m in memories:
        ext = ".mp4" if m["type"] == "video" else ".jpg"
        path = build_path(output_dir, m["date"], ext)

        success = download(m["url"], path)
        name = os.path.basename(path)

        if success:
            report.log(name, "OK")
        else:
            report.log(name, "FAILED")

        done += 1
        progress_cb(done, total)

    report.close()
