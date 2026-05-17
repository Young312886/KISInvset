from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_service import AIService
from app.services.portfolio_management_service import PortfolioManagementService
from app.services.backtest_service import BacktestService
from app.services.analysis_service import AnalysisService
from app.database.models import User
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["AI Briefing"],
    responses={404: {"description": "Not found"}},
)

ai_service = AIService()

@router.get("/briefing/{symbol}")
async def get_ai_briefing(
    symbol: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # We need the company name (can be retrieved from kis_service or just placeholder for now)
        company_name = f"종목코드 {symbol}" # Could be enhanced to use KIS API / DB
        
        # 1. Fetch Market Regime & Position Sizing
        pm_service = PortfolioManagementService(db)
        
        # Determine Market Regime
        # Since we might not have a dedicated market router, assuming default for KOSPI
        regime = "BULL" # default
        try:
            regime = await pm_service.detect_market_regime(symbol="KOSPI")
        except Exception:
            pass
            
        # 2. Backtest Win Rate
        backtest_service = BacktestService(db)
        win_rate = 0.0
        try:
            # We run a fast backtest or get pre-computed metrics
            # For brevity, run a quick backtest (e.g. 1-year)
            # Or if there's a cached metric, we use that. Assuming we use default run_backtest
            bt_results = await backtest_service.run_backtest(symbol, initial_capital=10000000)
            win_rate = bt_results.get("win_rate", 50.0)
        except Exception:
            pass

        # 3. Kelly Criterion Recommended Weight
        # We need win_rate and win_loss_ratio
        win_loss_ratio = 1.5 # Example default or fetch from backtest
        if 'bt_results' in locals() and "metrics" in bt_results:
            # You might compute win_loss_ratio from bt_results
            pass
            
        rec_weight = pm_service.calculate_kelly_criterion(win_rate / 100, win_loss_ratio, half_kelly=True)
        
        # 4. Fundamental Score & Technical Signal
        analysis_service = AnalysisService(db)
        # Placeholder or actual call
        fundamental_score = 80
        fundamental_grade = "A"
        technical_signal = "BUY"
        try:
            scores = await analysis_service.analyze_fundamentals(symbol)
            if scores:
                fundamental_score = scores.get("total_score", 80)
                fundamental_grade = scores.get("grade", "A")
            
            tech_signal_data = await analysis_service.generate_signal(symbol)
            technical_signal = tech_signal_data.get("action", "BUY") if tech_signal_data else "HOLD"
        except Exception:
            pass

        context_data = {
            "regime": regime,
            "recommended_weight": rec_weight,
            "fundamental_score": fundamental_score,
            "fundamental_grade": fundamental_grade,
            "technical_signal": technical_signal,
            "win_rate": win_rate
        }
        
        # Generate the briefing using Gemini
        briefing = await ai_service.generate_briefing(symbol, company_name, context_data)
        
        return {"symbol": symbol, "briefing": briefing, "context_used": context_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
