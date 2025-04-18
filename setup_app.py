import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Depends, HTTPException, status
from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

from fastapi.openapi.models import SecurityScheme, OAuthFlows, OAuthFlowPassword, OAuthFlowAuthorizationCode
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, Union, Optional
from jose import jwt, JWTError
from app.routing.setup_routes.setup_clients_route import client_router
from app.routing.setup_routes.setup_products_route import product_router
from app.routing.setup_routes.setup_rules_route import rules_router
from app.routing.setup_routes.client_productcategory_relation_route import client_product_router
from app.routing.authentication_routes.client_authentication_route import auth_router, get_current_user
from app.routing.setup_routes.productcategory_product_relation_route import productcategory_product_router
from app.routing.user_data_routes.customer_loan_profile_route import customer_profile_data


load_dotenv()


def setup_logging():
    log_formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )
    console_handler = logging.StreamHandler()  # Logs to stdout, which is captured by CloudWatch
    console_handler.setFormatter(log_formatter)
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler],  # Only use the console handler
    )


def create_setup_app() -> FastAPI:
    setup_app = FastAPI(
        title="BahirBits Data Service and Setup API",
        description="Setup API for managing clients, products, and rules",
        version="1.0.0",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",

    )

    # Add CORS middleware
    setup_app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("ALLOWED_ORIGIN", "*")],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    # Include Routers
    setup_app.include_router(
        client_router,
        prefix="/api/v1/setup/clients",
        tags=["Setup - Clients"],
    )
    setup_app.include_router(
        product_router,
        prefix="/api/v1/setup/products",
        tags=["Setup - Products"],
        # dependencies=[Depends(get_current_user)],
    )
    setup_app.include_router(
        rules_router,
        prefix="/api/v1/setup/rules",
        tags=["Setup - Rules"],
        # dependencies=[Depends(get_current_user)],
    )
    setup_app.include_router(
        client_product_router,
        prefix="/api/v1/setup/client_product_categories",
        tags=["Setup - Clients - ProductCategories"],
    )
    setup_app.include_router(
        productcategory_product_router,
        prefix="/api/v1/setup/product_categories_products",
        tags=["Setup - ProductCategories - Products"],
    )
    # -------------------------------------------
    # Add the customer_profile_data router here:
    setup_app.include_router(
        customer_profile_data,
        prefix="/api/v1/userdata/customer_profile",
        tags=["UserData - Customer Profile"],
    )

    setup_app.include_router(
        auth_router, prefix="/api/v1/auth", tags=["Authentication"])
    @setup_app.get("/", tags=["Health Check"])
    async def root():
        return {"message": "Welcome to the data service and Setup API", "status": "healthy"}
    return setup_app

setup_app = create_setup_app()

def run_server():
    setup_logging()
    uvicorn.run(
        setup_app,
        host="0.0.0.0",
        port=8003,
        log_level="debug",
        workers=2,
        reload=True,
        timeout_keep_alive=120,
    )

if __name__ == "__main__":
    setup_logging()
    run_server()
