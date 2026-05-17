import pytest
from app.services.fundamental_service import SRimService

def test_srim_calculate():
    service = SRimService()

    # Case 1: Positive excess profit
    bps = 10000
    roe = 0.10
    discount_rate = 0.05
    
    # Year 1:
    # EPS = 10000 * 0.10 = 1000
    # Required = 10000 * 0.05 = 500
    # Excess = 500
    # PV = 500 / 1.05 = 476.19
    # BPS = 10000 + 1000 = 11000
    
    result = service.calculate(bps=bps, roe=roe, discount_rate=discount_rate, forecast_years=1)
    
    assert result["discount_rate"] == 0.05
    assert result["excess_profit_pv"] == 476.19
    assert result["intrinsic_value"] == 10476.19

    # Case 2: Negative excess profit (ROE < Discount Rate)
    bps_2 = 10000
    roe_2 = 0.02
    discount_rate_2 = 0.05
    
    # Year 1:
    # EPS = 10000 * 0.02 = 200
    # Required = 10000 * 0.05 = 500
    # Excess = -300
    # PV = -300 / 1.05 = -285.71
    # Intrinsic = 10000 - 285.71 = 9714.29

    result_2 = service.calculate(bps=bps_2, roe=roe_2, discount_rate=discount_rate_2, forecast_years=1)
    
    assert result_2["discount_rate"] == 0.05
    assert result_2["excess_profit_pv"] == -285.71
    assert result_2["intrinsic_value"] == 9714.29

    # Case 3: Zero excess profit (ROE == Discount Rate)
    result_3 = service.calculate(bps=10000, roe=0.05, discount_rate=0.05, forecast_years=10)
    assert result_3["excess_profit_pv"] == 0.0
    assert result_3["intrinsic_value"] == 10000.0

def test_srim_default_discount_rate():
    service = SRimService()
    result = service.calculate(bps=10000, roe=0.10, forecast_years=1)
    assert result["discount_rate"] == SRimService.DEFAULT_DISCOUNT_RATE
