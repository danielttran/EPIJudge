"""Independently authored fixed-width bit algorithms in five languages."""


def body(ref, language):
    if ref == "5.1":
        return {
            "csharp": "int width=high-low+1; uint mask=width==32?uint.MaxValue:(1u<<width)-1u; uint bits=unchecked((uint)word), replacement=unchecked((uint)insert); uint result=(bits & ~(mask<<low)) | ((replacement & mask)<<low); return unchecked((int)result);",
            "java": "int width=high-low+1; long mask=(1L<<width)-1L; long bits=word & 0xffffffffL, replacement=insert & 0xffffffffL; long result=(bits & ~(mask<<low)) | ((replacement & mask)<<low); return (int)result;",
            "cpp": "int width=high-low+1; std::uint64_t mask=(1ULL<<width)-1ULL; std::uint64_t bits=static_cast<std::uint32_t>(word), replacement=static_cast<std::uint32_t>(insert); std::uint64_t result=(bits & ~(mask<<low)) | ((replacement & mask)<<low); if(result>=2147483648ULL)return static_cast<int>(static_cast<long long>(result)-4294967296LL); return static_cast<int>(result);",
            "javascript": "const width=high-low+1, mask=(2**width-1)>>>0; return (word & ~(mask<<low)) | ((insert & mask)<<low);",
            "python": "width = high - low + 1\nmask = (1 << width) - 1\nbits = ((word & 0xffffffff) & ~(mask << low)) | ((insert & mask) << low)\nreturn bits if bits < 0x80000000 else bits - 0x100000000",
        }[language]
    if ref == "5.6":
        return {
            "csharp": "uint difference=unchecked((uint)(first^second)); int count=0; while(difference!=0){ difference &= difference-1; ++count; } return count;",
            "java": "int difference=first^second,count=0; while(difference!=0){difference &= difference-1; ++count;} return count;",
            "cpp": "std::uint32_t difference=static_cast<std::uint32_t>(first)^static_cast<std::uint32_t>(second); int count=0; while(difference!=0){difference &= difference-1; ++count;} return count;",
            "javascript": "let difference=(first^second)>>>0,count=0; while(difference!==0){difference=(difference & (difference-1))>>>0;++count;} return count;",
            "python": "difference = (first ^ second) & 0xffffffff\ncount = 0\nwhile difference:\n    difference &= difference - 1\n    count += 1\nreturn count",
        }[language]
    if ref == "5.7":
        return {
            "csharp": "uint bits=unchecked((uint)word); uint result=((bits & 0x55555555u)<<1) | ((bits & 0xaaaaaaaau)>>1); return unchecked((int)result);",
            "java": "return ((word & 0x55555555)<<1) | ((word & 0xaaaaaaaa)>>>1);",
            "cpp": "std::uint32_t bits=static_cast<std::uint32_t>(word); std::uint32_t result=((bits & 0x55555555u)<<1) | ((bits & 0xaaaaaaaau)>>1); if(result>=2147483648u)return static_cast<int>(static_cast<long long>(result)-4294967296LL); return static_cast<int>(result);",
            "javascript": "return ((word & 0x55555555)<<1) | ((word & 0xaaaaaaaa)>>>1);",
            "python": "bits = word & 0xffffffff\nresult = ((bits & 0x55555555) << 1) | ((bits & 0xaaaaaaaa) >> 1)\nreturn result if result < 0x80000000 else result - 0x100000000",
        }[language]
    raise ValueError(ref)
