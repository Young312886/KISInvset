import requests
import json
import time
from datetime import datetime, timedelta
import websocket
import threading
import pandas as pd

# Relative import will work when run as a module
try:
    from app.core.config import settings
    from app.core.analysis.ichimoku import calculate_ichimoku
except ImportError:
    # Handle direct script execution for testing
    import sys
    import os
    # Add project root to path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
    from backend.app.core.config import settings
    from backend.app.core.analysis.ichimoku import calculate_ichimoku


class KISApi:
    """
    Korea Investment & Securities (KIS) API Wrapper
    - Handles OAuth 2.0 authentication and token management.
    - Provides methods for REST API calls and WebSocket connections.
    """
    def __init__(self):
        self.base_url = settings.KIS_BASE_URL
        # Correct WebSocket URL for mock trading
        self.ws_url = "ws://ops.koreainvestment.com:31000" if "vts" in self.base_url else "ws://ops.koreainvestment.com:21000"
        self.app_key = settings.KIS_APP_KEY
        self.app_secret = settings.KIS_APP_SECRET
        self._access_token = None
        self._token_expiry = None
        self._ensure_token()

    def _issue_token(self):
        """Issues a new access token from KIS API."""
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            res_data = response.json()
            
            self._access_token = res_data["access_token"]
            expiry_seconds = int(res_data.get("expires_in", 86400)) - 1800 
            self._token_expiry = datetime.now() + timedelta(seconds=expiry_seconds)
            
            print(f"New KIS access token issued. Expires at: {self._token_expiry}")

        except requests.exceptions.RequestException as e:
            print(f"Error issuing KIS access token: {e}")
            self._access_token = None
            self._token_expiry = None

    def _ensure_token(self):
        """Ensures a valid access token is available."""
        if self._access_token is None or (self._token_expiry and datetime.now() >= self._token_expiry):
            print("Access token is missing or expired. Issuing a new one.")
            self._issue_token()

    @property
    def access_token(self):
        self._ensure_token()
        return self._access_token

    def fetch_ohlcv(self, symbol: str, timeframe: str = 'D', end_date: str = None, period_code: str = '0') -> pd.DataFrame:
        """
        Fetches historical OHLCV data for a given stock.
        
        Args:
            symbol (str): The stock symbol (e.g., "005930").
            timeframe (str): 'D' for daily, 'W' for weekly, 'M' for monthly.
            end_date (str): The end date for the data in 'YYYYMMDD' format. Defaults to today.
            period_code (str): '0' for period, '1' for count.
        
        Returns:
            pd.DataFrame: A DataFrame with OHLCV data, or an empty DataFrame if the request fails.
        """
        self._ensure_token()
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST03010100"
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_INPUT_DATE_1": "19900101", # A sufficiently old start date
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": timeframe,
            "FID_ORG_ADJ_PRC": "0" # Adjusted price for dividends/splits
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data['rt_cd'] != '0':
                print(f"API Error: {data['msg1']}")
                return pd.DataFrame()

            ohlcv_list = data['output2']
            df = pd.DataFrame(ohlcv_list)
            
            # Rename columns to a standard format
            column_map = {
                'stck_bsop_date': 'date',
                'stck_oprc': 'open',
                'stck_hgpr': 'high',
                'stck_lwpr': 'low',
                'stck_clpr': 'close',
                'acml_vol': 'volume'
            }
            df = df.rename(columns=column_map)
            
            # Convert columns to numeric types
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col])

            # Set date as index
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            df = df.set_index('date')
            
            # API returns in reverse chronological order, so we reverse it
            return df.iloc[::-1]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching OHLCV data: {e}")
            return pd.DataFrame()

    def fetch_minute_ohlcv(self, symbol: str, time_div: str = '30') -> pd.DataFrame:
        """
        Fetches minute OHLCV data for a given stock.
        
        Args:
            symbol (str): The stock symbol (e.g., "005930").
            time_div (str): Minute division ('1', '3', '5', '10', '15', '30', '60'). Default '30'.
        
        Returns:
            pd.DataFrame: A DataFrame with minute OHLCV data.
        """
        self._ensure_token()
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
        
        current_time = datetime.now().strftime('%H%M%S')

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST03010200"
        }
        params = {
            "FID_ETC_CLS_CODE": "",
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_INPUT_HOUR_1": current_time,
            "FID_PW_DATA_INCU_YN": "N"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data['rt_cd'] != '0':
                print(f"API Error: {data['msg1']}")
                return pd.DataFrame()

            ohlcv_list = data['output2']
            df = pd.DataFrame(ohlcv_list)
            
            # Map columns
            column_map = {
                'stck_bsop_date': 'date',
                'stck_cntg_hour': 'time',
                'stck_oprc': 'open',
                'stck_hgpr': 'high',
                'stck_lwpr': 'low',
                'stck_prpr': 'close',
                'cntg_vol': 'volume'
            }
            df = df.rename(columns=column_map)
            
            # Create datetime index
            df['datetime'] = pd.to_datetime(df['date'] + df['time'], format='%Y%m%d%H%M%S')
            df = df.set_index('datetime')
            
            # Convert to numeric
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col])
                
            df = df.drop(columns=['date', 'time'])
            
            # API returns reverse chronological order
            return df.iloc[::-1]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching minute OHLCV data: {e}")
            return pd.DataFrame()

    def get_ws_approval_key(self):
        """Gets a temporary approval key for WebSocket connection."""
        self._ensure_token()
        url = f"{self.base_url}/oauth2/Approval"
        headers = {"content-type": "application/json", "authorization": f"Bearer {self.access_token}"}
        body = {"grant_type": "client_credentials", "appkey": self.app_key, "appsecret": self.app_secret}
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            return response.json().get("approval_key")
        except requests.exceptions.RequestException as e:
            print(f"Error getting WebSocket approval key: {e}")
            return None

    def _on_message(self, ws, message):
        if message[0] in ['0', '1']:
            parts = message.split('|')
            if len(parts) > 1 and parts[1] == "H0STCNT0":
                data = parts[3].split('^')
                print(f"[{data[1]}] {data[0]} - Price: {data[2]}, Volume: {data[6]}")
            else:
                print(f"Data: {message}")
        else:
            print(f"System: {message}")

    def _on_error(self, ws, error):
        print(f"WebSocket Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("### WebSocket Closed ###")

    def _on_open(self, ws, symbol):
        print("### WebSocket Opened ###")
        approval_key = self.get_ws_approval_key()
        if not approval_key:
            print("Failed to get approval key. Closing connection.")
            ws.close()
            return

        subscription_data = {
            "header": {"approval_key": approval_key, "custtype": "P", "tr_type": "1", "content-type": "utf-8"},
            "body": {"input": {"tr_id": "H0STCNT0", "tr_key": symbol}}
        }
        ws.send(json.dumps(subscription_data))
        print(f"Subscribed to real-time price for {symbol}")

    def start_websocket(self, symbol):
        ws_app = websocket.WebSocketApp(
            self.ws_url,
            on_open=lambda ws: self._on_open(ws, symbol),
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        wst = threading.Thread(target=ws_app.run_forever)
        wst.daemon = True
        wst.start()
        print("WebSocket thread started.")

if __name__ == "__main__":
    print("Initializing KIS API to test data fetching and analysis...")
    
    if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', '.env')):
        import shutil
        env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        env_example_path = env_path + '.example'
        shutil.copyfile(env_example_path, env_path)
        print(f"\nIMPORTANT: '.env' file created at '{env_path}'.")
        print("Please edit it with your actual KIS API credentials before running again.")
        sys.exit(0)

    api = KISApi()
    
    if api.access_token:
        print("\nSuccessfully obtained access token.")
        test_symbol = "005930" # Samsung Electronics
        
        print(f"\nFetching daily OHLCV data for {test_symbol}...")
        ohlcv_df = api.fetch_ohlcv(test_symbol, timeframe='D')

        if not ohlcv_df.empty:
            print(f"Successfully fetched {len(ohlcv_df)} days of data.")
            print("Latest data point:")
            print(ohlcv_df.tail(1))

            print("\nCalculating Ichimoku Cloud...")
            ichimoku_df = calculate_ichimoku(ohlcv_df)
            print("Ichimoku data (last 5 rows):")
            print(ichimoku_df[['close', 'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b']].tail())
        else:
            print("Failed to fetch OHLCV data.")

    else:
        print("\nFailed to obtain access token. Check credentials in 'backend/.env'")
