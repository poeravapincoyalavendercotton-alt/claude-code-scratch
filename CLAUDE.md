# How I work with Claude Code

I write skeletons that already contain the science (equations,
algorithm, parameters). You only fill mechanical stubs.
Outputs: verification_code.py and oracle.py.

# Code rules
- Print the answer as the LAST line of stdout.
- verification_code.py must call oracle.handle_query() — never read
  oracle's hidden constants directly.
- Oracles are deterministic — same params -> same return values.

# Don't
- Don't add constants, imports, helpers, or functions I didn't write.
- Don't refactor my structure or rename anything.
- Don't decide the science. If a comment is missing a formula or step,
  STOP and ask me — never invent equations, defaults, or algorithms.
