import typing

import edq.config.app
import edq.util.crypto
import edq.util.time
import lms.model.constants

import autograder.filespec

class Config(edq.config.app.BaseApplicationConfig):
    """
    An application config for the autograder.

    This config encompasses most of what will be read on the command-line and config files.
    This includes both more persistent options (like server, username, and password),
    and single command options like the target course or user.
    Config options not represented here should be available in edq.config.app.BaseApplicationConfig._extra.
    """

    def __init__(self,
            allow_late: typing.Union[bool, None] = None,
            assignment: typing.Union[str, None] = None,
            auth_pass: typing.Union[edq.util.crypto.Secret, None] = None,
            auth_user: typing.Union[str, None] = None,
            bcc: typing.Union[typing.List[str], None] = None,
            body: typing.Union[str, None] = None,
            cc: typing.Union[typing.List[str], None] = None,
            course: typing.Union[str, None] = None,
            dry_run: typing.Union[bool, None] = None,
            filespec: typing.Union[autograder.filespec.FileSpec, None] = None,
            filespec_path: typing.Union[str, None] = None,
            filespec_reference: typing.Union[str, None] = None,
            filespec_token: typing.Union[str, None] = None,
            filespec_type: typing.Union[str, None] = None,
            filespec_username: typing.Union[str, None] = None,
            files: typing.Union[typing.List[str], None] = None,
            force_compute: typing.Union[bool, None] = None,
            email_html: typing.Union[bool, None] = None,
            include_extra_fields: typing.Union[bool, None] = None,
            message: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            new_course_role: typing.Union[str, None] = None,
            new_course: typing.Union[str, None] = None,
            new_email: typing.Union[str, None] = None,
            new_lms_id: typing.Union[str, None] = None,
            new_name: typing.Union[str, None] = None,
            new_pass: typing.Union[str, None] = None,
            new_role: typing.Union[str, None] = None,
            out_dir: typing.Union[str, None] = None,
            output_format: typing.Union[lms.model.constants.OutputFormat, None] = None,
            overwrite_records: typing.Union[bool, None] = None,
            path: typing.Union[str, None] = None,
            pretty_headers: typing.Union[bool, None] = None,
            proxy_email: typing.Union[str, None] = None,
            proxy_time: typing.Union[edq.util.time.Timestamp, None] = None,
            query_after: typing.Union[edq.util.time.Timestamp, None] = None,
            query_before: typing.Union[edq.util.time.Timestamp, None] = None,
            query_level: typing.Union[str, None] = None,
            query_limit: typing.Union[int, None] = None,
            query_metric_type: typing.Union[str, None] = None,
            query_past: typing.Union[str, None] = None,
            query_sort: typing.Union[int, None] = None,
            query_target_assignment: typing.Union[str, None] = None,
            query_target_course: typing.Union[str, None] = None,
            query_target_email: typing.Union[str, None] = None,
            query_use_testing_data: typing.Union[bool, None] = None,
            query_where: typing.Union[typing.Dict[str, str], None] = None,
            raw_course_users: typing.Union[typing.List[typing.Dict[str, typing.Any]], None] = None,
            raw_server_users: typing.Union[typing.List[typing.Dict[str, typing.Any]], None] = None,
            regrade_cutoff: typing.Union[int, None] = None,
            send_emails: typing.Union[bool, None] = None,
            server: typing.Union[str, None] = None,
            skip_build_images: typing.Union[bool, None] = None,
            skip_emails: typing.Union[bool, None] = None,
            skip_headers: typing.Union[bool, None] = None,
            skip_inserts: typing.Union[bool, None] = None,
            skip_lms_sync: typing.Union[bool, None] = None,
            skip_rows: typing.Union[int, None] = None,
            skip_source_sync: typing.Union[bool, None] = None,
            skip_template_files: typing.Union[bool, None] = None,
            skip_updates: typing.Union[bool, None] = None,
            subject: typing.Union[str, None] = None,
            submission_specs: typing.Union[typing.List[str], None] = None,
            target_email: typing.Union[str, None] = None,
            target_submission: typing.Union[str, None] = None,
            target_users: typing.Union[typing.List[str], None] = None,
            target_user: typing.Union[str, None] = None,
            testing_mode: typing.Union[bool, None] = None,
            token_id: typing.Union[str, None] = None,
            to: typing.Union[typing.List[str], None] = None,
            wait_for_completion: typing.Union[bool, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.allow_late: typing.Union[bool, None] = allow_late
        """ Allow this submission to be graded, even if it is late. """

        self.assignment: typing.Union[str, None] = assignment
        """ The ID of the assignment to make this request to. """

        self.auth_pass: typing.Union[edq.util.crypto.Secret, None] = auth_pass
        """ The password of the user making this request. """

        self.auth_user: typing.Union[str, None] = auth_user
        """ The email of the user making this request. """

        self.bcc: typing.Union[typing.List[str], None] = bcc
        """ A list of email addresses. Accepts course user references. """

        self.body: typing.Union[str, None] = body
        """ The email body. """

        self.cc: typing.Union[typing.List[str], None] = cc
        """ A list of email addresses. Accepts course user references. """

        self.course: typing.Union[str, None] = course
        """ The ID of the course to make this request to. """

        self.dry_run: typing.Union[bool, None] = dry_run
        """ Do not commit/finalize the operation, just do all the steps and state what the result would look like. """

        self.filespec: typing.Union[autograder.filespec.FileSpec, None] = filespec
        """ A filespec pointing to a course to upload. """

        self.filespec_path: typing.Union[str, None] = filespec_path
        """ The path the filespec points to. """

        self.filespec_reference: typing.Union[str, None] = filespec_reference
        """ The reference (e.g., git commit/branch) of the filespec. """

        self.filespec_token: typing.Union[str, None] = filespec_token
        """ The token for filespec authentication. """

        self.filespec_type: typing.Union[str, None] = filespec_type
        """ The type of filespec. """

        self.filespec_username: typing.Union[str, None] = filespec_username
        """ The username for filespec authentication. """

        self.files: typing.Union[typing.List[str], None] = files
        """ The path to your submission file(s). """

        self.force_compute: typing.Union[bool, None] = force_compute
        """ Force the server to compute the result, ignoring any existing cache. """

        self.email_html: typing.Union[bool, None] = email_html
        """ Indicates the email body contains HTML. """

        self.include_extra_fields: typing.Union[bool, None] = include_extra_fields
        """ Include non-common (usually LMS-specific) fields in results. """

        self.message: typing.Union[str, None] = message
        """ An optional message to attach to the submission. """

        self.name: typing.Union[str, None] = name
        """ An optional name to use. """

        self.new_course_role: typing.Union[str, None] = new_course_role
        """ The course role for the new user. """

        self.new_course: typing.Union[str, None] = new_course
        """ An optional course to enroll the new user in """

        self.new_email: typing.Union[str, None] = new_email
        """ The email for the new user. """

        self.new_lms_id: typing.Union[str, None] = new_lms_id
        """ The LMS ID for the new user. """

        self.new_name: typing.Union[str, None] = new_name
        """ The name for the new user. """

        self.new_pass: typing.Union[str, None] = new_pass
        """ The new password. """

        self.new_role: typing.Union[str, None] = new_role
        """ The server role for the new user. """

        self.out_dir: typing.Union[str, None] = out_dir
        """ A directory to write output in. """

        self.output_format: typing.Union[lms.model.constants.OutputFormat, None] = output_format
        """ The format to display the output as. """

        self.overwrite_records: typing.Union[bool, None] = overwrite_records
        """ Replace any existing records that match the current operation (e.g. re-do existing results). """

        self.path: typing.Union[str, None] = path
        """ The path to your course material. """

        self.pretty_headers: typing.Union[bool, None] = pretty_headers
        """ When displaying headers, try to make them look "pretty". """

        self.proxy_email: typing.Union[str, None] = proxy_email
        """ The email of the user the request is pretending to be made under (the submission will be made on behalf of this user). """

        self.proxy_time: typing.Union[edq.util.time.Timestamp, None] = proxy_time
        """ The proxy timestamp that will be applied to the request. """

        self.query_after: typing.Union[edq.util.time.Timestamp, None] = query_after
        """ If supplied, only return records after this timestamp. """

        self.query_before: typing.Union[edq.util.time.Timestamp, None] = query_before
        """ If supplied, only return records before this timestamp. """

        self.query_level: typing.Union[str, None] = query_level
        """ The minimum level of log records to return. """

        self.query_limit: typing.Union[int, None] = query_limit
        """ The maximum number of records to return. """

        self.query_metric_type: typing.Union[str, None] = query_metric_type
        """ The type of metric to query for. See: https://github.com/edulinq/autograder-server/blob/main/internal/stats/metrics.go#L29 """

        self.query_past: typing.Union[str, None] = query_past
        """ If supplied, only return log records in this duration (using "h", "m", or "s" suffixes) (e.g., "24h", "10m", or "1h10m10s"). """

        self.query_sort: typing.Union[int, None] = query_sort
        """ Sort the results. -1 for ascending, 0 for no sorting, 1 for descending. """

        self.query_target_assignment: typing.Union[str, None] = query_target_assignment
        """ If supplied, only return records for this assignment. """

        self.query_target_course: typing.Union[str, None] = query_target_course
        """ If supplied, only return records for this course. """

        self.query_target_email: typing.Union[str, None] = query_target_email
        """ If supplied, only return records for this email. """

        self.query_use_testing_data: typing.Union[bool, None] = query_use_testing_data
        """ Query from hard-coded testing data (instead of real data). """

        self.query_where: typing.Union[typing.Dict[str, str], None] = query_where
        """ Only includes records with a patching key/value pair. """

        self.raw_course_users: typing.Union[typing.List[typing.Dict[str, typing.Any]], None] = raw_course_users
        """ Raw course users to operate on. """

        self.raw_server_users: typing.Union[typing.List[typing.Dict[str, typing.Any]], None] = raw_server_users
        """ Raw server users to operate on. """

        self.regrade_cutoff: typing.Union[int, None] = regrade_cutoff
        """ All submissions occurring before the cutoff time will be regraded. """

        self.send_emails: typing.Union[bool, None] = send_emails
        """ Send any relevant emails to users affected by this operation (e.g., a user being enrolled in a course). """

        self.server: typing.Union[str, None] = server
        """ The URL of the autograder server to communicate with. """

        self.skip_build_images: typing.Union[bool, None] = skip_build_images
        """ Skip building assignment Docker images. """

        self.skip_emails: typing.Union[bool, None] = skip_emails
        """ Skip sending any emails. """

        self.skip_headers: typing.Union[bool, None] = skip_headers
        """ Skip headers when outputting results, will not apply to all formats. """

        self.skip_inserts: typing.Union[bool, None] = skip_inserts
        """ Skip insert operations. """

        self.skip_lms_sync: typing.Union[bool, None] = skip_lms_sync
        """ Skip syncing with the LMS. """

        self.skip_rows: typing.Union[int, None] = skip_rows
        """ The number of header rows to skip. """

        self.skip_source_sync: typing.Union[bool, None] = skip_source_sync
        """ Skip syncing (updating with) the course source. """

        self.skip_template_files: typing.Union[bool, None] = skip_template_files
        """ Skip fetching assignment template files. """

        self.skip_updates: typing.Union[bool, None] = skip_updates
        """ Skip update operations. """

        self.subject: typing.Union[str, None] = subject
        """ The email subject. """

        self.submission_specs: typing.Union[typing.List[str], None] = submission_specs
        """ A list of submission specifications. """

        self.target_email: typing.Union[str, None] = target_email
        """ The email of the user that is the target of this request. """

        self.target_submission: typing.Union[str, None] = target_submission
        """ The ID of the submission (default to the most recent submission). """

        self.target_users: typing.Union[typing.List[str], None] = target_users
        """ A list of user references. """

        self.target_user: typing.Union[str, None] = target_user
        """ The user that is the target of this request (defaults to you). """

        self.testing_mode: typing.Union[bool, None] = testing_mode
        """ If we should run as if we are in a test. """

        self.token_id: typing.Union[str, None] = token_id
        """ The id of the token to target. """

        self.to: typing.Union[typing.List[str], None] = to
        """ A list of email addresses. """

        self.wait_for_completion: typing.Union[bool, None] = wait_for_completion
        """ Wait for the full job to complete before returning. """
