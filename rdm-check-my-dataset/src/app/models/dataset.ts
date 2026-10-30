import { User } from './user';

export interface DatasetBasicMetadata {
  identifier: string;
  title: string;
}

export interface Author {
  authorName: string |null;
  authorAffiliation: string | null;
} 

export interface Dataset {
  identifier: string;
  title: string;
  author: Author[];
  datasetUrl : string;
}

export enum Status {
  Draft = 'draft',
  SubmittedForReview = 'submitted_for_review',
  InReview = 'in_review',
  Returned = 'returned_to_author',
  Deaccessioned = 'deaccessioned',
  Published = 'published',
}


export interface CheckResult {
  result: boolean | null;
  warning: string | null;
}