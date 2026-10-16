#!/usr/bin/env python3
"""Batch TTS untuk Dark Mind Files fix: long (12 beat) + shorts1 (4 beat) + shorts2 (5 beat)."""
import subprocess, os, json, sys

BASE = "/home/hatch/workspace/youtube-otomatis/mind-en/2026-10-16-fix"
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:miles"

def tts_synth(text, out):
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

VIDEOS = {
    "long": [
        "Someone controlled you this week. And you thanked them for it. That is not an insult. It is how manipulation actually works. The best manipulators never raise their voice. They never make threats. They just say the right sentence at the right moment, and you do exactly what they wanted. Psychologists have identified seven exact phrases manipulators use over and over. Once you hear them, you will recognize them everywhere. Starting with number seven.",
        "Here is the deal. I am going to give you all seven phrases, word for word, plus what each one is really doing to your brain. And at the end, I will show you the one response that shuts every single one of them down. Number seven is the one you hear at work.",
        "Number seven. I am just trying to help you. It sounds caring. That is the point. This phrase reframes control as kindness, so if you resist, you look like the ungrateful one. A coworker rewrites your report and says it. A relative criticizes your life choices and says it. The real message is: I know better than you, and questioning me makes you the bad guy. Notice what happens in your body when you hear it. A little guilt. A little pressure to comply. That feeling is the leash tightening.",
        "Number six. You are overthinking this. Four words that delete your instincts. The moment you start noticing the pattern, the manipulator attacks the noticing itself. Your gut says something is wrong. They tell you your gut is broken. Do this three times and you stop trusting your own perception entirely. That is the goal. A person who does not trust their own mind has to borrow someone else's. Guess whose. The correct response is boring and powerful: I trust my read on this. Say it once, then stop explaining.",
        "Number five. After everything I have done for you. This is a debt you never agreed to. Every favor becomes a weapon, every kindness becomes a contract you did not sign. Here is the trick. Real generosity does not keep receipts. The manipulator keeps a ledger, and they only show it to you when you try to say no. The guilt you feel is manufactured. You do not owe obedience in exchange for kindness. Kindness with strings attached is not kindness. It is a purchase.",
        "Number four. Everyone agrees with me. They do not. But your brain does not check. This is social proof weaponized. The phrase borrows an imaginary crowd to make you feel isolated, because isolated people comply faster. In reality, everyone is usually two people, or nobody at all. Next time you hear it, ask one calm question: who specifically? Watch how fast the crowd evaporates. Manipulators hate specifics. Specifics are where vague power goes to die.",
        "Number three. I was just joking. The coward's escape hatch. They say something cruel, watch your reaction, and if you flinch, it was humor. If you laugh, it was a test you passed. Either way, they gathered data and paid nothing. This is called a boundary probe. The joke is a drone flying over your defenses, mapping where the walls are thinnest. People who respect you do not need to disguise cruelty as comedy. Call it plainly: that did not sound like a joke to me. Then watch their face.",
        "Number two. If you really loved me, you would. Love is not a remote control, but this phrase tries to install one. It turns your affection into an obligation with ever-moving goalposts. Today it is skipping your plans. Tomorrow it is cutting off your friend. The target never stops moving, because a finished test cannot be used again. Real love says: I want this, can we talk about it. Manipulation says: prove your love by obeying. One is a request. The other is a ransom note wearing love's clothes.",
        "Number one. The most powerful phrase on this list. You are the only one who understands me. It feels like the highest compliment you have ever received. That is exactly why it works. This is called forced intimacy. The manipulator hands you a crown made of responsibility. Now you are not just a partner or a friend. You are their therapist, their savior, the one person who cannot leave. Leaving would not just end a relationship. It would be abandonment of someone who trusted only you. See the cage? It is built entirely out of how special they made you feel.",
        "So what do you do when you hear one of these? You use the universal shutdown. It has three steps, and it works on all seven phrases. Step one: name it silently. Just think to yourself: that is phrase number four. Labeling breaks the spell because manipulation needs you confused. Step two: pause. Say: I need to think about that. Manipulators rush you because rushed people do not think. Step three: answer the real message, not the words. When they say after everything I have done for you, you hear: they want obedience. And you reply to that, calmly: I appreciate what you have done, and my answer is still no.",
        "Here is the uncomfortable truth. You will hear at least one of these seven phrases in the next forty-eight hours. Maybe from a boss. Maybe from family. Maybe from someone who genuinely loves you and does not realize they are doing it. Awareness does not make you cynical. It makes you free. The moment you can name the phrase, it stops working on you, and starts working for you. Because now you see the strings.",
        "Which of the seven have you heard most? Comment the number below. And if this opened your eyes, the next video breaks down the six silent tests manipulators run before they ever say a word. You are already being tested. Watch it next.",
    ],
    "shorts1": [
        "You are not crazy. You are being rewritten. Here are five signs someone is gaslighting you.",
        "One. You apologize constantly, even for things you did not do. Two. You rehearse every conversation in your head, because the last ten went sideways no matter what you said.",
        "Three. You stopped trusting your own memory. They deny what happened so often, you now ask them what is real.",
        "Four and five. You feel small around them but cannot explain why, and everyone else thinks they are wonderful. That gap is the proof. Trust it. Walk away.",
    ],
    "shorts2": [
        "Forget body language. Four words expose every liar.",
        "The words are: I. Do not. Remember. Liars almost never say I do not remember.",
        "Because admitting a blank looks guilty to them. So they fill it. They invent details, smooth and confident, where an honest person would just shrug.",
        "Truth-tellers say I forgot all the time. It costs them nothing. Liars cannot afford a single gap, because one gap unravels the whole story.",
        "So next time someone gives you a perfect story with zero gaps, that is your sign. The smoothest story is usually the fakest.",
    ],
}

for vname, beats in VIDEOS.items():
    adir = os.path.join(BASE, vname, "audio")
    os.makedirs(adir, exist_ok=True)
    print(f"=== {vname}: {len(beats)} beats ===", flush=True)
    durs = {}
    for i, txt in enumerate(beats, 1):
        out = os.path.join(adir, f"beat-{i:03d}.mp3")
        if os.path.exists(out) and dur(out) > 1:
            d = dur(out)
            print(f"  beat {i}: cached ({d:.1f}s)", flush=True)
        else:
            ok = False
            for attempt in range(3):
                if tts_synth(txt, out) and dur(out) > 1:
                    ok = True
                    break
                print(f"  beat {i}: retry {attempt+2}", flush=True)
            if not ok:
                print(f"GAGAL TTS: {vname} beat {i}"); sys.exit(1)
            d = dur(out)
            print(f"  beat {i}: {d:.1f}s", flush=True)
        durs[f"beat-{i:03d}"] = round(d, 2)
    # concat voiceover
    lst = os.path.join(adir, "list.txt")
    with open(lst, "w") as f:
        for i in range(1, len(beats) + 1):
            f.write(f"file '{adir}/beat-{i:03d}.mp3'\n")
    vo = os.path.join(adir, "voiceover.mp3")
    subprocess.run(["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh", "-y",
                    "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", vo], capture_output=True, check=True)
    total = sum(durs.values())
    json.dump(durs, open(os.path.join(adir, "durasi.json"), "w"), indent=1)
    print(f"  TOTAL {vname}: {total:.1f}s ({total/60:.1f} mnt)", flush=True)

print("SELESAI SEMUA TTS")
