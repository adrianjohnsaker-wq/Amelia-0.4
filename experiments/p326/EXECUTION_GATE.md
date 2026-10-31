# P3.26 execution gate

P3.26 registration is sealed at commit 26593461d370d7f02df381ca2dc670ba2bb356a0. The user authorized execution on 31 October 2026.

The workflow is push-triggered only on the dedicated P3.26 branch. It verifies the registration ancestor, frozen P3.16/P3.17 source hashes, field packet mapping, temporary flux restoration, and degree-preserving rewires before querying drand. Beacon selection begins no earlier than 90 seconds after the sealed registration commit. A post-acquisition failure is preserved and cannot be silently rerun under this registration.
