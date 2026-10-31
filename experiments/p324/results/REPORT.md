# P3.24 — Histogram-Balanced Independent-Order Relational Transduction Result

- histogram-balanced order transduction: **FAIL**
- canonical A→A accuracy: 0.052951
- canonical B→B accuracy: 0.048611
- chance accuracy: 0.041667
- A exact chance p: 0.036289568
- B exact chance p: 0.13525002
- best rewire A→A: 0.097222
- best rewire B→B: 0.098958
- A rank p: 0.680000
- B rank p: 0.920000
- A→B cross-encoding accuracy: 0.043403
- B→A cross-encoding accuracy: 0.044271
- A self-minus-cross mean: 0.009549, p=0.24935501
- B self-minus-cross mean: 0.004340, p=0.49833003

## Developmental contribution

- pooled FULL within-encoding accuracy: 0.050781
- pooled BLANK within-encoding accuracy: 0.051649
- mean paired window difference: -0.000868
- paired p: 0.51276974
- developmental contribution: **FAIL**

## Interpretation

P3.24 does not satisfy the full registered histogram-balanced order-transduction gate. Neither balanced temporal encoding carries above-chance held-out beacon-window information. Canonical identification is not uniquely above all rewired controls across both encodings. The paired cross-encoding tests do not establish robust encoding-specific temporal-order fingerprints. Mature development does not satisfy the registered positive contribution gate.
