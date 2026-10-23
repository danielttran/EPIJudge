"""Graph primitives and the explicit shared parent-linked tree-node API."""
from models08 import declare as typed_declare,header as base_header,TYPES
from core import starter_body

TREE_INPUT_REFS=('4.4','4.5','4.6','4.8','4.10','4.12')
TREE_OUTPUT_REFS=('4.2','4.3','4.9')
TREE_REFS=TREE_INPUT_REFS+TREE_OUTPUT_REFS
TREE={
 'csharp':'public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}\n',
 'java':'class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}\n',
 'cpp':'struct TreeNode {int Data;TreeNode* Left;TreeNode* Right;TreeNode* Parent;explicit TreeNode(int data):Data(data),Left(nullptr),Right(nullptr),Parent(nullptr){}};\n',
 'python':'class TreeNode:\n    def __init__(self, data: int):\n        self.Data = data\n        self.Left = self.Right = self.Parent = None\n',
 'javascript':'class TreeNode {constructor(data){this.Data=data;this.Left=this.Right=this.Parent=null;}}\n'}
for _language,_type in {'csharp':'TreeNode?','java':'TreeNode','cpp':'TreeNode*','python':'TreeNode | None'}.items():TYPES[_language]['tree']=_type

DEPTH={
 'csharp':'public class DepthLink {public TreeNode Value;public DepthLink? Next;public DepthLink(TreeNode value){Value=value;}}\n',
 'java':'class DepthLink {public TreeNode Value;public DepthLink Next;public DepthLink(TreeNode value){Value=value;}}\n',
 'cpp':'struct DepthLink {TreeNode* Value;DepthLink* Next;explicit DepthLink(TreeNode* value):Value(value),Next(nullptr){}};\n',
 'python':'class DepthLink:\n    def __init__(self, value: TreeNode):\n        self.Value = value\n        self.Next = None\n',
 'javascript':'class DepthLink {constructor(value){this.Value=value;this.Next=null;}}\n'}
for _language,_types in TYPES.items():
    _types['newtree']=_types['tree']
    _types['depths']={'csharp':'List<DepthLink>','java':'List<DepthLink>','cpp':'std::vector<DepthLink*>','python':'list[DepthLink]'}[_language]
    _types['sequences']=_types['sets']

def reference(ref,language):
    return (TREE[language] if ref in TREE_REFS else '')+(DEPTH[language] if ref=='4.3' else '')

def declare(spec,language,body,class_name='Solution'):

    return typed_declare(spec,language,body,class_name)

def header(ref,language):
    return base_header(ref,language)+((('#include <unordered_map>\n' if language=='cpp' else '')+reference(ref,language)) if ref in TREE_REFS else '')

def neutral(spec,language):
    if spec['result'] in ('tree','newtree'):return 'return None' if language=='python' else 'return nullptr;' if language=='cpp' else 'return null;'
    if spec['result'] in ('depths','sequences'):
        return 'return new ArrayList<>();' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    if spec['result']=='ai':
        return 'return new int[0];' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    return starter_body(spec,language)
