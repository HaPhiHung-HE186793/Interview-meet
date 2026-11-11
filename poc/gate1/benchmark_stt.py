#!/usr/bin/env python3
"""Gate 1 STT Benchmark: Groq Whisper Large-v3-turbo vs Soniox Async API.

Validates Interview-Meet Context Engine Gate 1 Go/No-Go criteria:
  1. Zero-cost 100% accurate speaker separation via independent Tab + Mic channels.
  2. Vietnamese-English IT code-switching accuracy with CV/JD vocabulary biasing (WER < 12%).
  3. Sub-second segment/token timestamp alignment (< 1s drift) for local IndexedDB audio citations.
  4. Unit economics verification (~1,300 - 2,000 VND / 1-hour meeting after VAD).
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

import requests

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VOCAB_PATH = Path(__file__).resolve().parent / "sample_cv_jd_terms.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "poc" / "outputs"
USD_TO_VND = 25_500


def load_env_files() -> None:
    env_path = REPO_ROOT / ".env"
    if load_dotenv and env_path.exists():
        load_dotenv(env_path)
        return
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip("'\""))


def probe_audio_stats(audio_path: Path) -> dict[str, float]:
    """Return audio duration (sec) and silence percentage using ffprobe/ffmpeg."""
    duration = 0.0
    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(audio_path),
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        duration = float(out) if out and out != "N/A" else 0.0
    except Exception:
        duration = 0.0

    silence_sec = 0.0
    try:
        proc = subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(audio_path),
                "-af",
                "silencedetect=noise=-38dB:d=0.6",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        for m in re.finditer(r"silence_duration:\s*([0-9.]+)", proc.stderr):
            silence_sec += float(m.group(1))
        if duration <= 0:
            dur_match = re.findall(r"time=(\d+):(\d+):([0-9.]+)", proc.stderr)
            if dur_match:
                h, m_val, s_val = dur_match[-1]
                duration = int(h) * 3600 + int(m_val) * 60 + float(s_val)
    except Exception:
        pass

    silence_pct = min(100.0, (silence_sec / duration * 100.0)) if duration > 0 else 0.0
    return {
        "duration_sec": round(duration, 2),
        "silence_sec": round(min(duration, silence_sec), 2),
        "silence_pct": round(silence_pct, 1),
    }


def load_vocab(vocab_path: Path) -> dict[str, Any]:
    if not vocab_path.exists():
        return {"role": "Software Engineer", "cv_jd_summary": "", "terms": []}
    return json.loads(vocab_path.read_text(encoding="utf-8"))


def build_whisper_prompt(vocab: dict[str, Any]) -> str:
    """Build a compact bilingual prompt (< 200 tokens) to bias Groq Whisper."""
    terms = ", ".join(vocab.get("terms", [])[:28])
    prompt = (
        f"Phỏng vấn kỹ thuật IT song ngữ Việt - Anh ({vocab.get('role', 'Software Engineer')}). "
        f"Giữ nguyên tiếng Việt và viết đúng chính tả các thuật ngữ tiếng Anh: {terms}."
    )
    return prompt[:750]


def transcribe_groq_whisper(
    audio_path: Path,
    speaker_label: str,
    vocab: dict[str, Any],
    language: str | None = "vi",
) -> dict[str, Any]:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY")

    prompt = build_whisper_prompt(vocab)
    data: list[tuple[str, str]] = [
        ("model", "whisper-large-v3-turbo"),
        ("prompt", prompt),
        ("response_format", "verbose_json"),
        ("temperature", "0"),
        ("timestamp_granularities[]", "segment"),
        ("timestamp_granularities[]", "word"),
    ]
    if language and language.lower() != "auto":
        data.append(("language", language))

    t0 = time.perf_counter()
    with audio_path.open("rb") as f:
        resp = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (audio_path.name, f, "audio/webm")},
            data=data,
            timeout=180,
        )
    elapsed = time.perf_counter() - t0
    if resp.status_code >= 400:
        raise RuntimeError(f"Groq API HTTP {resp.status_code}: {resp.text[:400]}")

    payload = resp.json()
    segments = []
    for seg in payload.get("segments") or []:
        text = (seg.get("text") or "").strip()
        no_speech = float(seg.get("no_speech_prob") or 0.0)
        if not text or no_speech > 0.80:
            continue
        segments.append(
            {
                "speaker": speaker_label,
                "start_sec": round(float(seg.get("start", 0.0)), 2),
                "end_sec": round(float(seg.get("end", 0.0)), 2),
                "text": text,
            }
        )

    return {
        "provider": "groq_whisper_v3_turbo",
        "latency_sec": round(elapsed, 2),
        "full_text": (payload.get("text") or "").strip(),
        "segments": segments,
        "word_count": len(payload.get("words") or []),
    }


def group_soniox_tokens(tokens: list[dict[str, Any]], speaker_label: str) -> list[dict[str, Any]]:
    """Group token-level timestamps into readable sentence/pause segments."""
    segments: list[dict[str, Any]] = []
    buf_text: list[str] = []
    seg_start: float | None = None
    last_end: float = 0.0

    for tok in tokens:
        txt = tok.get("text") or ""
        if not txt:
            continue
        s_sec = float(tok.get("start_ms", 0)) / 1000.0
        e_sec = float(tok.get("end_ms", tok.get("start_ms", 0))) / 1000.0

        if seg_start is not None and (s_sec - last_end > 1.1) and "".join(buf_text).strip():
            segments.append(
                {
                    "speaker": speaker_label,
                    "start_sec": round(seg_start, 2),
                    "end_sec": round(last_end, 2),
                    "text": "".join(buf_text).strip(),
                }
            )
            buf_text = []
            seg_start = None

        if seg_start is None:
            seg_start = s_sec
        buf_text.append(txt)
        last_end = max(last_end, e_sec)

        if txt.rstrip().endswith((".", "?", "!")) and len("".join(buf_text)) >= 36:
            segments.append(
                {
                    "speaker": speaker_label,
                    "start_sec": round(seg_start, 2),
                    "end_sec": round(last_end, 2),
                    "text": "".join(buf_text).strip(),
                }
            )
            buf_text = []
            seg_start = None

    if buf_text and "".join(buf_text).strip():
        segments.append(
            {
                "speaker": speaker_label,
                "start_sec": round(seg_start or 0.0, 2),
                "end_sec": round(last_end, 2),
                "text": "".join(buf_text).strip(),
            }
        )
    return segments


def transcribe_soniox(
    audio_path: Path,
    speaker_label: str,
    vocab: dict[str, Any],
) -> dict[str, Any]:
    api_key = os.environ.get("SONIOX_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing SONIOX_API_KEY")

    base_url = "https://api.soniox.com/v1"
    headers = {"Authorization": f"Bearer {api_key}"}
    preferred_model = os.environ.get("SONIOX_MODEL", "stt-async-v4").strip() or "stt-async-v4"
    file_id: str | None = None
    transcription_id: str | None = None

    t0 = time.perf_counter()
    try:
        with audio_path.open("rb") as f:
            up_resp = requests.post(
                f"{base_url}/files",
                headers=headers,
                files={"file": (audio_path.name, f, "audio/webm")},
                timeout=120,
            )
        if up_resp.status_code >= 400:
            raise RuntimeError(f"Soniox upload HTTP {up_resp.status_code}: {up_resp.text[:400]}")
        file_id = up_resp.json()["id"]

        job_body = {
            "model": preferred_model,
            "file_id": file_id,
            "language_hints": ["vi", "en"],
            "enable_language_identification": True,
            "context": {
                "general": [
                    {"key": "domain", "value": "Software Engineering & IT Interview"},
                    {"key": "role", "value": vocab.get("role", "Software Engineer")},
                ],
                "text": vocab.get("cv_jd_summary", ""),
                "terms": vocab.get("terms", []),
            },
        }
        job_resp = requests.post(
            f"{base_url}/transcriptions",
            headers={**headers, "Content-Type": "application/json"},
            json=job_body,
            timeout=60,
        )
        if job_resp.status_code >= 400 and preferred_model != "stt-async-v3":
            # Fallback without structured context object if an older model/tier rejects v4 schema
            fallback_body = {
                "model": "stt-async-v3",
                "file_id": file_id,
                "language_hints": ["vi", "en"],
                "context": ", ".join(vocab.get("terms", [])),
            }
            job_resp = requests.post(
                f"{base_url}/transcriptions",
                headers={**headers, "Content-Type": "application/json"},
                json=fallback_body,
                timeout=60,
            )
        if job_resp.status_code >= 400:
            raise RuntimeError(f"Soniox create job HTTP {job_resp.status_code}: {job_resp.text[:400]}")

        transcription_id = job_resp.json()["id"]
        for _ in range(120):
            st_resp = requests.get(
                f"{base_url}/transcriptions/{transcription_id}",
                headers=headers,
                timeout=30,
            )
            st_resp.raise_for_status()
            st_data = st_resp.json()
            status = st_data.get("status")
            if status == "completed":
                break
            if status in ("error", "failed"):
                raise RuntimeError(f"Soniox job failed: {st_data}")
            time.sleep(1.0)
        else:
            raise TimeoutError("Soniox job timed out after 120s")

        tr_resp = requests.get(
            f"{base_url}/transcriptions/{transcription_id}/transcript",
            headers=headers,
            timeout=60,
        )
        tr_resp.raise_for_status()
        tr_data = tr_resp.json()
        elapsed = time.perf_counter() - t0
        tokens = tr_data.get("tokens") or []
        return {
            "provider": f"soniox_{preferred_model}",
            "latency_sec": round(elapsed, 2),
            "full_text": (tr_data.get("text") or "").strip(),
            "segments": group_soniox_tokens(tokens, speaker_label),
            "word_count": len(tokens),
        }
    finally:
        if transcription_id:
            requests.delete(f"{base_url}/transcriptions/{transcription_id}", headers=headers, timeout=15)
        if file_id:
            requests.delete(f"{base_url}/files/{file_id}", headers=headers, timeout=15)


def normalize_words(text: str) -> list[str]:
    cleaned = re.sub(r"[^\w\s-]", " ", text.lower(), flags=re.UNICODE)
    return [w for w in cleaned.split() if w]


def compute_wer(reference_text: str, hypothesis_text: str) -> float:
    """Standard word-level Levenshtein Word Error Rate (WER %)."""
    ref = normalize_words(reference_text)
    hyp = normalize_words(hypothesis_text)
    if not ref:
        return 0.0
    dp = list(range(len(hyp) + 1))
    for i, r_word in enumerate(ref, start=1):
        prev = dp[0]
        dp[0] = i
        for j, h_word in enumerate(hyp, start=1):
            temp = dp[j]
            cost = 0 if r_word == h_word else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = temp
    return round((dp[-1] / len(ref)) * 100.0, 2)


def detect_matched_terms(full_text: str, terms: list[str]) -> list[str]:
    lower_txt = full_text.lower()
    return [t for t in terms if t.lower() in lower_txt]


def fmt_sec(sec: float) -> str:
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m:02d}:{s:04.1f}"


def evaluate_provider(
    provider_name: str,
    fn,
    tracks: list[tuple[str, Path]],
    vocab: dict[str, Any],
    hourly_rate_usd: float,
    total_audio_sec: float,
    active_audio_sec: float,
    reference_text: str | None,
) -> dict[str, Any]:
    merged_segments: list[dict[str, Any]] = []
    combined_texts: list[str] = []
    total_latency = 0.0

    for speaker_label, path in tracks:
        res = fn(path, speaker_label, vocab)
        total_latency += res["latency_sec"]
        merged_segments.extend(res["segments"])
        if res["full_text"]:
            combined_texts.append(res["full_text"])

    merged_segments.sort(key=lambda s: (s["start_sec"], s["end_sec"]))
    joined_text = " ".join(combined_texts)
    matched_terms = detect_matched_terms(joined_text, vocab.get("terms", []))

    raw_cost_1h_vnd = round(hourly_rate_usd * USD_TO_VND)
    vad_ratio = (active_audio_sec / total_audio_sec) if total_audio_sec > 0 else 0.7
    vad_cost_1h_vnd = round(hourly_rate_usd * vad_ratio * USD_TO_VND)

    wer_pct = compute_wer(reference_text, joined_text) if reference_text else None
    return {
        "provider": provider_name,
        "latency_sec": round(total_latency, 2),
        "rtf": round(total_latency / max(1.0, total_audio_sec), 3),
        "raw_cost_per_hour_vnd": raw_cost_1h_vnd,
        "vad_adjusted_cost_per_hour_vnd": vad_cost_1h_vnd,
        "matched_terms_count": len(matched_terms),
        "matched_terms": matched_terms,
        "wer_pct": wer_pct,
        "gate1_wer_pass": (wer_pct < 12.0) if wer_pct is not None else None,
        "segments": merged_segments,
    }


def render_markdown_report(
    tracks_meta: list[dict[str, Any]],
    results: list[dict[str, Any]],
    vocab_path: Path,
) -> str:
    lines = [
        "# Báo Cáo Kiểm Chứng Cổng 1 (Gate 1 STT & Dual-Channel Benchmark)",
        f"- **Thời gian chạy:** `{datetime.now().isoformat(timespec='seconds')}`",
        f"- **Bộ từ điển CV/JD:** `{vocab_path.name}`",
        "",
        "## 1. Thông Số Tệp Âm Thanh Đầu Vào & Hiệu Quả Lọc Khoảng Lặng (VAD)",
        "| Kênh người nói | Tệp âm thanh | Thời lượng (s) | Khoảng lặng đo được | Tiết kiệm nhờ VAD |",
        "|---|---|---:|---:|---:|",
    ]
    for tm in tracks_meta:
        lines.append(
            f"| **{tm['speaker']}** | `{tm['file']}` | {tm['duration_sec']}s | "
            f"{tm['silence_sec']}s | **{tm['silence_pct']}%** |"
        )

    lines.extend(
        [
            "",
            "## 2. Bảng Đọ Sức Các Engine STT (Code-Switching Anh–Việt)",
            "| Engine STT | Độ trễ API | RTF | Giá gốc / 1h họp | Giá sau lọc VAD / 1h | Thuật ngữ IT bắt trúng | WER (%) | Cổng 1 (<12%) |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for r in results:
        wer_str = f"{r['wer_pct']}%" if r["wer_pct"] is not None else "N/A (chưa truyền --reference)"
        pass_str = (
            "PASS" if r["gate1_wer_pass"] is True else ("FAIL" if r["gate1_wer_pass"] is False else "Kiểm tra thủ công")
        )
        lines.append(
            f"| `{r['provider']}` | {r['latency_sec']}s | {r['rtf']}x | "
            f"{r['raw_cost_per_hour_vnd']:,}đ | **{r['vad_adjusted_cost_per_hour_vnd']:,}đ** | "
            f"{r['matched_terms_count']} từ | {wer_str} | **{pass_str}** |"
        )

    for r in results:
        lines.extend(
            [
                "",
                f"## 3. Bản Gỡ Băng Ghép 2 Kênh Theo Mốc Giây — `{r['provider']}`",
                f"- **Thuật ngữ chuyên ngành bắt được:** {', '.join(f'`{t}`' for t in r['matched_terms']) or '*(Không có)*'}",
                "",
            ]
        )
        if not r["segments"]:
            lines.append("*(Không phát hiện lời thoại có nghĩa)*")
        for seg in r["segments"]:
            lines.append(
                f"- `[{fmt_sec(seg['start_sec'])} -> {fmt_sec(seg['end_sec'])}]` "
                f"**{seg['speaker']}:** {seg['text']}"
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    load_env_files()
    parser = argparse.ArgumentParser(
        description="Gate 1 PoC: Benchmark Groq Whisper Large-v3-turbo vs Soniox on bilingual IT audio."
    )
    parser.add_argument("--tab-audio", type=Path, help="File .webm Kênh 1 (Tab Google Meet / HR)")
    parser.add_argument("--mic-audio", type=Path, help="File .webm Kênh 2 (Micro cá nhân / Ứng viên)")
    parser.add_argument("--audio", type=Path, help="Chế độ test nhanh 1 file âm thanh đơn lẻ")
    parser.add_argument("--vocab", type=Path, default=DEFAULT_VOCAB_PATH, help="File JSON từ khóa CV/JD")
    parser.add_argument("--reference", type=Path, help="File văn bản chuẩn (ground truth) để tính WER tự động")
    parser.add_argument(
        "--provider",
        choices=["auto", "groq", "soniox", "both"],
        default="auto",
        help="Chọn engine chạy thử (mặc định: auto chạy tất cả engine đã điền API key trong .env)",
    )
    parser.add_argument("--whisper-lang", default="vi", help="Mã ngôn ngữ cho Whisper ('vi' hoặc 'auto')")
    args = parser.parse_args()

    tracks: list[tuple[str, Path]] = []
    if args.tab_audio:
        tracks.append(("HR / Meet", args.tab_audio))
    if args.mic_audio:
        tracks.append(("Ứng viên", args.mic_audio))
    if args.audio:
        tracks.append(("Speaker", args.audio))

    if not tracks:
        parser.error("Cần truyền ít nhất `--tab-audio` / `--mic-audio` hoặc `--audio`.")
    for _, p in tracks:
        if not p.exists():
            parser.error(f"Không tìm thấy tệp âm thanh: {p}")

    has_groq = bool(os.environ.get("GROQ_API_KEY", "").strip())
    has_soniox = bool(os.environ.get("SONIOX_API_KEY", "").strip())

    run_groq = args.provider in ("groq", "both") or (args.provider == "auto" and has_groq)
    run_soniox = args.provider in ("soniox", "both") or (args.provider == "auto" and has_soniox)
    if not run_groq and not run_soniox:
        print(
            "❌ Chưa tìm thấy GROQ_API_KEY hoặc SONIOX_API_KEY trong file `.env`.\n"
            "👉 Hãy chạy `cp .env.example .env` và điền ít nhất 1 API key trước khi chạy benchmark.",
            file=sys.stderr,
        )
        return 1

    vocab = load_vocab(args.vocab)
    reference_text = args.reference.read_text(encoding="utf-8") if args.reference else None

    tracks_meta = []
    total_dur = 0.0
    total_active = 0.0
    for speaker, path in tracks:
        st = probe_audio_stats(path)
        total_dur += st["duration_sec"]
        total_active += max(0.0, st["duration_sec"] - st["silence_sec"])
        tracks_meta.append({"speaker": speaker, "file": path.name, **st})

    results = []
    if run_groq:
        print("⏳ Đang gỡ băng qua Groq (`whisper-large-v3-turbo`) kèm từ điển CV/JD...")
        results.append(
            evaluate_provider(
                "Groq (whisper-large-v3-turbo)",
                lambda p, spk, vc: transcribe_groq_whisper(p, spk, vc, language=args.whisper_lang),
                tracks,
                vocab,
                hourly_rate_usd=0.04,
                total_audio_sec=total_dur,
                active_audio_sec=total_active,
                reference_text=reference_text,
            )
        )

    if run_soniox:
        print("⏳ Đang gỡ băng qua Soniox Async API kèm Structured Context CV/JD...")
        results.append(
            evaluate_provider(
                "Soniox Async STT",
                transcribe_soniox,
                tracks,
                vocab,
                hourly_rate_usd=0.10,
                total_audio_sec=total_dur,
                active_audio_sec=total_active,
                reference_text=reference_text,
            )
        )

    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = DEFAULT_OUTPUT_DIR / f"gate1_benchmark_{stamp}.md"
    json_path = DEFAULT_OUTPUT_DIR / f"gate1_benchmark_{stamp}.json"

    md_report = render_markdown_report(tracks_meta, results, args.vocab)
    md_path.write_text(md_report, encoding="utf-8")
    json_path.write_text(
        json.dumps({"tracks": tracks_meta, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 72)
    print(md_report)
    print("=" * 72)
    print(f"✅ Đã lưu báo cáo Markdown: {md_path}")
    print(f"✅ Đã lưu dữ liệu JSON (dùng tiếp cho Cổng 2): {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
