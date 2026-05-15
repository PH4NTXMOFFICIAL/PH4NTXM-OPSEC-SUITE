import os
import json
import string
import random

MARK_FILE = "/dev/shm/ph4-shred-marked.json"
LOCK_FILE = "/dev/shm/ph4-shred.lock"
MAX_PASSES = 7
DEFAULT_PASSES = 3
BLOCK_SIZE = 1024 * 1024

def _normalize(path):
    return os.path.realpath(path)

def _load_marks():
    if os.path.exists(MARK_FILE):
        try:
            with open(MARK_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_marks(files):
    try:
        with open(MARK_FILE, "w") as f:
            json.dump(files, f)
    except Exception:
        pass

def mark(file_path):
    file_path = _normalize(file_path)
    if not os.path.exists(file_path) or file_path == "/":
        return False
    files = _load_marks()
    if file_path not in files:
        files.append(file_path)
        _save_marks(files)
        return True
    return False

def unmark(file_path):
    file_path = _normalize(file_path)
    files = _load_marks()
    if file_path in files:
        files.remove(file_path)
        _save_marks(files)
        return True
    return False

def unmark_all():
    try:
        _save_marks([])
        return True
    except:
        return False

def list_marks():
    return _load_marks()

def _random_name(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def _overwrite_file(path, passes, callback=None):
    if not os.path.isfile(path) or os.path.islink(path):
        return
    try:
        size = os.path.getsize(path)
        patterns = [b'\x00', b'\xff']
        total_steps = (len(patterns) + max(1, passes - 2))
        current_step = 0
        with open(path, "r+b") as f:
            for p in patterns:
                f.seek(0)
                remaining = size
                chunk_data = p * BLOCK_SIZE
                while remaining > 0:
                    write_size = min(BLOCK_SIZE, remaining)
                    f.write(chunk_data[:write_size])
                    remaining -= write_size
                f.flush()
                os.fsync(f.fileno())
                current_step += 1
                if callback:
                    callback(path, int((current_step / total_steps) * 100))
            for _ in range(max(1, passes - 2)):
                f.seek(0)
                remaining = size
                while remaining > 0:
                    chunk = os.urandom(min(BLOCK_SIZE, remaining))
                    f.write(chunk)
                    remaining -= len(chunk)
                f.flush()
                os.fsync(f.fileno())
                current_step += 1
                if callback:
                    callback(path, int((current_step / total_steps) * 100))
    except Exception:
        pass

def _shred_item(path, passes, callback=None):
    if os.path.islink(path):
        try:
            os.unlink(path)
            return
        except:
            return
    if not os.path.exists(path):
        return
    try:
        os.utime(path, (0, 0))
    except:
        pass
    current_path = path
    for _ in range(3):
        new_tmp = os.path.join(os.path.dirname(current_path), _random_name())
        try:
            os.rename(current_path, new_tmp)
            current_path = new_tmp
        except:
            break
    _overwrite_file(current_path, passes, callback)
    try:
        with open(current_path, "r+b") as file:
            file.truncate(0)
            file.flush()
            os.fsync(file.fileno())
        os.remove(current_path)
    except:
        if os.path.exists(current_path):
            try: os.remove(current_path)
            except: os.unlink(current_path)

def shred_all(passes=DEFAULT_PASSES, progress_callback=None):
    if os.path.exists(LOCK_FILE):
        return [("error", "System", "Another process is running")]
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
        passes = max(1, min(MAX_PASSES, passes))
        files = _load_marks()
        results = []
        for f in list(files):
            try:
                if not os.path.lexists(f):
                    results.append(("missing", f))
                    files.remove(f)
                    _save_marks(files)
                    continue
                if os.path.isfile(f) or os.path.islink(f):
                    _shred_item(f, passes, progress_callback)
                    results.append(("shredded", f))
                    files.remove(f)
                    _save_marks(files)
                elif os.path.isdir(f):
                    for root, dirs, filenames in os.walk(f, topdown=False):
                        for name in filenames:
                            file_path = os.path.join(root, name)
                            try:
                                _shred_item(file_path, passes, progress_callback)
                            except:
                                try: os.unlink(file_path)
                                except: pass
                        for name in dirs:
                            dir_path = os.path.join(root, name)
                            try:
                                if os.path.islink(dir_path):
                                    os.unlink(dir_path)
                                else:
                                    os.utime(dir_path, (0, 0))
                                    os.rmdir(dir_path)
                            except:
                                try: os.unlink(dir_path)
                                except: pass
                    try:
                        os.utime(f, (0, 0))
                        os.rmdir(f)
                        results.append(("shredded_dir", f))
                        files.remove(f)
                        _save_marks(files)
                    except Exception as e:
                        results.append(("error", f, str(e)))
            except Exception as e:
                results.append(("error", f, str(e)))
        return results
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
