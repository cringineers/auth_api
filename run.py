import os
import time
import json
import logging
import jwt
import flask
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from core.db import check_user_data

if not os.path.exists(find_dotenv(".env")):
    logging.warning("Cant find .env file.")
load_dotenv()

app = Flask(__name__)
CORS(app)
secret = os.environ.get("JWT_KEY")
alg = os.environ.get("JWT_ALG")

connection_string = f"postgresql+asyncpg://" \
                    f"{os.environ.get('DB_USER')}:%s" % os.environ.get('DB_PASSWORD') + \
                    f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
sql_engine = create_async_engine(
    connection_string,
    pool_size=int(os.environ.get('POOL_SIZE')),
    max_overflow=int(os.environ.get('POOL_OVERFLOW')),
    pool_recycle=int(os.environ.get('POOL_RECYCLE')))


@app.post("/login")
async def login():
    body = request.get_json()
    user = body.get('username')
    password = body.get('password')
    status, id = await check_user_data(sql_engine, user, password)
    if status:
        token = jwt.encode(
            {
                "user_id": id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5)
            },
            algorithm=alg,
            key=secret)
        refresh_token = jwt.encode(
            {
                "user_id": id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1)
            },
            algorithm=alg,
            key=secret)
        return jsonify(token=token, refresh=refresh_token), 200
    else:
        return jsonify(error="Incorrect login or password"), 401


@app.post("/refresh")
async def refresh():
    try:
        body = request.get_json()
        refresh_token = body.get('refresh_token')
        if refresh_token:
            payload = jwt.decode(refresh_token, secret, alg)
            token = jwt.encode(
                {
                    "user_id": payload["user_id"],
                    "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5)
                },
                algorithm=alg,
                key=secret)
            if payload["exp"] - time.mktime(
                    datetime.now(tz=timezone.utc).timetuple()) < 1000 * 3600:
                refresh_token = jwt.encode(
                    {
                        "user_id": payload["user_id"],
                        "exp":
                        datetime.now(tz=timezone.utc) + timedelta(hours=1)
                    },
                    algorithm=alg,
                    key=secret)
            return jsonify(token=token, refresh=refresh_token), 200
        else:
            return jsonify(error="Incorrect login or password"), 401
    except Exception:
        return jsonify(error="Token expired")


if __name__ == '__main__':
    logging.warning("Server started")
    app.run(port=5000, host="0.0.0.0")
