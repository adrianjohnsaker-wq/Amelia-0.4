"""Stateless Chaquopy JSON boundary; no process-global lineage or clock.
Android owns durable checkpoint storage; persist the returned snapshot atomically.
"""
import json
from drift_core import Substrate, canonical_json, keyed_uniform, verify_canonical


def initialize(start=1):
    verify_canonical()
    return canonical_json(Substrate(start=int(start)).snapshot())


def advance(snapshot_json, randomness_hex, reset=False):
    s = Substrate.restore(json.loads(str(snapshot_json)))
    u = keyed_uniform(str(randomness_hex), s.P['tick'])
    event = s.advance(u, reset=bool(reset))
    return canonical_json(dict(snapshot=s.snapshot(), event=event, anomaly_eligible=False))


def inspect(snapshot_json):
    s = Substrate.restore(json.loads(str(snapshot_json)))
    return canonical_json(s.distribution())
