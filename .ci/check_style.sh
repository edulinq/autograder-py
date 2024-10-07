#!/bin/bash

# Check style.

readonly THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly BASE_DIR="${THIS_DIR}/.."

function main() {
    if [[ $# -ne 0 ]]; then
        echo "USAGE: $0"
        exit 1
    fi

    trap exit SIGINT

    local error_count=0

    python3 -m autograder.cli.util.style \
        --ignore "${BASE_DIR}/tests/api/data/hw0_no_compile.py" \
        "${BASE_DIR}/autograder" \
        "${BASE_DIR}/tests"
    ((error_count += $?))

    if [[ ${error_count} -gt 0 ]] ; then
        echo "Found ${error_count} style issues."
    else
        echo "No style issues found."
    fi

    return ${error_count}
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main "$@"
