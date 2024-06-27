CREATE OR REPLACE VIEW public.datasetversion_info
 AS
 SELECT DISTINCT ON (datasetversion.dataset_id) datasetversion.dataset_id,
    dvobject.authority,
    dvobject.identifier,
    datasetversion.id AS version_id,
    COALESCE(datasetversion.versionnumber, published.versionnumber) AS versionnumber,
    COALESCE(datasetversion.minorversionnumber, published.minorversionnumber) AS minorversionnumber,
    datasetversion.lastupdatetime,
    datasetversion.versionstate,
    dataset_locks.locks,
    dataset_reviewers.reviewers
   FROM datasetversion
     LEFT JOIN dvobject ON dvobject.id = datasetversion.dataset_id
     LEFT JOIN ( SELECT datasetlock.dataset_id,
            array_agg(datasetlock.reason) AS locks
           FROM datasetlock
          GROUP BY datasetlock.dataset_id) dataset_locks ON dataset_locks.dataset_id = datasetversion.dataset_id
     LEFT JOIN ( SELECT roleassignment.definitionpoint_id,
            array_agg(roleassignment.assigneeidentifier) AS reviewers
           FROM roleassignment
          WHERE roleassignment.role_id = 9
          GROUP BY roleassignment.definitionpoint_id) dataset_reviewers ON dataset_reviewers.definitionpoint_id = datasetversion.dataset_id
     LEFT JOIN ( SELECT DISTINCT ON (datasetversion_1.dataset_id) datasetversion_1.dataset_id,
            datasetversion_1.id AS version_id,
            datasetversion_1.versionnumber,
            datasetversion_1.minorversionnumber
           FROM datasetversion datasetversion_1
          WHERE datasetversion_1.versionstate::text <> 'DRAFT'::text
          ORDER BY datasetversion_1.dataset_id, datasetversion_1.id DESC) published ON published.dataset_id = datasetversion.dataset_id
  ORDER BY datasetversion.dataset_id, datasetversion.id DESC;

ALTER TABLE public.datasetversion_info
    OWNER TO __db_username__;
