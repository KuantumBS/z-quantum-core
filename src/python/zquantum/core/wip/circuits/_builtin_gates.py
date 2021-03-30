from typing import Callable, Union, Optional

from . import _gates
from . import _matrices


GatePrototype = Callable[..., _gates.MatrixFactoryGate]
GateRef = Union[_gates.Gate, GatePrototype]


def make_parametric_gate_prototype(name, matrix_factory, num_qubits) -> GatePrototype:
    def _factory(*gate_parameters):
        # TODO: check if len(gate_parameters) == len(arguments of matrix_factory)
        return _gates.MatrixFactoryGate(
            name, matrix_factory, gate_parameters, num_qubits
        )

    return _factory


def builtin_gate_by_name(name) -> Optional[GateRef]:
    return globals().get(name)


# --- non-parametric, single qubit gates ---

X = _gates.MatrixFactoryGate("X", _matrices.x_matrix, (), 1, is_hermitian=True)
Y = _gates.MatrixFactoryGate("Y", _matrices.y_matrix, (), 1, is_hermitian=True)
Z = _gates.MatrixFactoryGate("Z", _matrices.z_matrix, (), 1, is_hermitian=True)
H = _gates.MatrixFactoryGate("H", _matrices.h_matrix, (), 1, is_hermitian=True)
I = _gates.MatrixFactoryGate("I", _matrices.i_matrix, (), 1, is_hermitian=True)
S = _gates.MatrixFactoryGate("S", _matrices.s_matrix, (), 1)
T = _gates.MatrixFactoryGate("T", _matrices.t_matrix, (), 1)


# --- parametric, single qubit gates ---


RX = make_parametric_gate_prototype("RX", _matrices.rx_matrix, 1)
RY = make_parametric_gate_prototype("RY", _matrices.ry_matrix, 1)
RZ = make_parametric_gate_prototype("RZ", _matrices.rz_matrix, 1)
PHASE = make_parametric_gate_prototype("PHASE", _matrices.phase_matrix, 1)


# --- non-parametric, two qubit gates ---

CNOT = _gates.MatrixFactoryGate("CNOT", _matrices.cnot_matrix, (), 2, is_hermitian=True)
CZ = _gates.MatrixFactoryGate("CZ", _matrices.cz_matrix, (), 2, is_hermitian=True)
SWAP = _gates.MatrixFactoryGate("SWAP", _matrices.swap_matrix, (), 2, is_hermitian=True)
ISWAP = _gates.MatrixFactoryGate("ISWAP", _matrices.iswap_matrix, (), 2)


# --- parametric, two qubit gates ---

CPHASE = make_parametric_gate_prototype("CPHASE", _matrices.cphase_matrix, 2)
XX = make_parametric_gate_prototype("XX", _matrices.xx_matrix, 2)
YY = make_parametric_gate_prototype("YY", _matrices.yy_matrix, 2)
ZZ = make_parametric_gate_prototype("ZZ", _matrices.zz_matrix, 2)
XY = make_parametric_gate_prototype("XY", _matrices.xy_matrix, 2)