# DRIFT-1A G1.1: episodic embodiment amendment

Status: offline engineering pilot; not a live experiment registration. G1 remains
unchanged in ../drift1a. G1.1 wraps its byte-identical selector, memory, Governor,
and canonical graph. No metabolism, evolution, language relay, or memory-modulated
ingress is introduced.

## Event order and pairing

Each global tick, for each arm:
1. Derive both ingress and transition variates from the same supplied input using
   separate operation keys and the versioned G1.1 stream. Never include arm IDs
   or episode indices. The offline input tape is synthetic; no beacon is contacted.
2. If initial tick or the prior episode ended, apply uniform entry floor(10*u).
   Record this embodiment event; it costs no tick and adds no graph edge or history.
   Otherwise record the proposed entry as unused. Initial entry is uniform too;
   the UI therefore has no start-zone field.
3. M clears all selector history, including field registers, observations,
   classifier traces, commitment, retention and update counts. C/G retain history.
4. Evaluate legal candidates using prior selector history; sample one graph move
   with the shared transition variate; update history from that move only.
5. End the episode if the destination is in {0,3,6,9}. Otherwise end at 1260 moves
   as a cap termination. Boundary takes precedence at the cap. Enter again on the
   next tick. Starting inside the boundary still requires one legal move.

Every tick contains exactly one graph move per arm. Retention age, commitment decay
and all selector clocks remain global-tick based, never reset at ingress. Episode
index/length and pending-entry flag belong to present embodiment state; they are
not selector history and are not erased in M. No episode fields feed the selector.

Pairing means identical proposed entries and variates on every global tick, with
identical applied entries whenever both arms restart on that tick. It does not
mean identical restart schedules or an episode-index-matched entry sequence:
memory may change termination time. Requiring the latter would change this design.

## Arms and graph interpretation

C: canonical graph plus persistent G1 memory and soft candidate Governor.
G: the accepted G1 directed typed degree-matched rewiring, same memory/Governor.
M: canonical graph with complete history reset before each choice.

The canonical graph has terminal SCCs {0,9} and {3,6}; G has one ten-zone SCC.
The common boundary is structurally terminal only in C/M. It is a label-defined
experimental stopping convention in G. Thus C versus G tests route structure
under common embodiment. Shared rules do NOT guarantee equal episode-length
or entry distributions: their differences are outcomes. Warp/Plex labels in G
identify the boundary destination labels, not terminal components of G.
The current G1 selector's fixed D1 candidate weights are preserved: this wrapper
adopts the interface's terminal-entry convention, not every time-gating detail of
NumogramInterface or amelia_substrate's different memory architecture.

## Fixed descriptive measures

- Completed boundary episodes: Warp destinations {3,6} versus Plex {0,9}; report
  counts and Warp fraction with denominator equal to completed boundary episodes.
  Cap terminations and the final unfinished episode are reported separately.
- Length (number of graph moves), ordered route including entry and destinations,
  and typed edges in the ledger. Report right censoring at the fixed tick horizon.
- Per-source choice counts and numbers where commitment, Governor, and retention
  change their stage's candidate probabilities by more than 1e-12. Also report
  commitment-bias presence and retention activity separately. Governor cost
  differences, memory activation and actual probability changes are distinct.
- Post-move occupancy uses exactly N graph moves as denominator. Ingress is not
  an extra occupancy sample. Boundary occupancy is design-dependent and secondary;
  re-entry does not impose a universal low numerical occupancy cap.

Episode outcomes are history-dependent and episodes are not independent trials.
Different arms need not complete equal numbers of episodes at a common horizon.
No significance test, long-term superiority claim or live forecast schedule is
registered here. A prospective experiment must fix replication and inference.

## Validation and provenance

Core SHA256 checks preserve accepted G1 behavior and canonical source bytes.
Inherited TypeScript parity tests plus G1.1 tests cover legal moves, ordering,
full reset, pairing, boundary/cap semantics, resume and metric denominators.
A frozen 512-tick seed-101 reference contains all event values and final states;
Android compares structural/discrete values and numeric values within 1e-12.
Platform-sensitive state digest strings are omitted only from reference parity.
Saved device evidence retains and verifies every hash, with exact local replay.
Cross-platform audit reports numeric differences rather than claiming byte identity.
A separate package com.amelia.driftg11 installs alongside G1. The next acceptance
step is a physical-device 512-tick run, Verify run, and exported evidence audit.
