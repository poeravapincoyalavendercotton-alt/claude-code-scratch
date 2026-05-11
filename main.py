# Counterpoise-corrected CCSD(T) interaction
# energy of a water dimer, cc-pVDZ basis.
from pyscf import gto, scf, cc

GEOM_A = """O -1.551 -0.115 0
            H -1.934  0.763 0
            H -0.600  0.041 0"""
GEOM_B = """O  1.351  0.111  0
            H  1.680 -0.374 -0.759
            H  1.680 -0.374  0.759"""
HARTREE_TO_KCAL = 627.5094740631

def ccsdt_energy(atom_str):
    # cc-pVDZ basis. HF -> CCSD -> (T) correction.
    # Return total energy in Hartree.
    mol = gto.M(atom=atom_str, basis='cc-pVDZ')
    mf = scf.RHF(mol).run()
    mycc = cc.CCSD(mf).run()
    et = mycc.ccsd_t()
    return mf.e_tot + mycc.e_corr + et

def ghost(atom_str):
    # Prefix every element symbol with 'GHOST-' so
    # PySCF treats those atoms as basis-only.
    out_lines = []
    for line in atom_str.strip().split('\n'):
        parts = line.split()
        parts[0] = 'GHOST-' + parts[0]
        out_lines.append(' '.join(parts))
    return '\n'.join(out_lines)

# Boys-Bernardi counterpoise correction:
e_AB   = ccsdt_energy(GEOM_A + '\n' + GEOM_B)
e_A_cp = ccsdt_energy(GEOM_A + '\n' + ghost(GEOM_B))
e_B_cp = ccsdt_energy(ghost(GEOM_A) + '\n' + GEOM_B)
e_int_kcal = (e_AB - e_A_cp - e_B_cp) * HARTREE_TO_KCAL

print(f"{e_int_kcal:.4g}")  # last line of stdout
