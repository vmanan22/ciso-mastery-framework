package main

# ------------------------------------------------------------------------------
# Policy-as-Code: IAM Least Privilege Enforcement Rules
# Engine: Open Policy Agent (OPA) / Conftest
# ------------------------------------------------------------------------------

# Rule 1: Deny IAM Policies with Wildcard (*) Actions
deny[msg] {
    policy := input.resource.aws_iam_policy[name]
    statement := json_unmarshal_statement(policy.policy)[_]
    statement.Effect == "Allow"
    has_wildcard_action(statement.Action)
    msg := sprintf("SECURITY VIOLATION [Policy-IAM-01]: IAM Policy '%v' grants dangerous wildcard '*' Action! Must specify explicit actions.", [name])
}

# Helper function to check for wildcard action
has_wildcard_action(actions) {
    is_string(actions)
    actions == "*"
}

has_wildcard_action(actions) {
    is_array(actions)
    actions[_] == "*"
}

# Helper function to parse JSON policy strings safely
json_unmarshal_statement(policy_str) = statements {
    is_string(policy_str)
    parsed := json.unmarshal(policy_str)
    statements := parsed.Statement
} else = statements {
    is_object(policy_str)
    statements := policy_str.Statement
}
