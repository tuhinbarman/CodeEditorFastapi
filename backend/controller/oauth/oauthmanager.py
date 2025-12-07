from abc import ABC,abstractmethod
from authlib.integrations.starlette_client import OAuth
from fastapi.requests import Request
from sqlalchemy.orm import Session
import os
from conf import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET

oauth = OAuth()

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    api_base_url='https://openidconnect.googleapis.com/',
    client_kwargs={'scope': 'openid email profile'},
)

class OAuthStrategy(ABC):

    @abstractmethod
    def __init__(self,oauth : OAuth):
        pass
    
    @abstractmethod
    async def authorize_redirect(self,request : Request,redirect_url : str,state:str):
        pass

    @abstractmethod
    async def get_access_token(self,request):
        pass

    @abstractmethod
    async def get_user_data(self,token:dict):
        pass

class GoogleAuthStrategy(OAuthStrategy):

    def __init__(self,oauth : OAuth):
        self.__client = oauth.create_client('google')
    
    async def authorize_redirect(self,request : Request, redirect_url : str,state:str):
        print(redirect_url)
        result = await self.__client.authorize_redirect(request,redirect_uri = redirect_url ,state = state)
        return result
    
    async def get_access_token(self,request:Request):
        result = await self.__client.authorize_access_token(request)
        return result

    async def get_user_data(self, token: dict):
        resp = await self.__client.get('v1/userinfo', token=token)  
        user_data = resp.json()
        return user_data


    

def get_auth_strategies(provider : str) -> OAuthStrategy:
    strategies = {
        'google' : GoogleAuthStrategy
    }
    if provider not in strategies:
        raise ValueError(f"Unsupported provider: {provider}")
    strategy = strategies.get(provider) 

    return strategy(oauth=oauth) 



