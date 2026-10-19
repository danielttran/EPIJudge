import type { Draft } from './practiceModels';

const headers = { 'Content-Type': 'application/json', 'X-EpiJudge-Client': 'local-editor' };

export async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch('/api/practice' + path, {
    cache: 'no-store',
    signal: AbortSignal.timeout(20_000),
    ...options,
    headers,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(
      detail.message ??
        detail.detail ??
        'Could not reach saved answers. Your browser copy is retained.',
    );
  }
  return response.json();
}

export async function saveDraft(
  problem: string,
  language: string,
  write: { code: string; revision: number },
): Promise<{ saved: true; draft: Draft } | { saved: false; draft: Draft | null }> {
  const response = await fetch(`/api/practice/drafts/${encodeURIComponent(problem)}/${language}`, {
    method: 'PUT',
    signal: AbortSignal.timeout(15_000),
    headers,
    body: JSON.stringify({ code: write.code, revision: write.revision }),
  });
  if (response.status === 409) return { saved: false, draft: (await response.json()).draft };
  if (!response.ok)
    throw new Error('Could not save your answer. Retry saving before closing this tab.');
  return { saved: true, draft: await response.json() };
}

export async function downloadBackup() {
  const response = await fetch('/api/practice/export', {
    cache: 'no-store',
    signal: AbortSignal.timeout(60_000),
  });
  if (!response.ok) throw new Error('Could not export saved answers.');
  const url = URL.createObjectURL(await response.blob());
  try {
    const link = document.createElement('a');
    link.href = url;
    link.download = 'epi-answers-' + new Date().toISOString().slice(0, 10) + '.json';
    link.click();
  } finally {
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
}

export async function importBackup(text: string) {
  JSON.parse(text);
  await request('/import', { method: 'POST', body: text, signal: AbortSignal.timeout(120_000) });
}
