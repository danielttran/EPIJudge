import manifest from './content/lessons.json';

const bodies = import.meta.glob('./content/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
});
export const READING_LESSONS = manifest.map((lesson) => ({
  ...lesson,
  body: bodies[`./content/${lesson.id}.md`] as string,
}));
export type ReadingLesson = (typeof READING_LESSONS)[number];
export const readingLessonById = (id: string) => READING_LESSONS.find((lesson) => lesson.id === id);

export type ReadingDocument = {
  version: 1;
  notes: string;
  reviewed: boolean;
  checkpoints: string[];
  answers: Record<string, number>;
};
export const EMPTY_READING: ReadingDocument = {
  version: 1,
  notes: '',
  reviewed: false,
  checkpoints: [],
  answers: {},
};
export const EMPTY_READING_JSON = JSON.stringify(EMPTY_READING);

export function parseReading(code: string): ReadingDocument {
  try {
    const value = JSON.parse(code);
    if (
      value?.version !== 1 ||
      typeof value.notes !== 'string' ||
      value.notes.length > 20_000 ||
      typeof value.reviewed !== 'boolean' ||
      !Array.isArray(value.checkpoints) ||
      !value.checkpoints.every((id: unknown) => typeof id === 'string') ||
      !value.answers ||
      Array.isArray(value.answers) ||
      typeof value.answers !== 'object' ||
      !Object.values(value.answers).every(
        (answer) => Number.isInteger(answer) && Number(answer) >= 0,
      )
    )
      return { ...EMPTY_READING };
    return value;
  } catch {
    return { ...EMPTY_READING };
  }
}
