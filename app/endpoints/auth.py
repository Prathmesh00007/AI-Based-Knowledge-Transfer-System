# app/endpoints/auth.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from config import settings

router = APIRouter()

# Create a temporary Starlette config from your settings
temp_config = Config(environ=settings.dict())

oauth = OAuth(temp_config)
oauth.register(
    name="atlassian",
    client_id=settings.ATLASSIAN_CLIENT_ID,
    client_secret=settings.ATLASSIAN_CLIENT_SECRET,
    access_token_url="https://auth.atlassian.com/oauth/token",
    authorize_url="https://auth.atlassian.com/authorize",
    api_base_url="https://api.atlassian.com/",
    client_kwargs={"scope": "read:me read:jira-work"},
)

@router.get("/login")
async def login(request: Request):
    """Initiate OAuth2 flow by redirecting to Atlassian's login page."""
    redirect_uri = settings.BASE_URL + "/auth"
    return await oauth.atlassian.authorize_redirect(request, redirect_uri)

@router.get("/auth")
async def auth(request: Request):
    """OAuth callback endpoint to exchange code for token and fetch user info."""
    try:
        token = await oauth.atlassian.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error.error}")
    user_resp = await oauth.atlassian.get("me", token=token)
    user_info = user_resp.json()
    html_content = f"""
    <html>
      <head><title>Welcome</title></head>
      <body>
        <h1>Signed in with Atlassian</h1>
        <p><strong>Display Name:</strong> {user_info.get('displayName', 'N/A')}</p>
        <p><strong>Account ID:</strong> {user_info.get('account_id', 'N/A')}</p>
        <p><strong>Email:</strong> {user_info.get('email', 'Not provided')}</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)
