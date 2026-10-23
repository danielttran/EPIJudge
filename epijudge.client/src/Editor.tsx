import { useLayoutEffect, useRef } from 'react';
import { useTheme } from './theme';
import { useCodeFormatter } from './useCodeFormatter';
import type { CodeFormat } from './practiceModels';
import { AlignLeft, LoaderCircle } from 'lucide-react';
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
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: 'comment', foreground: '9aa6b8', fontStyle: 'italic' },
    { token: 'keyword', foreground: 'c5a6f7' },
    { token: 'string', foreground: 'dfac95' },
    { token: 'invalid', foreground: 'ff9595' },
  ],
  colors: {
    'editor.background': '#262626',
    'editorLineNumber.foreground': '#a0a0a0',
    'editorLineNumber.dimmedForeground': '#a0a0a0',
    'editorError.foreground': '#ff9595',
    'editorWidget.background': '#262626',
    'editor.lineHighlightBackground': '#2b2b2b',
    'editor.selectionBackground': '#30384a',
    'editor.inactiveSelectionBackground': '#30384a',
    'editorCursor.foreground': '#f6ad55',
    'editorBracketHighlight.foreground1': '#ffd700',
    'editorBracketHighlight.foreground2': '#e79ae6',
    'editorBracketHighlight.foreground3': '#8cbcff',
    'editorBracketHighlight.foreground4': '#c4b5fd',
    'editorBracketHighlight.foreground5': '#65d69a',
    'editorBracketHighlight.foreground6': '#ffb875',
  },
});

monaco.editor.defineTheme('epi-light', {
  base: 'vs',
  inherit: true,
  rules: [
    { token: 'comment', foreground: '52634c', fontStyle: 'italic' },
    { token: 'keyword', foreground: '7030a0' },
    { token: 'number', foreground: '0b6b4b' },
    { token: 'string', foreground: '9b302c' },
    { token: 'type.identifier', foreground: '125a75' },
    { token: 'invalid', foreground: 'ac253b' },
  ],
  colors: {
    'editor.background': '#ffffff',
    'editor.foreground': '#202733',
    'editorLineNumber.foreground': '#626b78',
    'editorLineNumber.dimmedForeground': '#626b78',
    'editorError.foreground': '#ac253b',
    'editorWidget.background': '#ffffff',
    'editor.lineHighlightBackground': '#f0f3f7',
    'editor.selectionBackground': '#edf3ff',
    'editor.inactiveSelectionBackground': '#edf3ff',
    'editorCursor.foreground': '#965000',
    'editorBracketHighlight.foreground1': '#1257b8',
    'editorBracketHighlight.foreground2': '#14633b',
    'editorBracketHighlight.foreground3': '#8a4900',
    'editorBracketHighlight.foreground4': '#7030a0',
    'editorBracketHighlight.foreground5': '#125a75',
    'editorBracketHighlight.foreground6': '#9b302c',
  },
});
function useEditorTheme() {
  const theme = useTheme();
  useLayoutEffect(() => {
    monaco.editor.setTheme('epi-' + theme);
  }, [theme]);
  return 'epi-' + theme;
}

type Props = {
  code: string;
  scope?: string;
  codeFormat?: CodeFormat;
  language?: string;
  onChange: (value: string) => void;
  onRun: () => void;
  onSubmit: () => void;
  busy: boolean;
};

