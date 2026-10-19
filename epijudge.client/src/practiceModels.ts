export type Draft = {
  problemId: string;
  language: string;
  code: string;
  revision: number;
  updatedAt: string;
};
export type Pending = { code: string; revision: number; conflict?: Draft; writtenAt?: number };
export type Progress = {
  problemId: string;
  status: 'solved' | 'attempted';
  acceptedLanguages: string[];
};
export type CatalogEntry = { id: string };
