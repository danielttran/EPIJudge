# Native website regression fixtures

These twelve reference implementations were copied from this repository's
`epi_judge_cpp_solutions` and `epi_judge_java_solutions` trees for the native web
regression suite. The repository LICENSE applies. They cover scalar values,
unordered results, linked lists, mutation, posting-list identity, and parent
links in trees. The website does not expose these implementations as starters.

Keeping these focused fixtures allows the full C++/Java solution directories
to be retired without removing the website's regression checks.

After building `EPIJudge.Web.slnx`, run:

```powershell
./scripts/Verify-NativeWeb.ps1 -StartServer
```

This starts a hidden temporary API server on localhost:5189, verifies both
218-entry catalogs and real Run/Submit responses, then stops that server.
Use `-SkipTimeout` only after timeout termination has already been checked.
