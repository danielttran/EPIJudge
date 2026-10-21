import type { CodeFormat } from './practiceModels';

export type CodeReference = { title: string; code: string; names: string[] };

export type Problem = {
  id: string;
  title: string;
  topic: string;
  difficulty: string;
  description: string;
  constraints: string[];
  signature: string;
  testCount: number;
  starterCode: string;
  codeFormat?: CodeFormat;
  references?: CodeReference[];
  collection?: string;
  position?: number;
  diagram?: string | null;
  diagramAlt?: string | null;
  sourceUrl?: string | null;
  sourceAttribution?: string | null;
  jsSignature?: string;
  jsStarterCode?: string;
  pySignature?: string;
  pyStarterCode?: string;
  starters?: Record<
    string,
    {
      signature: string;
      starterCode: string;
      filename: string;
      runtime: string;
      codeFormat?: CodeFormat;
      references?: CodeReference[];
    }
  >;
  examples: { input: string; output: string; explanation: string }[];
};

export type LanguageConfig = {
  id: string;
  shortLabel: string;
  label: string;
  runtime: string;
  filename: string;
  monacoLang: string;
};

export const LANGUAGES: LanguageConfig[] = [
  {
    id: 'csharp',
    shortLabel: 'C#',
    label: 'C# (.NET 10)',
    runtime: 'C# .NET 10',
    filename: 'Solution.cs',
    monacoLang: 'csharp',
  },
  {
    id: 'javascript',
    shortLabel: 'JS',
    label: 'JavaScript (Node.js 24)',
    runtime: 'JavaScript Node.js 24',
    filename: 'solution.js',
    monacoLang: 'javascript',
  },
  {
    id: 'python',
    shortLabel: 'PY',
    label: 'Python (Python 3.14)',
    runtime: 'Python 3.14',
    filename: 'solution.py',
    monacoLang: 'python',
  },
  {
    id: 'cpp',
    shortLabel: 'C++',
    label: 'C++ (C++17)',
    runtime: 'C++17',
    filename: 'solution.cpp',
    monacoLang: 'cpp',
  },
  {
    id: 'java',
    shortLabel: 'JAVA',
    label: 'Java (JDK 21)',
    runtime: 'Java 21',
    filename: 'Solution.java',
    monacoLang: 'java',
  },
];

export function getStarterCode(p: Problem, lang: string): string {
  if (p.starters?.[lang]) return p.starters[lang].starterCode;
  if (lang === 'python') {
    return p.starters?.python?.starterCode || p.pyStarterCode || p.starterCode;
  }
  if (lang === 'javascript') {
    return p.starters?.javascript?.starterCode || p.jsStarterCode || p.starterCode;
  }
  return p.starters?.csharp?.starterCode || p.starterCode;
}

export function getStarterFormat(p: Problem, lang: string): CodeFormat {
  return p.starters?.[lang]?.codeFormat ?? p.codeFormat ?? 'legacy-v1';
}

export function getCodeReferences(p: Problem, lang: string): CodeReference[] {
  return p.starters?.[lang]?.references ?? p.references ?? [];
}

export function getSignature(p: Problem, lang: string): string {
  if (p.starters?.[lang]) return p.starters[lang].signature;
  if (lang === 'python') {
    return p.starters?.python?.signature || p.pySignature || p.signature;
  }
  if (lang === 'javascript') {
    return p.starters?.javascript?.signature || p.jsSignature || p.signature;
  }
  return p.starters?.csharp?.signature || p.signature;
}

export type TestCase = {
  number: number;
  passed: boolean;
  input: string | null;
  expected: string | null;
  actual: string | null;
  error: string | null;
  elapsedMs: number;
  hidden: boolean;
};
export type Result = {
  id: string;
  status: string;
  passed: number;
  total: number;
  elapsedMs: number;
  diagnostics: string | null;
  cases: TestCase[];
};
export type Attempt = {
  id: string;
  problemId: string;
  mode: string;
  status: string;
  passed: number;
  total: number;
  elapsedMs: number;
  timestamp: string;
  language: string | null;
  code: string | null;
  result: Result | null;
  legacy: boolean;
  sequence: number;
  codeFormat?: CodeFormat;
};
