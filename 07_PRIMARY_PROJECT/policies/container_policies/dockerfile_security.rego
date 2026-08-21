package main

# ------------------------------------------------------------------------------
# Policy-as-Code: Container & Dockerfile Security Rules
# Engine: Open Policy Agent (OPA) / Conftest
# ------------------------------------------------------------------------------

# Rule 1: Deny containers running as root (USER root or missing USER instruction)
deny[msg] {
    input[i].Cmd == "user"
    val := input[i].Value[0]
    val == "root"
    msg := sprintf("SECURITY VIOLATION [Policy-Container-01]: Line %d — Container must NOT run as root! Specify a non-root USER (e.g. USER 10001).", [i])
}

deny[msg] {
    users := [input[i] | input[i].Cmd == "user"]
    count(users) == 0
    msg := "SECURITY VIOLATION [Policy-Container-02]: Dockerfile lacks explicit 'USER' instruction! Default root user is prohibited."
}

# Rule 2: Deny using ':latest' tag for base images
deny[msg] {
    input[i].Cmd == "from"
    val := input[i].Value[0]
    contains(val, ":latest")
    msg := sprintf("SECURITY VIOLATION [Policy-Container-03]: Line %d — Base image '%v' uses dangerous ':latest' tag. Use pinned digest or explicit version tag.", [i, val])
}

# Rule 3: Deny ADD command (prefer COPY)
deny[msg] {
    input[i].Cmd == "add"
    val := input[i].Value[0]
    msg := sprintf("SECURITY VIOLATION [Policy-Container-04]: Line %d — Use of 'ADD' instruction ('%v') detected. Use 'COPY' to prevent remote URL extraction vulnerabilities.", [i, val])
}
