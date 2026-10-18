import { useLayoutEffect, useRef } from 'react';
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import * as csharp from 'monaco-editor/esm/vs/basic-languages/csharp/csharp';
import * as javascript from 'monaco-editor/esm/vs/basic-languages/javascript/javascript';
import * as python from 'monaco-editor/esm/vs/basic-languages/python/python';
import * as cpp from 'monaco-editor/esm/vs/basic-languages/cpp/cpp';
import * as java from 'monaco-editor/esm/vs/basic-languages/java/java';
import EditorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';

self.MonacoEnvironment = { getWorker: () => new EditorWorker() };
// Switching problems or languages never fetches another grammar module.
for (const [id, grammar] of Object.entries({ csharp, javascript, python, cpp, java })) {
  if (!monaco.languages.getLanguages().some((language) => language.id === id))
    monaco.languages.register({ id });
  monaco.languages.setLanguageConfiguration(id, grammar.conf);
  monaco.languages.setMonarchTokensProvider(id, grammar.language);
}
monaco.editor.defineTheme('epi-dark', {
  base: 'vs-dark', inherit: true,
  rules: [
    { token: 'comment', foreground: '6f7d8e', fontStyle: 'italic' },
    { token: 'keyword', foreground: 'c5a6f7' },
  ],
  colors: {
    'editor.background': '#262626', 'editorLineNumber.foreground': '#4b5462',
    'editor.lineHighlightBackground': '#2b2b2b', 'editor.selectionBackground': '#354057',
    'editorCursor.foreground': '#f6ad55',
  },
});

type Props = {
  code: string;
  language?: string;
  onChange: (value: string) => void;
  onRun: () => void;
  onSubmit: () => void;
  busy: boolean;
};

export default function CodeEditor({ code, language = 'csharp', onChange, onRun, onSubmit, busy }: Props) {
  const container = useRef<HTMLDivElement>(null);
  const instance = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const callbacks = useRef({ onChange, onRun, onSubmit });
  callbacks.current = { onChange, onRun, onSubmit };
  const updating = useRef(false);

  useLayoutEffect(() => {
    const model = monaco.editor.createModel('', 'csharp');
    const editor = monaco.editor.create(container.current!, {
      model, theme: 'epi-dark', ariaLabel: 'Editor content',
      fontSize: 14, fontFamily: "'Cascadia Code', Consolas, monospace",
      minimap: { enabled: false }, padding: { top: 16, bottom: 16 },
      scrollBeyondLastLine: false, automaticLayout: true, tabSize: 4,
      wordWrap: 'on', smoothScrolling: true, renderLineHighlight: 'all',
      overviewRulerBorder: false, lineNumbersMinChars: 4, fixedOverflowWidgets: true,
    });
    instance.current = editor;
    const subscription = editor.onDidChangeModelContent(() => {
      // Programmatic switches must not overwrite another problem's saved code.
      if (!updating.current) callbacks.current.onChange(editor.getValue());
    });
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => callbacks.current.onRun());
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => callbacks.current.onSubmit());
    return () => {
      subscription.dispose();
      instance.current = null;
      editor.dispose();
      model.dispose();
    };
  }, []);

  useLayoutEffect(() => {
    const editor = instance.current;
    const model = editor?.getModel();
    if (!editor || !model) return;
    updating.current = true;
    try {
      if (model.getLanguageId() !== language) monaco.editor.setModelLanguage(model, language);
      if (editor.getValue() !== code) editor.setValue(code);
      editor.updateOptions({ readOnly: busy });
    } finally { updating.current = false; }
  }, [code, language, busy]);

  return <div ref={container} style={{ height: '100%', width: '100%' }} />;
}
