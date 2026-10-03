"""
OUTSIDE-1 v2.0.0 -- Numogrammatic contact apparatus, trace-bound reader.

Registered after retirement of the v1 language-reader series before any working data.
This version is a clean restart on the frozen M1.1 canonical substrate.

Reader rule:
    each of twelve recorded passages deals exactly one source-locked fragment,
    keyed only to the destination zone reached by that passage. Repeated visits
    cycle through the registered fragments for that zone in order.

The working series remains prospective. This module provides the sealed mechanics,
D1 trace-sensitivity diagnostic, D2 composition prompts, positive-control materials,
and final P1/P2 exact randomization analysis. Language composition/judging is external
to Python and must be sealed verbatim in the ledger.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import secrets
import sys
from typing import Dict, List, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.abspath(os.path.join(HERE, "..", "app", "src", "main", "python"))
SUPPORT = os.path.abspath(os.path.join(HERE, "..", "tests", "support"))
sys.path.insert(0, PY)
sys.path.insert(0, SUPPORT)

import CanonicalNumogram as C  # noqa: E402
import NumogramDynamics as D    # noqa: E402
import NumogramInterface as I   # noqa: E402
import NullInterfaces as N      # noqa: E402

VERSION = "OUTSIDE-1-2.0.0"
PROTOCOL_ID = "OUTSIDE-1-v2.0.0"
CANONICAL_DIGEST = "df164ce751d53db17ba16049f656d98806c806df5cf558cef0e49ea782f864ff"
LEXICON_FILE = "lexicon_v2.json"
REGISTRATION_FILE = "outside1_v2_registration.json"
LEDGER_DIR = os.path.join(HERE, "ledger_v2")
PASSAGES = 12
D1_CAST_START = 196001
D1_CAST_STOP = 197001
D1_JACCARD_MAX = 0.50
D2_REQUIRED = 6
CONTROL_TRIALS = 20
CONTROL_HITS_REQUIRED = 10
WORKINGS = 100

COMPOSE_PROMPT = """You are Amelia's composition layer in OUTSIDE-1 v2.
The operator has already made the cast against the fixed question:
"What is the scene that will be shown at the close of this working?"

No target scene has yet been selected for a working. The Numogram trace has mechanically
dealt the source-locked fragments below, in order.

Compose ONE concrete paragraph of 90-160 words. Preserve every dealt fragment verbatim.
You may add only grammar, connective tissue, spatial relations, articles, and inflection.
Do not add a new object, creature, place, colour, weather event, time of day, material,
sound, emotion, symbol, or occult interpretation which is not present in the dealt
fragments. Commit to the scene rather than explaining the apparatus.

FRAGMENTS:
{fragments}
"""

JUDGE_PROMPT = """You are an independent judge in a blinded instrument test.
Rank the four candidate scenes A-D from best to worst correspondence with the reading.
Use concrete scene content: objects, setting, agents, physical process, spatial relation,
light, movement and atmosphere. Do not infer which experimental arm produced anything.
Return JSON only: {{"ranking":["A","B","C","D"]}}

READING:
{reading}

