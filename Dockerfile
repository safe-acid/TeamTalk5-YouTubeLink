FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    AUDIO_SINK_NAME=Source \
    AUDIO_SOURCE_NAME=VirtualMic \
    AUDIO_MASTER=Source.monitor \
    TT_SDK_VER=v5.19a \
    PATH="/home/app/.local/bin:${PATH}"

# System packages:
# - pulseaudio + pulseaudio-utils: audio server + pactl
# - mpv + libmpv-dev + pkg-config: mpv player and dev headers for Python bindings
# - ffmpeg: media processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl nano procps \
    pulseaudio pulseaudio-utils \
    mpv libmpv-dev pkg-config \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 app
USER app
WORKDIR /opt/app/src

# Copy your local project (config.py, setup.py, requirements.txt, etc.)
# Place this Dockerfile in the project root and run build from there
COPY --chown=app:app . /opt/app/src

# (Optional) Auto-patch setup.py: enforce HTTPS, v5.19a, and tt5sdk_* filenames
RUN python - <<'PY'
import io, re
p = "setup.py"
try:
    s = io.open(p, "r", encoding="utf-8").read()
except FileNotFoundError:
    raise SystemExit(0)
changed = False
if re.search(r'BASE_URL\s*=', s):
    s = re.sub(r'BASE_URL\s*=\s*["\'].*?["\']',
               'BASE_URL = "https://www.bearware.dk/teamtalksdk/"', s); changed = True
if re.search(r'FILE_NAMES\s*=\s*\{', s):
    s = re.sub(r'FILE_NAMES\s*=\s*\{[\s\S]*?\}\s*',
               ('SDK_VER = os.getenv("TT_SDK_VER", "v5.19a")\n'
                'FILE_NAMES = {\n'
                '    "Linux":   f"tt5sdk_{SDK_VER}_ubuntu22_x86_64.7z",\n'
                '    "Darwin":  f"tt5sdk_{SDK_VER}_macos_universal.7z",\n'
                '    "Windows": f"tt5sdk_{SDK_VER}_win64.7z",\n'
                '}\n'), s); changed = True
s = s.replace("v5.15a", "v5.19a")
s = re.sub(r'download_url\s*=\s*urljoin\([^)]*\)',
           'download_url = urljoin(urljoin(BASE_URL, (SDK_VER if "SDK_VER" in globals() else "v5.19a") + "/"), filename)', s)
if changed or "v5.15a" in s:
    io.open(p, "w", encoding="utf-8").write(s)
    print("[patch] setup.py adjusted to tt5sdk v5.19a over https")
else:
    print("[patch] setup.py looks OK; no changes")
PY

# Install Python dependencies and SDK via your setup.py
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python setup.py

# PulseAudio runtime dir
RUN mkdir -p /opt/app/runtime/pulse

# Entrypoint (starts PulseAudio, creates virtual devices, runs your app)
COPY --chown=app:app entrypoint.sh /opt/app/entrypoint.sh
RUN chmod +x /opt/app/entrypoint.sh

ENTRYPOINT ["/opt/app/entrypoint.sh"]
