"""The same original links change from left/right to previous/next."""
from models08 import TYPES
BINODE={
'csharp':'public class BiNode { public int Data; public BiNode? Node1; public BiNode? Node2; public BiNode(int data){Data=data;} }\n',
'java':'class BiNode { public int Data; public BiNode Node1; public BiNode Node2; public BiNode(int data){Data=data;} }\n',
'cpp':'struct BiNode { int Data; BiNode* Node1=nullptr; BiNode* Node2=nullptr; explicit BiNode(int data):Data(data){} };\n',
'python':'class BiNode:\n    def __init__(self,data: int):\n        self.Data=data\n        self.Node1: BiNode | None = None\n        self.Node2: BiNode | None = None\n',
'javascript':'class BiNode {constructor(data){this.Data=data;this.Node1=null;this.Node2=null;}}\n'}
for language,kind in [('csharp','BiNode?'),('java','BiNode'),('cpp','BiNode*'),('python','BiNode | None')]:TYPES[language]['binode']=kind
