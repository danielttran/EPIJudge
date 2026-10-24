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
import { libraryEntries, selectedStudyPlan, STUDY_PLANS } from './studyPlans';
import { availableCollections } from './collections';
import { availablePatterns, patternTags } from './problemGuidance';
import { EMPTY_READING_JSON, parseReading } from './reading/readingLessons';

type Props = {
  open: boolean;
  problems: Problem[];
  selected: string;
  busy: boolean;
  practice: PracticeClient;
  storageNotice: string;
  filter: string;
  onFilterChange(value: string): void;
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
  filter,
  onFilterChange,
  onClose,
  onSelect,
  onExport,
  onImport,
}: Props) {
  const libraryDialog = useRef<HTMLDialogElement>(null);
  const importInput = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState('');
  useEffect(() => {
    if (open) libraryDialog.current?.showModal();
    else if (libraryDialog.current?.open) libraryDialog.current.close();
  }, [open]);
  const solved = new Set(
    Object.values(practice.progress)
      .filter((p) => p.status === 'solved')
      .map((p) => p.problemId),
  );
  const entries = libraryEntries(problems, filter, query);
  const plan = selectedStudyPlan(filter);
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
          <span className="count-chip">{entries.length}</span>
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
          value={filter}
          onChange={(event) => onFilterChange(event.target.value)}
          aria-label="Filter by topic or study plan"
        >
          <option value="">All topics</option>
          <option value="kind:coding">Coding</option>
          <optgroup label="Collections">
            {availableCollections(problems).map((collection) => (
              <option key={collection.id} value={`collection:${collection.id}`}>
                {collection.name} — {collection.count} problems
              </option>
            ))}
          </optgroup>
          <optgroup label="Study plans">
            {STUDY_PLANS.map((plan) => (
              <option key={plan.id} value={`plan:${plan.id}`}>
                {plan.label}
              </option>
            ))}
          </optgroup>
          <optgroup label="Patterns">
            {availablePatterns(problems).map((tag) => (
              <option key={tag} value={`pattern:${tag}`}>
                {tag}
              </option>
            ))}
          </optgroup>
          <optgroup label="Topics">
            {topics.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </optgroup>
        </select>
        {plan && (
          <p className="study-plan-note">
            Follow this list in order. Ungraded items open a reading or design companion.
          </p>
        )}
        <div className="sidebar-label">
          {entries.length} ITEMS
          {plan ? ` · ${entries.filter((e) => e.problem).length} CODING` : ''}
          {entries.some((e) => e.lesson)
            ? ` · ${entries.filter((e) => e.lesson).length} READING`
            : ''}
        </div>
        <nav className="problem-list" aria-label="Problems">
          {entries.map((entry) => {
            const item = entry.problem;
            const lesson = entry.lesson;
            const id = item?.id ?? lesson?.id;
            const status = item
              ? (practice.progress[item.id]?.status ?? '')
              : lesson &&
                  parseReading(practice.codeFor(lesson.id, 'reading', EMPTY_READING_JSON)).reviewed
                ? 'reviewed'
                : '';
            return (
              <button
                key={entry.number}
                disabled={busy || !id}
                className={
                  'problem-link ' +
                  status +
                  (id === selected ? ' selected' : '') +
                  (!id ? ' book-only' : '')
                }
                title={
                  entry.title +
                  ' · ' +
                  entry.topic +
                  ' · ' +
                  (entry.reason ?? (status || 'Not started'))
                }
                aria-label={`${entry.number}. ${entry.title} — ${item ? status || 'Not started' : lesson ? status || 'Reading companion' : 'Book only'}`}
                aria-current={id === selected ? 'page' : undefined}
                onClick={() => {
                  if (!id) return;
                  onSelect(id);
                  onClose();
                }}
              >
                <span className={'problem-indicator ' + status}>
                  {(item && solved.has(item.id)) || status === 'reviewed' ? (
                    <CheckCircle2 size={16} />
                  ) : status === 'attempted' ? (
                    <Clock3 size={16} />
                  ) : (
                    <Circle size={15} />
                  )}
                </span>
                <span className="problem-link-text">
                  <strong>
                    {entry.number}. {entry.title}
                  </strong>
                  {item && (
                    <span className="library-patterns">{patternTags(item.id).join(' · ')}</span>
                  )}
                </span>
                {lesson && (
                  <span className="reading-badge">
                    {status === 'reviewed' ? 'Reviewed' : 'Read'}
                  </span>
                )}
                {id && <ChevronRight size={14} className="problem-arrow" />}
              </button>
            );
          })}
          {problems.length > 0 && entries.length === 0 && (
            <p className="sidebar-empty">No matching problems.</p>
          )}
        </nav>
        <div className="library-note">
          <span className="tiny-dot" /> Practice collections
          <p>
            All {problems.length} repository exercises available in C#, JavaScript, Python, C++, and
            Java.
          </p>
        </div>
        <div className="status-legend">
          <span className="solved">● Solved</span>
          <span className="attempted">● Attempted</span>
          <span className="reviewed">● Reviewed</span>
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
            <span>Overall coding progress</span>
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
