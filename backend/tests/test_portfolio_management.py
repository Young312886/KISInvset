import pytest
from app.services.portfolio_management_service import PortfolioManagementService

def test_kelly_criterion_positive_edge():
    service = PortfolioManagementService()
    # 55% win rate, 1.2 win/loss ratio, half-kelly
    # Kelly = 0.55 - (0.45 / 1.2) = 0.55 - 0.375 = 0.175
    # Half-Kelly = 0.0875
    pct = service.calculate_kelly_criterion(win_rate=0.55, win_loss_ratio=1.2, fraction=0.5)
    assert round(pct, 4) == 0.0875

def test_kelly_criterion_negative_edge():
    service = PortfolioManagementService()
    # 40% win rate, 1.0 win/loss ratio
    # Kelly = 0.40 - (0.60 / 1.0) = -0.20 -> 0.0
    pct = service.calculate_kelly_criterion(win_rate=0.40, win_loss_ratio=1.0, fraction=0.5)
    assert pct == 0.0

def test_kelly_criterion_edge_cases():
    service = PortfolioManagementService()
    # 0 win rate
    pct = service.calculate_kelly_criterion(0.0, 2.0)
    assert pct == 0.0
    
    # Very high edge
    pct = service.calculate_kelly_criterion(0.8, 3.0, fraction=1.0)
    assert round(pct, 4) == 0.7333

def test_detect_market_regime_insufficient_data(mocker):
    service = PortfolioManagementService()
    # Mock api to return empty dataframe
    mocker.patch.object(service.api, 'fetch_ohlcv', return_value=None)
    
    result = service.detect_market_regime()
    assert result['regime'] == 'UNKNOWN'
    assert result['technical_weight'] == 0.5
    assert result['fundamental_weight'] == 0.5
