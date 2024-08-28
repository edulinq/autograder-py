USER_HEADERS = ['email', 'name']

COURSE_USER_HEADERS = USER_HEADERS + ['role', 'lms-id']
SYNC_HEADERS = COURSE_USER_HEADERS + ['operation']

BASE_SERVER_USER_HEADERS = USER_HEADERS + ['role']
SERVER_USER_HEADERS = BASE_SERVER_USER_HEADERS + ['courses']
COURSE_INFO_HEADERS = ['id', 'name', 'role']

INDENT = '    '

SYNC_USERS_KEYS = [
    ('add-users', 'Added', 'add'),
    ('mod-users', 'Modified', 'mod'),
    ('del-users', 'Deleted', 'delete'),
    ('skip-users', 'Skipped', 'skip'),
]

# Set course_users to True if listing course users, False for server users.
# An error will be raised if a user of a different type is found.
def list_users(users, course_users, table = False, normalize = False):
    if (course_users):
        if (table):
            _list_course_users_table(users)
        else:
            _list_course_users(users)
    else:
        if (table):
            if (normalize):
                _list_server_users_table_normalize(users)
            else:
                _list_server_users_table(users)
        else:
            _list_server_users(users)

def _list_course_users(users, indent = ''):
    for user in users:
        if (user['type'] != "CourseType"):
            raise ValueError("Invalid user type for listing course users: '%s'.", user['type'])

        print(indent + "Email:", user['email'])
        print(indent + "Name:", user['name'])
        print(indent + "Role:", user['role'])
        print(indent + "LMS ID:", user['lms-id'])
        print()

def _list_course_users_table(users, header = True, keys = COURSE_USER_HEADERS):
    rows = []
    for user in users:
        if (user['type'] != "CourseType"):
            raise ValueError("Invalid user type for listing course users table: '%s'.",
                    user['type'])

        row = [user[key] for key in keys]
        rows.append(row)

    _print_tsv(rows, header, keys)

def _list_server_users(users, indent = ''):
    for user in users:
        if (user['type'] != "ServerType"):
            raise ValueError("Invalid user type for listing server users: '%s'.", user['type'])

        print(indent + "Email:", user['email'])
        print(indent + "Name:", user['name'])
        print(indent + "Role:", user['role'])
        print(indent + "Courses:")
        for course in user['courses']:
            print(indent + INDENT + "ID:", user['courses'][course]['id'])
            print(indent + INDENT + "Name:", user['courses'][course]['name'])
            print(indent + INDENT + "Role:", user['courses'][course]['role'])
            print()
        print()

def _list_server_users_table(users, header = True, keys = SERVER_USER_HEADERS):
    rows = []
    for user in users:
        if (user['type'] != "ServerType"):
            raise ValueError("Invalid user type for listing server users table: '%s'.",
                    user['type'])

        row = [user[key] for key in keys]
        rows.append(row)

    _print_tsv(rows, header, keys)

def _list_server_users_table_normalize(users, header = True, keys = BASE_SERVER_USER_HEADERS):
    rows = []
    for user in users:
        if (user['type'] != "ServerType"):
            raise ValueError("Invalid user type for listing server users: '%s'.", user['type'])

        row = [user[key] for key in keys]
        if ((user.get('courses') is None) or (not user['courses'])):
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

        _list_course_users_table(users, header = False, keys = SYNC_HEADERS)

def list_add_users(result, table = False):
    errors = result['errors']
    if ((errors is not None) and (len(errors) > 0)):
        print("Encounted %d errors." % (len(errors)))
        for error in errors:
            print("    Index: %d, Email: '%s', Message: '%s'." % (
                error['index'], error['email'], error['message']))

    list_sync_users(result, table = table)

def _print_tsv(rows, header, header_keys):
    lines = []
    if (header):
        lines.append("\t".join(header_keys))

    for row in rows:
        lines.append("\t".join([str(value) for value in row]))

    print("\n".join(lines))
