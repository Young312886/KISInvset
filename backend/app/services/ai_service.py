import os
import google.generativeai as genai
from typing import Dict, Any

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Use gemini-1.5-flash for fast text generation
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def generate_briefing(self, symbol: str, company_name: str, context_data: Dict[str, Any]) -> str:
        """
        Generates an investment thesis based on technical, fundamental, and portfolio data.
        """
        if not self.model:
            return f"[{company_name} 투자 브리핑 (MOCK)]\n현재 시장은 {context_data.get('regime', 'BULL')} 국면을 지나고 있으며, 해당 종목은 펀더멘털 스코어 {context_data.get('fundamental_score', 80)}점(등급: {context_data.get('fundamental_grade', 'A')})으로 견조한 실적을 뒷받침하고 있습니다. 기술적으로도 {context_data.get('technical_signal', 'BUY')} 시그널이 발생하여 상승 추세에 올라탔습니다.\n\n리스크 관리 측면에서 백테스트 승률 {context_data.get('win_rate', 50.0):.1f}% 기반의 켈리 공식 분석 결과, 전체 포트폴리오 대비 {context_data.get('recommended_weight', 0.0)*100:.1f}%의 비중으로 분할 매수하는 것이 통계적으로 가장 우수한 위험 대비 수익률을 기대할 수 있습니다.\n\n결론적으로 현 시점은 매수(BUY) 관점으로 접근하되, 지수 변동성을 감안하여 권장 비중을 준수하는 보수적인 자금 관리를 병행하시길 권장드립니다."

        # Extract data from context
        regime = context_data.get('regime', 'UNKNOWN')
        kelly_pct = context_data.get('recommended_weight', 0.0) * 100
        fundamental_score = context_data.get('fundamental_score', 0)
        fundamental_grade = context_data.get('fundamental_grade', 'N/A')
        technical_signal = context_data.get('technical_signal', 'HOLD')
        win_rate = context_data.get('win_rate', 0.0)
        
        prompt = f"""
        너는 여의도 최고 수준의 기관 트레이더이자 리서치 애널리스트야.
        다음 수치형 데이터들을 바탕으로 개인 투자자가 직관적으로 이해할 수 있는 3단락 분량의 짧고 명확한 '투자 논거(Investment Thesis)'를 한국어로 작성해줘.
        왜 이 비중을 추천했는지 장세와 결합해서 설명해.
        
        [분석 대상]
        종목: {company_name} ({symbol})
        
        [시장 및 포트폴리오 데이터]
        시장 국면 (Market Regime): {regime}
        권장 투자 비중 (Kelly Criterion 기반): {kelly_pct:.1f}%
        전략 백테스트 승률: {win_rate:.1f}%
        
        [종목 평가 데이터]
        펀더멘털 점수: {fundamental_score}점 (등급: {fundamental_grade})
        기술적 분석 시그널: {technical_signal}
        
        [출력 형식 가이드라인]
        1. 첫 번째 단락: 현재 시장 국면과 해당 종목의 전반적인 매력도 (기술적/펀더멘털 결합)
        2. 두 번째 단락: 권장 투자 비중({kelly_pct:.1f}%)에 대한 트레이더 관점의 해석 및 리스크 관리 코멘트
        3. 세 번째 단락: 핵심 요약 및 최종 행동 가이드 (매수/매도/관망)
        
        전문적이면서도 개인 투자자가 읽기 쉽도록 가독성 있게 작성해.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI 브리핑 생성 중 오류가 발생했습니다: {str(e)}"
