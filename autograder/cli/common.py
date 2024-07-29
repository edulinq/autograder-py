HEADERS = ['email', 'name', 'role']
COURSE_HEADERS = ['id', 'name', 'role']
SYNC_HEADERS = HEADERS + ['operation']

SYNC_USERS_KEYS = [
    ('add-users', 'Added', 'add'),
    ('mod-users', 'Modified', 'mod'),
    ('del-users', 'Deleted', 'delete'),
    ('skip-users', 'Skipped', 'skip'),
]

def list_users(users, table = False):
    if (table):
        _list_users_table(users)
    else:
        _list_users(users)

def _list_users(users, indent = '', course_indent = '  '):
    for user in users:
        print(indent + "Email:", user['email'])
        print(indent + "Name:", user['name'])
        print(indent + "Role:", user['role'])
        print(indent + "Courses:")
        for course in user['courses']:
            print(indent + course_indent + "ID:", user['courses'][course]['id'])
            print(indent + course_indent + "Name:", user['courses'][course]['name'])
            print(indent + course_indent + "Role:", user['courses'][course]['role'])
            print()
        print()

def _list_users_table(users, header = True, keys = HEADERS, course_keys = COURSE_HEADERS):
    if (header):
        all_keys = keys + ["course-" + course_key for course_key in course_keys]
        print("\t".join(all_keys))

    for user in users:
        row = [user[key] for key in keys]
        for course in user['courses']:
            row.extend([user['courses'][course][course_key] for course_key in course_keys])

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
        _list_users(users, indent = '    ')

def _list_sync_users_table(sync_users):
    print("\t".join(SYNC_HEADERS))

    for (key, _, op) in SYNC_USERS_KEYS:
        users = sync_users[key]
        for user in users:
            user['operation'] = op

        _list_users_table(users, header = False, keys = SYNC_HEADERS)

def list_add_users(result, table = False):
    errors = result['errors']
    if ((errors is not None) and (len(errors) > 0)):
        print("Encounted %d errors." % (len(errors)))
        for error in errors:
            print("    Index: %d, Email: '%s', Message: '%s'." % (
                error['index'], error['email'], error['message']))

    list_sync_users(result, table = table)
