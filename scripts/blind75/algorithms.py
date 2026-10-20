"""Actual test-only implementations for all ordinary Blind 75 function contracts.

C#, JavaScript, C++ and Java implementations are independent of expected outputs.
Python fixtures use oracle.py's executable algorithms. Order below: CS, JS, CPP, Java.
"""
BODIES={}
def add(method,cs,js,cpp,java):BODIES[method]=(cs,js,cpp,java)

add('TwoSum',
'var seen=new Dictionary<int,int>();for(int i=0;i<nums.Length;i++){if(seen.TryGetValue(target-nums[i],out int j))return [j,i];seen[nums[i]]=i;}return [];',
'const seen=new Map();for(let i=0;i<nums.length;i++){if(seen.has(target-nums[i]))return [seen.get(target-nums[i]),i];seen.set(nums[i],i);}return [];',
'std::unordered_map<int,int>seen;for(int i=0;i<static_cast<int>(nums.size());i++){auto j=seen.find(target-nums[i]);if(j!=seen.end())return {j->second,i};seen[nums[i]]=i;}return {};',
'Map<Integer,Integer>seen=new HashMap<>();for(int i=0;i<nums.length;i++){Integer j=seen.get(target-nums[i]);if(j!=null)return new int[]{j,i};seen.put(nums[i],i);}return new int[0];')
add('ContainsDuplicate',
'return nums.Distinct().Count()!=nums.Length;',
'return new Set(nums).size!==nums.length;',
'return std::unordered_set<int>(nums.begin(),nums.end()).size()!=nums.size();',
'Set<Integer>seen=new HashSet<>();for(int v:nums)if(!seen.add(v))return true;return false;')
add('TopKFrequent',
'return nums.GroupBy(v=>v).OrderByDescending(g=>g.Count()).Take(k).Select(g=>g.Key).ToArray();',
'const counts=new Map();for(const v of nums)counts.set(v,(counts.get(v)||0)+1);return [...counts].sort((a,b)=>b[1]-a[1]).slice(0,k).map(p=>p[0]);',
'std::unordered_map<int,int>counts;for(int v:nums)counts[v]++;std::vector<std::pair<int,int>>a;for(auto p:counts)a.emplace_back(p.second,p.first);std::sort(a.rbegin(),a.rend());std::vector<int>out;for(int i=0;i<k;i++)out.push_back(a[i].second);return out;',
'Map<Integer,Integer>counts=new HashMap<>();for(int v:nums)counts.merge(v,1,Integer::sum);return counts.keySet().stream().sorted((a,b)->Integer.compare(counts.get(b),counts.get(a))).limit(k).mapToInt(v->v).toArray();')
add('ProductExceptSelf',
'var outp=new int[nums.Length];int product=1;for(int i=0;i<nums.Length;i++){outp[i]=product;product*=nums[i];}product=1;for(int i=nums.Length-1;i>=0;i--){outp[i]*=product;product*=nums[i];}return outp;',
'const out=Array(nums.length);let product=1;for(let i=0;i<nums.length;i++){out[i]=product;product*=nums[i];}product=1;for(let i=nums.length-1;i>=0;i--){out[i]*=product;product*=nums[i];}return out;',
'std::vector<int>out(nums.size());int product=1;for(size_t i=0;i<nums.size();i++){out[i]=product;product*=nums[i];}product=1;for(size_t i=nums.size();i-->0;){out[i]*=product;product*=nums[i];}return out;',
'int[]out=new int[nums.length];int product=1;for(int i=0;i<nums.length;i++){out[i]=product;product*=nums[i];}product=1;for(int i=nums.length-1;i>=0;i--){out[i]*=product;product*=nums[i];}return out;')
add('LongestConsecutive',
'var seen=nums.ToHashSet();int best=0;foreach(int v in seen)if(!seen.Contains(v-1)){int end=v;while(seen.Contains(end))end++;best=Math.Max(best,end-v);}return best;',
'const seen=new Set(nums);let best=0;for(const v of seen)if(!seen.has(v-1)){let end=v;while(seen.has(end))end++;best=Math.max(best,end-v);}return best;',
'std::unordered_set<int>seen(nums.begin(),nums.end());int best=0;for(int v:seen)if(!seen.count(v-1)){int end=v;while(seen.count(end))end++;best=std::max(best,end-v);}return best;',
'Set<Integer>seen=new HashSet<>();for(int v:nums)seen.add(v);int best=0;for(int v:seen)if(!seen.contains(v-1)){int end=v;while(seen.contains(end))end++;best=Math.max(best,end-v);}return best;')
add('ThreeSum',
'Array.Sort(nums);var outp=new List<int[]>();for(int i=0;i<nums.Length;i++){if(i>0&&nums[i]==nums[i-1])continue;int l=i+1,r=nums.Length-1;while(l<r){int sum=nums[i]+nums[l]+nums[r];if(sum<0)l++;else if(sum>0)r--;else{outp.Add([nums[i],nums[l],nums[r]]);int x=nums[l],y=nums[r];while(l<r&&nums[l]==x)l++;while(l<r&&nums[r]==y)r--;}}}return outp.ToArray();',
'nums.sort((a,b)=>a-b);const out=[];for(let i=0;i<nums.length;i++){if(i&&nums[i]===nums[i-1])continue;let l=i+1,r=nums.length-1;while(l<r){const sum=nums[i]+nums[l]+nums[r];if(sum<0)l++;else if(sum>0)r--;else{out.push([nums[i],nums[l],nums[r]]);const x=nums[l],y=nums[r];while(l<r&&nums[l]===x)l++;while(l<r&&nums[r]===y)r--;}}}return out;',
'std::sort(nums.begin(),nums.end());std::vector<std::vector<int>>out;for(int i=0;i<static_cast<int>(nums.size());i++){if(i&&nums[i]==nums[i-1])continue;int l=i+1,r=static_cast<int>(nums.size())-1;while(l<r){int sum=nums[i]+nums[l]+nums[r];if(sum<0)l++;else if(sum>0)r--;else{out.push_back({nums[i],nums[l],nums[r]});int x=nums[l],y=nums[r];while(l<r&&nums[l]==x)l++;while(l<r&&nums[r]==y)r--;}}}return out;',
'Arrays.sort(nums);List<int[]>out=new ArrayList<>();for(int i=0;i<nums.length;i++){if(i>0&&nums[i]==nums[i-1])continue;int l=i+1,r=nums.length-1;while(l<r){int sum=nums[i]+nums[l]+nums[r];if(sum<0)l++;else if(sum>0)r--;else{out.add(new int[]{nums[i],nums[l],nums[r]});int x=nums[l],y=nums[r];while(l<r&&nums[l]==x)l++;while(l<r&&nums[r]==y)r--;}}}return out.toArray(int[][]::new);')
add('MaxArea',
'int l=0,r=height.Length-1,best=0;while(l<r){best=Math.Max(best,(r-l)*Math.Min(height[l],height[r]));if(height[l]<height[r])l++;else r--;}return best;',
'let l=0,r=height.length-1,best=0;while(l<r){best=Math.max(best,(r-l)*Math.min(height[l],height[r]));if(height[l]<height[r])l++;else r--;}return best;',
'int l=0,r=static_cast<int>(height.size())-1,best=0;while(l<r){best=std::max(best,(r-l)*std::min(height[l],height[r]));if(height[l]<height[r])l++;else r--;}return best;',
'int l=0,r=height.length-1,best=0;while(l<r){best=Math.max(best,(r-l)*Math.min(height[l],height[r]));if(height[l]<height[r])l++;else r--;}return best;')
add('MaxProfit',
'int low=prices[0],best=0;foreach(int p in prices){best=Math.Max(best,p-low);low=Math.Min(low,p);}return best;',
'let low=prices[0],best=0;for(const p of prices){best=Math.max(best,p-low);low=Math.min(low,p);}return best;',
'int low=prices[0],best=0;for(int p:prices){best=std::max(best,p-low);low=std::min(low,p);}return best;',
'int low=prices[0],best=0;for(int p:prices){best=Math.max(best,p-low);low=Math.min(low,p);}return best;')
add('CombinationSum',
'var outp=new List<int[]>();var path=new List<int>();void Visit(int start,int remaining){if(remaining==0){outp.Add(path.ToArray());return;}for(int i=start;i<candidates.Length;i++)if(candidates[i]<=remaining){path.Add(candidates[i]);Visit(i,remaining-candidates[i]);path.RemoveAt(path.Count-1);}}Visit(0,target);return outp.ToArray();',
'const out=[],path=[];function visit(start,remaining){if(remaining===0){out.push([...path]);return;}for(let i=start;i<candidates.length;i++)if(candidates[i]<=remaining){path.push(candidates[i]);visit(i,remaining-candidates[i]);path.pop();}}visit(0,target);return out;',
'std::vector<std::vector<int>>out;std::vector<int>path;std::function<void(int,int)>visit=[&](int start,int remaining){if(!remaining){out.push_back(path);return;}for(int i=start;i<static_cast<int>(candidates.size());i++)if(candidates[i]<=remaining){path.push_back(candidates[i]);visit(i,remaining-candidates[i]);path.pop_back();}};visit(0,target);return out;',
'List<int[]>out=new ArrayList<>();List<Integer>path=new ArrayList<>();class Search{void visit(int start,int remaining){if(remaining==0){out.add(path.stream().mapToInt(v->v).toArray());return;}for(int i=start;i<candidates.length;i++)if(candidates[i]<=remaining){path.add(candidates[i]);visit(i,remaining-candidates[i]);path.remove(path.size()-1);}}}new Search().visit(0,target);return out.toArray(int[][]::new);')
add('Merge',
'var outp=new List<int[]>();foreach(var row in intervals.OrderBy(r=>r[0])){if(outp.Count>0&&row[0]<=outp[^1][1])outp[^1][1]=Math.Max(outp[^1][1],row[1]);else outp.Add(row.ToArray());}return outp.ToArray();',
'const out=[];for(const row of [...intervals].sort((a,b)=>a[0]-b[0])){if(out.length&&row[0]<=out.at(-1)[1])out.at(-1)[1]=Math.max(out.at(-1)[1],row[1]);else out.push([...row]);}return out;',
'auto rows=intervals;std::sort(rows.begin(),rows.end());std::vector<std::vector<int>>out;for(auto row:rows){if(!out.empty()&&row[0]<=out.back()[1])out.back()[1]=std::max(out.back()[1],row[1]);else out.push_back(row);}return out;',
'int[][]rows=intervals.clone();Arrays.sort(rows,Comparator.comparingInt(r->r[0]));List<int[]>out=new ArrayList<>();for(int[]row:rows){if(!out.isEmpty()&&row[0]<=out.get(out.size()-1)[1])out.get(out.size()-1)[1]=Math.max(out.get(out.size()-1)[1],row[1]);else out.add(row.clone());}return out.toArray(int[][]::new);')
add('Insert',
'var all=intervals.Append(newInterval).ToArray();var outp=new List<int[]>();foreach(var row in all.OrderBy(r=>r[0])){if(outp.Count>0&&row[0]<=outp[^1][1])outp[^1][1]=Math.Max(outp[^1][1],row[1]);else outp.Add(row.ToArray());}return outp.ToArray();',
'const out=[];for(const row of [...intervals,newInterval].sort((a,b)=>a[0]-b[0])){if(out.length&&row[0]<=out.at(-1)[1])out.at(-1)[1]=Math.max(out.at(-1)[1],row[1]);else out.push([...row]);}return out;',
'auto rows=intervals;rows.push_back(newInterval);std::sort(rows.begin(),rows.end());std::vector<std::vector<int>>out;for(auto row:rows){if(!out.empty()&&row[0]<=out.back()[1])out.back()[1]=std::max(out.back()[1],row[1]);else out.push_back(row);}return out;',
'int[][]rows=Arrays.copyOf(intervals,intervals.length+1);rows[intervals.length]=newInterval;Arrays.sort(rows,Comparator.comparingInt(r->r[0]));List<int[]>out=new ArrayList<>();for(int[]row:rows){if(!out.isEmpty()&&row[0]<=out.get(out.size()-1)[1])out.get(out.size()-1)[1]=Math.max(out.get(out.size()-1)[1],row[1]);else out.add(row.clone());}return out.toArray(int[][]::new);')
add('EraseOverlapIntervals',
'int end=int.MinValue,kept=0;foreach(var row in intervals.OrderBy(r=>r[1]))if(row[0]>=end){kept++;end=row[1];}return intervals.Length-kept;',
'let end=-Infinity,kept=0;for(const row of [...intervals].sort((a,b)=>a[1]-b[1]))if(row[0]>=end){kept++;end=row[1];}return intervals.length-kept;',
'auto rows=intervals;std::sort(rows.begin(),rows.end(),[](auto&a,auto&b){return a[1]<b[1];});int end=INT32_MIN,kept=0;for(auto row:rows)if(row[0]>=end){kept++;end=row[1];}return static_cast<int>(rows.size())-kept;',
'int[][]rows=intervals.clone();Arrays.sort(rows,Comparator.comparingInt(r->r[1]));int end=Integer.MIN_VALUE,kept=0;for(int[]row:rows)if(row[0]>=end){kept++;end=row[1];}return rows.length-kept;')
add('CanAttendMeetings',
'var rows=intervals.OrderBy(r=>r[0]).ToArray();for(int i=1;i<rows.Length;i++)if(rows[i][0]<rows[i-1][1])return false;return true;',
'const rows=[...intervals].sort((a,b)=>a[0]-b[0]);return rows.every((row,i)=>i===0||rows[i-1][1]<=row[0]);',
'auto rows=intervals;std::sort(rows.begin(),rows.end());for(size_t i=1;i<rows.size();i++)if(rows[i][0]<rows[i-1][1])return false;return true;',
'int[][]rows=intervals.clone();Arrays.sort(rows,Comparator.comparingInt(r->r[0]));for(int i=1;i<rows.length;i++)if(rows[i][0]<rows[i-1][1])return false;return true;')
add('MinMeetingRooms',
'var events=intervals.SelectMany(row=>new[]{(time:row[0],delta:1),(time:row[1],delta:-1)}).OrderBy(e=>e.time).ThenBy(e=>e.delta);int active=0,best=0;foreach(var e in events){active+=e.delta;best=Math.Max(best,active);}return best;',
'const events=intervals.flatMap(([s,e])=>[[s,1],[e,-1]]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);let active=0,best=0;for(const [,d] of events){active+=d;best=Math.max(best,active);}return best;',
'std::vector<std::pair<int,int>>events;for(auto row:intervals){events.emplace_back(row[0],1);events.emplace_back(row[1],-1);}std::sort(events.begin(),events.end());int active=0,best=0;for(auto e:events){active+=e.second;best=std::max(best,active);}return best;',
'List<int[]>events=new ArrayList<>();for(int[]row:intervals){events.add(new int[]{row[0],1});events.add(new int[]{row[1],-1});}events.sort((a,b)->a[0]==b[0]?Integer.compare(a[1],b[1]):Integer.compare(a[0],b[0]));int active=0,best=0;for(int[]e:events){active+=e[1];best=Math.max(best,active);}return best;')
add('MissingNumber',
'int missing=nums.Length;for(int i=0;i<nums.Length;i++)missing^=i^nums[i];return missing;',
'let missing=nums.length;for(let i=0;i<nums.length;i++)missing^=i^nums[i];return missing;',
'int missing=static_cast<int>(nums.size());for(int i=0;i<static_cast<int>(nums.size());i++)missing^=i^nums[i];return missing;',
'int missing=nums.length;for(int i=0;i<nums.length;i++)missing^=i^nums[i];return missing;')
add('IsAnagram',
'return s.Order().SequenceEqual(t.Order());',
'return [...s].sort().join("")===[...t].sort().join("");',
'std::sort(s.begin(),s.end());std::sort(t.begin(),t.end());return s==t;',
'char[]a=s.toCharArray(),b=t.toCharArray();Arrays.sort(a);Arrays.sort(b);return Arrays.equals(a,b);')
add('GroupAnagrams',
'return strs.GroupBy(s=>new string(s.Order().ToArray())).Select(g=>g.ToArray()).ToArray();',
'const groups=new Map();for(const s of strs){const key=[...s].sort().join("");if(!groups.has(key))groups.set(key,[]);groups.get(key).push(s);}return [...groups.values()];',
'std::map<std::string,std::vector<std::string>>groups;for(auto s:strs){auto key=s;std::sort(key.begin(),key.end());groups[key].push_back(s);}std::vector<std::vector<std::string>>out;for(auto p:groups)out.push_back(p.second);return out;',
'Map<String,List<String>>groups=new HashMap<>();for(String s:strs){char[]c=s.toCharArray();Arrays.sort(c);groups.computeIfAbsent(new String(c),k->new ArrayList<>()).add(s);}return groups.values().stream().map(g->g.toArray(String[]::new)).toArray(String[][]::new);')
add('IsPalindrome',
'var a=s.Where(c=>c is >=\'a\' and <=\'z\' or >=\'A\' and <=\'Z\' or >=\'0\' and <=\'9\').Select(char.ToLowerInvariant).ToArray();return a.SequenceEqual(a.Reverse());',
'const a=s.toLowerCase().replace(/[^a-z0-9]/g,"");return a===[...a].reverse().join("");',
'std::string a;for(unsigned char c:s)if((c>=\'a\'&&c<=\'z\')||(c>=\'A\'&&c<=\'Z\')||(c>=\'0\'&&c<=\'9\'))a.push_back(c>=\'A\'&&c<=\'Z\'?c-\'A\'+\'a\':c);auto b=a;std::reverse(b.begin(),b.end());return a==b;',
'String a=s.toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9]","");return a.contentEquals(new StringBuilder(a).reverse());')
add('LengthOfLongestSubstring',
'var last=new Dictionary<char,int>();int left=0,best=0;for(int i=0;i<s.Length;i++){if(last.TryGetValue(s[i],out int j))left=Math.Max(left,j+1);last[s[i]]=i;best=Math.Max(best,i-left+1);}return best;',
'const last=new Map();let left=0,best=0;for(let i=0;i<s.length;i++){if(last.has(s[i]))left=Math.max(left,last.get(s[i])+1);last.set(s[i],i);best=Math.max(best,i-left+1);}return best;',
'std::array<int,128>last;last.fill(-1);int left=0,best=0;for(int i=0;i<static_cast<int>(s.size());i++){auto c=static_cast<unsigned char>(s[i]);left=std::max(left,last[c]+1);last[c]=i;best=std::max(best,i-left+1);}return best;',
'int[]last=new int[128];Arrays.fill(last,-1);int left=0,best=0;for(int i=0;i<s.length();i++){char c=s.charAt(i);left=Math.max(left,last[c]+1);last[c]=i;best=Math.max(best,i-left+1);}return best;')
add('CharacterReplacement',
'var counts=new int[26];int left=0,most=0,best=0;for(int r=0;r<s.Length;r++){most=Math.Max(most,++counts[s[r]-\'A\']);while(r-left+1-most>k)counts[s[left++]-\'A\']--;best=Math.Max(best,r-left+1);}return best;',
'const counts=Array(26).fill(0);let left=0,most=0,best=0;for(let r=0;r<s.length;r++){most=Math.max(most,++counts[s.charCodeAt(r)-65]);while(r-left+1-most>k)counts[s.charCodeAt(left++)-65]--;best=Math.max(best,r-left+1);}return best;',
'std::array<int,26>counts{};int left=0,most=0,best=0;for(int r=0;r<static_cast<int>(s.size());r++){most=std::max(most,++counts[s[r]-\'A\']);while(r-left+1-most>k)counts[s[left++]-\'A\']--;best=std::max(best,r-left+1);}return best;',
'int[]counts=new int[26];int left=0,most=0,best=0;for(int r=0;r<s.length();r++){most=Math.max(most,++counts[s.charAt(r)-\'A\']);while(r-left+1-most>k)counts[s.charAt(left++)-\'A\']--;best=Math.max(best,r-left+1);}return best;')
add('MinWindow',
'var need=new int[128];foreach(char c in t)need[c]++;int missing=t.Length,left=0,start=0,length=int.MaxValue;for(int r=0;r<s.Length;r++){if(need[s[r]]-->0)missing--;while(missing==0){if(r-left+1<length){start=left;length=r-left+1;}if(++need[s[left++]]>0)missing++;}}return length==int.MaxValue?"":s.Substring(start,length);',
'const need=Array(128).fill(0);for(const c of t)need[c.charCodeAt(0)]++;let missing=t.length,left=0,start=0,length=Infinity;for(let r=0;r<s.length;r++){if(need[s.charCodeAt(r)]-->0)missing--;while(missing===0){if(r-left+1<length){start=left;length=r-left+1;}if(++need[s.charCodeAt(left++)]>0)missing++;}}return length===Infinity?"":s.slice(start,start+length);',
'std::array<int,128>need{};for(unsigned char c:t)need[c]++;int missing=static_cast<int>(t.size()),left=0,start=0,length=INT32_MAX;for(int r=0;r<static_cast<int>(s.size());r++){if(need[static_cast<unsigned char>(s[r])]-->0)missing--;while(!missing){if(r-left+1<length){start=left;length=r-left+1;}if(++need[static_cast<unsigned char>(s[left++])]>0)missing++;}}return length==INT32_MAX?"":s.substr(start,length);',
'int[]need=new int[128];for(char c:t.toCharArray())need[c]++;int missing=t.length(),left=0,start=0,length=Integer.MAX_VALUE;for(int r=0;r<s.length();r++){if(need[s.charAt(r)]-->0)missing--;while(missing==0){if(r-left+1<length){start=left;length=r-left+1;}if(++need[s.charAt(left++)]>0)missing++;}}return length==Integer.MAX_VALUE?"":s.substring(start,start+length);')
add('LongestPalindrome',
'int start=0,length=0;void Expand(int l,int r){while(l>=0&&r<s.Length&&s[l]==s[r]){if(r-l+1>length||(r-l+1==length&&l<start)){start=l;length=r-l+1;}l--;r++;}}for(int i=0;i<s.Length;i++){Expand(i,i);Expand(i,i+1);}return s.Substring(start,length);',
'let start=0,length=0;function expand(l,r){while(l>=0&&r<s.length&&s[l]===s[r]){if(r-l+1>length||(r-l+1===length&&l<start)){start=l;length=r-l+1;}l--;r++;}}for(let i=0;i<s.length;i++){expand(i,i);expand(i,i+1);}return s.slice(start,start+length);',
'int start=0,length=0;auto expand=[&](int l,int r){while(l>=0&&r<static_cast<int>(s.size())&&s[l]==s[r]){if(r-l+1>length||(r-l+1==length&&l<start)){start=l;length=r-l+1;}l--;r++;}};for(int i=0;i<static_cast<int>(s.size());i++){expand(i,i);expand(i,i+1);}return s.substr(start,length);',
'int start=0,length=0;for(int i=0;i<s.length();i++)for(int parity=0;parity<2;parity++){int l=i,r=i+parity;while(l>=0&&r<s.length()&&s.charAt(l)==s.charAt(r)){if(r-l+1>length||(r-l+1==length&&l<start)){start=l;length=r-l+1;}l--;r++;}}return s.substring(start,start+length);')
add('CountSubstrings',
'int count=0;for(int i=0;i<s.Length;i++)for(int p=0;p<2;p++){int l=i,r=i+p;while(l>=0&&r<s.Length&&s[l--]==s[r++])count++;}return count;',
'let count=0;for(let i=0;i<s.length;i++)for(let p=0;p<2;p++){let l=i,r=i+p;while(l>=0&&r<s.length&&s[l--]===s[r++])count++;}return count;',
'int count=0;for(int i=0;i<static_cast<int>(s.size());i++)for(int p=0;p<2;p++){int l=i,r=i+p;while(l>=0&&r<static_cast<int>(s.size())&&s[l--]==s[r++])count++;}return count;',
'int count=0;for(int i=0;i<s.length();i++)for(int p=0;p<2;p++){int l=i,r=i+p;while(l>=0&&r<s.length()&&s.charAt(l--)==s.charAt(r++))count++;}return count;')
add('IsValid',
'var stack=new Stack<char>();foreach(char c in s){if(c is \'(\' or \'[\' or \'{\')stack.Push(c);else{int j=")] }".Replace(" ","").IndexOf(c);if(stack.Count==0||stack.Pop()!="([{ age"[j])return false;}}return stack.Count==0;'.replace('([{ age','([{'),
'const stack=[];for(const c of s){if("([{ ".includes(c))stack.push(c);else{const j=")] }".replace(/ /g,"").indexOf(c);if(!stack.length||stack.pop()!=="([{ "[j])return false;}}return !stack.length;',
'std::vector<char>stack;for(char c:s){auto i=std::string("([{").find(c);if(i!=std::string::npos)stack.push_back(c);else{auto j=std::string(")]}").find(c);if(stack.empty()||stack.back()!=std::string("([{")[j])return false;stack.pop_back();}}return stack.empty();',
'Deque<Character>stack=new ArrayDeque<>();for(char c:s.toCharArray()){if("([{".indexOf(c)>=0)stack.push(c);else{int j=")] }".replace(" ","").indexOf(c);if(stack.isEmpty()||stack.pop()!="([{".charAt(j))return false;}}return stack.isEmpty();')
add('SpiralOrder',
'var outp=new List<int>();int top=0,bottom=matrix.Length-1,left=0,right=matrix[0].Length-1;while(top<=bottom&&left<=right){for(int c=left;c<=right;c++)outp.Add(matrix[top][c]);top++;for(int r=top;r<=bottom;r++)outp.Add(matrix[r][right]);right--;if(top<=bottom){for(int c=right;c>=left;c--)outp.Add(matrix[bottom][c]);bottom--;}if(left<=right){for(int r=bottom;r>=top;r--)outp.Add(matrix[r][left]);left++;}}return outp.ToArray();',
'const out=[];let top=0,bottom=matrix.length-1,left=0,right=matrix[0].length-1;while(top<=bottom&&left<=right){for(let c=left;c<=right;c++)out.push(matrix[top][c]);top++;for(let r=top;r<=bottom;r++)out.push(matrix[r][right]);right--;if(top<=bottom){for(let c=right;c>=left;c--)out.push(matrix[bottom][c]);bottom--;}if(left<=right){for(let r=bottom;r>=top;r--)out.push(matrix[r][left]);left++;}}return out;',
'std::vector<int>out;int top=0,bottom=static_cast<int>(matrix.size())-1,left=0,right=static_cast<int>(matrix[0].size())-1;while(top<=bottom&&left<=right){for(int c=left;c<=right;c++)out.push_back(matrix[top][c]);top++;for(int r=top;r<=bottom;r++)out.push_back(matrix[r][right]);right--;if(top<=bottom){for(int c=right;c>=left;c--)out.push_back(matrix[bottom][c]);bottom--;}if(left<=right){for(int r=bottom;r>=top;r--)out.push_back(matrix[r][left]);left++;}}return out;',
'List<Integer>out=new ArrayList<>();int top=0,bottom=matrix.length-1,left=0,right=matrix[0].length-1;while(top<=bottom&&left<=right){for(int c=left;c<=right;c++)out.add(matrix[top][c]);top++;for(int r=top;r<=bottom;r++)out.add(matrix[r][right]);right--;if(top<=bottom){for(int c=right;c>=left;c--)out.add(matrix[bottom][c]);bottom--;}if(left<=right){for(int r=bottom;r>=top;r--)out.add(matrix[r][left]);left++;}}return out.stream().mapToInt(v->v).toArray();')
add('FindMin',
'int l=0,r=nums.Length-1;while(l<r){int mid=l+(r-l)/2;if(nums[mid]>nums[r])l=mid+1;else r=mid;}return nums[l];',
'let l=0,r=nums.length-1;while(l<r){const mid=Math.floor((l+r)/2);if(nums[mid]>nums[r])l=mid+1;else r=mid;}return nums[l];',
'int l=0,r=static_cast<int>(nums.size())-1;while(l<r){int mid=l+(r-l)/2;if(nums[mid]>nums[r])l=mid+1;else r=mid;}return nums[l];',
'int l=0,r=nums.length-1;while(l<r){int mid=l+(r-l)/2;if(nums[mid]>nums[r])l=mid+1;else r=mid;}return nums[l];')
add('Search',
'int l=0,r=nums.Length-1;while(l<=r){int mid=l+(r-l)/2;if(nums[mid]==target)return mid;if(nums[l]<=nums[mid]){if(nums[l]<=target&&target<nums[mid])r=mid-1;else l=mid+1;}else{if(nums[mid]<target&&target<=nums[r])l=mid+1;else r=mid-1;}}return -1;',
'let l=0,r=nums.length-1;while(l<=r){const mid=Math.floor((l+r)/2);if(nums[mid]===target)return mid;if(nums[l]<=nums[mid]){if(nums[l]<=target&&target<nums[mid])r=mid-1;else l=mid+1;}else{if(nums[mid]<target&&target<=nums[r])l=mid+1;else r=mid-1;}}return -1;',
'int l=0,r=static_cast<int>(nums.size())-1;while(l<=r){int mid=l+(r-l)/2;if(nums[mid]==target)return mid;if(nums[l]<=nums[mid]){if(nums[l]<=target&&target<nums[mid])r=mid-1;else l=mid+1;}else{if(nums[mid]<target&&target<=nums[r])l=mid+1;else r=mid-1;}}return -1;',
'int l=0,r=nums.length-1;while(l<=r){int mid=l+(r-l)/2;if(nums[mid]==target)return mid;if(nums[l]<=nums[mid]){if(nums[l]<=target&&target<nums[mid])r=mid-1;else l=mid+1;}else{if(nums[mid]<target&&target<=nums[r])l=mid+1;else r=mid-1;}}return -1;')

