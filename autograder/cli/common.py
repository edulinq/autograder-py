BASE_USER_HEADERS = ['email', 'name', 'role']

COURSE_USER_HEADERS = BASE_USER_HEADERS + ['lms-id']
SYNC_HEADERS = COURSE_USER_HEADERS + ['operation']

SERVER_USER_HEADERS = BASE_USER_HEADERS + ['courses']
COURSE_INFO_HEADERS = ['id', 'name', 'role']

INDENT = '    '
COURSE_USER_INFO_TYPE = 'course'
SERVER_USER_INFO_TYPE = 'server'

INDENT = '    '

SYNC_USERS_KEYS = [
    ('add-users', 'Added', 'add'),
    ('mod-users', 'Modified', 'mod'),
    ('del-users', 'Deleted', 'delete'),
    ('skip-users', 'Skipped', 'skip'),
]

USER_OP_KEYS = [
    ('added', 'Added'),
    ('modified', 'Modified'),
    ('removed', 'Removed'),
    ('skipped', 'Skipped'),
    ('not-exists', 'Not Exists'),
    ('emailed', 'Emailed'),
    ('enrolled', 'Enrolled'),
    ('dopped', 'Dropped'),
]

USER_OP_ERROR_KEYS = [
    ('validation-error', 'Validation Error'),
    ('system-error', 'System Error'),
    ('communication-error', 'Communication Error'),
]

ALL_USER_OP_KEYS = [
    ('email', 'Email'),
] + USER_OP_KEYS + USER_OP_ERROR_KEYS

# Set course_users to True if listing course users, False for server users.
# An error will be raised if a user of a different type is found.
def list_users(users, course_users, table = False, normalize = False):
    if (course_users):
        if (table):
            _list_users_table(users, True)
        else:
            _list_course_users(users)
    else:
        if (table):
            if (normalize):
                _list_server_users_table_normalize(users)
            else:
                _list_users_table(users, False)
        else:
            _list_server_users(users)

# Set course_users to True if listing course users, False for server users.
# An error will be raised if a user of a different type is found.
def _list_users_table(users, course_users, header = True, keys = []):
    expected_user_info_type = ''
    if (course_users):
        expected_user_info_type = COURSE_USER_INFO_TYPE
        if (len(keys) == 0):
            keys = COURSE_USER_HEADERS
    else:
        expected_user_info_type = SERVER_USER_INFO_TYPE
        if (len(keys) == 0):
            keys = SERVER_USER_HEADERS

    rows = []
    for user in users:
        if (user['type'] != expected_user_info_type):
            raise ValueError("Invalid user type for listing users table: Expected: '%s',"
                    + " actual: '%s'.", expected_user_info_type, user['type'])

        row = [user[key] for key in keys]
        rows.append(row)

    _print_tsv(rows, header, keys)

def _list_course_users(users, indent = ''):
    for i in range(len(users)):
        user = users[i]

        if (user['type'] != COURSE_USER_INFO_TYPE):
            raise ValueError("Invalid user type for listing course users: Expected: '%s',"
                    + " actual: '%s'.", COURSE_USER_INFO_TYPE, user['type'])

        if (i != 0):
            print()

        print(indent + "Email: " + user['email'])
        print(indent + "Name: " + user['name'])
        print(indent + "Role: " + user['role'])
        print(indent + "LMS ID: " + user['lms-id'])

def _list_server_users(users, indent = ''):
    for i in range(len(users)):
        user = users[i]

        if (user['type'] != SERVER_USER_INFO_TYPE):
            raise ValueError("Invalid user type for listing server users: Expected: '%s',"
                    + "actual: '%s'.", SERVER_USER_INFO_TYPE, user['type'])

        if (i != 0):
            print()

        print(indent + "Email: " + user['email'])
        print(indent + "Name: " + user['name'])
        print(indent + "Role: " + user['role'])
        print(indent + "Courses:")

        for j, course in enumerate(user['courses']):
            if (j != 0):
                print()

            print(indent + INDENT + "ID: " + user['courses'][course]['id'])
            print(indent + INDENT + "Name: " + user['courses'][course]['name'])
            print(indent + INDENT + "Role: " + user['courses'][course]['role'])

def _list_server_users_table_normalize(users, header = True, keys = BASE_USER_HEADERS):
    rows = []
    for user in users:
        if (user['type'] != SERVER_USER_INFO_TYPE):
            raise ValueError("Invalid user type for listing normalized server users table:"
                    + " Expected: '%s', actual: '%s'.", SERVER_USER_INFO_TYPE, user['type'])

        row = [user[key] for key in keys]
        if ((user.get('courses') is None) or (len(user['courses']) == 0)):
            row = row + ['' for key in COURSE_INFO_HEADERS]
            rows.append(row)
        else:
            for course in user['courses']:
                course_row = row + [user['courses'][course][key] for key in COURSE_INFO_HEADERS]
                rows.append(course_row)

    header_keys = keys + ["course-" + course_key for course_key in COURSE_INFO_HEADERS]
    _print_tsv(rows, header, header_keys)

def list_sync_users(sync_users, table = False):
    if (table):
        _list_sync_users_table(sync_users)
    else:
        _list_sync_users(sync_users)

def _list_sync_users(sync_users):
    count = (len(sync_users['add-users'])
            + len(sync_users['mod-users'])
            + len(sync_users['del-users']))
    print("Synced %d users." % (count))

    for (key, label, _) in SYNC_USERS_KEYS:
        users = sync_users[key]
        if (len(users) == 0):
            continue

        print("%s Users:" % (label))
        _list_course_users(users, indent = INDENT)

def _list_sync_users_table(sync_users):
    print("\t".join(SYNC_HEADERS))

    for (key, _, op) in SYNC_USERS_KEYS:
        users = sync_users[key]
        for user in users:
            user['operation'] = op

        _list_users_table(users, True, header = False, keys = SYNC_HEADERS)

def list_add_users(result, table = False):
    errors = result['errors']
    if ((errors is not None) and (len(errors) > 0)):
        print("Encountered %d errors." % (len(errors)))
        for error in errors:
            print("    Index: %d, Email: '%s', Message: '%s'." % (
                error['index'], error['email'], error['message']))

    list_sync_users(result, table = table)

def _list_user_op_responses(results):
    error_count = 0
    for result in results:
        print(result['email'])
        for op_key, label in USER_OP_KEYS:
            if (result.get(op_key, None) is not None):
                print(INDENT + label)
                if (isinstance(result[op_key], list)):
                    for value in result[op_key]:
                        print(INDENT + INDENT + value)

        for error_key, label in USER_OP_ERROR_KEYS:
            if (result.get(error_key, None) is not None):
                error_count += 1
                print(INDENT + label)
                print(INDENT + INDENT + result[error_key]['message'])

    print()
    print("Processed %d users. Encountered %d errors." % (len(results), error_count))

def _list_user_op_responses_table(results, header = True, keys = ALL_USER_OP_KEYS):
    rows = []
    for result in results:
        for error_key, _ in USER_OP_ERROR_KEYS:
            if (result.get(error_key, None) is not None):
                result[error_key] = result[error_key]['message']

        rows.append([result.get(key, '') for key, _ in keys])

    _print_tsv(rows, header, [header_key for _, header_key in keys])

def list_user_op_responses(results, table = False):
    if (table):
        _list_user_op_responses_table(results)
    else:
        _list_user_op_responses(results)

def _print_tsv(rows, header, header_keys):
    lines = []
    if (header):
        lines.append("\t".join(header_keys))

    for row in rows:
        lines.append("\t".join([str(value) for value in row]))

    print("\n".join(lines))
