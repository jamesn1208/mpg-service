from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register(app: FastAPI):
    origins = [
        "http://james-server:8080/app",
        "http://james-server:8080",
        "http://james-server:5173/app",
        "http://james-server:5173"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=[
            "X-Auth-Token",
            "Accept",
            "Content-Type"
        ],
    )
