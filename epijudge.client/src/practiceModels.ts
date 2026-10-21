export type CodeFormat = 'legacy-v1' | 'callable-v1';
export type CodeDocument = { code: string; codeFormat: CodeFormat };
export const codeFormatOrLegacy = (format?: CodeFormat): CodeFormat => format ?? 'legacy-v1';

export type Draft = {
  problemId: string;
  language: string;
  code: string;
  revision: number;
  updatedAt: string;
  codeFormat?: CodeFormat;
};
export type Pending = {
  code: string;
  revision: number;
  codeFormat?: CodeFormat;
  conflict?: Draft;
  writtenAt?: number;
};
export type Progress = {
  problemId: string;
  status: 'solved' | 'attempted';
  acceptedLanguages: string[];
};
export type CatalogEntry = { id: string };
