from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from controller.oauth.oauthmanager import get_auth_strategies
from utils import generate_state
from conf import APP_URL

router = APIRouter(prefix='/oauth')

@router.get('/login/{provider}')
async def login(provider : str, request : Request):
    try:
        
        strategy = get_auth_strategies(provider)
        state = generate_state()
        request.session['oauth_state'] = state
        redirect_url = f"{APP_URL}/oauth/callback/{provider}"
        response = await strategy.authorize_redirect(request=request,redirect_url = redirect_url,state =state)
        return response

    except Exception as err:
        print('error',err)
        return JSONResponse(content={'data' : 'Something went wrong','message' : 'Fail'},status_code=500)
    

@router.get('/callback/{provider}')
async def callback(provider : str, request : Request):
    try:
        
        state = request.session['oauth_state']
        received_state = request.query_params.get('state')
        strategy = get_auth_strategies(provider.lower())

        if not state or not received_state:
            return JSONResponse(content={'data' : 'Missing state parameter','message' : 'Fail'},status_code=400)
        
        if state != received_state:
            return JSONResponse(content= {'data' : 'State mismatch','message' : 'Fail'},status_code=400)
        
        request.session.pop('oauth_state')
        token = await strategy.get_access_token(request)
        user_data = await strategy.get_user_data(token)
        return JSONResponse(content={'data' : user_data,'message' : 'Success'},status_code=200)
        
    except Exception as err:
        print('error',err)
        return JSONResponse(content={'data' : 'Something went wrong','message' : 'Fail'},status_code=500)

