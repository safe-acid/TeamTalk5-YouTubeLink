#!/usr/bin/env bash
set -euo pipefail

export HOME="/home/app"
export XDG_RUNTIME_DIR="/opt/app/runtime"
export PULSE_RUNTIME_PATH="$XDG_RUNTIME_DIR/pulse"
export PULSE_SERVER="unix:${PULSE_RUNTIME_PATH}/native"

# 1) Clean PulseAudio runtime on every start
mkdir -p "$PULSE_RUNTIME_PATH"
rm -f "${PULSE_RUNTIME_PATH}/"* || true
rm -f "${HOME}/.config/pulse/pid" "${HOME}/.config/pulse/*.tdb" 2>/dev/null || true

# 2) Kill any stale PulseAudio daemon if it exists
pulseaudio -k >/dev/null 2>&1 || true

# 3) Start PulseAudio and wait until it's ready
pulseaudio -D --exit-idle-time=-1 --log-level=info --log-target=stderr || true

# Wait until pactl responds (max ~5 seconds)
for i in 1 2 3 4 5; do
  if pactl info >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

# 4) Create virtual audio devices (idempotent)
pactl unload-module module-virtual-source >/dev/null 2>&1 || true
pactl unload-module module-null-sink      >/dev/null 2>&1 || true

pactl load-module module-null-sink sink_name="${AUDIO_SINK_NAME:-Source}" \
  sink_properties=device.description="VirtualOut" >/dev/null

pactl load-module module-virtual-source source_name="${AUDIO_SOURCE_NAME:-VirtualMic}" \
  master="${AUDIO_MASTER:-Source.monitor}" >/dev/null

echo "[audio] sinks:";   pactl list short sinks   || true
echo "[audio] sources:"; pactl list short sources || true

# 5) Start the bot
cd /opt/app/src
exec python youtube_main.py
