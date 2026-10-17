import Editor, { loader, type OnMount } from '@monaco-editor/react';
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import 'monaco-editor/esm/vs/basic-languages/csharp/csharp.contribution';
import EditorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';

self.MonacoEnvironment = { getWorker: () => new EditorWorker() };
loader.config({ monaco });

type Props = {
  code: string;
  onChange: (value: string) => void;
  onRun: () => void;
  onSubmit: () => void;
  busy: boolean;
};

export default function CodeEditor({ code, onChange, onRun, onSubmit, busy }: Props) {
  const mount: OnMount = (editor, api) => {
    api.editor.defineTheme('epi-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'comment', foreground: '6f7d8e', fontStyle: 'italic' },
        { token: 'keyword', foreground: 'c5a6f7' },
      ],
      colors: {
        'editor.background': '#15181e',
        'editorLineNumber.foreground': '#4b5462',
        'editor.lineHighlightBackground': '#1c2028',
        'editor.selectionBackground': '#354057',
        'editorCursor.foreground': '#f6ad55',
      },
    });
    api.editor.setTheme('epi-dark');
    editor.addCommand(api.KeyMod.CtrlCmd | api.KeyCode.Enter, onRun);
    editor.addCommand(api.KeyMod.CtrlCmd | api.KeyMod.Shift | api.KeyCode.Enter, onSubmit);
  };
  return (
    <Editor
      height="100%"
      language="csharp"
      theme="epi-dark"
      value={code}
      onChange={(value) => onChange(value ?? '')}
      onMount={mount}
      loading={<div className="editor-loading">Preparing your editor…</div>}
      options={{
        fontSize: 14,
        fontFamily: "'Cascadia Code', Consolas, monospace",
        minimap: { enabled: false },
        padding: { top: 22, bottom: 16 },
        scrollBeyondLastLine: false,
        automaticLayout: true,
        tabSize: 4,
        wordWrap: 'on',
        readOnly: busy,
        smoothScrolling: true,
        renderLineHighlight: 'all',
        overviewRulerBorder: false,
        lineNumbersMinChars: 4,
        fixedOverflowWidgets: true,
      }}
    />
  );
}
