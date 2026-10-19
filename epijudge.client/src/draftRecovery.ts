import type { Pending } from './practiceModels';

export function read<T>(key: string, fallback: T): T {
  try {
    return JSON.parse(localStorage.getItem(key) ?? 'null') ?? fallback;
  } catch {
    return fallback;
  }
}
export function write(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

export class DraftRecovery {
  readonly unavailable = new Set<string>();
  private readonly tabId = crypto.randomUUID();
  private recoveryKey(key: string) {
    return `epi:pending:${this.tabId}:${key}`;
  }
  keep(key: string, pending: Pending) {
    pending.writtenAt = Date.now();
    if (write(this.recoveryKey(key), pending)) this.unavailable.delete(key);
    else this.unavailable.add(key);
  }
  find(key: string): Pending | null {
    try {
      const copies: Pending[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const storageKey = localStorage.key(i)!;
        if (storageKey.startsWith('epi:pending:') && storageKey.endsWith(':' + key)) {
          const pending = read<Pending | null>(storageKey, null);
          if (
            pending &&
            typeof pending.code === 'string' &&
            Number.isSafeInteger(pending.revision) &&
            pending.revision >= 0
          )
            copies.push(pending);
        }
      }
      return copies.sort((a, b) => (b.writtenAt ?? 0) - (a.writtenAt ?? 0))[0] ?? null;
    } catch {
      return null;
    }
  }
  clear(key: string, code: string) {
    try {
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const storageKey = localStorage.key(i)!;
        if (
          storageKey.startsWith('epi:pending:') &&
          storageKey.endsWith(':' + key) &&
          read<Pending | null>(storageKey, null)?.code === code
        )
          localStorage.removeItem(storageKey);
      }
    } catch {
      /* A retained copy is safer than discarding it. */
    }
  }
}
