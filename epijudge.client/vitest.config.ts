import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    restoreMocks: true,
    clearMocks: true,
    coverage: {
      include: [
        'src/practice*.ts',
        'src/draftRecovery.ts',
        'src/legacyMigration.ts',
        'src/workspaceModels.ts',
        'src/studyPlans.ts',
        'src/collections.ts',
        'src/reading/readingLessons.ts',
        'src/reading/raceSimulation.ts',
        'src/use*.ts',
      ],
      reporter: ['text', 'json-summary'],
      thresholds: { lines: 90, statements: 90, functions: 85, branches: 80 },
    },
  },
});
