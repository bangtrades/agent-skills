#!/usr/bin/env python3
"""Execute explicit argv, retain a private complete log, return a bounded tail."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys


def run(command, log, max_chars=8000, timeout=120):
    if not command or max_chars < 0 or timeout <= 0:
        raise ValueError('command, nonnegative excerpt size and positive timeout required')
    path = Path(log).resolve()
    # Exclusive creation preserves earlier evidence; no shell expansion.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    timed_out = False
    with os.fdopen(fd, 'wb') as stream:
        proc = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT,
                                start_new_session=(os.name == 'posix'))
        try:
            code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == 'posix':
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
            proc.wait()
            code = 124
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
        size = stream.tell()
        offset = max(0, size - max_chars * 4)
        stream.seek(offset)
        decoded = stream.read().decode('utf-8', errors='replace')
        tail = decoded[-max_chars:] if max_chars else ''
        complete = offset == 0 and len(decoded) <= max_chars
    return dict(exit_code=code, timed_out=timed_out, log=str(path),
                sha256=digest.hexdigest(), bytes=size, excerpt_chars=len(tail),
                excerpt=tail, excerpt_is_complete=complete)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', required=True)
    parser.add_argument('--max-chars', type=int, default=8000)
    parser.add_argument('--timeout', type=float, default=120)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    try:
        result = run(command, args.log, args.max_chars, args.timeout)
        print(json.dumps(result, ensure_ascii=False))
        return result['exit_code'] if result['exit_code'] >= 0 else 128-result['exit_code']
    except (OSError, ValueError) as error:
        print(json.dumps({'error': str(error)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
