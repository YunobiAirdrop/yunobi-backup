#!/usr/bin/env python3
"""Phase 2: shorts2 TTS (5 beat) + long expansion (re-TTS beats 3-9 dengan teks lebih panjang)."""
import subprocess, os, json, sys

BASE = "/home/hatch/workspace/youtube-otomatis/mind-en/2026-10-16-fix"
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:miles"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"

def tts_synth(text, out):
    if os.path.exists(out):
        os.remove(out)
    r = subprocess.run([TTS, "--voice", VOICE, "--text", text, "--output", out],
                       capture_output=True, text=True, timeout=180)
    return os.path.exists(out) and os.path.getsize(out) > 1000

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def concat_vo(adir, n):
    lst = os.path.join(adir, "list.txt")
    with open(lst, "w") as f:
        for i in range(1, n + 1):
            f.write(f"file '{adir}/beat-{i:03d}.mp3'\n")
    vo = os.path.join(adir, "voiceover.mp3")
    if os.path.exists(vo):
        os.remove(vo)
    subprocess.run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", vo], capture_output=True, check=True)
    return vo

# ============ SHORTS2 (5 beat) ============
s2_beats = [
    "Forget body language. Four words expose every liar.",
    "The words are: I. Do not. Remember. Liars almost never say I do not remember.",
    "Because admitting a blank looks guilty to them. So they fill it. They invent details, smooth and confident, where an honest person would just shrug.",
    "Truth-tellers say I forgot all the time. It costs them nothing. Liars cannot afford a single gap, because one gap unravels the whole story.",
    "So next time someone gives you a perfect story with zero gaps, that is your sign. The smoothest story is usually the fakest.",
]
adir = os.path.join(BASE, "shorts2", "audio")
os.makedirs(adir, exist_ok=True)
print("=== shorts2: 5 beats ===", flush=True)
durs = {}
for i, txt in enumerate(s2_beats, 1):
    out = os.path.join(adir, f"beat-{i:03d}.mp3")
    for attempt in range(3):
        if tts_synth(txt, out) and dur(out) > 1:
            break
        print(f"  s2 beat {i}: retry {attempt+2}", flush=True)
    else:
        print(f"GAGAL TTS: shorts2 beat {i}"); sys.exit(1)
    d = dur(out)
    durs[f"beat-{i:03d}"] = round(d, 2)
    print(f"  beat {i}: {d:.1f}s", flush=True)
concat_vo(adir, 5)
json.dump(durs, open(os.path.join(adir, "durasi.json"), "w"), indent=1)
print(f"  TOTAL shorts2: {sum(durs.values()):.1f}s", flush=True)

