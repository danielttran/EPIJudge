"""Graph primitives and the explicit shared parent-linked tree-node API."""
from models08 import declare as typed_declare,header as base_header,TYPES
from core import starter_body

TREE_REFS=('4.4','4.5','4.6','4.8','4.10','4.12')
TREE={
 'csharp':'public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}\n',
 'java':'class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}\n',
 'cpp':'struct TreeNode {int Data;TreeNode* Left;TreeNode* Right;TreeNode* Parent;explicit TreeNode(int data):Data(data),Left(nullptr),Right(nullptr),Parent(nullptr){}};\n',
 'python':'class TreeNode:\n    def __init__(self, data: int):\n        self.Data = data\n        self.Left = self.Right = self.Parent = None\n',
 'javascript':'class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}\n'}
for _language,_type in {'csharp':'TreeNode?','java':'TreeNode','cpp':'TreeNode*','python':'TreeNode | None'}.items():TYPES[_language]['tree']=_type

def declare(spec,language,body,class_name='Solution'):
    return typed_declare(spec,language,body,class_name)

def header(ref,language):
    return base_header(ref,language)+((('#include <unordered_map>\n' if language=='cpp' else '')+TREE[language]) if ref in TREE_REFS else '')

def neutral(spec,language):
    if spec['result']=='tree':return 'return None' if language=='python' else 'return nullptr;' if language=='cpp' else 'return null;'
    if spec['result']=='ai':
        return 'return new int[0];' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    return starter_body(spec,language)
