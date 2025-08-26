from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.db import transaction
from .models import Profile


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


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def register(request):
    payload = request.data or {}
    username = payload.get("username")
    email = payload.get("email")
    password = payload.get("password")
    user_type = payload.get("userType", "other")

    if not username or not email or not password:
        return Response({"message": "username, email, password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"message": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    Profile.objects.create(user=user, user_type=user_type if user_type in dict(Profile.USER_TYPE_CHOICES) else "other")

    return Response({
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    payload = request.data or {}
    username = payload.get("username")
    password = payload.get("password")
    user_type = payload.get("userType")

    if not username or not password:
        return Response({"message": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Optionally check user_type match if exists
    try:
        profile = user.profile
        if user_type and profile.user_type != user_type:
            return Response({"message": "User type mismatch"}, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        profile = None

    django_login(request, user)
    return Response({
        "user": {"id": user.id, "username": user.username, "email": user.email},
        # In the future, issue JWT; for now, session-based
    })


@api_view(["POST"])
def logout(request):
    django_logout(request)
    return Response({"message": "Logged out"})
