"""This test module contains all tests regarding the Inconsistent KernelSHAP-IQ regression
approximator."""

import copy

import pytest

from shapiq.approximator import InconsistentKernelSHAPIQ
from shapiq.games.benchmark import DummyGame
from shapiq.interaction_values import InteractionValues


@pytest.mark.parametrize("n", [3, 7, 10])
def test_initialization(n):
    """Tests the initialization of the Inconsistent KernelSHAP-IQ approximator."""
    approximator = InconsistentKernelSHAPIQ(n)
    assert approximator.n == n
    assert approximator.max_order == 2
    assert approximator.top_order is False
    assert approximator.min_order == 0
    assert approximator.iteration_cost == 1

    approximator_copy = copy.copy(approximator)
    approximator_deepcopy = copy.deepcopy(approximator)
    approximator_deepcopy.index = "something"
    assert approximator_copy == approximator  # check that the copy is equal
    assert approximator_deepcopy != approximator  # check that the deepcopy is not equal
    approximator_string = str(approximator)
    assert repr(approximator) == approximator_string
    assert hash(approximator) == hash(approximator_copy)
    assert hash(approximator) != hash(approximator_deepcopy)
    with pytest.raises(ValueError):
        _ = approximator == 1

    # check for error when index is not in AVAILABLE_INDICES_KERNELSHAPIQ
    with pytest.raises(ValueError):
        _ = InconsistentKernelSHAPIQ(n, index="something")


@pytest.mark.parametrize("budget, order", [(100, 1), (100, 2), (100, 3), (100, 4)])
def test_approximate(budget, order):
    """Tests the approximation of the Inconsistent KernelSHAP-IQ approximator."""
    n = 7
    interaction = (1, 2)
    game = DummyGame(n, interaction)

    approximator = InconsistentKernelSHAPIQ(n, max_order=order, index="SII")
    sii_estimates = approximator.approximate(budget, game)
    assert isinstance(sii_estimates, InteractionValues)
    assert sii_estimates.max_order == order
    assert sii_estimates.min_order == 0

    # check that the budget is respected
    assert game.access_counter <= budget

    assert sii_estimates[(1,)] == pytest.approx(0.6429, abs=0.01)
    assert sii_estimates[(2,)] == pytest.approx(0.6429, abs=0.01)

    if order > 1:
        assert sii_estimates[(1, 2)] == pytest.approx(1.0, abs=0.01)

    assert sii_estimates[(1, 2, 3)] == pytest.approx(0, abs=0.01)