"""This test module contains all tests for the Unbiased KernelSHAP approximator."""

from __future__ import annotations

import pytest

from shapiq.approximator import UnbiasedKernelSHAP
from shapiq.games.benchmark import DummyGame


def test_basic_functionality():
    """Tests the initialization of the RegressionFSII approximator."""
    n_players = 7

    approximator = UnbiasedKernelSHAP(n_players)
    assert approximator.n == n_players
    assert approximator.max_order == 1
    assert approximator.top_order is False
    assert approximator.min_order == 0
    assert approximator.iteration_cost == 1
    assert approximator.index == "SV"

    # test that the approximator can approximate the correct values
    interaction = (1, 2)
    game = DummyGame(n_players, interaction)
    budget = 2**n_players

    approximator = UnbiasedKernelSHAP(n_players)
    sv_estimates = approximator.approximate(budget, game)
    assert sv_estimates.n_players == n_players
    assert sv_estimates.max_order == 1
    assert sv_estimates.min_order == 0
    assert sv_estimates.index == "SV"
    assert sv_estimates.estimated is False
    assert sv_estimates.estimation_budget == budget

    # check that the values are correct
    assert sv_estimates[()] == 0.0
    assert sv_estimates[(0,)] == pytest.approx(0.1429, 0.01)
    assert sv_estimates[(1,)] == pytest.approx(0.6429, 0.01)

    # smaller budget
    budget = int(budget * 0.75)
    sv_estimates = approximator.approximate(budget, game)
    assert sv_estimates.n_players == n_players
    assert sv_estimates.max_order == 1
    assert sv_estimates.min_order == 0
    assert sv_estimates.index == "SV"
    assert sv_estimates.estimated is True
    assert sv_estimates.estimation_budget == budget
