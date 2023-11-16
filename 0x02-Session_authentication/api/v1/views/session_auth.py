#!/usr/bin/env python3
"""Flask view that handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=True)
def session_login():
    """POST /api/v1/auth_session/login"""
    from api.v1.app import auth

    email = request.form.get('email')
    psswd = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not psswd or psswd == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    user_psswd = user.is_valid_password(psswd)
    if not user_psswd:
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    cookie_name = getenv('SESSION_NAME')
    res.set_cookie(cookie_name, session_id)
    return res


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=True)
def session_logout():
    """DELETE /api/v1/auth_session/logout"""
    from api.v1.app import auth

    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    return jsonify({}), 200