add('Exist',
'int rows=board.Length,cols=board[0].Length;var used=Enumerable.Range(0,rows).Select(_=>new bool[cols]).ToArray();bool Visit(int r,int c,int i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r][c]!=word[i])return false;if(i==word.Length-1)return true;used[r][c]=true;bool ok=Visit(r-1,c,i+1)||Visit(r+1,c,i+1)||Visit(r,c-1,i+1)||Visit(r,c+1,i+1);used[r][c]=false;return ok;}for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(Visit(r,c,0))return true;return false;',
'const rows=board.length,cols=board[0].length,used=Array.from({length:rows},()=>Array(cols).fill(false));function visit(r,c,i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r][c]!==word[i])return false;if(i===word.length-1)return true;used[r][c]=true;const ok=visit(r-1,c,i+1)||visit(r+1,c,i+1)||visit(r,c-1,i+1)||visit(r,c+1,i+1);used[r][c]=false;return ok;}for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)if(visit(r,c,0))return true;return false;',
'int rows=static_cast<int>(board.size()),cols=static_cast<int>(board[0].size());std::vector<std::vector<bool>>used(rows,std::vector<bool>(cols));std::function<bool(int,int,int)>visit=[&](int r,int c,int i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r][c]!=word[i])return false;if(i==static_cast<int>(word.size())-1)return true;used[r][c]=true;bool ok=visit(r-1,c,i+1)||visit(r+1,c,i+1)||visit(r,c-1,i+1)||visit(r,c+1,i+1);used[r][c]=false;return ok;};for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(visit(r,c,0))return true;return false;',
'int rows=board.length,cols=board[0].length();boolean[][]used=new boolean[rows][cols];class Search{boolean visit(int r,int c,int i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r].charAt(c)!=word.charAt(i))return false;if(i==word.length()-1)return true;used[r][c]=true;boolean ok=visit(r-1,c,i+1)||visit(r+1,c,i+1)||visit(r,c-1,i+1)||visit(r,c+1,i+1);used[r][c]=false;return ok;}}Search search=new Search();for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(search.visit(r,c,0))return true;return false;')
# Word Search II invokes the same independent DFS for each distinct dictionary word.
BODIES['FindWords']=(
'var outp=new List<string>();foreach(string word in words.Distinct()){int rows=board.Length,cols=board[0].Length;var used=Enumerable.Range(0,rows).Select(_=>new bool[cols]).ToArray();bool Visit(int r,int c,int i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r][c]!=word[i])return false;if(i==word.Length-1)return true;used[r][c]=true;bool ok=Visit(r-1,c,i+1)||Visit(r+1,c,i+1)||Visit(r,c-1,i+1)||Visit(r,c+1,i+1);used[r][c]=false;return ok;}bool found=false;for(int r=0;r<rows&&!found;r++)for(int c=0;c<cols&&!found;c++)found=Visit(r,c,0);if(found)outp.Add(word);}return outp.ToArray();',
'const out=[];for(const word of new Set(words)){const rows=board.length,cols=board[0].length,used=Array.from({length:rows},()=>Array(cols).fill(false));function visit(r,c,i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r][c]!==word[i])return false;if(i===word.length-1)return true;used[r][c]=true;const ok=visit(r-1,c,i+1)||visit(r+1,c,i+1)||visit(r,c-1,i+1)||visit(r,c+1,i+1);used[r][c]=false;return ok;}let found=false;for(let r=0;r<rows&&!found;r++)for(let c=0;c<cols&&!found;c++)found=visit(r,c,0);if(found)out.push(word);}return out;',
'std::vector<std::string>out;std::set<std::string>unique(words.begin(),words.end());for(const auto&word:unique){int rows=static_cast<int>(board.size()),cols=static_cast<int>(board[0].size());std::vector<std::vector<bool>>used(rows,std::vector<bool>(cols));std::function<bool(int,int,int)>visit=[&](int r,int c,int i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r][c]!=word[i])return false;if(i==static_cast<int>(word.size())-1)return true;used[r][c]=true;bool ok=visit(r-1,c,i+1)||visit(r+1,c,i+1)||visit(r,c-1,i+1)||visit(r,c+1,i+1);used[r][c]=false;return ok;};bool found=false;for(int r=0;r<rows&&!found;r++)for(int c=0;c<cols&&!found;c++)found=visit(r,c,0);if(found)out.push_back(word);}return out;',
'List<String>out=new ArrayList<>();for(String word:new HashSet<>(Arrays.asList(words))){int rows=board.length,cols=board[0].length();boolean[][]used=new boolean[rows][cols];class Search{boolean visit(int r,int c,int i){if(r<0||r>=rows||c<0||c>=cols||used[r][c]||board[r].charAt(c)!=word.charAt(i))return false;if(i==word.length()-1)return true;used[r][c]=true;boolean ok=visit(r-1,c,i+1)||visit(r+1,c,i+1)||visit(r,c-1,i+1)||visit(r,c+1,i+1);used[r][c]=false;return ok;}}Search search=new Search();boolean found=false;for(int r=0;r<rows&&!found;r++)for(int c=0;c<cols&&!found;c++)found=search.visit(r,c,0);if(found)out.add(word);}return out.toArray(String[]::new);')
add('NumIslands',
'int rows=grid.Length,cols=grid[0].Length,count=0;var seen=new bool[rows,cols];int[]dr=[-1,1,0,0],dc=[0,0,-1,1];for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(grid[r][c]==\'1\'&&!seen[r,c]){count++;seen[r,c]=true;var q=new Queue<(int,int)>();q.Enqueue((r,c));while(q.TryDequeue(out var p))for(int i=0;i<4;i++){int u=p.Item1+dr[i],v=p.Item2+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&grid[u][v]==\'1\'&&!seen[u,v]){seen[u,v]=true;q.Enqueue((u,v));}}}return count;',
'const rows=grid.length,cols=grid[0].length,seen=Array.from({length:rows},()=>Array(cols).fill(false)),dr=[-1,1,0,0],dc=[0,0,-1,1];let count=0;for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)if(grid[r][c]==="1"&&!seen[r][c]){count++;seen[r][c]=true;const q=[[r,c]];for(let j=0;j<q.length;j++)for(let i=0;i<4;i++){const u=q[j][0]+dr[i],v=q[j][1]+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&grid[u][v]==="1"&&!seen[u][v]){seen[u][v]=true;q.push([u,v]);}}}return count;',
'int rows=static_cast<int>(grid.size()),cols=static_cast<int>(grid[0].size()),count=0;std::vector<std::vector<bool>>seen(rows,std::vector<bool>(cols));int dr[]={-1,1,0,0},dc[]={0,0,-1,1};for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(grid[r][c]==\'1\'&&!seen[r][c]){count++;seen[r][c]=true;std::queue<std::pair<int,int>>q;q.emplace(r,c);while(!q.empty()){auto p=q.front();q.pop();for(int i=0;i<4;i++){int u=p.first+dr[i],v=p.second+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&grid[u][v]==\'1\'&&!seen[u][v]){seen[u][v]=true;q.emplace(u,v);}}}}return count;',
'int rows=grid.length,cols=grid[0].length(),count=0;boolean[][]seen=new boolean[rows][cols];int[]dr={-1,1,0,0},dc={0,0,-1,1};for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(grid[r].charAt(c)==\'1\'&&!seen[r][c]){count++;seen[r][c]=true;Deque<int[]>q=new ArrayDeque<>();q.add(new int[]{r,c});while(!q.isEmpty()){int[]p=q.remove();for(int i=0;i<4;i++){int u=p[0]+dr[i],v=p[1]+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&grid[u].charAt(v)==\'1\'&&!seen[u][v]){seen[u][v]=true;q.add(new int[]{u,v});}}}}return count;')
add('PacificAtlantic',
'int rows=heights.Length,cols=heights[0].Length;bool[,] Flood(bool pacific){var seen=new bool[rows,cols];var q=new Queue<(int,int)>();for(int r=0;r<rows;r++){int c=pacific?0:cols-1;if(!seen[r,c]){seen[r,c]=true;q.Enqueue((r,c));}}for(int c=0;c<cols;c++){int r=pacific?0:rows-1;if(!seen[r,c]){seen[r,c]=true;q.Enqueue((r,c));}}int[]dr=[-1,1,0,0],dc=[0,0,-1,1];while(q.TryDequeue(out var p))for(int i=0;i<4;i++){int u=p.Item1+dr[i],v=p.Item2+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&!seen[u,v]&&heights[u][v]>=heights[p.Item1][p.Item2]){seen[u,v]=true;q.Enqueue((u,v));}}return seen;}var a=Flood(true);var b=Flood(false);var outp=new List<int[]>();for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(a[r,c]&&b[r,c])outp.Add([r,c]);return outp.ToArray();',
'const rows=heights.length,cols=heights[0].length;function flood(pacific){const seen=Array.from({length:rows},()=>Array(cols).fill(false)),q=[];function add(r,c){if(!seen[r][c]){seen[r][c]=true;q.push([r,c]);}}for(let r=0;r<rows;r++)add(r,pacific?0:cols-1);for(let c=0;c<cols;c++)add(pacific?0:rows-1,c);const dr=[-1,1,0,0],dc=[0,0,-1,1];for(let j=0;j<q.length;j++)for(let i=0;i<4;i++){const [r,c]=q[j],u=r+dr[i],v=c+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&!seen[u][v]&&heights[u][v]>=heights[r][c])add(u,v);}return seen;}const a=flood(true),b=flood(false),out=[];for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)if(a[r][c]&&b[r][c])out.push([r,c]);return out;',
'int rows=static_cast<int>(heights.size()),cols=static_cast<int>(heights[0].size());auto flood=[&](bool pacific){std::vector<std::vector<bool>>seen(rows,std::vector<bool>(cols));std::queue<std::pair<int,int>>q;auto add=[&](int r,int c){if(!seen[r][c]){seen[r][c]=true;q.emplace(r,c);}};for(int r=0;r<rows;r++)add(r,pacific?0:cols-1);for(int c=0;c<cols;c++)add(pacific?0:rows-1,c);int dr[]={-1,1,0,0},dc[]={0,0,-1,1};while(!q.empty()){auto p=q.front();q.pop();for(int i=0;i<4;i++){int u=p.first+dr[i],v=p.second+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&!seen[u][v]&&heights[u][v]>=heights[p.first][p.second])add(u,v);}}return seen;};auto a=flood(true),b=flood(false);std::vector<std::vector<int>>out;for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(a[r][c]&&b[r][c])out.push_back({r,c});return out;',
'int rows=heights.length,cols=heights[0].length;class Flow{boolean[][]flood(boolean pacific){boolean[][]seen=new boolean[rows][cols];Deque<int[]>q=new ArrayDeque<>();for(int r=0;r<rows;r++){int c=pacific?0:cols-1;if(!seen[r][c]){seen[r][c]=true;q.add(new int[]{r,c});}}for(int c=0;c<cols;c++){int r=pacific?0:rows-1;if(!seen[r][c]){seen[r][c]=true;q.add(new int[]{r,c});}}int[]dr={-1,1,0,0},dc={0,0,-1,1};while(!q.isEmpty()){int[]p=q.remove();for(int i=0;i<4;i++){int u=p[0]+dr[i],v=p[1]+dc[i];if(u>=0&&u<rows&&v>=0&&v<cols&&!seen[u][v]&&heights[u][v]>=heights[p[0]][p[1]]){seen[u][v]=true;q.add(new int[]{u,v});}}}return seen;}}Flow flow=new Flow();boolean[][]a=flow.flood(true),b=flow.flood(false);List<int[]>out=new ArrayList<>();for(int r=0;r<rows;r++)for(int c=0;c<cols;c++)if(a[r][c]&&b[r][c])out.add(new int[]{r,c});return out.toArray(int[][]::new);')
add('CanFinish',
'var graph=Enumerable.Range(0,numCourses).Select(_=>new List<int>()).ToArray();var degree=new int[numCourses];foreach(var e in prerequisites){graph[e[1]].Add(e[0]);degree[e[0]]++;}var q=new Queue<int>(Enumerable.Range(0,numCourses).Where(v=>degree[v]==0));int count=0;while(q.TryDequeue(out int v)){count++;foreach(int u in graph[v])if(--degree[u]==0)q.Enqueue(u);}return count==numCourses;',
'const graph=Array.from({length:numCourses},()=>[]),degree=Array(numCourses).fill(0);for(const [a,b] of prerequisites){graph[b].push(a);degree[a]++;}const q=[];for(let v=0;v<numCourses;v++)if(!degree[v])q.push(v);for(let i=0;i<q.length;i++)for(const u of graph[q[i]])if(--degree[u]===0)q.push(u);return q.length===numCourses;',
'std::vector<std::vector<int>>graph(numCourses);std::vector<int>degree(numCourses);for(auto e:prerequisites){graph[e[1]].push_back(e[0]);degree[e[0]]++;}std::queue<int>q;for(int i=0;i<numCourses;i++)if(!degree[i])q.push(i);int count=0;while(!q.empty()){int v=q.front();q.pop();count++;for(int u:graph[v])if(!--degree[u])q.push(u);}return count==numCourses;',
'List<List<Integer>>graph=new ArrayList<>();for(int i=0;i<numCourses;i++)graph.add(new ArrayList<>());int[]degree=new int[numCourses];for(int[]e:prerequisites){graph.get(e[1]).add(e[0]);degree[e[0]]++;}Deque<Integer>q=new ArrayDeque<>();for(int i=0;i<numCourses;i++)if(degree[i]==0)q.add(i);int count=0;while(!q.isEmpty()){int v=q.remove();count++;for(int u:graph.get(v))if(--degree[u]==0)q.add(u);}return count==numCourses;')
add('CountComponents',
'var parent=Enumerable.Range(0,n).ToArray();int Find(int v){while(v!=parent[v]){parent[v]=parent[parent[v]];v=parent[v];}return v;}int count=n;foreach(var e in edges){int a=Find(e[0]),b=Find(e[1]);if(a!=b){parent[a]=b;count--;}}return count;',
'const parent=Array.from({length:n},(_,i)=>i);function find(v){while(v!==parent[v]){parent[v]=parent[parent[v]];v=parent[v];}return v;}let count=n;for(const [u,v] of edges){const a=find(u),b=find(v);if(a!==b){parent[a]=b;count--;}}return count;',
'std::vector<int>parent(n);for(int i=0;i<n;i++)parent[i]=i;auto find=[&](int v){while(v!=parent[v]){parent[v]=parent[parent[v]];v=parent[v];}return v;};int count=n;for(auto e:edges){int a=find(e[0]),b=find(e[1]);if(a!=b){parent[a]=b;count--;}}return count;',
'int[]parent=new int[n];for(int i=0;i<n;i++)parent[i]=i;java.util.function.IntUnaryOperator find=value->{int v=value;while(v!=parent[v]){parent[v]=parent[parent[v]];v=parent[v];}return v;};int count=n;for(int[]e:edges){int a=find.applyAsInt(e[0]),b=find.applyAsInt(e[1]);if(a!=b){parent[a]=b;count--;}}return count;')
BODIES['ValidTree']=tuple(prefix+body.rsplit('return count;',1)[0]+'return count==1;' for prefix,body in zip([
'if(n==0||edges.Length!=n-1)return false;',
'if(n===0||edges.length!==n-1)return false;',
'if(n==0||edges.size()!=static_cast<size_t>(n-1))return false;',
'if(n==0||edges.length!=n-1)return false;'],BODIES['CountComponents']))
add('AlienOrder',
'var graph=new Dictionary<char,HashSet<char>>();foreach(char c in string.Concat(words))graph.TryAdd(c,[]);for(int i=1;i<words.Length;i++){string a=words[i-1],b=words[i];int j=0;while(j<Math.Min(a.Length,b.Length)&&a[j]==b[j])j++;if(j==Math.Min(a.Length,b.Length)){if(a.Length>b.Length)return "";}else graph[a[j]].Add(b[j]);}var degree=graph.Keys.ToDictionary(c=>c,_=>0);foreach(var row in graph.Values)foreach(char c in row)degree[c]++;var ready=new SortedSet<char>(degree.Where(p=>p.Value==0).Select(p=>p.Key));var outp=new List<char>();while(ready.Count>0){char c=ready.Min;ready.Remove(c);outp.Add(c);foreach(char next in graph[c])if(--degree[next]==0)ready.Add(next);}return outp.Count==graph.Count?new string(outp.ToArray()):"";',
'const graph=new Map();for(const c of words.join(""))if(!graph.has(c))graph.set(c,new Set());for(let i=1;i<words.length;i++){const a=words[i-1],b=words[i];let j=0;while(j<Math.min(a.length,b.length)&&a[j]===b[j])j++;if(j===Math.min(a.length,b.length)){if(a.length>b.length)return "";}else graph.get(a[j]).add(b[j]);}const degree=new Map([...graph.keys()].map(c=>[c,0]));for(const row of graph.values())for(const c of row)degree.set(c,degree.get(c)+1);const ready=[...degree].filter(p=>p[1]===0).map(p=>p[0]),out=[];while(ready.length){ready.sort();const c=ready.shift();out.push(c);for(const next of graph.get(c)){degree.set(next,degree.get(next)-1);if(!degree.get(next))ready.push(next);}}return out.length===graph.size?out.join(""):"";',
'std::map<char,std::set<char>>graph;for(auto&w:words)for(char c:w)graph[c];for(size_t i=1;i<words.size();i++){auto&a=words[i-1];auto&b=words[i];size_t j=0;while(j<std::min(a.size(),b.size())&&a[j]==b[j])j++;if(j==std::min(a.size(),b.size())){if(a.size()>b.size())return "";}else graph[a[j]].insert(b[j]);}std::map<char,int>degree;for(auto p:graph)degree[p.first]=0;for(auto p:graph)for(char c:p.second)degree[c]++;std::set<char>ready;for(auto p:degree)if(!p.second)ready.insert(p.first);std::string out;while(!ready.empty()){char c=*ready.begin();ready.erase(c);out+=c;for(char next:graph[c])if(!--degree[next])ready.insert(next);}return out.size()==graph.size()?out:"";',
'Map<Character,Set<Character>>graph=new HashMap<>();for(String w:words)for(char c:w.toCharArray())graph.computeIfAbsent(c,k->new HashSet<>());for(int i=1;i<words.length;i++){String a=words[i-1],b=words[i];int j=0;while(j<Math.min(a.length(),b.length())&&a.charAt(j)==b.charAt(j))j++;if(j==Math.min(a.length(),b.length())){if(a.length()>b.length())return "";}else graph.get(a.charAt(j)).add(b.charAt(j));}Map<Character,Integer>degree=new HashMap<>();for(char c:graph.keySet())degree.put(c,0);for(Set<Character>row:graph.values())for(char c:row)degree.put(c,degree.get(c)+1);PriorityQueue<Character>ready=new PriorityQueue<>();for(var e:degree.entrySet())if(e.getValue()==0)ready.add(e.getKey());StringBuilder out=new StringBuilder();while(!ready.isEmpty()){char c=ready.remove();out.append(c);for(char next:graph.get(c)){degree.put(next,degree.get(next)-1);if(degree.get(next)==0)ready.add(next);}}return out.length()==graph.size()?out.toString():"";')
add('ClimbStairs',
'int a=1,b=1;for(int i=1;i<n;i++){int next=a+b;a=b;b=next;}return b;',
'let a=1,b=1;for(let i=1;i<n;i++){const next=a+b;a=b;b=next;}return b;',
'int a=1,b=1;for(int i=1;i<n;i++){int next=a+b;a=b;b=next;}return b;',
'int a=1,b=1;for(int i=1;i<n;i++){int next=a+b;a=b;b=next;}return b;')
add('Rob',
'int Run(int lo,int hi){int a=0,b=0;for(int i=lo;i<hi;i++){int next=Math.Max(b,a+nums[i]);a=b;b=next;}return b;}return Run(0,nums.Length);',
'function run(lo,hi){let a=0,b=0;for(let i=lo;i<hi;i++){const next=Math.max(b,a+nums[i]);a=b;b=next;}return b;}return run(0,nums.length);',
'auto run=[&](int lo,int hi){int a=0,b=0;for(int i=lo;i<hi;i++){int next=std::max(b,a+nums[i]);a=b;b=next;}return b;};return run(0,static_cast<int>(nums.size()));',
'java.util.function.IntBinaryOperator run=(lo,hi)->{int a=0,b=0;for(int i=lo;i<hi;i++){int next=Math.max(b,a+nums[i]);a=b;b=next;}return b;};return run.applyAsInt(0,nums.length);')
add('NumDecodings',
'System.Numerics.BigInteger a=1,b=s[0]==\'0\'?0:1;for(int i=1;i<s.Length;i++){System.Numerics.BigInteger next=s[i]==\'0\'?0:b;int pair=(s[i-1]-\'0\')*10+s[i]-\'0\';if(pair>=10&&pair<=26)next+=a;a=b;b=next;}return (int)b;',
'let a=1n,b=s[0]==="0"?0n:1n;for(let i=1;i<s.length;i++){let next=s[i]==="0"?0n:b;const pair=Number(s.slice(i-1,i+1));if(pair>=10&&pair<=26)next+=a;a=b;b=next;}return Number(b);',
'uint64_t a=1,b=s[0]==\'0\'?0:1;for(size_t i=1;i<s.size();i++){uint64_t next=s[i]==\'0\'?0:b;int pair=(s[i-1]-\'0\')*10+s[i]-\'0\';if(pair>=10&&pair<=26)next+=a;a=b;b=next;}return static_cast<int>(b);',
'java.math.BigInteger a=java.math.BigInteger.ONE,b=s.charAt(0)==\'0\'?java.math.BigInteger.ZERO:java.math.BigInteger.ONE;for(int i=1;i<s.length();i++){java.math.BigInteger next=s.charAt(i)==\'0\'?java.math.BigInteger.ZERO:b;int pair=(s.charAt(i-1)-\'0\')*10+s.charAt(i)-\'0\';if(pair>=10&&pair<=26)next=next.add(a);a=b;b=next;}return b.intValueExact();')
add('CoinChange',
'var dp=Enumerable.Repeat(amount+1,amount+1).ToArray();dp[0]=0;for(int v=1;v<=amount;v++)foreach(int c in coins)if(c<=v)dp[v]=Math.Min(dp[v],dp[v-c]+1);return dp[amount]>amount?-1:dp[amount];',
'const dp=Array(amount+1).fill(amount+1);dp[0]=0;for(let v=1;v<=amount;v++)for(const c of coins)if(c<=v)dp[v]=Math.min(dp[v],dp[v-c]+1);return dp[amount]>amount?-1:dp[amount];',
'std::vector<int>dp(amount+1,amount+1);dp[0]=0;for(int v=1;v<=amount;v++)for(int c:coins)if(c<=v)dp[v]=std::min(dp[v],dp[v-c]+1);return dp[amount]>amount?-1:dp[amount];',
'int[]dp=new int[amount+1];Arrays.fill(dp,amount+1);dp[0]=0;for(int v=1;v<=amount;v++)for(int c:coins)if(c<=v)dp[v]=Math.min(dp[v],dp[v-c]+1);return dp[amount]>amount?-1:dp[amount];')
add('MaxProduct',
'int high=nums[0],low=nums[0],best=nums[0];foreach(int v in nums.Skip(1)){int a=high*v,b=low*v;high=Math.Max(v,Math.Max(a,b));low=Math.Min(v,Math.Min(a,b));best=Math.Max(best,high);}return best;',
'let high=nums[0],low=nums[0],best=nums[0];for(const v of nums.slice(1)){const a=high*v,b=low*v;high=Math.max(v,a,b);low=Math.min(v,a,b);best=Math.max(best,high);}return best;',
'int high=nums[0],low=nums[0],best=nums[0];for(size_t i=1;i<nums.size();i++){int v=nums[i],a=high*v,b=low*v;high=std::max(v,std::max(a,b));low=std::min(v,std::min(a,b));best=std::max(best,high);}return best;',
'int high=nums[0],low=nums[0],best=nums[0];for(int i=1;i<nums.length;i++){int v=nums[i],a=high*v,b=low*v;high=Math.max(v,Math.max(a,b));low=Math.min(v,Math.min(a,b));best=Math.max(best,high);}return best;')
add('WordBreak',
'var possible=new bool[s.Length+1];possible[0]=true;for(int i=0;i<s.Length;i++)if(possible[i])foreach(string w in wordDict)if(i+w.Length<=s.Length&&s.AsSpan(i,w.Length).SequenceEqual(w))possible[i+w.Length]=true;return possible[^1];',
'const possible=Array(s.length+1).fill(false);possible[0]=true;for(let i=0;i<s.length;i++)if(possible[i])for(const w of wordDict)if(s.startsWith(w,i))possible[i+w.length]=true;return possible[s.length];',
'std::vector<bool>possible(s.size()+1);possible[0]=true;for(size_t i=0;i<s.size();i++)if(possible[i])for(auto&w:wordDict)if(s.compare(i,w.size(),w)==0)possible[i+w.size()]=true;return possible.back();',
'boolean[]possible=new boolean[s.length()+1];possible[0]=true;for(int i=0;i<s.length();i++)if(possible[i])for(String w:wordDict)if(s.startsWith(w,i))possible[i+w.length()]=true;return possible[s.length()];')
add('LengthOfLIS',
'var tails=new List<int>();foreach(int v in nums){int l=0,r=tails.Count;while(l<r){int mid=l+(r-l)/2;if(tails[mid]<v)l=mid+1;else r=mid;}if(l==tails.Count)tails.Add(v);else tails[l]=v;}return tails.Count;',
'const tails=[];for(const v of nums){let l=0,r=tails.length;while(l<r){const mid=Math.floor((l+r)/2);if(tails[mid]<v)l=mid+1;else r=mid;}tails[l]=v;}return tails.length;',
'std::vector<int>tails;for(int v:nums){auto it=std::lower_bound(tails.begin(),tails.end(),v);if(it==tails.end())tails.push_back(v);else *it=v;}return static_cast<int>(tails.size());',
'int[]tails=new int[nums.length];int length=0;for(int v:nums){int l=0,r=length;while(l<r){int mid=l+(r-l)/2;if(tails[mid]<v)l=mid+1;else r=mid;}tails[l]=v;if(l==length)length++;}return length;')
add('UniquePaths',
'var dp=Enumerable.Repeat(1,n).ToArray();for(int r=1;r<m;r++)for(int c=1;c<n;c++)dp[c]+=dp[c-1];return dp[n-1];',
'const dp=Array(n).fill(1);for(let r=1;r<m;r++)for(let c=1;c<n;c++)dp[c]+=dp[c-1];return dp[n-1];',
'std::vector<int>dp(n,1);for(int r=1;r<m;r++)for(int c=1;c<n;c++)dp[c]+=dp[c-1];return dp[n-1];',
'int[]dp=new int[n];Arrays.fill(dp,1);for(int r=1;r<m;r++)for(int c=1;c<n;c++)dp[c]+=dp[c-1];return dp[n-1];')
add('CanJump',
'int far=0;for(int i=0;i<nums.Length&&i<=far;i++){far=Math.Max(far,i+nums[i]);if(far>=nums.Length-1)return true;}return false;',
'let far=0;for(let i=0;i<nums.length&&i<=far;i++){far=Math.max(far,i+nums[i]);if(far>=nums.length-1)return true;}return false;',
'int far=0;for(int i=0;i<static_cast<int>(nums.size())&&i<=far;i++){far=std::max(far,i+nums[i]);if(far>=static_cast<int>(nums.size())-1)return true;}return false;',
'int far=0;for(int i=0;i<nums.length&&i<=far;i++){far=Math.max(far,i+nums[i]);if(far>=nums.length-1)return true;}return false;')
add('CombinationSum4',
'var dp=new System.Numerics.BigInteger[target+1];dp[0]=1;for(int v=1;v<=target;v++)foreach(int c in nums)if(c<=v)dp[v]+=dp[v-c];return (int)dp[target];',
'const dp=Array(target+1).fill(0n);dp[0]=1n;for(let v=1;v<=target;v++)for(const c of nums)if(c<=v)dp[v]+=dp[v-c];return Number(dp[target]);',
'std::vector<uint64_t>dp(target+1);dp[0]=1;for(int v=1;v<=target;v++)for(int c:nums)if(c<=v)dp[v]+=dp[v-c];return static_cast<int>(dp[target]);',
'java.math.BigInteger[]dp=new java.math.BigInteger[target+1];Arrays.fill(dp,java.math.BigInteger.ZERO);dp[0]=java.math.BigInteger.ONE;for(int v=1;v<=target;v++)for(int c:nums)if(c<=v)dp[v]=dp[v].add(dp[v-c]);return dp[target].intValueExact();')
add('MaxSubArray',
'int best=nums[0],ending=nums[0];foreach(int v in nums.Skip(1)){ending=Math.Max(v,ending+v);best=Math.Max(best,ending);}return best;',
'let best=nums[0],ending=nums[0];for(const v of nums.slice(1)){ending=Math.max(v,ending+v);best=Math.max(best,ending);}return best;',
'int best=nums[0],ending=nums[0];for(size_t i=1;i<nums.size();i++){ending=std::max(nums[i],ending+nums[i]);best=std::max(best,ending);}return best;',
'int best=nums[0],ending=nums[0];for(int i=1;i<nums.length;i++){ending=Math.max(nums[i],ending+nums[i]);best=Math.max(best,ending);}return best;')
add('HammingWeight',
'int count=0;while(n!=0){n&=n-1;count++;}return count;',
'let count=0;while(n!==0){n=(n>>>0)&((n-1)>>>0);n>>>=0;count++;}return count;',
'int count=0;while(n){n&=n-1;count++;}return count;',
'int count=0;while(n!=0){n&=n-1;count++;}return count;')
add('CountBits',
'var outp=new int[n+1];for(int i=1;i<=n;i++)outp[i]=outp[i>>1]+(i&1);return outp;',
'const out=Array(n+1).fill(0);for(let i=1;i<=n;i++)out[i]=out[i>>1]+(i&1);return out;',
'std::vector<int>out(n+1);for(int i=1;i<=n;i++)out[i]=out[i>>1]+(i&1);return out;',
'int[]out=new int[n+1];for(int i=1;i<=n;i++)out[i]=out[i>>1]+(i&1);return out;')
add('ReverseBits',
'long result=0;for(int i=0;i<32;i++){result=(result<<1)|(n&1);n>>=1;}return result;',
'let result=0;for(let i=0;i<32;i++){result=result*2+(n%2);n=Math.floor(n/2);}return result;',
'long long result=0;for(int i=0;i<32;i++){result=(result<<1)|(n&1);n>>=1;}return result;',
'long result=0;for(int i=0;i<32;i++){result=(result<<1)|(n&1);n>>=1;}return result;')
add('GetSum',
'while(b!=0){int carry=(a&b)<<1;a^=b;b=carry;}return a;',
'while(b!==0){const carry=(a&b)<<1;a^=b;b=carry;}return a;',
'uint32_t x=static_cast<uint32_t>(a),y=static_cast<uint32_t>(b);while(y){uint32_t carry=(x&y)<<1;x^=y;y=carry;}return static_cast<int32_t>(x);',
'while(b!=0){int carry=(a&b)<<1;a^=b;b=carry;}return a;')

def body(s,lang):
    if lang=='python':return None
    index=['csharp','javascript','cpp','java'].index(lang)
    result=BODIES.get(s['method'])
    if result is None:return None
    code=result[index]
    if s['method']=='Rob' and s['title']=='House Robber II':
        old=['return Run(0,nums.Length);','return run(0,nums.length);','return run(0,static_cast<int>(nums.size()));','return run.applyAsInt(0,nums.length);'][index]
        new=['return nums.Length<=1?nums.FirstOrDefault():Math.Max(Run(0,nums.Length-1),Run(1,nums.Length));','return nums.length<=1?(nums[0]??0):Math.max(run(0,nums.length-1),run(1,nums.length));','return nums.size()<=1?(nums.empty()?0:nums[0]):std::max(run(0,static_cast<int>(nums.size())-1),run(1,static_cast<int>(nums.size())));','return nums.length<=1?(nums.length==0?0:nums[0]):Math.max(run.applyAsInt(0,nums.length-1),run.applyAsInt(1,nums.length));'][index]
        code=code.replace(old,new)
    return {s['method']:code}
