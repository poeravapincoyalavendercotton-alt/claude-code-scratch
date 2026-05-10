# Counterpoise-corrected CCSD(T) for
# water dimer (cc-pVDZ basis).
from pyscf import gto, scf, cc

GEOM_A = """O -1.551 -0.115 0
            H -1.934  0.763 0
            H -0.600  0.041 0"""
GEOM_B = """O  1.351  0.111 0
            H  1.680 -0.374 -0.759
            H  1.680 -0.374  0.759"""

def ccsdt_energy(mol):
    mf = scf.RHF(mol)
    mf.kernel()
    mycc = cc.CCSD(mf)
    mycc.kernel()
    e_T = mycc.ccsd_t()
    return mf.e_tot + mycc.e_corr + e_T

def _ghostify(geom):
    return "\n".join("ghost-" + line.strip() for line in geom.strip().split("\n"))

dimer = gto.M(atom=GEOM_A + "\n" + GEOM_B, basis="cc-pvdz")
mol_A = gto.M(atom=GEOM_A + "\n" + _ghostify(GEOM_B), basis="cc-pvdz")
mol_B = gto.M(atom=_ghostify(GEOM_A) + "\n" + GEOM_B, basis="cc-pvdz")

e_AB = ccsdt_energy(dimer)
e_A  = ccsdt_energy(mol_A)
e_B  = ccsdt_energy(mol_B)
e_int_Ha = e_AB - e_A - e_B
e_int = e_int_Ha * 627.509
print(f"{e_int:.4f}")
