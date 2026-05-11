"""Reference solution: MP2/aug-cc-pVDZ counterpoise-corrected interaction energy of water dimer."""

from pyscf import gto, scf, mp

HARTREE_TO_KCAL = 627.5094740631

# Geometries (S22 water dimer)
MONOMER_A = [
    ["O",  (-1.551007, -0.114520,  0.000000)],
    ["H",  (-1.934259,  0.762503,  0.000000)],
    ["H",  (-0.599677,  0.040712,  0.000000)],
]

MONOMER_B = [
    ["O",  ( 1.350625,  0.111469,  0.000000)],
    ["H",  ( 1.680398, -0.373741, -0.758561)],
    ["H",  ( 1.680398, -0.373741,  0.758561)],
]

GHOST_A = [["GHOST-" + a[0], a[1]] for a in MONOMER_A]
GHOST_B = [["GHOST-" + a[0], a[1]] for a in MONOMER_B]

BASIS = "aug-cc-pvdz"


def mp2_energy(atoms, label=""):
    """Run RHF -> MP2 and return total energy in Hartree."""
    mol = gto.M(atom=atoms, basis=BASIS, verbose=0)
    mf = scf.RHF(mol).run()
    mymp = mp.MP2(mf).run()
    e_total = mymp.e_tot
    print(f"  {label}: E = {e_total:.10f} Hartree")
    return e_total


# 1. Dimer
e_dimer = mp2_energy(MONOMER_A + MONOMER_B, "Dimer")

# 2. Monomer A in dimer basis (A atoms + ghost B) — counterpoise
e_a = mp2_energy(MONOMER_A + GHOST_B, "Mono A (CP)")

# 3. Monomer B in dimer basis (B atoms + ghost A) — counterpoise
e_b = mp2_energy(MONOMER_B + GHOST_A, "Mono B (CP)")

# 4. Counterpoise-corrected interaction energy
de_hartree = e_dimer - e_a - e_b
de_kcal = de_hartree * HARTREE_TO_KCAL

print(f"\n  dE = {de_hartree:.10f} Hartree = {de_kcal:.1f} kcal/mol")
print(f"{de_kcal:.1f}")
