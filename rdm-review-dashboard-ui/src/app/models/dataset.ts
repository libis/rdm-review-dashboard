import { User } from "./user.model";
import Status = Dataset.Status;

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
}

export interface DatasetCount {
  status: string;
  count: number
}
export interface DatasetContact {
  datasetContactName: string | null;
  datasetContactAffiliation: string | null;
  datasetContactEmail: string | null;
}

export namespace Dataset {
  export enum Status {
    Draft = 'draft',
    SubmittedForReview = 'submitted_for_review',
    InReview = 'in_review',
    Returned = 'returned_to_author',
    Deaccessioned = 'deaccessioned',
    Published = 'published'
  }

export function statusString(dataset: Dataset | null): string {
  if (!dataset) { return 'N/A' }

  switch (dataset.status) {
    case Dataset.Status.InReview: return 'In review';
    case Dataset.Status.SubmittedForReview: return 'Submitted for review'
    case Dataset.Status.Returned: return 'Returned to author';
    case Dataset.Status.Draft: return 'Draft';
    case Dataset.Status.Deaccessioned: return 'Deaccessioned';
    case Dataset.Status.Published: return 'Published';
  }
  return 'N/A';
}


export function getStatus(statusValue: string): Dataset.Status {
  switch (statusValue) {
    case 'deaccessioned': return Dataset.Status.Deaccessioned;
    case 'in_review': return Dataset.Status.InReview;
    case 'submitted_for_review': return Dataset.Status.SubmittedForReview;
    case 'returned_to_author': return Dataset.Status.Returned;
    case 'published': return Dataset.Status.Published;
    case 'draft': return Dataset.Status.Draft;
  }

  return Dataset.Status.Draft;
}



}




