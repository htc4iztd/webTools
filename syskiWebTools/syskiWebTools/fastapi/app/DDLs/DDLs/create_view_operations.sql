CREATE VIEW operations AS
WITH CalculatedColumns AS (
    SELECT
        t1.seq_no,
        t1.issue_name,
        t1.incharge_team,
        t1.incharge_person,
        t1.changed_ope_manhours,
        t2.issue_consideration_status,
        COALESCE(CASE WHEN t2.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_name = '適切なカテゴリID' AND category_id = 1) AS INTEGER) ELSE 0 END, 0) AS issue_consideration_inprogress_manhours,
        COALESCE(CASE WHEN t2.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_name = '課題残数' AND category_id = 2) AS INTEGER) ELSE 0 END, 0) AS correspond_manhours,
        COALESCE(CASE WHEN t2.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_name = '想定打ち合わせ時間' AND category_id = 3) AS INTEGER) ELSE 0 END, 0) AS estimated_mtg_inprogress_manhours,
        COALESCE(CASE WHEN t2.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_name = 'その他作業時間' AND category_id = 4) AS INTEGER) ELSE 0 END, 0) AS other_work_inprogress_manhours
    FROM
        issues t1
    JOIN
        operations_manual_input t2 ON t1.seq_no = t2.seq_no
),
Counts AS (
    SELECT
        t1.seq_no AS seq_no,
        COUNT(*) AS syski_task_remain,
        t3.quarters || t3.issues_type || '(' || t3.issues_seq_no::text || ')' AS combined_column
    FROM
        task t3
    JOIN
        issues t1 ON t1.seq_no = t3.issues_seq_no
    WHERE
        t3.incharge IN (SELECT mst_value FROM general_mst WHERE category_name = '業務設計担当T')
    GROUP BY combined_column, t1.seq_no
)
SELECT
    cc.*,
    co.syski_task_remain,
    (COALESCE(cc.issue_consideration_inprogress_manhours, 0) + COALESCE(cc.correspond_manhours, 0) + COALESCE(cc.estimated_mtg_inprogress_manhours, 0) + COALESCE(cc.other_work_inprogress_manhours, 0)) AS total_manhours,
    op.remarks
FROM
    CalculatedColumns cc
JOIN
    Counts co ON cc.seq_no = co.seq_no
JOIN
    operations_manual_input op ON cc.seq_no = op.seq_no;