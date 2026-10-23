"""Execute the graph batch through the established standalone loop."""
from chapter04 import SPECS
from corpus04 import cases,valid_observation
from generate04 import generate04
from harness04 import source
from verify08 import verify

if __name__=='__main__':verify(specs=SPECS,batch=4,generator=generate04,case_builder=cases,matcher=valid_observation,adapter=source)
