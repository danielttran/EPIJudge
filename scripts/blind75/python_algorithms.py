"""Efficient Python reference fixtures, independent of the brute-force corpus oracle."""
HELPERS='''
from collections import Counter, defaultdict, deque
from bisect import bisect_left
from heapq import heappop, heappush

def word_exists(board,word):
    rows,cols=len(board),len(board[0]);used=set()
    def visit(r,c,i):
        if not(0<=r<rows and 0<=c<cols) or (r,c) in used or board[r][c]!=word[i]:return False
        if i==len(word)-1:return True
        used.add((r,c));found=any(visit(r+dr,c+dc,i+1) for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]);used.remove((r,c));return found
    return any(visit(r,c,0) for r in range(rows) for c in range(cols))

def component_count(n,edges):
    parent=list(range(n));count=n
    def find(v):
        while v!=parent[v]:parent[v]=parent[parent[v]];v=parent[v]
        return v
    for u,v in edges:
        a,b=find(u),find(v)
        if a!=b:parent[a]=b;count-=1
    return count
'''
B={}
def add(method,body):B[method]=body
add('TwoSum','''seen={}
for i,v in enumerate(nums):
    if target-v in seen:return [seen[target-v],i]
    seen[v]=i
return []''')
add('ContainsDuplicate','return len(set(nums))<len(nums)')
add('TopKFrequent','return [v for v,_ in Counter(nums).most_common(k)]')
add('ProductExceptSelf','''out=[];product=1
for v in nums:out.append(product);product*=v
product=1
for i in range(len(nums)-1,-1,-1):out[i]*=product;product*=nums[i]
return out''')
add('LongestConsecutive','''seen=set(nums);best=0
for v in seen:
    if v-1 not in seen:
        end=v
        while end in seen:end+=1
        best=max(best,end-v)
return best''')
add('ThreeSum','''nums=sorted(nums);out=[]
for i in range(len(nums)):
    if i and nums[i]==nums[i-1]:continue
    l,r=i+1,len(nums)-1
    while l<r:
        value=nums[i]+nums[l]+nums[r]
        if value<0:l+=1
        elif value>0:r-=1
        else:
            out.append([nums[i],nums[l],nums[r]]);x,y=nums[l],nums[r]
            while l<r and nums[l]==x:l+=1
            while l<r and nums[r]==y:r-=1
return out''')
add('MaxArea','''l,r,best=0,len(height)-1,0
while l<r:
    best=max(best,(r-l)*min(height[l],height[r]))
    if height[l]<height[r]:l+=1
    else:r-=1
return best''')
add('MaxProfit','''low=prices[0];best=0
for p in prices:best=max(best,p-low);low=min(low,p)
return best''')
add('CombinationSum','''out=[];path=[]
def visit(i,remaining):
    if remaining==0:out.append(path[:]);return
    for j in range(i,len(candidates)):
        if candidates[j]<=remaining:path.append(candidates[j]);visit(j,remaining-candidates[j]);path.pop()
visit(0,target)
return out''')
add('Merge','''out=[]
for start,end in sorted(intervals):
    if out and start<=out[-1][1]:out[-1][1]=max(end,out[-1][1])
    else:out.append([start,end])
return out''')
add('Insert',B['Merge'].replace('sorted(intervals)','sorted(intervals+[newInterval])'))
add('EraseOverlapIntervals','''end=float('-inf');kept=0
for start,finish in sorted(intervals,key=lambda row:row[1]):
    if start>=end:end=finish;kept+=1
return len(intervals)-kept''')
add('CanAttendMeetings','''rows=sorted(intervals)
return all(rows[i-1][1]<=rows[i][0] for i in range(1,len(rows)))''')
add('MinMeetingRooms','''active=best=0
for _,delta in sorted([(s,1) for s,e in intervals]+[(e,-1) for s,e in intervals]):active+=delta;best=max(best,active)
return best''')
add('MissingNumber','''missing=len(nums)
for i,v in enumerate(nums):missing^=i^v
return missing''')
add('IsAnagram','return Counter(s)==Counter(t)')
add('GroupAnagrams','''groups=defaultdict(list)
for s in strs:groups[''.join(sorted(s))].append(s)
return list(groups.values())''')
add('IsPalindrome','''a=''.join(c.lower() for c in s if c.isascii() and c.isalnum())
return a==a[::-1]''')
add('LengthOfLongestSubstring','''last={};left=best=0
for i,c in enumerate(s):left=max(left,last.get(c,-1)+1);last[c]=i;best=max(best,i-left+1)
return best''')
add('CharacterReplacement','''counts=Counter();left=most=best=0
for r,c in enumerate(s):
    counts[c]+=1;most=max(most,counts[c])
    while r-left+1-most>k:counts[s[left]]-=1;left+=1
    best=max(best,r-left+1)
return best''')
add('MinWindow','''need=Counter(t);missing=len(t);left=start=0;length=len(s)+1
for r,c in enumerate(s):
    if need[c]>0:missing-=1
    need[c]-=1
    while missing==0:
        if r-left+1<length:start=left;length=r-left+1
        need[s[left]]+=1
        if need[s[left]]>0:missing+=1
        left+=1
return '' if length>len(s) else s[start:start+length]''')
add('LongestPalindrome','''start=length=0
for i in range(len(s)):
    for parity in [0,1]:
        l,r=i,i+parity
        while l>=0 and r<len(s) and s[l]==s[r]:
            if r-l+1>length or r-l+1==length and l<start:start=l;length=r-l+1
            l-=1;r+=1
return s[start:start+length]''')
add('CountSubstrings','''count=0
for i in range(len(s)):
    for parity in [0,1]:
        l,r=i,i+parity
        while l>=0 and r<len(s) and s[l]==s[r]:count+=1;l-=1;r+=1
return count''')
add('IsValid','''stack=[];pairs={')':'(',']':'[','}':'{'}
for c in s:
    if c in '([{':stack.append(c)
    elif not stack or stack.pop()!=pairs[c]:return False
return not stack''')
add('SpiralOrder','''top,bottom,left,right=0,len(matrix)-1,0,len(matrix[0])-1;out=[]
while top<=bottom and left<=right:
    out.extend(matrix[top][c] for c in range(left,right+1));top+=1
    out.extend(matrix[r][right] for r in range(top,bottom+1));right-=1
    if top<=bottom:out.extend(matrix[bottom][c] for c in range(right,left-1,-1));bottom-=1
    if left<=right:out.extend(matrix[r][left] for r in range(bottom,top-1,-1));left+=1
return out''')
add('FindMin','''l,r=0,len(nums)-1
while l<r:
    mid=(l+r)//2
    if nums[mid]>nums[r]:l=mid+1
    else:r=mid
return nums[l]''')
add('Search','''l,r=0,len(nums)-1
while l<=r:
    mid=(l+r)//2
    if nums[mid]==target:return mid
    if nums[l]<=nums[mid]:
        if nums[l]<=target<nums[mid]:r=mid-1
        else:l=mid+1
    else:
        if nums[mid]<target<=nums[r]:l=mid+1
        else:r=mid-1
return -1''')
add('Exist','return word_exists(board,word)')
add('FindWords','''trie={}
for word in words:
    node=trie
    for c in word:node=node.setdefault(c,{})
    node['$']=word
rows,cols=len(board),len(board[0]);used=set();out=[]
def visit(r,c,node):
    if not(0<=r<rows and 0<=c<cols) or (r,c) in used:return
    ch=board[r][c]
    if ch not in node:return
    child=node[ch]
    if '$' in child:out.append(child.pop('$'))
    used.add((r,c))
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:visit(r+dr,c+dc,child)
    used.remove((r,c))
    if not child:del node[ch]
for r in range(rows):
    for c in range(cols):visit(r,c,trie)
return out''')
add('NumIslands','''rows,cols=len(grid),len(grid[0]);seen=set();count=0
for r in range(rows):
    for c in range(cols):
        if grid[r][c]!='1' or (r,c) in seen:continue
        count+=1;seen.add((r,c));q=deque([(r,c)])
        while q:
            i,j=q.popleft()
            for u,v in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
                if 0<=u<rows and 0<=v<cols and grid[u][v]=='1' and (u,v) not in seen:seen.add((u,v));q.append((u,v))
return count''')
add('PacificAtlantic','''rows,cols=len(heights),len(heights[0])
def flood(cells):
    seen=set(cells);q=deque(seen)
    while q:
        r,c=q.popleft()
        for u,v in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
            if 0<=u<rows and 0<=v<cols and (u,v) not in seen and heights[u][v]>=heights[r][c]:seen.add((u,v));q.append((u,v))
    return seen
a=flood([(r,0) for r in range(rows)]+[(0,c) for c in range(cols)])
b=flood([(r,cols-1) for r in range(rows)]+[(rows-1,c) for c in range(cols)])
return [list(p) for p in sorted(a&b)]''')
add('CanFinish','''graph=[[] for _ in range(numCourses)];degree=[0]*numCourses
for a,b in prerequisites:graph[b].append(a);degree[a]+=1
q=deque(i for i in range(numCourses) if degree[i]==0);count=0
while q:
    v=q.popleft();count+=1
    for u in graph[v]:
        degree[u]-=1
        if degree[u]==0:q.append(u)
return count==numCourses''')
add('CountComponents','return component_count(n,edges)')
add('ValidTree','return n>0 and len(edges)==n-1 and component_count(n,edges)==1')
add('AlienOrder','''graph={c:set() for w in words for c in w}
for a,b in zip(words,words[1:]):
    for x,y in zip(a,b):
        if x!=y:graph[x].add(y);break
    else:
        if len(a)>len(b):return ''
degree={c:0 for c in graph}
for row in graph.values():
    for c in row:degree[c]+=1
ready=[]
for c,d in degree.items():
    if d==0:heappush(ready,c)
out=[]
while ready:
    c=heappop(ready);out.append(c)
    for v in graph[c]:
        degree[v]-=1
        if degree[v]==0:heappush(ready,v)
return ''.join(out) if len(out)==len(graph) else '' ''')
add('ClimbStairs','''a=b=1
for _ in range(1,n):a,b=b,a+b
return b''')
add('Rob','''def run(values):
    a=b=0
    for v in values:a,b=b,max(b,a+v)
    return b
return run(nums)''')
add('NumDecodings','''a,b=1,int(s[0]!='0')
for i in range(1,len(s)):
    value=b if s[i]!='0' else 0
    if 10<=int(s[i-1:i+1])<=26:value+=a
    a,b=b,value
return b''')
add('CoinChange','''dp=[0]+[amount+1]*amount
for v in range(1,amount+1):
    for c in coins:
        if c<=v:dp[v]=min(dp[v],dp[v-c]+1)
return dp[amount] if dp[amount]<=amount else -1''')
add('MaxProduct','''high=low=best=nums[0]
for v in nums[1:]:
    a,b=high*v,low*v;high=max(v,a,b);low=min(v,a,b);best=max(best,high)
return best''')
add('WordBreak','''possible=[True]+[False]*len(s)
for i in range(len(s)):
    if possible[i]:
        for word in wordDict:
            if s.startswith(word,i):possible[i+len(word)]=True
return possible[-1]''')
add('LengthOfLIS','''tails=[]
for v in nums:
    i=bisect_left(tails,v)
    if i==len(tails):tails.append(v)
    else:tails[i]=v
return len(tails)''')
add('UniquePaths','''dp=[1]*n
for _ in range(1,m):
    for c in range(1,n):dp[c]+=dp[c-1]
return dp[-1]''')
add('CanJump','''far=0
for i,v in enumerate(nums):
    if i>far:return False
    far=max(far,i+v)
return True''')
add('CombinationSum4','''dp=[1]+[0]*target
for v in range(1,target+1):dp[v]=sum(dp[v-c] for c in nums if c<=v)
return dp[target]''')
add('MaxSubArray','''ending=best=nums[0]
for v in nums[1:]:ending=max(v,ending+v);best=max(best,ending)
return best''')
add('HammingWeight','return n.bit_count()')
add('CountBits','return [i.bit_count() for i in range(n+1)]')
add('ReverseBits',"return int(f'{n:032b}'[::-1],2)")
add('GetSum','''mask=0xffffffff
a&=mask;b&=mask
while b:a,b=(a^b)&mask,((a&b)<<1)&mask
return a if a<=0x7fffffff else ~(a^mask)''')

def body(s):
    result=B.get(s['method'])
    if result is None:return None
    if s['method']=='Rob' and s['title']=='House Robber II':result=result.replace('return run(nums)','return (nums[0] if nums else 0) if len(nums)<=1 else max(run(nums[:-1]),run(nums[1:]))')
    return {s['method']:result.rstrip()}
