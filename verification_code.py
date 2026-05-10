# Counterpoise-corrected CCSD(T) for
# water dimer (cc-pVDZ basis).
from pyscf import gto, scf, cc

GEOM_A = """O -1.551 -0.115 0
            H -1.934  0.763 0
            H -0.600  0.041 0"""
GEOM_B = """O  1.351  0.111 0
            H  1.680 -0.374 -0.759
            H  1.680 -0.374  0.759"""
HARTREE_TO_KCAL = 627.5094740631

def ccsdt_energy(atom_str):
    mol = gto.M(atom=atom_str, basis="cc-pVDZ")
    mf  = scf.RHF(mol).run()
    cc_ = cc.CCSD(mf).run()
    et  = cc_.ccsd_t()
    return mf.e_tot + cc_.e_corr + et

def ghost(atom_str):
    out = []
    for line in atom_str.strip().split("\n"):
        sym, rest = line.split(None, 1)
        out.append(f"GHOST-{sym} {rest}")
    return "\n".join(out)

e_dimer = ccsdt_energy(GEOM_A + "\n" + GEOM_B)
e_A     = ccsdt_energy(GEOM_A + "\n" + ghost(GEOM_B))
e_B     = ccsdt_energy(ghost(GEOM_A) + "\n" + GEOM_B)
e_int_kcal = (e_dimer - e_A - e_B) * HARTREE_TO_KCAL
print(f"{e_int_kcal:.4f}")
