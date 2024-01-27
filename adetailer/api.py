from typing import Callable
from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from adetailer import (
    api_models,
    get_models,
)

from modules import paths, shared

no_huggingface = getattr(shared.cmd_opts, "ad_no_huggingface", False)
adetailer_dir = Path(paths.models_path, "adetailer")
extra_models_dir = shared.opts.data.get("ad_extra_models_dir", "")


class Api:
    def __init__(self, app: FastAPI, prefix: str = None) -> None:

        self.app = app
        self.prefix = prefix

        self.add_api_route(
            'models',
            self.get_models,
            methods=['GET'],
            response_model=api_models.AdetailerModelResponse
        )

    def add_api_route(self, path: str, endpoint: Callable, **kwargs):
        if self.prefix:
            path = f'{self.prefix}/{path}'

        if shared.cmd_opts.api_auth:
            return self.app.add_api_route(path, endpoint, dependencies=[Depends(self.auth)], **kwargs)
        return self.app.add_api_route(path, endpoint, **kwargs)

    def get_models(self):
        model_mapping = get_models(
            adetailer_dir, extra_dir=extra_models_dir, huggingface=not no_huggingface
        )
        models = list(model_mapping.keys())
        response_data = {
            "models": models,
        }
        return api_models.AdetailerModelResponse(**response_data)


def on_app_started(_, app: FastAPI):
    Api(app, '/adetailer/v1')
