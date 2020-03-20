# Copyright (c) 2020. All rights reserved. Nico Coetzee <nicc777@gmail.com>
# Please check LICENSE.txt for licencing information or visit https://github.com/nicc777/flask-prod-docker

import os
import requests
import base64
import traceback
import cognitojwt
from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
from example import ServiceLogger

app = Flask(__name__)
L = ServiceLogger()
app.secret_key = os.getenv('SECRET_KEY', 'DEVELOPMENT KEY WHICH IS SADLY NOT SECRET').encode('utf-8')
cognito_client_id = os.getenv('COGNITO_CLIENT_ID', 'not-set')
cognito_client_secret = os.getenv('COGNITO_CLIENT_SECRET', 'not-set')
cognito_domain = os.getenv('COGNITO_DOMAIN', 'not-set')
cognito_login_callback_url = os.getenv('COGNITO_LOGIN_CALLBACK_URL', 'not-set')
cognito_logout_callback_url = os.getenv('COGNITO_LOGOUT_CALLBACK_URL', 'not-set')
cognito_scope = 'openid+profile'
cognito_state = 'DEMO-STATE'
cognito_interim_creds = '{}:{}'.format(cognito_client_id, cognito_client_secret)
encoded_cognito_interim_creds = base64.b64encode(cognito_interim_creds.encode('utf-8'))
cognito_final_creds = encoded_cognito_interim_creds.decode('utf-8') 
L.info(message='cognito_scope={}'.format(cognito_scope))
L.info(message='cognito_state={}'.format(cognito_state))


@app.route('/')
def home():
	L.info(message='Rendering home page')
	return render_template('home.html')


@app.route('/login')
def login():
    """
    From: https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html

        https://mydomain.auth.us-east-1.amazoncognito.com/login?
        response_type=code&
        client_id=aaaaaaaaaaaaa&
        redirect_uri=https://YOUR_APP/redirect_uri&
        state=STATE&
        scope=openid+profile
    """
    target_url = '{}/oauth2/authorize?response_type=code&client_id={}&redirect_uri={}&state={}&scope={}'.format(
        cognito_domain,
        cognito_client_id,
        cognito_login_callback_url,
        cognito_state,
        cognito_scope
    )
    L.info(message='Redirecting to "{}"'.format(target_url))
    return redirect(target_url)

@app.route('/secret')
def secret():
    secret_heading = 'No secrets today...'
    secret_message = 'You lack the authority to know the worlds secrets!'
    username = 'Anonymous'
    if 'username' in session:
        username = session['username']
        secret_heading = 'The JFK assassination'
        secret_message = 'The secret behind the JFK assassination is simply this: it only happened in some universes - he\'s perfectly fine in others...'
    return render_template(
        'secret.html',
        username=username,
        secret_heading=secret_heading,
        secret_message=secret_message
    )

@app.route('/logout')
def logout():
    """
        Refer to https://docs.aws.amazon.com/cognito/latest/developerguide/logout-endpoint.html
    """
    try:
        print('pre-logout: username={}'.format(session['username']))
        print('pre-logout: cognito_raw_data={}'.format(session['cognito_raw_data']))
        print('pre-logout: logged_in={}'.format(session['logged_in']))
        session.pop('username', None)
        session.pop('logged_in', None)
        session.pop('cognito_raw_data', None)
        flash('You were logged out successfully!')
        return redirect(
            '{}/logout?client_id={}&logout_uri={}'.format(
                cognito_domain,
                cognito_client_id,
                cognito_logout_callback_url
            )
        )
    except:
        flash('Failed to logout from Cognito, but your local sessions on the server was cleared!')
        print('EXCEPTION: {}'.format(traceback.format_exc()))
    return redirect('/')


@app.route('/cognito_callback')
def cognito_callback():
    """
        Read: https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html

        A successful authentication will have the following dictionary:

            { 
                "access_token": "......", 
                "refresh_token": "......", 
                "id_token": "......",
                "token_type": "Bearer", 
                "expires_in": 3600
            }

    """
    L.info(message='Got stuff back from Cognito')
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    L.info(message='code={}'.format(code))
    L.info(message='state={}'.format(state))
    if state is not None and code is not None:
        if state == 'DEMO-STATE':
            # Exchange code for token
            target_url = '{}/oauth2/token'.format(cognito_domain)
            L.info(message='target_url={}'.format(target_url))
            L.info(message='cognito_client_id={}'.format(cognito_client_id))
            L.info(message='code={}'.format(code))
            L.info(message='cognito_login_callback_url={}'.format(cognito_login_callback_url))
            try:
                token_request_response = requests.post(
                    target_url,
                    data={
                        'grant_type': 'authorization_code',
                        'client_id': cognito_client_id,
                        'code': code,
                        'redirect_uri': cognito_login_callback_url,
                    },
                    headers={
                        'Authorization': 'Basic {}'.format(cognito_final_creds),
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                )
                if token_request_response.status_code == 200:
                    flash('Thanks for logging in!')
                    json_response = token_request_response.json()
                    L.info(message='json_response={}'.format(json_response))

                    # Validate token
                    verified_claims = dict()
                    try:
                        verified_claims: dict = cognitojwt.decode(
                            json_response['access_token'],
                            os.getenv('COGNITO_REGION', 'us-east-1'),
                            os.getenv('COGNITO_USER_POOL_ID', 'not-set'),
                            app_client_id=cognito_client_id,  
                            testmode=False  
                        )
                        L.info(message='verified_claims={}'.format(verified_claims))
                    except:
                        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
                        L.error(message='TOKENS ARE UNVERIFIED')

                    user_info_target_url = '{}/oauth2/userInfo'.format(cognito_domain)
                    user_info_response = requests.get(
                        user_info_target_url,
                        headers={
                            'Authorization': 'Bearer {}'.format(json_response['access_token']),
                        }
                    )
                    L.info(message='user_info_response={}'.format(user_info_response))
                    if user_info_response.status_code == 200:
                        user_info_json_response = user_info_response.json()
                        L.info(message='user_info_json_response={}'.format(user_info_json_response))
                        session['logged_in'] = True
                        session['username'] = user_info_json_response['email']
                        session['cognito_raw_data'] = user_info_json_response
                        return redirect('/secret')
                    else:
                        L.info(message='ERROR: LEG 2: return code: {}'.format(user_info_response.status_code))
                        flash('We failed to get a token - please ensure you are not being hacked! Or are you the haxor?')
                else:
                    L.info(message='ERROR: LEG 1: return code: {}'.format(token_request_response.status_code))
                    flash('We failed to get a token - please ensure you are not being hacked! Or are you the haxor?')
            except:
                L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return redirect('/')


@app.route('/cognito_logout_callback')
def cognito_logout_callback():
    return redirect('/')

# EOF
