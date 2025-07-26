# ==============================  pipeline.py  ==============================
"""
Minimal-Pipeline zum Erkennen von Flirt-/Ambivalenz-Drift.
1.   Daten-Ingest  – Chat-Records ◁ JSON / DB / API
2.   Marker-Scoring – Regex-/ML-Tagger → marker_lookup
3.   Detector-Stage – ruft unsere Detector-Funktionen
4.   Reporting      – schreibt Flags in DB oder sendet Webhook
"""
from datetime import datetime, timedelta
from detector_utils import linear_slope
from detectors import (
    detect_sustained_contact,
    detect_secret_bonding,
    detect_adaptive_polarization,
    detect_flirt_dance_drift,
)

# --------------------------------------------------------------------------
# 1)  Simulierter Chat-Stream (chronologisch)
# --------------------------------------------------------------------------
CHAT_LOG = [
    {"id": "m1", "ts": datetime(2025, 7, 1, 9,  0), "text": "Du bist süß ;)",     },
    {"id": "m2", "ts": datetime(2025, 7, 1, 9,  1), "text": "Nicht verraten!",     },
    {"id": "m3", "ts": datetime(2025, 7, 2, 22, 0), "text": "Gute Nacht 🌙",       },
    {"id": "m4", "ts": datetime(2025, 7, 3,  8, 0), "text": "Dir zum ersten Mal …"},
    {"id": "m5", "ts": datetime(2025, 7, 3, 22, 0), "text": "Lösch den Chat 😊",   },
    {"id": "m6", "ts": datetime(2025, 7, 4, 20, 0), "text": "Du fehlst mir – egal",},
    {"id": "m7", "ts": datetime(2025, 7, 5, 21, 0), "text": "VIP-Tattoo? 😏",      },
]

# --------------------------------------------------------------------------
# 2)  VERY simple Marker-Tagging (RegEx-Demo) -------------------------------
#     → in der Praxis ersetzt du das durch dein echtes Marker-Engine-API.
# --------------------------------------------------------------------------
import re
PATTERNS = {
    "A_SOFT_FLIRT": re.compile(r"\b(süß|😉|😊|😏)\b", re.I),
    "S_MENTION_OF_SECRECY": re.compile(r"(nicht verraten|unter uns|lösch)", re.I),
    "C_ADAPTIVE_POLARIZATION": re.compile(r"du fehlst mir.*egal", re.I),
    "C_RAPID_SELF_DISCLOSURE": re.compile(r"zum ersten mal|noch nie erzählt", re.I),
}
marker_lookup = {}

for m in CHAT_LOG:
    found = [mid for mid, rx in PATTERNS.items() if rx.search(m["text"])]
    marker_lookup[m["id"]] = found

# --------------------------------------------------------------------------
# 3)  Detector-Stage --------------------------------------------------------
# --------------------------------------------------------------------------
detected = {}

ok, info = detect_sustained_contact(CHAT_LOG)
detected["C_SUSTAINED_CONTACT"] = ok

ok, info = detect_secret_bonding(CHAT_LOG, marker_lookup)
detected["C_SECRET_BONDING"] = ok

ok, info = detect_adaptive_polarization(CHAT_LOG, marker_lookup)
detected["C_ADAPTIVE_POLARIZATION"] = ok

ok, span = detect_flirt_dance_drift(CHAT_LOG, marker_lookup)
detected["MM_FLIRT_DANCE_DRIFT"] = ok

# --------------------------------------------------------------------------
# 4)  Report / Action -------------------------------------------------------
# --------------------------------------------------------------------------
if detected["MM_FLIRT_DANCE_DRIFT"]:
    print("⚠️  FLIRT-DANCE-DRIFT erkannt!")
    for msg in span:
        print(f"  {msg['ts'].strftime('%Y-%m-%d %H:%M')} – {msg['text']}")
else:
    print("Keine kritische Flirt-Drift erkannt.")

# ============================  Ende pipeline.py  ===========================
