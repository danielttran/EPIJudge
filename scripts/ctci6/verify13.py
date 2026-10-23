"""Run actual functional aggregation implementations and neutral starters."""
from chapter13 import SPECS
from corpus13 import cases,valid_observation
from generate13 import generate13
from harness13 import source
from verify08 import verify
if __name__=='__main__':verify(specs=SPECS,batch=13,generator=generate13,case_builder=cases,matcher=valid_observation,adapter=source)
