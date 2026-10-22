"""Exercise the actual credit validators with alternate and deliberately wrong Max results.

Only submission/class plumbing is replaced. Lookup deliberately throws: Max must
be checked using independent expected state, never by asking the submission.
Generated compiler artifacts stay in a temporary directory.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = [["ClientsCreditsInfo", "", 0]]
TIE = START + [["insert", "Nora", 10], ["insert", "Zoe", 10], ["insert", "Low", 3]]
CASES = [
    (START, "", True),
    (START, "Ghost", False),
    (TIE, "Nora", True),
    (TIE, "Zoe", True),
    (TIE, "Low", False),
    (TIE, "Ghost", False),
    (TIE, "", False),
    (TIE + [["add_all", "", -20], ["insert", "Nora", -11]], "Zoe", True),
    (TIE + [["add_all", "", -20], ["insert", "Nora", -11]], "Nora", False),
    (TIE + [["remove", "Zoe", 1]], "Nora", True),
    (TIE + [["remove", "Zoe", 1]], "Zoe", False),
    (TIE + START, "", True),
    (TIE + START, "Nora", False),
]
CASES = [
    (ops + [["max", "Nora", 0]], actual, expected) for ops, actual, expected in CASES
]


def block(source, marker):
    start = source.index(marker)
    opening = source.index("{", start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


def run(command, **kwargs):
    result = subprocess.run(
        command, text=True, capture_output=True, check=False, **kwargs
    )
    if result.returncode:
        raise AssertionError(
            " ".join(map(str, command)) + "\n" + result.stdout + result.stderr
        )
    print(result.stdout.strip()) if result.stdout.strip() else None


sys.path.insert(0, str(ROOT / "epi_judge_python"))
spec = importlib.util.spec_from_file_location(
    "credits_solution", ROOT / "solutions/python/adding_credits.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
namespace = module.__dict__


class Submission:
    chosen = ""

    def insert(self, *_):
        pass

    def add_all(self, *_):
        pass

    def remove(self, *_):
        return True

    def lookup(self, *_):
        raise AssertionError("Validator trusted submitted lookup")

    def max(self):
        return self.chosen


namespace["ClientsCreditsInfo"] = Submission
for ops, actual, expected in CASES:
    Submission.chosen = actual
    try:
        namespace["client_credits_info_tester"](ops)
        accepted = True
    except namespace["TestFailure"]:
        accepted = False
    assert accepted == expected, ("python", ops, actual, expected)
print("Python: 13 adversarial oracle checks passed")

with tempfile.TemporaryDirectory(prefix="epi-credits-oracle-") as temporary:
    temp = Path(temporary)
    source = (ROOT / "EpiJudge.Runner/EpiJavascriptHarness.js").read_text()
    branch = block(source, "case 'adding_credits':")
    js = (
        """let chosen = ''; class Submission {
      insert() {} addAll() {} remove() { return true; }
      lookup() { throw new Error('Validator trusted submitted lookup'); }
      max() { return chosen; }
    }
    class Rejected extends Error {}
    function check(value) { if (!value) throw new Rejected(); }
    function invoke(a) { const getConstructor = () => Submission;
      switch ('adding_credits') { """
        + branch
        + """ } }
    for (const [ops, result, expected] of """
        + json.dumps(CASES)
        + """) {
      chosen = result; let accepted = true;
      try { invoke([ops]); } catch (e) { if (!(e instanceof Rejected)) throw e; accepted = false; }
      if (accepted !== expected) throw new Error(JSON.stringify([ops, result, expected]));
    }
    console.log('JavaScript: 13 adversarial oracle checks passed');"""
    )
    (temp / "check.js").write_text(js)
    run(["node", str(temp / "check.js")])

    source = (ROOT / "solutions/cpp/adding_credits.cpp").read_text()
    function = block(source, "void ClientsCreditsInfoTester(")
    cpp = (
        """#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <stdexcept>
