import httpx
from typing import Dict, Any, Optional, List
from config import BASE_API_URL, DEFAULT_HEADERS, API_TIMEOUT

class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class FinanceAPIClient:
    def __init__(self):
        self.base_url = BASE_API_URL
        self.client = httpx.Client(timeout=API_TIMEOUT)
        
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = DEFAULT_HEADERS.copy()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _handle_response(self, response: httpx.Response) -> Any:
        try:
            response.raise_for_status()
            # 204 No Content doesn't have JSON body
            if response.status_code == 204:
                return True
            return response.json()
        except httpx.HTTPStatusError as e:
            error_data = {}
            try:
                error_data = e.response.json()
            except:
                pass
            detail = error_data.get("detail", str(e))
            raise APIError(f"API Error: {detail}", status_code=e.response.status_code)
        except httpx.RequestError as e:
            raise APIError(f"Request Error: {str(e)}")

    # --- Authentication ---
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and return access token."""
        url = f"{self.base_url}/auth/login"
        data = {"username": email, "password": password} # OAuth2 expects form data
        response = self.client.post(url, data=data)
        return self._handle_response(response)

    # --- Users ---
    def create_user(self, email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        url = f"{self.base_url}/users/"
        payload = {"email": email, "password": password}
        response = self.client.post(url, json=payload, headers=self._get_headers())
        return self._handle_response(response)

    # --- Transactions ---
    def get_transactions(self, token: str, limit: int = 10, skip: int = 0, search: Optional[str] = None, sort_by: str = "desc") -> List[Dict[str, Any]]:
        """Fetch transactions for the current user."""
        url = f"{self.base_url}/transactions/"
        params = {"limit": limit, "skip": skip, "sort_by": sort_by}
        if search:
            params["search"] = search
        response = self.client.get(url, params=params, headers=self._get_headers(token))
        return self._handle_response(response)

    def create_transaction(self, token: str, amount: float, description: str, category_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new transaction."""
        url = f"{self.base_url}/transactions/"
        payload = {
            "amount": amount,
            "description": description,
            "category_id": category_id
        }
        response = self.client.post(url, json=payload, headers=self._get_headers(token))
        return self._handle_response(response)

    def get_transaction_stats(self, token: str) -> Dict[str, Any]:
        """Get overall transaction statistics."""
        url = f"{self.base_url}/transactions/stats"
        response = self.client.get(url, headers=self._get_headers(token))
        return self._handle_response(response)

    def get_monthly_stats(self, token: str, month: Optional[int] = None, year: Optional[int] = None) -> Dict[str, Any]:
        """Get custom monthly/yearly statistics."""
        url = f"{self.base_url}/transactions/custom_stats"
        params = {}
        if month: params["month"] = month
        if year: params["year"] = year
        response = self.client.get(url, params=params, headers=self._get_headers(token))
        return self._handle_response(response)

    def delete_transaction(self, token: str, transaction_id: int) -> bool:
        """Delete a transaction by ID."""
        url = f"{self.base_url}/transactions/{transaction_id}"
        response = self.client.delete(url, headers=self._get_headers(token))
        return self._handle_response(response)

    # --- Placeholder Functions ---
    # According to prompt: "If an endpoint is unknown, create a placeholder function in api_client.py 
    # that can easily be mapped to the real endpoint later."
    
    def get_portfolio_summary(self, token: str) -> Dict[str, Any]:
        """Placeholder for fetching portfolio details."""
        # Simulated structure based on common finance apps
        return {
            "total_value": 0.0,
            "assets": []
        }
        
    def get_ai_predictions(self, token: str) -> Dict[str, Any]:
        """Placeholder for AI prediction endpoints if separated from transaction creation."""
        return {
            "insights": ["AI insights will appear here once connected."]
        }

# Global instance for easier import
api = FinanceAPIClient()
