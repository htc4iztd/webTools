CREATE TABLE issues(
    search_key VARCHAR(100) PRIMARY KEY,
    withdrawal VARCHAR(100),
    seq_no INTEGER,
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
    considered_ope_manhours DECIMAL,
    point VARCHAR(100),
    changed_ope_manhours DECIMAL,
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
    consideration_ope_manhours DECIMAL,
    premise_sapproximate_estimate VARCHAR(100),
    act_ope_manhours DECIMAL,
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