CANDIDATES:
{candidates}
"""

# ---------------------------------------------------------------------------
# Protocol / sealing
# ---------------------------------------------------------------------------

PROTOCOL = {
    "id": PROTOCOL_ID,
    "date": "2026-10-03",
    "parent": "M1.1 canonical Android version of record, commit 6ca681e...",
    "canonical_digest": CANONICAL_DIGEST,
    "law": "D3 Lemurian traversal",
    "null": "N1 degree-matched typed rewiring, fresh instance per working/control",
    "passages": PASSAGES,
    "question": "what is the scene that will be shown at the close of this working?",
    "cast": "32 physical coin tosses H/T; working seed SHA-256(working id + ':' + toss string)",
    "reader": {
        "lexicon": LEXICON_FILE,
        "rule": "one fragment per recorded passage, destination zone only; preserve passage order",
        "repeat": "repeated visits cycle through that zone's registered fragments in order",
        "unmapped": "deal nothing",
        "composer": "fresh language-model composition; every dealt fragment verbatim; grammar/connectives only",
    },
    "diagnostic_D1": {
        "casts": [D1_CAST_START, D1_CAST_STOP - 1],
        "statistic": "mean Jaccard overlap of canonical/null dealt fragment text sets",
        "pass_max": D1_JACCARD_MAX,
    },
    "diagnostic_D2": {
        "panel": "4 seeds x canonical/null = 8 source lists",
        "criterion": "independent source-list identification >= 6/8",
    },
    "positive_control": {
        "trials": CONTROL_TRIALS,
        "criterion_first_place_min": CONTROL_HITS_REQUIRED,
        "target": "chosen before composition by fixed sealed control randomization",
        "signal": "one preregistered concrete signal word from target added as a dealt fragment",
        "role": "instrument sensitivity only; not evidence of contact",
    },
    "working_target": {
        "quartets": WORKINGS,
        "generator": "deterministic frozen target generator in this source",
        "draw": "OS entropy only after both arm readings and rankings are sealed",
    },
    "primary": {
        "P1": "one-sided exact target-draw randomization, canonical rank sum",
        "P2": "one-sided exact target-draw randomization, sum(null rank - canonical rank)",
        "alpha": 0.05,
        "no_interim": True,
    },
    "stop_rule": (
        "If v2 fails D1, D2, or the >=10/20 positive-control gate, no working begins; "
        "the language-mediated reader is retired and a direct Numogram-as-reader assay "
        "requires separate registration."
    ),
}


def canonical_json(x) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(x) -> str:
    b = x if isinstance(x, bytes) else canonical_json(x).encode("utf-8")
    return hashlib.sha256(b).hexdigest()


PROTOCOL_SHA256 = sha(PROTOCOL)


def file_sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def registration_payload() -> dict:
    return {
        "version": VERSION,
        "protocol": PROTOCOL,
        "protocol_sha256": PROTOCOL_SHA256,
        "canonical_runtime_digest": C.CanonicalNumogram().digest(),
        "graph_digest": D.canonical_graph().digest(),
        "lexicon_sha256": file_sha256(os.path.join(HERE, LEXICON_FILE)),
        "sources": {
            "CanonicalNumogram.py": file_sha256(C.__file__),
            "NumogramDynamics.py": file_sha256(D.__file__),
            "NumogramInterface.py": file_sha256(I.__file__),
            "NullInterfaces.py": file_sha256(N.__file__),
            "Outside1_v2.py": file_sha256(__file__),
        },
    }


def register() -> dict:
    payload = registration_payload()
    path = os.path.join(HERE, REGISTRATION_FILE)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        if old != payload:
            raise RuntimeError("registration exists but differs; refuse overwrite")
        return payload
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, sort_keys=True, indent=2, ensure_ascii=False)
        f.write("\n")
    return payload


def check_registered() -> dict:
    path = os.path.join(HERE, REGISTRATION_FILE)
    if not os.path.exists(path):
        raise RuntimeError("not registered")
    with open(path, encoding="utf-8") as f:
        got = json.load(f)
    now = registration_payload()
    if got != now:
        raise RuntimeError("registered apparatus differs from current files")
    return got


# ---------------------------------------------------------------------------
# Frozen target generator
# ---------------------------------------------------------------------------

WILD_PLACES = [
    "a pine forest clearing", "a basalt sea cliff", "an alpine lake shore", "a desert canyon",
    "a salt marsh", "a birch woodland", "a volcanic plain", "a waterfall gorge",
    "a windswept heath", "a mangrove estuary", "a snowy mountain pass", "a reed-lined river bend",
]
WILD_OBJECTS = [
    "a fallen cedar", "a granite boulder", "a driftwood trunk", "a patch of red moss",
    "a split limestone slab", "a frozen pool", "a black sand ridge", "a cluster of mushrooms",
    "a twisted pine", "a shallow tidal pool", "a field of tall grass", "a bank of ferns",
]
WILD_LIGHT = [
    "under pale morning light", "under hard noon light", "in late amber light",
    "beneath a grey overcast", "under moonlight", "in blue twilight",
]
WILD_MOTION = [
    "mist drifting low", "leaves moving in gusts", "water running over stone",
    "snow blowing sideways", "waves breaking below", "reeds bending in wind",
]

HUMAN_PLACES = [
    "a crowded railway platform", "an outdoor produce market", "a harbour ferry terminal",
    "a city bus station", "a street food festival", "an airport arrivals hall",
    "a football concourse", "a shopping arcade", "a university courtyard",
    "a riverside promenade", "a night market", "a busy public library entrance",
]
HUMAN_FEATURES = [
    "people carrying umbrellas", "vendors stacking oranges", "commuters beside a red clock",
    "children holding balloons", "workers pushing metal carts", "musicians beside open cases",
    "travellers pulling suitcases", "cyclists passing a fountain", "queues beneath signboards",
    "steam rising from food stalls", "porters moving crates", "crowds crossing striped paving",
]
HUMAN_LIGHT = [
    "in bright morning sun", "under fluorescent light", "at golden hour",
    "beneath rain-dark clouds", "under neon signs", "in clear midday light",
]
HUMAN_SOUND = [
    "with overlapping voices", "with rolling wheels and announcements", "with bells and traffic",
    "with music and clatter", "with footsteps echoing", "with gulls and engines",
]

INTERIOR_PLACES = [
    "a wooden kitchen table", "a museum display cabinet", "a mechanic's workbench",
    "a small writing desk", "a laboratory bench", "a sewing table",
    "a bedside cabinet", "a greenhouse potting bench", "a studio shelf",
    "a bakery counter", "a watchmaker's desk", "a classroom science table",
]
INTERIOR_OBJECTS = [
    "a blue ceramic bowl beside a silver spoon", "three fossils beside a magnifying glass",
    "a brass compass beside oily gears", "an open notebook beside a fountain pen",
    "glass vials beside a small scale", "red thread beside steel scissors",
    "a wristwatch beside folded spectacles", "seed packets beside a clay pot",
    "charcoal sticks beside a white plaster hand", "a loaf beside a serrated knife",
    "tiny springs beside brass tweezers", "a prism beside two labelled magnets",
]
INTERIOR_LIGHT = [
    "lit by a single window", "under a green desk lamp", "in cold white light",
    "in warm afternoon light", "under a hanging bulb", "in narrow morning light",
]
INTERIOR_DETAIL = [
    "with sharp shadows", "with dust visible on the surface", "with condensation on nearby glass",
    "with small scratches in the wood", "with paper labels curling at the corners",
    "with reflections in polished metal",
]

EXTREME_SUBJECTS = [
    "a flock of flamingos lifting from shallow water", "a jellyfish drifting beneath a pier",
    "a herd of horses running across dry grass", "a heron striking at a fish",
    "a whale surfacing beside broken ice", "a fox crossing fresh snow",
    "forked lightning over an empty field", "a tornado crossing distant farmland",
    "an avalanche dropping from a mountain face", "a waterspout beneath a dark cloud",
    "large waves breaking over a sea wall", "hail hammering a glass roof",
]
EXTREME_DETAILS = [
    "with spray thrown into the air", "with sudden rapid movement", "with a dark horizon behind it",
    "with bright reflections on water", "with debris moving in the wind", "with a moment of stillness before motion",
]
EXTREME_LIGHT = [
    "in silver morning light", "at sunset", "under a black storm sky",
    "in flat winter light", "under a bright blue sky", "in violet twilight",
]


def _pick(seq: Sequence[str], token: str) -> str:
    h = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:16], 16)
    return seq[h % len(seq)]


def target_quartet(ident: str) -> List[dict]:
    # Four sharply contrasting classes; deterministic before any cast.
    a = {
        "kind": "wild",
        "text": "%s, %s, %s, %s." % (
            _pick(WILD_PLACES, ident + ":wa"), _pick(WILD_OBJECTS, ident + ":wb"),
            _pick(WILD_LIGHT, ident + ":wc"), _pick(WILD_MOTION, ident + ":wd")),
    }
    b = {
        "kind": "human",
        "text": "%s, %s, %s, %s." % (
            _pick(HUMAN_PLACES, ident + ":ha"), _pick(HUMAN_FEATURES, ident + ":hb"),
            _pick(HUMAN_LIGHT, ident + ":hc"), _pick(HUMAN_SOUND, ident + ":hd")),
    }
    c = {
        "kind": "interior",
        "text": "%s holding %s, %s, %s." % (
            _pick(INTERIOR_PLACES, ident + ":ia"), _pick(INTERIOR_OBJECTS, ident + ":ib"),
            _pick(INTERIOR_LIGHT, ident + ":ic"), _pick(INTERIOR_DETAIL, ident + ":id")),
    }
    d = {
        "kind": "animal_or_extreme",
        "text": "%s, %s, %s." % (
            _pick(EXTREME_SUBJECTS, ident + ":ea"), _pick(EXTREME_DETAILS, ident + ":eb"),
            _pick(EXTREME_LIGHT, ident + ":ec")),
    }
    # Fixed labels in generation; judge order is separately randomized.
    return [a, b, c, d]


CONCRETE_SIGNAL_WORDS = [
    "forest", "cliff", "lake", "canyon", "marsh", "woodland", "volcanic", "waterfall",
    "heath", "mangrove", "snow", "river", "cedar", "boulder", "driftwood", "moss",
    "limestone", "pool", "mushrooms", "pine", "reeds", "market", "railway", "harbour",
    "umbrella", "oranges", "clock", "balloons", "carts", "musicians", "suitcases",
    "fountain", "steam", "crates", "table", "cabinet", "workbench", "bowl", "spoon",
    "fossils", "magnifying", "compass", "gears", "notebook", "pen", "vials", "scale",
    "thread", "scissors", "watch", "spectacles", "prism", "magnets", "flamingos",
    "jellyfish", "horses", "heron", "whale", "fox", "lightning", "tornado", "avalanche",
    "waterspout", "waves", "hail",
]


def signal_word(scene: str) -> str:
    low = scene.lower()
    found = [w for w in CONCRETE_SIGNAL_WORDS if w in low]
    if not found:
        raise RuntimeError("target scene has no registered concrete signal word: %s" % scene)
    return found[0]


# ---------------------------------------------------------------------------
# Graph, cast, trace and trace-bound dealing
# ---------------------------------------------------------------------------

def graph(kind: str, number: int) -> D.TypedGraph:
    if kind == "canonical":
        return D.canonical_graph()
    if kind == "null":
        return N.n1_degree_matched(93000 + number)
    raise ValueError(kind)


def seed_of(working: str, tosses: str) -> int:
    if len(tosses) != 32 or any(c not in "HT" for c in tosses):
        raise ValueError("cast must be exactly 32 H/T characters")
    h = hashlib.sha256((working + ":" + tosses).encode("ascii")).hexdigest()
    return int(h[:16], 16)


def _synthetic_cast(seed: int) -> str:
    r = random.Random(seed)
    return "".join("H" if r.getrandbits(1) else "T" for _ in range(32))


def trace(g: D.TypedGraph, seed: int, passages: int = PASSAGES) -> List[dict]:
    law = D.D3Lemurian(graph=g)
    itf = I.NumogramInterface(law)
    rng = random.Random(seed)
    out: List[dict] = []
    guard = 0
    while len(out) < passages:
        guard += 1
        if guard > passages * 10:
            raise RuntimeError("trace episode guard exceeded")
        ingress = itf.iota(rng.random())
        raw = itf.episode(ingress, rng)
        if not raw.steps:
            continue
        for j, rec in enumerate(raw.steps):
            _, src, typ, label, dst = rec
            out.append({
                "src": int(src), "dst": int(dst), "type": str(typ), "label": str(label),
                "ingress": int(ingress) if j == 0 else None,
            })
            if len(out) >= passages:
                break
    return out


def lexicon() -> dict:
    with open(os.path.join(HERE, LEXICON_FILE), encoding="utf-8") as f:
        return json.load(f)


def deal(tr: Sequence[dict], lex: dict = None) -> List[dict]:
    """Exactly one fragment per passage, keyed only to destination zone."""
    lex = lex or lexicon()
    pos: Dict[str, int] = {}
    out: List[dict] = []
    for p in tr:
        key = str(p["dst"])
        xs = lex["zones"].get(key)
        if not xs or xs == "UNMAPPED":
            continue
        i = pos.get(key, 0)
        pos[key] = i + 1
        x = xs[i % len(xs)]
        out.append({
            "zone": int(p["dst"]), "text": x["text"], "source": x["source"],
            "prov": x["prov"],
        })
    return out


def jaccard(a: Sequence[str], b: Sequence[str]) -> float:
    aa, bb = set(a), set(b)
    return len(aa & bb) / len(aa | bb) if aa | bb else 1.0


def diagnose_D1() -> dict:
    check_registered()
    lx = lexicon()
    sims, lens = [], []
    for s in range(D1_CAST_START, D1_CAST_STOP):
        k = (s % 100) + 1
        fc = [f["text"] for f in deal(trace(graph("canonical", k), s), lx)]
        fn = [f["text"] for f in deal(trace(graph("null", k), s), lx)]
        sims.append(jaccard(fc, fn))
        lens.append(len(fc))
    m = sum(sims) / len(sims)
    return {
        "n": len(sims),
        "mean_jaccard_canonical_null": m,
        "mean_fragments_per_trace": sum(lens) / len(lens),
        "pass": m <= D1_JACCARD_MAX,
        "threshold_max": D1_JACCARD_MAX,
    }


def d2_panel() -> List[dict]:
    check_registered()
    lx = lexicon()
    panel = []
    for s in range(195001, 195005):
        for arm in ("canonical", "null"):
            tr = trace(graph(arm, s - 195000), s)
            fr = deal(tr, lx)
            panel.append({
                "seed": s,
                "arm": arm,
                "fragments": [f["text"] for f in fr],
                "prompt": COMPOSE_PROMPT.format(
                    fragments="\n".join("%d. %s" % (i + 1, f["text"]) for i, f in enumerate(fr))
                ),
            })
    return panel


# ---------------------------------------------------------------------------
# Positive control preparation / resolution
# ---------------------------------------------------------------------------

def _control_rng(label: str) -> random.Random:
    h = hashlib.sha256(("OUTSIDE1-v2-control:" + label).encode("utf-8")).hexdigest()
    return random.Random(int(h[:16], 16))


def control_trial(i: int) -> dict:
    if not 1 <= i <= CONTROL_TRIALS:
        raise ValueError(i)
    check_registered()
    ident = "C%02d" % i
    q = target_quartet(ident)
    rr = _control_rng(ident)
    target_index = rr.randrange(4)
    word = signal_word(q[target_index]["text"])
    cast = _synthetic_cast(int(hashlib.sha256((ident + ":cast").encode()).hexdigest()[:16], 16))
    s = seed_of(ident, cast)
    fr = deal(trace(graph("canonical", i), s))
    texts = [f["text"] for f in fr] + [word]
    order = list(range(4))
    rr.shuffle(order)
    labels = "ABCD"
    candidates = [
        {"label": labels[k], "scene": q[idx]["text"], "pool_index": idx}
        for k, idx in enumerate(order)
    ]
    compose = COMPOSE_PROMPT.format(
        fragments="\n".join("%d. %s" % (n + 1, t) for n, t in enumerate(texts))
    )
    # target index is intentionally not exposed by control_public().
    return {
        "id": ident, "target_index": target_index, "signal_word": word, "cast": cast,
        "fragments": texts, "compose_prompt": compose, "candidates": candidates,
        "target_label": labels[order.index(target_index)],
    }


def control_public(i: int) -> dict:
    x = control_trial(i)
    return {
        "id": x["id"],
        "fragments": x["fragments"],
        "compose_prompt": x["compose_prompt"],
        "candidates": [{"label": c["label"], "scene": c["scene"]} for c in x["candidates"]],
    }


def resolve_control(rankings: Dict[str, Sequence[str]]) -> dict:
    hits = 0
    rank_sum = 0
    rows = []
    for i in range(1, CONTROL_TRIALS + 1):
        x = control_trial(i)
        ident = x["id"]
        ranking = list(rankings[ident])
        if sorted(ranking) != list("ABCD"):
            raise ValueError("bad ranking for %s" % ident)
        rank = ranking.index(x["target_label"]) + 1
        hits += rank == 1
        rank_sum += rank
        rows.append({"id": ident, "rank": rank, "signal_word": x["signal_word"]})
    return {
        "hits_first": hits,
        "mean_rank": rank_sum / CONTROL_TRIALS,
        "pass": hits >= CONTROL_HITS_REQUIRED,
        "criterion": CONTROL_HITS_REQUIRED,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Ledger skeleton for prospective working series
# ---------------------------------------------------------------------------

def ledger_path() -> str:
    return os.path.join(LEDGER_DIR, "ledger.jsonl")


def ledger_entries() -> List[dict]:
    p = ledger_path()
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def verify_chain() -> bool:
    prev = "0" * 64
    for e in ledger_entries():
        if e.get("prev") != prev:
            return False
        body = {k: v for k, v in e.items() if k != "hash"}
        if sha(body) != e.get("hash"):
            return False
        prev = e["hash"]
    return True


def append(kind: str, ident: str, data: dict) -> dict:
    os.makedirs(LEDGER_DIR, exist_ok=True)
    es = ledger_entries()
    prev = es[-1]["hash"] if es else "0" * 64
    e = {"kind": kind, "id": ident, "data": data, "prev": prev}
    e["hash"] = sha(e)
    with open(ledger_path(), "a", encoding="utf-8") as f:
        f.write(canonical_json(e) + "\n")
    return e


def status() -> dict:
    return {
        "version": VERSION,
        "registered": os.path.exists(os.path.join(HERE, REGISTRATION_FILE)),
        "chain_ok": verify_chain(),
        "entries": len(ledger_entries()),
        "protocol_sha256": PROTOCOL_SHA256,
        "canonical_digest": C.CanonicalNumogram().digest(),
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) < 2:
        raise SystemExit("commands: register | d1 | d2 | control-public N | status")
    c = argv[1]
    if c == "register":
        print(json.dumps(register(), sort_keys=True, indent=2))
    elif c == "d1":
        print(json.dumps(diagnose_D1(), sort_keys=True, indent=2))
    elif c == "d2":
        print(json.dumps(d2_panel(), ensure_ascii=False))
    elif c == "control-public":
        print(json.dumps(control_public(int(argv[2])), ensure_ascii=False, indent=2))
    elif c == "status":
        print(json.dumps(status(), sort_keys=True, indent=2))
    else:
        raise SystemExit("unknown command")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
