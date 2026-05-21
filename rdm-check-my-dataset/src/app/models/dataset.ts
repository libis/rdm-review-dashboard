import { User } from './user';

export interface DatasetBasicMetadata {
  identifier: string;
  title: string;
}

export interface Dataset {
  identifier: string;
  title: string;
  description: string[];
  authorName: string[];
  status: Status;
  reviewer: string[];
  contributor: string[];
  reviewerDetails: User[];
  contributorDetails: User[];
  persistentUrl: string;
  version: number | null;
  versionMinorNumber: number | null;
  versionMajorNumber: number | null;
  createTime: string;
  lastUpdateTime: string;
  size: number;
  faculty: string[];
  department: string[];
  warnings: string[];
  locks: string[];
  datasetUrl: string;
}

export enum Status {
  Draft = 'draft',
  SubmittedForReview = 'submitted_for_review',
  InReview = 'in_review',
  Returned = 'returned_to_author',
  Deaccessioned = 'deaccessioned',
  Published = 'published',
}
