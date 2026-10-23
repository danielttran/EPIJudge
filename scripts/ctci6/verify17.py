"""Reuse the existing standalone validation loop for the moderate batch."""
from chapter17 import SPECS
from corpus17 import cases, valid_observation
from generate17 import generate17
from harness17 import source
from verify08 import verify

if __name__ == '__main__':
    verify(specs=SPECS,batch=17,generator=generate17,case_builder=cases,matcher=valid_observation,adapter=source)
