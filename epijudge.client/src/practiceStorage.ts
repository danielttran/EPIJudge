import { useEffect, useState, useSyncExternalStore } from 'react';
import { PracticeClient } from './practiceClient';
import type { CatalogEntry } from './practiceModels';

export { PracticeClient } from './practiceClient';

export function usePractice(catalog: CatalogEntry[]) {
  const [client] = useState(() => new PracticeClient());
  useSyncExternalStore(client.subscribe, client.snapshot);
  useEffect(() => {
    if (!catalog.length) return;
    void client.initialize(catalog);
    const focus = () => {
      void client.sync();
    };
    const visibility = () => {
      if (document.visibilityState === 'hidden') void client.flush().catch(() => {});
    };
    window.addEventListener('focus', focus);
    document.addEventListener('visibilitychange', visibility);
    return () => {
      window.removeEventListener('focus', focus);
      document.removeEventListener('visibilitychange', visibility);
    };
  }, [catalog, client]);
  return client;
}
