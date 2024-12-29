from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.gateway.middlewares.auth import AuthMiddleware
from app.gateway.middlewares.rate_limit import RateLimitMiddleware
from app.gateway.routes import api_router
from app.gateway.config import GatewayConfig

class GatewayServer:
    def __init__(self, config: GatewayConfig):
        self.app = FastAPI(title="API Gateway")
        self.config = config
        self._setup_middlewares()
        self._setup_routes()

    def _setup_middlewares(self):
        # CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 认证中间件
        self.app.add_middleware(AuthMiddleware)
        
        # 限流中间件
        self.app.add_middleware(RateLimitMiddleware)

    def _setup_routes(self):
        self.app.include_router(api_router) 