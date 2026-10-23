"""Reuse the existing standalone validation loop for the moderate batch."""
from chapter10 import SPECS
from corpus10 import cases, valid_observation
from generate10 import generate10
from harness10 import source
from verify08 import verify

if __name__ == '__main__':
    verify(specs=SPECS,batch=10,generator=generate10,case_builder=cases,matcher=valid_observation,adapter=source)
