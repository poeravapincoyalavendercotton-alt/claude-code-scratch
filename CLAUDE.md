# How I work with Claude Code

Tell me first: is this a FORWARD or INVERSE task?
  Forward → I'll give you ONE skeleton: main.py. 
  Inverse → I'll give you TWO skeletons: main.py + oracle.py.

I write skeletons that contain the science (method, equations,
algorithm, parameters). You fill function bodies and stubs.

# Always
- Print the answer as the LAST line of stdout.
- Don't add constants, imports, helpers, or functions I didn't write.
- Don't refactor my structure or rename anything.
- If a comment is missing a formula or step, STOP and ask me. Never invent equations, defaults, or algorithms.

# Inverse tasks only  (when there's an oracle.py)
- main.py must call oracle.handle_query() - never reference oracle's hidden constants directly.
- Oracles are deterministic: same parameters → same return values.
- The simulation lives in oracle.py, not main.py.

# Forward tasks only  (no oracle)
- The full simulation runs inside main.py.
- No handle_query, no hidden values - every parameter is in the skeleton.
