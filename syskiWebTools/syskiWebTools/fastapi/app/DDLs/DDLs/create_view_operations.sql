CREATE VIEW operations AS
WITH CalculatedColumns AS (
    SELECT
        t1.seq_no,
        t1.issue_name,
        t1.incharge_team AS issue_team,
        t1.incharge_person,
        t1.act_ope_manhours,
        t2.issue_consideration_status,
        COALESCE(
          CASE
            WHEN t2.issue_consideration_status = '要件定義中' AND t1.act_ope_manhours = '想定不可' THEN CAST((SELECT mst_value FROM general_mst WHERE id = 6) AS INTEGER)
            WHEN t2.issue_consideration_status = '要件定義中' AND t1.act_ope_manhours = '特大' THEN CAST((SELECT mst_value FROM general_mst WHERE id = 7) AS INTEGER)
            WHEN t2.issue_consideration_status = '要件定義中' AND t1.act_ope_manhours = '大' THEN CAST((SELECT mst_value FROM general_mst WHERE id = 8) AS INTEGER)
            WHEN t2.issue_consideration_status = '要件定義中' AND t1.act_ope_manhours = '中' THEN CAST((SELECT mst_value FROM general_mst WHERE id = 9) AS INTEGER)
            WHEN t2.issue_consideration_status = '要件定義中' AND t1.act_ope_manhours = '小' THEN CAST((SELECT mst_value FROM general_mst WHERE id = 10) AS INTEGER)
            WHEN t2.issue_consideration_status = '要件定義中' AND t1.act_ope_manhours = '極小' THEN CAST((SELECT mst_value FROM general_mst WHERE id = 11) AS INTEGER)
            ELSE 0
          END, 0
        ) AS issue_consideration_inprogress_manhours,
        t2.estimated_mtg_last2wk_time,
        COALESCE(CASE WHEN t2.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_key = '想定打ち合わせ時間' AND category_value = CAST(t2.estimated_mtg_last2wk_time AS VARCHAR)) AS INTEGER)
                      ELSE 0
                    END, 0
                ) AS estimated_mtg_inprogress_manhours,
        t2.other_work_last2wk_time AS other_work_last2wk_time,
        COALESCE(CASE WHEN t2.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_key = 'その他作業時間' AND category_value = CAST(t2.other_work_last2wk_time AS VARCHAR)) AS INTEGER)
                      ELSE 0
                     END, 0
                ) AS other_work_inprogress_manhours,
        t2.remarks
    FROM
        issues t1
    JOIN
        operations_manual_input t2 ON t1.seq_no = t2.seq_no
),
syskiCounts AS (
    SELECT
        t1.seq_no AS seq_no,
        COUNT(*) AS syski_task_remain
    FROM
        task t3
    JOIN
        issues t1 ON t1.seq_no = t3.quarters || t3.issues_type || '(' || t3.issues_seq_no || ')'
    WHERE
        t3.incharge IN (SELECT mst_value FROM general_mst WHERE category_key = '業務設計担当T')
    GROUP BY t1.seq_no
),
allCounts AS (
    SELECT
        t1.seq_no AS seq_no,
        COUNT(*) AS all_task_remain
    FROM
        task t3
    JOIN
        issues t1 ON t1.seq_no = t3.quarters || t3.issues_type || '(' || t3.issues_seq_no || ')'
    GROUP BY t1.seq_no
)
SELECT
    cc.seq_no,
    cc.issue_name,
    cc.issue_team,
    cc.incharge_person,
    cc.act_ope_manhours,
    cc.issue_consideration_status,
    cc.issue_consideration_inprogress_manhours,
    sc.syski_task_remain,
    ac.all_task_remain,
    COALESCE(
      CASE 
        WHEN cc.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_key = '課題残数' AND category_value = CAST(sc.syski_task_remain AS VARCHAR)) AS INTEGER)
        ELSE 0
       END, 0
    ),
    cc.estimated_mtg_last2wk_time,
    cc.estimated_mtg_inprogress_manhours,
    cc.other_work_last2wk_time,
    cc.other_work_inprogress_manhours,
    COALESCE(cc.issue_consideration_inprogress_manhours, 0
    ) + COALESCE(
         CASE 
           WHEN cc.issue_consideration_status = '要件定義中' THEN CAST((SELECT mst_value FROM general_mst WHERE category_key = '課題残数' AND category_value = CAST(sc.syski_task_remain AS VARCHAR)) AS INTEGER)
           ELSE 0
         END, 0
    ) + COALESCE(cc.estimated_mtg_inprogress_manhours,0) + COALESCE(cc.other_work_inprogress_manhours,0) AS total_manhours,
    cc.remarks
FROM
    CalculatedColumns cc
JOIN
    syskiCounts sc ON cc.seq_no = sc.seq_no
JOIN
    allCounts ac ON cc.seq_no = ac.seq_no
;