USER_HEADERS = ['email', 'name']
COURSE_USER_HEADERS = USER_HEADERS + ['role', 'lms-id']
SERVER_USER_HEADERS = USER_HEADERS + ['role', 'courses']
COURSE_HEADERS = ['id', 'name', 'role']
EXPANDED_SERVER_USER_HEADERS = USER_HEADERS + ['role'] + COURSE_HEADERS
SYNC_HEADERS = COURSE_USER_HEADERS + ['operation']

INDENT = '    '

SYNC_USERS_KEYS = [
    ('add-users', 'Added', 'add'),
    ('mod-users', 'Modified', 'mod'),
    ('del-users', 'Deleted', 'delete'),
    ('skip-users', 'Skipped', 'skip'),
]

# TODO: Add a param for expanding table.
def list_users(users, course_users, table = False):
    if (table):
        if course_users:
            _list_course_users_table(users)
        else:
            _list_server_users_table(users)
    else:
        if course_users:
            _list_course_users(users)
        else:
            _list_server_users(users)

def _list_course_users(users, indent = ''):
    for user in users:
        if user['type'] != "CourseType":
            raise ValueError("Invalid user type for listing course users: '%s'.", user['type'])

        print(indent + "Email:", user['email'])
        print(indent + "Name:", user['name'])
        print(indent + "Role:", user['role'])
        print(indent + "LMS ID:", user['lms-id'])
        print()

def _list_course_users_table(users, header = True, keys = COURSE_USER_HEADERS):
    if (header):
        print("\t".join(keys))

    for user in users:
        if user['type'] != "CourseType":
            raise ValueError("Invalid user type for listing course users: '%s'.", user['type'])

        row = [user[key] for key in keys]
        print("\t".join([str(value) for value in row]))

def _list_server_users(users, indent = ''):
    for user in users:
        if user['type'] != "ServerType":
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

# TODO: Fix extending the column to a better type.
def _list_server_users_table(users, header = True, keys = SERVER_USER_HEADERS):
    if (header):
        print("\t".join(keys))

    for user in users:
        if user['type'] != "ServerType":
            raise ValueError("Invalid user type for listing server users: '%s'.", user['type'])

        row = [user[key] for key in keys]
        # for course in user['courses']:
        #     row.extend([user['courses'][course][course_key] for course_key in course_keys])

        print("\t".join([str(value) for value in row]))

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
