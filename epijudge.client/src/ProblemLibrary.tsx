import { useEffect, useRef, useState } from 'react';
import {
  Braces,
  CheckCircle2,
  ChevronRight,
  Circle,
  Clock3,
  Code2,
  Download,
  Search,
  Upload,
  X,
} from 'lucide-react';
import type { Problem } from './workspaceModels';
import type { PracticeClient } from './practiceClient';

type Props = {
  open: boolean;
  problems: Problem[];
  selected: string;
  busy: boolean;
  practice: PracticeClient;
  storageNotice: string;
  onClose(): void;
  onSelect(id: string): void;
  onExport(): Promise<unknown>;
  onImport(file: File): Promise<unknown>;
};

export function ProblemLibrary({
  open,
  problems,
  selected,
  busy,
  practice,
  storageNotice,
  onClose,
  onSelect,
  onExport,
  onImport,
}: Props) {
  const libraryDialog = useRef<HTMLDialogElement>(null);
  const importInput = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState('');
  const [topic, setTopic] = useState('');
  useEffect(() => {
    if (open) libraryDialog.current?.showModal();
    else if (libraryDialog.current?.open) libraryDialog.current.close();
  }, [open]);
  const solved = new Set(
    Object.values(practice.progress)
      .filter((p) => p.status === 'solved')
      .map((p) => p.problemId),
  );
  const visibleProblems = problems.filter(
    (item) =>
      (!topic || item.topic === topic) &&
      `${item.title} ${item.topic} ${item.id}`.toLowerCase().includes(query.toLowerCase()),
  );
  const topics = [...new Set(problems.map((item) => item.topic))].sort();
  const solvedCount = problems.filter((item) => solved.has(item.id)).length;
  return (
    <dialog
      ref={libraryDialog}
      id="problem-library"
      className="library-dialog"
      aria-label="Problem library"
      onClose={onClose}
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <aside className="sidebar">
        <div className="library-heading">
          <span>
            <Code2 size={17} /> Problem library
          </span>
          <span className="count-chip">{problems.length}</span>
          <button className="icon-button" aria-label="Close problem list" onClick={() => onClose()}>
            <X size={20} />
          </button>
        </div>
        <label className="search-box">
          <Search size={15} />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Find a problem…"
            aria-label="Search problems"
          />
        </label>
        <select
          className="topic-filter"
          value={topic}
          onChange={(event) => setTopic(event.target.value)}
          aria-label="Filter by topic"
        >
          <option value="">All topics</option>
          {topics.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
        <div className="sidebar-label">{visibleProblems.length} EXERCISES</div>
        <nav className="problem-list" aria-label="Problems">
          {visibleProblems.map((item, index) => (
            <button
              key={item.id}
              disabled={busy}
              className={
                'problem-link ' +
                (practice.progress[item.id]?.status ?? '') +
                (item.id === selected ? ' selected' : '')
              }
              title={
                item.title +
                ' · ' +
                item.topic +
                ' · ' +
                (practice.progress[item.id]?.status ?? 'Not started')
              }
              aria-label={`${String(problems.indexOf(item) + 1).padStart(2, '0')}. ${item.title} — ${practice.progress[item.id]?.status ?? 'Not started'}`}
              aria-current={item.id === selected ? 'page' : undefined}
              onClick={() => {
                onSelect(item.id);
                onClose();
              }}
            >
              <span className={'problem-indicator ' + (practice.progress[item.id]?.status ?? '')}>
                {solved.has(item.id) ? (
                  <CheckCircle2 size={16} />
                ) : practice.progress[item.id]?.status === 'attempted' ? (
                  <Clock3 size={16} />
                ) : (
                  <Circle size={15} />
                )}
              </span>
              <span className="problem-link-text">
                <strong>
                  {String(problems.indexOf(item) + 1 || index + 1).padStart(2, '0')}. {item.title}
                </strong>
              </span>
              <ChevronRight size={14} className="problem-arrow" />
            </button>
          ))}
          {problems.length > 0 && visibleProblems.length === 0 && (
            <p className="sidebar-empty">No matching problems.</p>
          )}
        </nav>
        <div className="library-note">
          <span className="tiny-dot" /> Built on the EPI test corpus
          <p>
            All {problems.length} repository exercises available in C#, JavaScript, Python, C++, and
            Java.
          </p>
        </div>
        <div className="status-legend">
          <span className="solved">● Solved</span>
          <span className="attempted">● Attempted</span>
        </div>
        <div className="backup-actions">
          <button disabled={!practice.ready} onClick={() => void onExport()}>
            <Download size={14} /> Export answers
          </button>
          <button disabled={!practice.ready || busy} onClick={() => importInput.current?.click()}>
            <Upload size={14} /> Import answers
          </button>
          <input
            ref={importInput}
            type="file"
            accept="application/json,.json"
            hidden
            aria-label="Import answers file"
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) void onImport(file);
              event.target.value = '';
            }}
          />
        </div>
        {storageNotice && (
          <p className="storage-notice" role="status">
            {storageNotice}
          </p>
        )}
        <div className="progress-card">
          <div>
            <span>Your progress</span>
            <strong>
              {solvedCount}
              <small> / {problems.length}</small>
            </strong>
          </div>
          <div className="progress-track">
            <i style={{ width: `${(solvedCount / Math.max(1, problems.length)) * 100}%` }} />
          </div>
          <p>One problem at a time.</p>
        </div>
        <div className="sidebar-footer">
          <Braces size={15} />
          <span>React + ASP.NET Core</span>
          <span className="version">v0.1</span>
        </div>
      </aside>
    </dialog>
  );
}
