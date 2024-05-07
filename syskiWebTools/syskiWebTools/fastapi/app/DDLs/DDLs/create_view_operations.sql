CREATE VIEW operations AS
SELECT
  t1.seq_no,
  t1.issue_name,
  t1.issue_team,
  t1.issue_incharge,
  t1.issue_scale,
  t2.issue_consideration_status,
  COALESCE((CASE
    WHEN t2.issue_consideration_status = '要件定義中' THEN (SELECT general_mst.value FROM general_mst WHERE t1.issue_scale = general_mst.category_name)
    ELSE '0'
  END), 0) as issue_consideration_inprogress_manhours,
  t3_count.syski_task_remain,
  t3_count_all.all_task_remain,
  COALESCE((CASE
    WHEN t2.issue_consideration_status = '要件定義中' THEN (SELECT general_mst.value FROM general_mst WHERE t3_count.syski_task_remain = general_mst.category_name AND category_id = '課題残数')
    ELSE '0'
  END), 0) as correspond_manhours,
  t2.estimated_mtg_last2wk_time,
  COALESCE((CASE
    WHEN t2.issue_consideration_status = '要件定義中' THEN (SELECT general_mst.value FROM general_mst WHERE t2.estimated_mtg_last2wk_time = general_mst.category_name AND category_id = '想定打ち合わせ時間')
    ELSE '0'
  END), 0) as estimated_mtg_inprogress_manhours,
  t2.other_work_last2wk_time,
  COALESCE((CASE
    WHEN t2.issue_consideration_status = '要件定義中' THEN (SELECT general_mst.value FROM general_mst WHERE t2.other_work_last2wk_time = general_mst.category_name AND category_id = 'その他作業時間')
    ELSE '0'
  END), 0) as other_work_inprogress_manhours,
  (COALESCE(issue_consideration_inprogress_manhours, 0) + COALESCE(correspond_manhours, 0) + COALESCE(estimated_mtg_inprogress_manhours, 0) + COALESCE(other_work_inprogress_manhours, 0)) AS total_manhours,
  operations_manual_input.remarks
FROM
  issues t1
JOIN
  operations_manual_input t2 ON t1.seq_no = t2.seq_no
LEFT JOIN (
  SELECT
    t3.quarters || t3.issues_type || '(' || t3.issues_seq_no::text || ')' AS combined_column,
    COUNT(*) AS syski_task_remain
  FROM
    task t3
  WHERE
    t3.incharge IN (SELECT general_mst.value FROM general_mst WHERE category_name = '業務設計担当T')
  GROUP BY combined_column
) t3_count ON t1.seq_no = t3_count.combined_column
LEFT JOIN (
  SELECT
    t3.quarters || t3.issues_type || '(' || t3.issues_seq_no::text || ')' AS combined_column_2,
    COUNT(*) AS all_task_remain
  FROM
    task t3
  GROUP BY combined_column_2
) t3_count_all ON t1.seq_no = t3_count_all.combined_column_2;
;