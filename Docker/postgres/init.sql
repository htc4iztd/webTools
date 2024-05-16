\c syskidatabase

CREATE TABLE general_mst(
	id INTEGER,
	category_key VARCHAR(100),
	category_value VARCHAR(100),
	mst_value VARCHAR(100),
	remarks VARCHAR(100)
);

CREATE TABLE issues(
    search_key VARCHAR(100) PRIMARY KEY,
    withdrawal VARCHAR(100),
    seq_no VARCHAR(100),
    seq_branch_no INTEGER,
    issue_name VARCHAR(100),
    issue_div_conditions VARCHAR(100),
    req_department VARCHAR(100),
    req_incharge VARCHAR(100),
    req_department_mail VARCHAR(100),
    personal_folder_link VARCHAR(100),
    preliminary_items VARCHAR(100),
    req_doc_folder_link VARCHAR(100),
    application_category VARCHAR(100),
    changes_service_ope_req VARCHAR(100),
    review_purpose_effect VARCHAR(100),
    past_issue_seq INTEGER,
    first_entry_quarter INTEGER,
    info_sys_consul_center VARCHAR(100),
    mp_classification VARCHAR(100),
    issue_group VARCHAR(100),
    incharge_team VARCHAR(100),
    incharge_person VARCHAR(100),
    issue_explanation_team_leader VARCHAR(100),
    dev_promotion_candidate VARCHAR(100),
    sys_requirements VARCHAR(100),
    dev_promotion_confirm VARCHAR(100),
    necessity_prelim_exam VARCHAR(100),
    not_entry_allowed VARCHAR(100),
    considered_ope_manhours VARCHAR(100),
    point VARCHAR(100),
    changed_ope_manhours VARCHAR(100),
    after_reduction_adjustment VARCHAR(100),
    ope_unknown_mid VARCHAR(100),
    service_unknown_large VARCHAR(100),
    judge_logic VARCHAR(100),
    manual_ope_small VARCHAR(100),
    service_authorization_unknown_mid VARCHAR(100),
    outside_headquater_unorganized_mid VARCHAR(100),
    many_outside_mtgs VARCHAR(100),
    premise_outside_specification_mid VARCHAR(100),
    no_applicable_system VARCHAR(100),
    significant_review_functional_layout_tlarge VARCHAR(100),
    new_service_large VARCHAR(100),
    various_system_large VARCHAR(100),
    scalability_large VARCHAR(100),
    multi_option_large VARCHAR(100),
    effects_need_tobe_examined_mid VARCHAR(100),
    reduct_require VARCHAR(100),
    consideration_ope_manhours VARCHAR(100),
    premise_sapproximate_estimate VARCHAR(100),
    act_ope_manhours VARCHAR(100),
    variation_factor_selection VARCHAR(100),
    variation_factor_supplement VARCHAR(100),
    sapproximate_subject VARCHAR(100),
    sapproximate_policy VARCHAR(100),
    for_policy_consideration VARCHAR(100),
    premise_sapproximate VARCHAR(100),
    hearing_notices VARCHAR(100),
    spare VARCHAR(100),
    outside_headquater_issues VARCHAR(100),
    outside_headquarter_system VARCHAR(100),
    ld_related_flags VARCHAR(100),
    ae_related_flags VARCHAR(100),
    owl_influence VARCHAR(100),
    dev_integration_consul_target VARCHAR(100),
    sys_requirements_before_sin VARCHAR(100),
    incharge_exam VARCHAR(100),
    exam_tasklist_creation_date DATE,
    exam_tasklist_update_date DATE,
    exam_status VARCHAR(100),
    issue_overview VARCHAR(100),
    selection_file_first VARCHAR(100),
    comment_to_personal_selection_file VARCHAR(100),
    first_reflect_selection VARCHAR(100),
    first_selection_confirm VARCHAR(100),
    first_selection_condition VARCHAR(100)
);

CREATE TABLE operations_manual_input(
    seq_no VARCHAR(20),
    issue_consideration_status VARCHAR(15),
    estimated_mtg_last2wk_time DECIMAL,
    other_work_last2wk_time DECIMAL,
    remarks TEXT
);

CREATE TABLE task(
	id INTEGER,
	project_id INTEGER,
	project_name VARCHAR(100),
	key_id INTEGER,
	key VARCHAR(50),
	type_id INTEGER,
	type VARCHAR(30),
	category_id INTEGER,
	category_name VARCHAR(10),
	subject VARCHAR(1000),
	description TEXT,
	status_id INTEGER,
	status VARCHAR(10),
	close_reason_id INTEGER,
	close_reason VARCHAR(10),
	incharge_id INTEGER,
	incharge VARCHAR(10),
	register_id INTEGER,
	register VARCHAR(10),
	register_date TIMESTAMP,
	parent_task_key INTEGER,
	deadline DATE,
	changer_id INTEGER,
	changer INTEGER,
	change_date TIMESTAMP,
	attached INTEGER,
	system_under_consideration VARCHAR(30),
	system_tobe_consideration VARCHAR(30),
	quarters INTEGER,
	issues_type VARCHAR(10),
	issues_seq_no VARCHAR(10),
	require_doc_capture_necessity VARCHAR(10),
	require_doc_capture_version DECIMAL
);

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