#!.venv/bin/python

from pytorch_lightning.cli import LightningCLI

from model import LightningModel
from datamodule import DataModule

cli = LightningCLI(
    LightningModel,
    DataModule,
    parser_kwargs={"parser_mode": "omegaconf"},
)
