"""Reuse the existing standalone validation loop for the moderate batch."""
from chapter16 import SPECS
from corpus16 import cases, valid_observation
from generate16 import generate16
from harness16 import source
from verify08 import verify

if __name__ == '__main__':
    verify(specs=SPECS,batch=16,generator=generate16,case_builder=cases,matcher=valid_observation,adapter=source)