# ============ LONG EXPANSION (beats 3-9) ============
long_expanded = {
    3: "Number seven. I am just trying to help you. It sounds caring. That is the point. This phrase reframes control as kindness, so if you resist, you look like the ungrateful one. A coworker rewrites your report and says it. A relative criticizes your life choices and says it. The real message is: I know better than you, and questioning me makes you the bad guy. Notice what happens in your body when you hear it. A little guilt. A little pressure to comply. That feeling is the leash tightening. Here is a real example. Your manager calls on Friday evening. She says the client presentation needs rework, and she is just trying to help you look good. You cancel your weekend. Monday comes, and she presents your reworked slides as her own initiative. When you mention it, she looks hurt. After all, she was just trying to help you. See how it works? The help was real. The control was realer.",
    4: "Number six. You are overthinking this. Four words that delete your instincts. The moment you start noticing the pattern, the manipulator attacks the noticing itself. Your gut says something is wrong. They tell you your gut is broken. Do this three times and you stop trusting your own perception entirely. That is the goal. A person who does not trust their own mind has to borrow someone else's. Guess whose. The correct response is boring and powerful: I trust my read on this. Say it once, then stop explaining. Picture this. You notice your partner hides their phone screen when you walk in. You ask about it calmly. They laugh and say you are overthinking this, that you have been stressed lately. You drop it. Two weeks later you find the messages. The overthinking was actually pattern recognition. Your brain was doing its job.",
    5: "Number five. After everything I have done for you. This is a debt you never agreed to. Every favor becomes a weapon, every kindness becomes a contract you did not sign. Here is the trick. Real generosity does not keep receipts. The manipulator keeps a ledger, and they only show it to you when you try to say no. The guilt you feel is manufactured. You do not owe obedience in exchange for kindness. Kindness with strings attached is not kindness. It is a purchase. Think about the last family gathering. Your uncle paid for your college books five years ago. Now he wants you to hire his unqualified son at your company. You hesitate. He goes quiet, then says it. After everything I have done for you. Suddenly you are not making a hiring decision. You are repaying a debt. Real help never sends an invoice.",
    6: "Number four. Everyone agrees with me. They do not. But your brain does not check. This is social proof weaponized. The phrase borrows an imaginary crowd to make you feel isolated, because isolated people comply faster. In reality, everyone is usually two people, or nobody at all. Next time you hear it, ask one calm question: who specifically? Watch how fast the crowd evaporates. Manipulators hate specifics. Specifics are where vague power goes to die. This one thrives in meetings. Your colleague pitches a terrible idea. You raise a concern. He smiles and says everyone agrees with me on this. The room goes quiet. Nobody wants to be the lone dissenter. So you fold. Later, three people tell you they hated the idea too. Everyone was a fiction. But it worked.",
    7: "Number three. I was just joking. The coward's escape hatch. They say something cruel, watch your reaction, and if you flinch, it was humor. If you laugh, it was a test you passed. Either way, they gathered data and paid nothing. This is called a boundary probe. The joke is a drone flying over your defenses, mapping where the walls are thinnest. People who respect you do not need to disguise cruelty as comedy. Call it plainly: that did not sound like a joke to me. Then watch their face. Here is how it plays out at dinner. Your friend says, in front of everyone, that you would lose your head if it was not attached. Everyone laughs. You force a smile, but it stung. Later you mention it privately. Oh come on, I was just joking, do not be so sensitive. Now you are the problem. Not the insult, your reaction to the insult.",
    8: "Number two. If you really loved me, you would. Love is not a remote control, but this phrase tries to install one. It turns your affection into an obligation with ever-moving goalposts. Today it is skipping your plans. Tomorrow it is cutting off your friend. The target never stops moving, because a finished test cannot be used again. Real love says: I want this, can we talk about it. Manipulation says: prove your love by obeying. One is a request. The other is a ransom note wearing love's clothes. A woman told me her boyfriend used this every week. If you really loved me, you would skip your sister's birthday. She went. If you really loved me, you would stop talking to your best friend. She did. Each time, love was the currency and obedience was the price. Someone who loves you does not make you prove it on demand.",
    9: "Number one. The most powerful phrase on this list. You are the only one who understands me. It feels like the highest compliment you have ever received. That is exactly why it works. This is called forced intimacy. The manipulator hands you a crown made of responsibility. Now you are not just a partner or a friend. You are their therapist, their savior, the one person who cannot leave. Leaving would not just end a relationship. It would be abandonment of someone who trusted only you. See the cage? It is built entirely out of how special they made you feel. This is the favorite tool of the covert narcissist. In the first month, you are perfect. Nobody has ever understood me like you do. By month six, you are their unpaid therapist, absorbing crises at midnight. When you try to pull back, the guilt arrives on schedule. But you are the only one who understands me. The crown has become a collar.",
}
adir = os.path.join(BASE, "long", "audio")
print("=== long expansion: beats 3-9 ===", flush=True)
for i in range(3, 10):
    out = os.path.join(adir, f"beat-{i:03d}.mp3")
    for attempt in range(3):
        if tts_synth(long_expanded[i], out) and dur(out) > 1:
            break
        print(f"  long beat {i}: retry {attempt+2}", flush=True)
    else:
        print(f"GAGAL TTS: long beat {i}"); sys.exit(1)
    print(f"  beat {i}: {dur(out):.1f}s", flush=True)

# rebuild durasi.json + voiceover
durs = {}
for i in range(1, 13):
    durs[f"beat-{i:03d}"] = round(dur(os.path.join(adir, f"beat-{i:03d}.mp3")), 2)
json.dump(durs, open(os.path.join(adir, "durasi.json"), "w"), indent=1)
concat_vo(adir, 12)
total = sum(durs.values())
print(f"  TOTAL long (expanded): {total:.1f}s ({total/60:.2f} mnt)", flush=True)
print("SELESAI PHASE 2")
