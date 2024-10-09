import json

def handle_results(results, full_output = False):
    results = results['results']

    if (len(results) == 0):
        print("No courses found.")
        return 2

    error_count = 0
    for result in results:
        success = result['success']
        course_id = result['course-id']

        if (not success):
            error_count += 1

        if (full_output):
            continue

        if (not success):
            print("Course '%s' not updated." % (course_id))
            print("Message from server: '%s'." % (result.get('message', '')))
        elif (result.get('created', False)):
            print("Course '%s' created." % (course_id))
        else:
            print("Course '%s' updated." % (course_id))

    if (full_output):
        print(json.dumps(results, indent = 4))

    return error_count

def add_full_output_argument(parser):
    parser.add_argument('--full-output', dest = 'full_output',
        action = 'store_true', default = False,
        help = 'See the full course update output (as JSON) (default: %(default)s).')