#include <iostream>
struct Operation { std::string op, s_arg; int i_arg; };
struct PropertyName { static constexpr int COMMAND = 0; };
struct TestFailure : std::runtime_error {
 using std::runtime_error::runtime_error;
 template<class A, class B> TestFailure& WithProperty(A, B) { return *this; }
 template<class A, class B, class C> TestFailure& WithMismatchInfo(A, B, C) { return *this; }
};
std::string chosen;
struct ClientsCreditsInfo {
 void Insert(std::string,int) {} void AddAll(int) {} bool Remove(std::string) {return true;}
 int Lookup(std::string) {throw std::logic_error("Validator trusted submitted lookup");}
 std::string Max() {return chosen;}
};
"""
        + function
        + "\nint main() {\n"
    )
    for ops, actual, expected in CASES:
        entries = ",".join(
            "{" + json.dumps(op) + "," + json.dumps(client) + "," + str(value) + "}"
            for op, client, value in ops
        )
        cpp += (
            "{chosen="
            + json.dumps(actual)
            + "; bool accepted=true; try {ClientsCreditsInfoTester({"
            + entries
            + "});} catch(const TestFailure&) {accepted=false;} if(accepted!="
            + str(expected).lower()
            + ") return 1;}\n"
        )
    cpp += 'std::cout << "C++: 13 adversarial oracle checks passed\\n";}\n'
    (temp / "check.cpp").write_text(cpp)
    run(["g++", "-std=c++17", str(temp / "check.cpp"), "-o", str(temp / "check")])
    run([str(temp / "check")])

    source = (ROOT / "solutions/java/adding_credits.java").read_text()
    function = block(source, "public static void ClientsCreditsInfoTester(")
    java = (
        """import java.util.*;
public class CreditsCheck {
 static String chosen;
 static class Operation {String op,sArg;int iArg; Operation(String op,String sArg,int iArg){this.op=op;this.sArg=sArg;this.iArg=iArg;}}
 static class TestFailure extends Exception {
 TestFailure(String s){super(s);} static class PropertyName {static int COMMAND=0;}
 TestFailure withProperty(Object a,Object b){return this;}
 TestFailure withMismatchInfo(Object a,Object b,Object c){return this;}
 }
 static class ClientsCreditsInfo {
 void insert(String s,int i){} void addAll(int i){} boolean remove(String s){return true;}
 int lookup(String s){throw new AssertionError("Validator trusted submitted lookup");}
 String max(){return chosen;}
 }
"""
        + function
        + "\npublic static void main(String[] args) throws Exception {\n"
    )
    for ops, actual, expected in CASES:
        entries = ",".join(
            "new Operation("
            + json.dumps(op)
            + ","
            + json.dumps(client)
            + ","
            + str(value)
            + ")"
            for op, client, value in ops
        )
        java += (
            "{chosen="
            + json.dumps(actual)
            + "; boolean accepted=true; try{ClientsCreditsInfoTester(List.of("
            + entries
            + "));}catch(TestFailure e){accepted=false;} if(accepted!="
            + str(expected).lower()
            + ")throw new AssertionError();}\n"
        )
    java += 'System.out.println("Java: 13 adversarial oracle checks passed");}}'
    (temp / "CreditsCheck.java").write_text(java)
    jdk = (
        Path(
            os.environ.get("EPI_JAVA_HOME")
            or os.environ.get("JAVA_HOME")
            or Path(shutil.which("javac")).resolve().parents[1]
        )
        / "bin"
    )
    run([str(jdk / "javac"), str(temp / "CreditsCheck.java")])
    run([str(jdk / "java"), "-cp", str(temp), "CreditsCheck"])

    source = (ROOT / "EpiJudge.Runner/JudgeAdapters.cs").read_text()
    branch = block(source, 'case "adding_credits":').replace(
        "Arg<List<(string, string, int)>>(a, 0)", "ops"
    )
    csharp = (
        """using System; using System.Linq; using System.Collections.Generic;
public class Submission {
 public static string Chosen="";
 public void Initialize(){} public void Insert(string s,int v){} public void AddAll(int v){}
 public bool Remove(string s)=>true;
 public int Lookup(string s)=>throw new InvalidOperationException("Validator trusted submitted lookup");
 public string Max()=>Chosen;
}
public class Rejected : Exception {}
public class Program {
 static void Check(bool value){if(!value)throw new Rejected();}
 static bool Invoke(List<(string,string,int)> ops) {dynamic s=new Submission(); switch("adding_credits") {"""
        + branch
        + """ default: throw new Exception();}}
 public static void Main() {
"""
    )
    for ops, actual, expected in CASES:
        entries = ",".join(
            "(" + json.dumps(op) + "," + json.dumps(client) + "," + str(value) + ")"
            for op, client, value in ops
        )
        csharp += (
            "{Submission.Chosen="
            + json.dumps(actual)
            + ";bool accepted=true;try{Invoke(new(){"
            + entries
            + "});}catch(Rejected){accepted=false;}if(accepted!="
            + str(expected).lower()
            + ")throw new Exception();}\n"
        )
    csharp += 'Console.WriteLine("C#: 13 adversarial oracle checks passed");}}'
    csharp = "using System.IO;\n" + csharp
    (temp / "Program.cs").write_text(csharp)
    (temp / "check.csproj").write_text(
        '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>'
    )
    run(
        [
            shutil.which("dotnet") or "dotnet",
            "run",
            "--project",
            str(temp / "check.csproj"),
            "--verbosity",
            "quiet",
        ]
    )
print("65 total adversarial checks passed across all five validators")
