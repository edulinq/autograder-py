HEADERS = ['email', 'name', 'role', 'lms-id']
SYNC_HEADERS = HEADERS + ['operation']

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
    ('validation-errors', 'Validation Errors'),
    ('system-errors', 'System Errors'),
]

ALL_USER_OP_KEYS = [
    ('email', 'Email'),
] + USER_OP_KEYS + USER_OP_ERROR_KEYS

def list_users(users, table = False):
    if (table):
        _list_users_table(users)
    else:
        _list_users(users)

def _list_users(users, indent = ''):
    for user in users:
        print(indent + "Email:", user['email'])
        print(indent + "Name:", user['name'])
        print(indent + "Role:", user['role'])
        print(indent + "LMS ID:", user['lms-id'])
        print()

def _list_users_table(users, header = True, keys = HEADERS):
    if (header):
        print("\t".join(keys))

    for user in users:
        row = [user[key] for key in keys]
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
        _list_users(users, indent = INDENT)

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

def _list_user_op_results(results):
    op_results = {}
    for (key, label) in USER_OP_KEYS:
        emails = []
        for result in results:
            if (result.get(key, None) is not None):
                emails.append(result['email'])

        if (len(emails) > 0):
            op_results[label] = emails

    _print_user_op_results_from_dict(op_results)

    # Print all errors last so users can easily see them.
    for result in results:
        val_errors = result.get('validation-errors', None)
        if ((val_errors is not None) and (len(val_errors) > 0)):
            print("Encountered %d validation errors while operating on user: '%s'." % (
                len(val_errors), result['email']))

            for i in range(len(val_errors)):
                print(INDENT + "Index: %d, Message: '%s'." % (i, val_errors[i]['external-message']))

        sys_errors = result.get('system-errors', None)
        if ((sys_errors is not None) and (len(sys_errors) > 0)):
            print("Encountered %d system errors while operating on user: '%s'." % (
                len(sys_errors), result['email']))

            for i in range(len(sys_errors)):
                print(INDENT + "Index: %d, Message: '%s'." % (i, sys_errors[i]['external-message']))

def _list_user_op_results_table(results, header = True, keys = ALL_USER_OP_KEYS):
    rows = []
    for result in results:
        # Clean the error messages into a better format.
        for error_key, _ in USER_OP_ERROR_KEYS:
            if (result.get(error_key, None) is not None):
                result[error_key] = [error['external-message'] for error in result[error_key]]

        rows.append([result.get(key, '') for key, _ in keys])

    _print_tsv(rows, header, [header_key for _, header_key in keys])

def list_user_op_results(results, table = False):
    sorted_results = sorted(results, key=lambda x: x["email"])

    if (table):
        _list_user_op_results_table(sorted_results)
    else:
        _list_user_op_results(sorted_results)

def _print_user_op_results_from_dict(result):
    lines = []
    for label, emails in result.items():
        lines.append(label)
        for email in emails:
            lines.append(INDENT + email)

    print("\n".join(lines))

def _print_tsv(rows, header, header_keys):
    lines = []
    if (header):
        lines.append("\t".join(header_keys))

    for row in rows:
        lines.append("\t".join([str(value) for value in row]))

    print("\n".join(lines))
