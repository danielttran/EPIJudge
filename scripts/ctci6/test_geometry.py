import unittest
from corpus_geometry import oracle,valid_observation

class GeometryTests(unittest.TestCase):
    def valid(self,ref,args,actual):return valid_observation(ref,dict(arguments=args,expected=oracle(ref,args)),dict(actual=actual,mutationOk=True))
    def test_unique_crossing_fraction_and_point_segments(self):
        args=[[[0,0],[3,3],[0,2],[3,0]]]
        self.assertTrue(self.valid('16.3',args,[1.2,1.2]));self.assertFalse(self.valid('16.3',args,[1,1]))
        self.assertTrue(self.valid('16.3',[[[1,1],[1,1],[0,0],[2,2]]],[1,1]))
        self.assertTrue(self.valid('16.3',[[[1,1],[1,1],[2,2],[2,2]]],[]))
    def test_arbitrary_overlap_point_and_vertical_overlap(self):
        args=[[[0,0],[4,0],[2,0],[6,0]]]
        for point in ([2,0],[3,0],[4,0]):self.assertTrue(self.valid('16.3',args,point))
        for point in ([1,0],[5,0],[3,1]):self.assertFalse(self.valid('16.3',args,point))
        self.assertTrue(self.valid('16.3',[[[0,4],[0,0],[0,1],[0,3]]],[0,2]))
    def test_infinite_line_crossing_outside_segments(self):
        self.assertTrue(self.valid('16.3',[[[0,0],[1,1],[2,0],[2,3]]],[]))
    def test_square_full_span_and_endpoint_order(self):
        args=[[[0,0,2],[4,0,2]]]
        for actual in ([0,1,6,1],[6,1,0,1]):self.assertTrue(self.valid('16.13',args,actual))
        for actual in ([1,1,5,1],[0,0,6,0],[0,1,2,1]):self.assertFalse(self.valid('16.13',args,actual))
    def test_concentric_all_directions_and_nested_radius(self):
        args=[[[0,0,4],[1,1,2]]]
        for actual in ([0,2,4,2],[2,0,2,4],[0,0,4,4],[4,4,0,0]):self.assertTrue(self.valid('16.13',args,actual))
        for actual in ([1,2,3,2],[0,0,0,0],[0,1,4,1]):self.assertFalse(self.valid('16.13',args,actual))
    def test_finite_and_typed_coordinates(self):
        for actual in ([True,1],[float('nan'),1],[1,float('inf')]):self.assertFalse(self.valid('16.3',[[[1,1]]*4],actual))

if __name__=='__main__':unittest.main()