export default function CodeEditor({
  code,
  language = 'csharp',
  scope = language,
  codeFormat = 'callable-v1',
  onChange,
  onRun,
  onSubmit,
  busy,
}: Props) {
  const editorTheme = useEditorTheme();
  const container = useRef<HTMLDivElement>(null);
  const instance = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const callbacks = useRef({ onChange, onRun, onSubmit });
  callbacks.current = { onChange, onRun, onSubmit };
  const updating = useRef(false);

  const formatter = useCodeFormatter({
    scope: `${scope}:${language}:${codeFormat}`,
    language,
    codeFormat,
    busy,
    read: () => {
      const editor = instance.current;
      const model = editor?.getModel();
      return editor && model ? { code: editor.getValue(), version: model.getVersionId() } : null;
    },
    apply: (formatted, original) => {
      const editor = instance.current;
      const model = editor?.getModel();
      if (
        !editor ||
        !model ||
        model.getVersionId() !== original.version ||
        editor.getValue() !== original.code
      )
        return;
      const view = editor.saveViewState();
      editor.pushUndoStop();
      editor.executeEdits('format-code', [
        { range: model.getFullModelRange(), text: formatted, forceMoveMarkers: true },
      ]);
      editor.pushUndoStop();
      if (view) editor.restoreViewState(view);
    },
  });

  useLayoutEffect(() => {
    const model = monaco.editor.createModel('', 'csharp');
    const editor = monaco.editor.create(container.current!, {
      model,
      theme: editorTheme,
      ariaLabel: 'Editor content',
      fontSize: 14,
      fontFamily: "'Cascadia Code', Consolas, monospace",
      minimap: { enabled: false },
      padding: { top: 16, bottom: 16 },
      scrollBeyondLastLine: false,
      automaticLayout: true,
      tabSize: 4,
      wordWrap: 'on',
      smoothScrolling: true,
      renderLineHighlight: 'all',
      overviewRulerBorder: false,
      lineNumbersMinChars: 4,
      fixedOverflowWidgets: true,
    });
    instance.current = editor;
    const subscription = editor.onDidChangeModelContent(() => {
      // Programmatic switches must not overwrite another problem's saved code.
      if (!updating.current) {
        formatter.clearMessage();
        callbacks.current.onChange(editor.getValue());
      }
    });
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () =>
      callbacks.current.onRun(),
    );
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () =>
      callbacks.current.onSubmit(),
    );
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
    } finally {
      updating.current = false;
    }
  }, [code, language, busy]);

  return (
    <div className="editable-code">
      <div className="format-toolbar">
        <button
          type="button"
          className="format-code-button"
          disabled={busy || formatter.pending}
          aria-busy={formatter.pending}
          onClick={() => void formatter.format()}
        >
          {formatter.pending ? (
            <LoaderCircle size={14} className="spin" />
          ) : (
            <AlignLeft size={14} />
          )}
          {formatter.pending ? 'Formatting…' : 'Format code'}
        </button>
        <span role="status" className="format-message">
          {formatter.message}
        </span>
      </div>
      <div ref={container} className="monaco-surface" />
    </div>
  );
}

// Each reference view owns a separate, read-only model. It has no change,
// grading, or storage callbacks and never reuses the user's editor model.
export function ReadOnlyCode({
  code,
  language,
  label,
  className = 'solution-code',
}: {
  code: string;
  language: string;
  label: string;
  className?: string;
}) {
  const editorTheme = useEditorTheme();
  const container = useRef<HTMLDivElement>(null);
  const instance = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const height = Math.min(480, Math.max(160, code.split('\n').length * 20 + 28));

  useLayoutEffect(() => {
    const model = monaco.editor.createModel('', 'csharp');
    const editor = monaco.editor.create(container.current!, {
      model,
      theme: editorTheme,
      readOnly: true,
      domReadOnly: true,
      ariaLabel: label,
      fontSize: 13,
      fontFamily: "'Cascadia Code', Consolas, monospace",
      lineNumbers: 'on',
      lineNumbersMinChars: 3,
      minimap: { enabled: false },
      padding: { top: 12, bottom: 12 },
      scrollBeyondLastLine: false,
      automaticLayout: true,
      tabSize: 4,
      wordWrap: 'on',
      renderLineHighlight: 'none',
      overviewRulerBorder: false,
      fixedOverflowWidgets: true,
    });
    instance.current = editor;
    return () => {
      instance.current = null;
      editor.dispose();
      model.dispose();
    };
  }, []);

  useLayoutEffect(() => {
    const editor = instance.current;
    const model = editor?.getModel();
    if (!editor || !model) return;
    if (model.getLanguageId() !== language) monaco.editor.setModelLanguage(model, language);
    if (editor.getValue() !== code) {
      editor.setValue(code);
      editor.setScrollPosition({ scrollTop: 0, scrollLeft: 0 });
    }
    editor.updateOptions({ ariaLabel: label });
  }, [code, language, label]);

  return <div ref={container} className={className} style={{ height }} />;
}
