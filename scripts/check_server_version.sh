#!/bin/bash

# Check that the supported server version in autograder/api/version.json
# matches the version in the server testdata.

readonly THIS_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd | xargs realpath)"
readonly ROOT_DIR="${THIS_DIR}/.."

function main() {
    if [[ $# -ne 0 ]]; then
        echo "USAGE: $0"
        exit 1
    fi

    set -e
    trap exit SIGINT

    cd "${ROOT_DIR}"

    local api_version
    local testdata_version

    api_version=$(python3 -c "import json; print(json.load(open('autograder/api/version.json'))['base-version'])")
    testdata_version=$(python3 -c "import json; print(json.load(open('testdata/autograder-testdata/autograder-server/resources/VERSION.json'))['base-version'])")

    if [[ "${api_version}" != "${testdata_version}" ]]; then
        echo "ERROR: autograder/api/version.json (${api_version}) does not match testdata server VERSION.json (${testdata_version})."
        return 1
    fi

    return 0
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main "$@"
