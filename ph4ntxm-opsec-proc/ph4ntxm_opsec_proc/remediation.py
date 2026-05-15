import os
import signal
import subprocess

TERMINATION_TIMEOUT = 3

def result(ok, message=None, error=None):
    return {
        "ok": ok,
        "message": message,
        "error": error
    }

def process_exists(pid):

    try:
        pid = int(pid)

    except (TypeError, ValueError):
        return False

    try:
        os.kill(pid, 0)
        return True

    except OSError:
        return False

def get_child_pids(pid):

    try:
        pid = int(pid)

    except (TypeError, ValueError):
        return []

    children = set()

    try:
        output = subprocess.check_output(
            ["ps", "-eo", "pid,ppid"],
            text=True
        )

        process_map = {}

        for line in output.splitlines()[1:]:

            parts = line.split()

            if len(parts) != 2:
                continue

            child_pid = int(parts[0])
            parent_pid = int(parts[1])

            process_map.setdefault(
                parent_pid,
                []
            ).append(child_pid)

        stack = [pid]

        while stack:

            current = stack.pop()

            for child in process_map.get(current, []):

                if child not in children:
                    children.add(child)
                    stack.append(child)

    except Exception:
        pass

    return sorted(children)

def terminate_pid(pid):

    try:
        pid = int(pid)

    except (TypeError, ValueError):

        return result(
            False,
            error="Invalid pid"
        )

    if not process_exists(pid):
        return result(
            True,
            message=f"Pid {pid} already exited"
        )

    try:
        os.kill(pid, signal.SIGTERM)

    except Exception as exc:
        return result(
            False,
            error=str(exc)
        )

    try:
        for _ in range(TERMINATION_TIMEOUT * 10):

            if not process_exists(pid):
                return result(
                    True,
                    message=f"Pid {pid} terminated"
                )

            subprocess.run(
                ["sleep", "0.1"],
                check=False
            )

        os.kill(pid, signal.SIGKILL)

        return result(
            True,
            message=f"Pid {pid} force killed"
        )

    except Exception as exc:
        return result(
            False,
            error=str(exc)
        )

def terminate_process(proc):

    try:
        pid = int(proc.get("pid"))

    except (TypeError, ValueError):

        return result(
            False,
            error="Invalid pid"
        )

    return terminate_pid(pid)

def terminate_process_tree(proc):

    try:
        pid = int(proc.get("pid"))

    except (TypeError, ValueError):

        return result(
            False,
            error="Invalid pid"
        )

    targets = get_child_pids(pid)
    targets.reverse()

    terminated = []

    for child_pid in targets:

        child_result = terminate_pid(child_pid)

        if child_result["ok"]:
            terminated.append(str(child_pid))

    parent_result = terminate_pid(pid)

    if not parent_result["ok"]:
        return parent_result

    if terminated:

        return result(
            True,
            message=(
                f"Process tree terminated "
                f"(children: {', '.join(terminated)})"
            )
        )

    return result(
        True,
        message="Process terminated"
    )

def freeze_process(proc):

    try:
        pid = int(proc.get("pid"))

    except (TypeError, ValueError):

        return result(
            False,
            error="Invalid pid"
        )

    try:
        os.kill(pid, signal.SIGSTOP)

        return result(
            True,
            message=f"Pid {pid} frozen"
        )

    except Exception as exc:
        return result(
            False,
            error=str(exc)
        )

def available_actions(proc):

    reasons = set(proc.get("reasons", []))

    actions = []

    if reasons.intersection({
        "memfd_execution",
        "deleted_executable",
        "ephemeral_executable",
        "detached_shell",
        "untrusted_executable_path",
    }):

        actions.extend([
            "terminate",
            "terminate_tree",
            "freeze",
        ])

    return actions

PROCESS_ACTIONS = {
    "terminate": {
        "label": "Terminate Process",
        "description": "Send SIGTERM/SIGKILL to process",
        "severity": "bad",
        "action": terminate_process,
    },

    "terminate_tree": {
        "label": "Terminate Process Tree",
        "description": "Kill process and all child processes",
        "severity": "bad",
        "action": terminate_process_tree,
    },

    "freeze": {
        "label": "Freeze Process",
        "description": "Suspend process using SIGSTOP",
        "severity": "warn",
        "action": freeze_process,
    },
}