#!/usr/bin/env python3
"""Original aggressive drift-phonk style bed: hard kick, distorted sliding 808,
phonk cowbell riff, claps, hi-hat rolls, riser into a drop. Seeded and deterministic.

usage: python3 phonk.py OUT.wav SECONDS [--drop 3.6] [--bpm 140] [--key 0..11] [--seed N] [--outro 1.5]
--outro is the fade-out length in seconds at the end (keep it short, e.g. 1.5).
Needs: pip install numpy. MIT license, by OctaneWire.
"""
import argparse
import wave

import numpy as np

SR = 48000


def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def kick(rng):
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 45 + 140 * np.exp(-t * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 7.5)
    click = rng.standard_normal(n) * env_exp(n, 220) * 0.4
    return np.tanh((s + click) * 2.6) * 0.95


def clap(rng):
    n = int(0.3 * SR); x = rng.standard_normal(n)
    # band-limit by differencing + smoothing
    x = np.convolve(np.diff(x, prepend=0), np.ones(6) / 6, mode="same")
    e = np.zeros(n)
    for d in (0, 0.011, 0.022):
        i = int(d * SR); e[i:] += env_exp(n - i, 38)
    return np.tanh(x * e * 3.0) * 0.55


def hat(rng, open_=False):
    n = int((0.16 if open_ else 0.045) * SR); x = rng.standard_normal(n)
    x = np.diff(x, prepend=0); x = np.diff(x, prepend=0)
    return x * env_exp(n, 18 if open_ else 95) * 0.11


def cowbell(freq_scale, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f1, f2 = 540 * freq_scale, 800 * freq_scale
    sq = lambda f: np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t) * 0.5
    s = (sq(f1) + sq(f2)) * 0.5
    s = s - np.convolve(s, np.ones(40) / 40, mode="same")  # crude high-pass
    e = np.minimum(1, t / 0.002) * (0.65 * np.exp(-t * 9) + 0.35 * np.exp(-t * 2.2))
    return np.tanh(s * e * 1.6) * 0.32


def bass808(notes, total_n, spb, slide=0.06, drive=4.5):
    """notes: list of (start_beat, length_beats, freq). Gliding sine, saturated."""
    f = np.zeros(total_n); amp = np.zeros(total_n)
    last = None
    for sb, lb, fr in notes:
        i0, i1 = int(sb * spb * SR), min(total_n, int((sb + lb) * spb * SR))
        if i0 >= total_n:
            continue
        seg = i1 - i0
        if last is not None:
            g = min(seg, int(slide * SR))
            f[i0:i0 + g] = np.linspace(last, fr, g)
            f[i0 + g:i1] = fr
        else:
            f[i0:i1] = fr
        tt = np.arange(seg) / SR
        amp[i0:i1] = np.minimum(1, tt / 0.004) * np.exp(-tt * 0.9) * np.minimum(1, (seg - np.arange(seg)) / (0.01 * SR))
        last = fr
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph)
    return np.tanh(s * amp * drive) * 0.55 * (amp > 0)


def saw_stab(freqs, dur, rng):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for fr in freqs:
        for det in (-0.6, 0, 0.7):
            s += 2 * (((fr + det) * t + rng.random()) % 1) - 1
    s = np.convolve(s, np.ones(8) / 8, mode="same")
    return np.tanh(s * 0.5 * env_exp(n, 7) * 2.2) * 0.22


