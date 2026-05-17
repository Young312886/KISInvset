import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust as needed for production

export interface AIBriefingResponse {
  symbol: string;
  briefing: string;
  context_used: {
    regime: string;
    recommended_weight: number;
    fundamental_score: number;
    fundamental_grade: string;
    technical_signal: string;
    win_rate: number;
  };
}

export const getAIBriefing = async (symbol: string): Promise<AIBriefingResponse> => {
  const token = localStorage.getItem('token');
  const response = await axios.get(`${API_BASE_URL}/ai/briefing/${symbol}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
