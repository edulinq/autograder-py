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

    trap exit SIGINT

    cd "${ROOT_DIR}"

    readonly API_VERSION_FILE="${ROOT_DIR}/autograder/api/version.json"
    readonly TESTDATA_VERSION_FILE="${ROOT_DIR}/testdata/autograder-testdata/autograder-server/resources/VERSION.json"

    if [[ ! -f "${API_VERSION_FILE}" ]]; then
        echo "ERROR: API version file not found: ${API_VERSION_FILE}"
        exit 2
    fi

    if [[ ! -f "${TESTDATA_VERSION_FILE}" ]]; then
        echo "ERROR: Testdata version file not found: ${TESTDATA_VERSION_FILE}"
        exit 3
    fi

    local api_version=$(python3 -c "import edq.util.json; print(edq.util.json.load_path('${API_VERSION_FILE}')['base-version'])")
    local testdata_version=$(python3 -c "import edq.util.json; print(edq.util.json.load_path('${TESTDATA_VERSION_FILE}')['base-version'])")

    if [[ "${api_version}" != "${testdata_version}" ]]; then
        echo "ERROR: autograder/api/version.json (${api_version}) does not match testdata server VERSION.json (${testdata_version})."
        exit 4
    fi

    return 0
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main "$@"