def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf) or i < 0:
        return
    e = min(len(buf), i + len(sig)); buf[i:e] += sig[: e - i] * gain


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("seconds", type=float)
    ap.add_argument("--drop", type=float, default=3.6); ap.add_argument("--bpm", type=float, default=140)
    ap.add_argument("--key", type=int, default=5); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--outro", type=float, default=1.5)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    n = int(a.seconds * SR); spb = 60 / a.bpm
    L = np.zeros(n); R = np.zeros(n)
    root = 43.65 * 2 ** (a.key / 12)  # F1 by default offset
    minor = [0, 3, 5, 7, 10, 12, 15]
    riff_bank = [[0, 3, 5, 3, 7, 5, 3, 0], [0, 0, 3, 5, 6, 5, 3, 5], [7, 5, 3, 5, 0, 3, 5, 7], [0, 3, 7, 10, 7, 5, 3, 5]]
    riff = riff_bank[a.seed % len(riff_bank)]
    bass_bank = [[0, 0, 3, -2], [0, 5, 3, 0], [0, -2, -4, -2], [0, 3, 5, 7]]
    bprog = bass_bank[(a.seed // 2) % len(bass_bank)]
    end = a.seconds - a.outro
    drop_beat = a.drop / spb
    K = kick(rng); C = clap(rng)
    beats = int(a.seconds / spb) + 2
    # --- intro: filtered cowbell + riser + reversed-ish swell
    for b in range(int(drop_beat * 2)):
        t = b * spb / 2
        if t >= a.drop: break
        cb = cowbell(2 ** (riff[b % 8] / 12), spb * 0.9)
        cb = np.convolve(cb, np.ones(14) / 14, mode="same")  # muffled before the drop
        place(L, cb, t, 0.55 + 0.4 * t / a.drop); place(R, cb, t, 0.5 + 0.4 * t / a.drop)
    rn = int(a.drop * SR); tt = np.arange(rn) / SR
    riser = rng.standard_normal(rn) * (tt / a.drop) ** 3 * 0.22
    riser += np.sin(2 * np.pi * (180 + 900 * (tt / a.drop) ** 2) * tt) * (tt / a.drop) ** 2 * 0.12
    L[:rn] += riser; R[:rn] += riser
    # snare roll into the drop
    for k in range(16):
        tr = a.drop - spb * 2 + k * spb / 8
        if tr > 0: place(L, C, tr, 0.25 + k * 0.03); place(R, C, tr, 0.25 + k * 0.03)
    # --- drop: drums, 808, cowbell lead, stabs
    notes = []
    b = drop_beat
    while b * spb < end:
        bar = int((b - drop_beat) // 4)
        tb = b * spb
        beat_in_bar = int(round(b - drop_beat)) % 4
        # kick pattern: 1, 2.75, 3 (+ variation)
        for off in ((0,), (0.75,), (0, 0.5), (0.75,))[beat_in_bar]:
            place(L, K, tb + off * spb, 1.0); place(R, K, tb + off * spb, 1.0)
        if beat_in_bar in (1, 3):
            place(L, C, tb, 0.9); place(R, C, tb, 0.85)
        # hats: 8ths, with 1/32 rolls on the last beat of every second bar
        if beat_in_bar == 3 and bar % 2 == 1:
            for k in range(8):
                h = hat(rng); place(L, h, tb + k * spb / 8, 0.8); place(R, h, tb + k * spb / 8, 0.9)
        else:
            for k in range(2):
                h = hat(rng, open_=(k == 1 and beat_in_bar == 2)); place(L, h, tb + k * spb / 2, 0.9); place(R, h, tb + k * spb / 2, 1.0)
        # cowbell riff on 8ths
        for k in range(2):
            idx = (int(round(b - drop_beat)) * 2 + k) % 8
            semi = riff[idx] + (12 if (bar % 4 == 3 and k == 1) else 0)
            cb = cowbell(2 ** (semi / 12), spb * 0.6)
            place(L, cb, tb + k * spb / 2, 0.9); place(R, cb, tb + k * spb / 2 + 0.012, 0.8)
        if beat_in_bar == 0:
            fr = root * 2 ** (bprog[bar % 4] / 12)
            notes.append((b, 2.5, fr)); notes.append((b + 2.5, 1.5, fr * 2 ** (minor[(bar + 2) % 4] / 12)))
            st = saw_stab([fr * 4, fr * 4 * 2 ** (3 / 12), fr * 4 * 2 ** (7 / 12)], spb * 0.9, rng)
            place(L, st, tb, 0.8); place(R, st, tb + 0.008, 0.8)
        b += 1
    bass = bass808(notes, n, spb)
    L += bass; R += bass
    # --- outro: final impact, let it ring
    ie = int(end * SR)
    imp = kick(rng); place(L, imp, end, 1.0); place(R, imp, end, 1.0)
    tail = np.sin(2 * np.pi * root * 2 * np.arange(n - ie) / SR) * env_exp(n - ie, 1.6) * 0.5
    L[ie:] += np.tanh(tail * 3) * 0.4; R[ie:] += np.tanh(tail * 3) * 0.4
    mix = np.stack([L, R], 1)
    mix = np.tanh(mix * 1.15)
    mix /= np.max(np.abs(mix)) * 1.02
    fade = int(0.08 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    w = wave.open(a.out, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32000).astype(np.int16).tobytes()); w.close()


if __name__ == "__main__":
    main()
