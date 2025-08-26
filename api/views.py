from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


def _run_metta_via_python_api(code: str):
    try:
        # Attempt to import Hyperon/MeTTa Python API if installed
        from hyperon import MeTTa
    except Exception as import_error:
        raise RuntimeError(f"MeTTa Python API not available: {import_error}")

    try:
        interpreter = MeTTa()
        result = interpreter.run(code)
        # Convert result to JSON-serializable structure if needed
        return result
    except Exception as exec_error:
        raise RuntimeError(f"MeTTa execution failed: {exec_error}")


def _run_metta_via_subprocess(code: str):
    import subprocess
    try:
        process = subprocess.Popen(
            ["metta"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as e:
        raise RuntimeError("MeTTa CLI 'metta' not found in PATH") from e

    stdout, stderr = process.communicate(input=code)
    if process.returncode != 0:
        raise RuntimeError(f"MeTTa error: {stderr}")
    return stdout


@api_view(["POST"])
def execute_metta(request):
    payload = request.data or {}
    code = payload.get("code", "")
    prefer = payload.get("prefer", "python")  # 'python' or 'cli'

    if not code or not isinstance(code, str):
        return Response({"error": "'code' must be a non-empty string"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if prefer == "cli":
            result = _run_metta_via_subprocess(code)
        else:
            # Try Python API, fallback to CLI
            try:
                result = _run_metta_via_python_api(code)
            except Exception:
                result = _run_metta_via_subprocess(code)

        return Response({"result": result})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
