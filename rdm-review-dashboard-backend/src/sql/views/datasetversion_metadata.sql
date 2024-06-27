CREATE OR REPLACE VIEW public.datasetversion_metadata
 AS
 SELECT metadata.version_id,
    metadata.fieldtype_id,
    datasetfieldtype.name,
    array_agg(metadata.value) AS value
   FROM ( SELECT datasetfield.datasetversion_id AS version_id,
            datasetfield.datasetfieldtype_id AS fieldtype_id,
            datasetfieldvalue.value
           FROM datasetfield
             LEFT JOIN datasetfieldvalue ON datasetfield.id = datasetfieldvalue.datasetfield_id
        UNION ALL
         SELECT parentdatasetfield.datasetversion_id AS version_id,
            datasetfield.datasetfieldtype_id AS fieldtype_id,
            datasetfieldvalue.value
           FROM datasetfield
             LEFT JOIN datasetfieldcompoundvalue ON datasetfieldcompoundvalue.id = datasetfield.parentdatasetfieldcompoundvalue_id
             LEFT JOIN datasetfield parentdatasetfield ON datasetfieldcompoundvalue.parentdatasetfield_id = parentdatasetfield.id
             LEFT JOIN datasetfieldvalue ON datasetfield.id = datasetfieldvalue.datasetfield_id
             LEFT JOIN datasetfieldtype compoundfieldtype ON compoundfieldtype.id = datasetfield.datasetfieldtype_id
        UNION ALL
         SELECT datasetfield.datasetversion_id AS version_id,
            datasetfield.datasetfieldtype_id AS fieldtype_id,
            controlledvocabularyvalue.strvalue AS value
           FROM datasetfield
             LEFT JOIN datasetfield_controlledvocabularyvalue ON datasetfield_controlledvocabularyvalue.datasetfield_id = datasetfield.id
             LEFT JOIN controlledvocabularyvalue ON controlledvocabularyvalue.id = datasetfield_controlledvocabularyvalue.controlledvocabularyvalues_id) metadata
     LEFT JOIN datasetfieldtype ON datasetfieldtype.id = metadata.fieldtype_id
  WHERE metadata.value IS NOT NULL
  GROUP BY metadata.version_id, metadata.fieldtype_id, datasetfieldtype.name;

ALTER TABLE public.datasetversion_metadata
    OWNER TO __db_username__;
