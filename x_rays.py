from dataclasses import dataclass

shell_names = "KLMN"
orbitals = "spdfg"

# orbital_J_values[x] indicates the l and J values for the orbital position x
orbital_J_values = [
    (orbital, J) if J > 0 else None
    for orbital_idx, orbital in enumerate(orbitals)
    for offset in [-1 / 2, 1 / 2]
    for J in [orbital_idx + offset]
]


class NotationClass:
    """
    wrapper class for classes whose purpose is to provide a python interface for some sort of notation
    """

    @classmethod
    def latex_format_iupac(cls, iupac_str):
        """
        take the unformatted IUPAC string and use LaTeX to properly display it
        """
        return cls.parse_iupac(iupac_str).to_iupac_str(latex=True)


@dataclass(frozen=True)
class ElectronPos(NotationClass):
    """
    class to store the position of an electron in an atom
    """

    N: int
    orbital: str
    J: float

    @classmethod
    def parse_iupac(cls, pos_str, skip_rest=True):
        shell_name = pos_str[0]
        N = shell_names.index(shell_name.upper()) + 1
        if len(pos_str) > 1 and pos_str[1].isdecimal():
            orbital_J_id = int(pos_str[1])
            pos_str = pos_str[2:]
        else:
            orbital_J_id = 1
            pos_str = pos_str[1:]
        orbital, J = orbital_J_values[orbital_J_id]
        if skip_rest:
            return cls(N, orbital, J)
        else:
            return cls(N, orbital, J), pos_str

    def to_iupac_str(self, latex=True):
        orbital_J_id = orbital_J_values.index((self.orbital, self.J))
        shell_name = shell_names[self.N - 1]
        return shell_name + (
            ("_" if latex else "") + str(orbital_J_id)
            if orbital_J_id != 1
            else ""
        )


@dataclass(frozen=True)
class Decay(NotationClass):
    """
    class to store the start and end positions of an electron decay
    """

    start: ElectronPos
    end: ElectronPos

    @classmethod
    def parse_iupac(cls, decay_str, skip_rest=True):
        end, decay_str = ElectronPos.parse_iupac(decay_str, skip_rest=False)
        start, rest = ElectronPos.parse_iupac(decay_str, skip_rest=False)
        if skip_rest:
            return cls(start, end)
        else:
            return cls(start, end), rest

    def to_iupac_str(self, latex=True):
        return ElectronPos.to_iupac_str(
            self.end, latex
        ) + ElectronPos.to_iupac_str(self.start, latex)
