/*
Using this as a query:
  SELECT isolate.id, isolate.labid, isolate.isolate_number, isolate.creation_date_timestamp, isolate.final_date_timestamp, ren_drug.mnemo, ren_drug.long_name, assay_ast_analysis_result.mic, assay_ast_analysis_result.relationship_operator
   FROM isolate
   INNER JOIN assay ON isolate.id = assay.ast_assay_isolate_id
   RIGHT JOIN assay_ast_analysis_result ON assay.ast_assay_result_id = assay_ast_analysis_result.ast_assay_result_id
   INNER JOIN ren_drug ON assay_ast_analysis_result.drug_id = ren_drug.id;
*/
\c vitek_db
\copy (SELECT isolate.id, isolate.labid, isolate.isolate_number, isolate.creation_date_timestamp, isolate.final_date_timestamp, ren_drug.mnemo, ren_drug.long_name, assay_ast_analysis_result.mic, assay_ast_analysis_result.relationship_operator FROM isolate INNER JOIN assay ON isolate.id = assay.ast_assay_isolate_id RIGHT JOIN assay_ast_analysis_result ON assay.ast_assay_result_id = assay_ast_analysis_result.ast_assay_result_id INNER JOIN ren_drug ON assay_ast_analysis_result.drug_id = ren_drug.id) TO STDOUT CSV HEADER
