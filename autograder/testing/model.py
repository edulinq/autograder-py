"""
Data for tests.
Most model data will be copied over from the LMS toolkit and updated for the autograder.
"""

import typing

import lms.model.testdata.users
import lms.model.users

import autograder.model.log

def _clean_server_user(user: lms.model.users.ServerUser) -> None:
    """
    Clean the server user for use with the autograder.
    Replace the ID with email.
    """

    user.id = str(user.email)

def _clean_server_users() -> typing.Dict[str, lms.model.users.ServerUser]:
    """ Copy over the LMS Toolkit test server users, but clean users. """

    users = lms.model.testdata.users.SERVER_USERS.copy()
    for user in users.values():
        _clean_server_user(user)

    return users

def _clean_course_users() -> typing.Dict[str, typing.Dict[str, lms.model.users.CourseUser]]:
    """ Copy over the LMS Toolkit test course users, but clean users. """

    course_users = {}

    for name, raw_users in lms.model.testdata.users.COURSE_USERS.items():
        users = raw_users.copy()
        for user in users.values():
            _clean_server_user(user)

        course_users[name] = users

    return course_users

# {name: user, ...}
SERVER_USERS: typing.Dict[str, lms.model.users.ServerUser] = _clean_server_users()

# {course_name: {user_name: user, ...}, ...}
COURSE_USERS: typing.Dict[str, typing.Dict[str, lms.model.users.CourseUser]] = _clean_course_users()

API_LOGS: typing.List[typing.Dict[str, typing.Any]] = [
    {
        "assignment": "hw0",
        "course": "course101",
        "level": -20,
        "message": "Trace Course Log",
        "timestamp": 100,
        "user": "course-other@test.edulinq.org"
    },
    {
        "level": -20,
        "message": "Trace Server Log",
        "timestamp": 150,
        "user": "server-user@test.edulinq.org"
    },
    {
        "assignment": "hw0",
        "course": "course101",
        "level": -10,
        "message": "Debug Course Log",
        "timestamp": 200,
        "user": "course-student@test.edulinq.org"
    },
    {
        "level": -10,
        "message": "Debug Server Log",
        "timestamp": 250,
        "user": "server-creator@test.edulinq.org"
    },
    {
        "assignment": "hw0",
        "course": "course101",
        "level": 0,
        "message": "Info Course Log",
        "timestamp": 300,
        "user": "course-grader@test.edulinq.org"
    },
    {
        "level": 0,
        "message": "Info Server Log",
        "timestamp": 350,
        "user": "server-admin@test.edulinq.org"
    },
    {
        "assignment": "hw0",
        "course": "course101",
        "error": "Course Warning",
        "level": 10,
        "message": "Warn Course Log",
        "timestamp": 400,
        "user": "course-admin@test.edulinq.org"
    },
    {
        "error": "Server Warning",
        "level": 10,
        "message": "Warn Server Log",
        "timestamp": 450,
        "user": "server-owner@test.edulinq.org"
    },
    {
        "course": "course101",
        "error": "Course Error",
        "level": 20,
        "message": "Error Course Log",
        "timestamp": 500,
        "user": "course-owner@test.edulinq.org"
    },
    {
        "error": "Server Error",
        "level": 20,
        "message": "Error Server Log",
        "timestamp": 550
    },
    {
        "course": "course101",
        "level": 30,
        "message": "Fatal Course Log",
        "timestamp": 600
    },
    {
        "level": 30,
        "message": "Fatal Server Log",
        "timestamp": 650
    }
]

PARSED_LOGS: typing.List[autograder.model.log.LogRecord] = [autograder.model.log.LogRecord.from_api(record) for record in API_LOGS]

# pylint: disable=line-too-long
STACK_TRACE_PAYLOAD: typing.Dict[str, typing.Any] = {
    "count": 11,
    "stacks": [
        {
            "name": "goroutine 69",
            "records": [
                {
                    "call": "github.com/edulinq/autograder/internal/util.getStackTraces(0x1)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/util/stack.go",
                    "line": 47,
                    "pointer": "+0x65"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/util.GetAllStackTraces(...)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/util/stack.go",
                    "line": 38,
                    "pointer": ""
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/system.HandleStacks(0x0?)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/system/stacks.go",
                    "line": 20,
                    "pointer": "+0x19"
                },
                {
                    "call": "reflect.Value.call({0xdab400?, 0x1012168?, 0xc0002340e0?}, {0xed5e4e, 0x4}, {0xc000541840, 0x1, 0xc000541858?})",
                    "file": "/usr/lib/go/src/reflect/value.go",
                    "line": 581,
                    "pointer": "+0xcc6"
                },
                {
                    "call": "reflect.Value.Call({0xdab400?, 0x1012168?, 0x0?}, {0xc000541840?, 0x0?, 0x0?})",
                    "file": "/usr/lib/go/src/reflect/value.go",
                    "line": 365,
                    "pointer": "+0xb9"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/core.callHandler({0xdab400?, 0x1012168?}, {0xdd1c40?, 0xc00054c000?})",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/core/routing.go",
                    "line": 237,
                    "pointer": "+0xf6"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/core.handleAPIEndpoint({0x1112390, 0xc0002e03c0}, 0xc000390a00, {0xdab400, 0x1012168})",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/core/routing.go",
                    "line": 116,
                    "pointer": "+0x166"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/core.MustNewAPIRoute.func1({0x1112390, 0xc0002e03c0}, 0xc000390a00)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/core/route.go",
                    "line": 87,
                    "pointer": "+0xc5"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/core.(*BaseRoute).Handle(...)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/core/route.go",
                    "line": 48,
                    "pointer": ""
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/core.ServeRoutes(0xc000328018, {0x1112390, 0xc0002e03c0}, 0xc000390a00)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/core/routing.go",
                    "line": 72,
                    "pointer": "+0x37d"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.createAPIServer.GetRouteServer.func1({0x1112390?, 0xc0002e03c0?}, 0x1?)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/core/routing.go",
                    "line": 43,
                    "pointer": "+0x2d"
                },
                {
                    "call": "net/http.HandlerFunc.ServeHTTP(0x41f445?, {0x1112390?, 0xc0002e03c0?}, 0xc0002e0301?)",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 2322,
                    "pointer": "+0x29"
                },
                {
                    "call": "net/http.serverHandler.ServeHTTP({0x110fbf8?}, {0x1112390?, 0xc0002e03c0?}, 0x6?)",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 3340,
                    "pointer": "+0x8e"
                },
                {
                    "call": "net/http.(*conn).serve(0xc0005007e0, {0x1114498, 0xc0002f4a80})",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 2109,
                    "pointer": "+0x665"
                },
                {
                    "call": "created by net/http.(*Server).Serve in goroutine 30",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 3493,
                    "pointer": "+0x485"
                }
            ],
            "status": "running"
        },
        {
            "name": "goroutine 1",
            "records": [
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock(0xc0003b24c0, {0xedf2a7?, 0x0?})",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 68,
                    "pointer": "+0x25f"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/procedures/server.RunAndBlock.RunAndBlockFull.func1(0xc00017de78, {0xedf2a7, 0xe}, 0xf8?)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/procedures/server/start.go",
                    "line": 113,
                    "pointer": "+0x115"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/procedures/server.RunAndBlockFull(...)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/procedures/server/start.go",
                    "line": 118,
                    "pointer": ""
                },
                {
                    "call": "github.com/edulinq/autograder/internal/procedures/server.RunAndBlock({0xedf2a7?, 0x0?})",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/procedures/server/start.go",
                    "line": 96,
                    "pointer": "+0x2b"
                },
                {
                    "call": "main.main()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/cmd/server/main.go",
                    "line": 23,
                    "pointer": "+0xf6"
                }
            ],
            "status": "chan receive"
        },
        {
            "name": "goroutine 7",
            "records": [
                {
                    "call": "github.com/edulinq/autograder/internal/lockmanager.removeStaleLocks()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/lockmanager/lockmanager.go",
                    "line": 108,
                    "pointer": "+0x54"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/lockmanager.init.0 in goroutine 1",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/lockmanager/lockmanager.go",
                    "line": 28,
                    "pointer": "+0x4c"
                }
            ],
            "status": "chan receive"
        },
        {
            "name": "goroutine 27",
            "records": [
                {
                    "call": "github.com/shirou/gopsutil/v4/internal/common.Sleep({0x1113ef8, 0x1758900}, 0x0?)",
                    "file": "/home/edulinq/go/pkg/mod/github.com/shirou/gopsutil/v4@v4.24.11/internal/common/sleep.go",
                    "line": 13,
                    "pointer": "+0x76"
                },
                {
                    "call": "github.com/shirou/gopsutil/v4/cpu.PercentWithContext({0x1113ef8, 0x1758900}, 0xdf8475800, 0x0)",
                    "file": "/home/edulinq/go/pkg/mod/github.com/shirou/gopsutil/v4@v4.24.11/cpu/cpu.go",
                    "line": 164,
                    "pointer": "+0x71"
                },
                {
                    "call": "github.com/shirou/gopsutil/v4/cpu.Percent(...)",
                    "file": "/home/edulinq/go/pkg/mod/github.com/shirou/gopsutil/v4@v4.24.11/cpu/cpu.go",
                    "line": 150,
                    "pointer": ""
                },
                {
                    "call": "github.com/edulinq/autograder/internal/stats.getSystemMetrics(0xc00018b860?)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/stats/system.go",
                    "line": 149,
                    "pointer": "+0xc5"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/stats.collectSystemStats(0xea60)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/stats/system.go",
                    "line": 62,
                    "pointer": "+0xe8"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/stats.startSystemStatsCollection in goroutine 1",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/stats/system.go",
                    "line": 95,
                    "pointer": "+0x137"
                }
            ],
            "status": "select"
        },
        {
            "name": "goroutine 29",
            "records": [
                {
                    "call": "time.Sleep(0x1bf08eb000)",
                    "file": "/usr/lib/go/src/runtime/time.go",
                    "line": 363,
                    "pointer": "+0x165"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/tasks.runTasks()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/tasks/core.go",
                    "line": 58,
                    "pointer": "+0x6f"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/tasks.Start in goroutine 1",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/tasks/core.go",
                    "line": 27,
                    "pointer": "+0x7f"
                }
            ],
            "status": "sleep"
        },
        {
            "name": "goroutine 30",
            "records": [
                {
                    "call": "internal/poll.runtime_pollWait(0x7f026465b600, 0x72)",
                    "file": "/usr/lib/go/src/runtime/netpoll.go",
                    "line": 351,
                    "pointer": "+0x85"
                },
                {
                    "call": "internal/poll.(*pollDesc).wait(0xc00048e080?, 0x900000036?, 0x0)",
                    "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                    "line": 84,
                    "pointer": "+0x27"
                },
                {
                    "call": "internal/poll.(*pollDesc).waitRead(...)",
                    "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                    "line": 89,
                    "pointer": ""
                },
                {
                    "call": "internal/poll.(*FD).Accept(0xc00048e080)",
                    "file": "/usr/lib/go/src/internal/poll/fd_unix.go",
                    "line": 613,
                    "pointer": "+0x28c"
                },
                {
                    "call": "net.(*netFD).accept(0xc00048e080)",
                    "file": "/usr/lib/go/src/net/fd_unix.go",
                    "line": 161,
                    "pointer": "+0x29"
                },
                {
                    "call": "net.(*TCPListener).accept(0xc0000b92c0)",
                    "file": "/usr/lib/go/src/net/tcpsock_posix.go",
                    "line": 159,
                    "pointer": "+0x1b"
                },
                {
                    "call": "net.(*TCPListener).Accept(0xc0000b92c0)",
                    "file": "/usr/lib/go/src/net/tcpsock.go",
                    "line": 380,
                    "pointer": "+0x30"
                },
                {
                    "call": "net/http.(*Server).Serve(0xc00037e100, {0x1112090, 0xc0000b92c0})",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 3463,
                    "pointer": "+0x30c"
                },
                {
                    "call": "net/http.(*Server).ListenAndServe(0xc00037e100)",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 3389,
                    "pointer": "+0x72"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.runAPIServerInternal()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/http_socket.go",
                    "line": 135,
                    "pointer": "+0x85"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.runAPIServer(0xc000328018, 0xc000270ce0)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/http_socket.go",
                    "line": 54,
                    "pointer": "+0x152"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock.func2()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 48,
                    "pointer": "+0x2f"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock in goroutine 1",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 47,
                    "pointer": "+0x13f"
                }
            ],
            "status": "IO wait"
        },
        {
            "name": "goroutine 31",
            "records": [
                {
                    "call": "internal/poll.runtime_pollWait(0x7f026465b800, 0x72)",
                    "file": "/usr/lib/go/src/runtime/netpoll.go",
                    "line": 351,
                    "pointer": "+0x85"
                },
                {
                    "call": "internal/poll.(*pollDesc).wait(0xc000037b00?, 0xc00036ed70?, 0x0)",
                    "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                    "line": 84,
                    "pointer": "+0x27"
                },
                {
                    "call": "internal/poll.(*pollDesc).waitRead(...)",
                    "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                    "line": 89,
                    "pointer": ""
                },
                {
                    "call": "internal/poll.(*FD).Accept(0xc000037b00)",
                    "file": "/usr/lib/go/src/internal/poll/fd_unix.go",
                    "line": 613,
                    "pointer": "+0x28c"
                },
                {
                    "call": "net.(*netFD).accept(0xc000037b00)",
                    "file": "/usr/lib/go/src/net/fd_unix.go",
                    "line": 161,
                    "pointer": "+0x29"
                },
                {
                    "call": "net.(*UnixListener).accept(0x41f445?)",
                    "file": "/usr/lib/go/src/net/unixsock_posix.go",
                    "line": 172,
                    "pointer": "+0x16"
                },
                {
                    "call": "net.(*UnixListener).Accept(0xc00028cf60)",
                    "file": "/usr/lib/go/src/net/unixsock.go",
                    "line": 260,
                    "pointer": "+0x30"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.runUnixSocketServer(0xc000270ce0)",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/unix_socket.go",
                    "line": 49,
                    "pointer": "+0x14f"
                },
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock.func3()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 52,
                    "pointer": "+0x25"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock in goroutine 1",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 51,
                    "pointer": "+0x199"
                }
            ],
            "status": "IO wait"
        },
        {
            "name": "goroutine 50",
            "records": [
                {
                    "call": "os/signal.signal_recv()",
                    "file": "/usr/lib/go/src/runtime/sigqueue.go",
                    "line": 152,
                    "pointer": "+0x29"
                },
                {
                    "call": "os/signal.loop()",
                    "file": "/usr/lib/go/src/os/signal/signal_unix.go",
                    "line": 23,
                    "pointer": "+0x13"
                },
                {
                    "call": "created by os/signal.Notify.func1.1 in goroutine 1",
                    "file": "/usr/lib/go/src/os/signal/signal.go",
                    "line": 152,
                    "pointer": "+0x1f"
                }
            ],
            "status": "syscall"
        },
        {
            "name": "goroutine 51",
            "records": [
                {
                    "call": "github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock.func4()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 61,
                    "pointer": "+0x25"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock in goroutine 1",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/api/server/server.go",
                    "line": 60,
                    "pointer": "+0x23e"
                }
            ],
            "status": "chan receive"
        },
        {
            "name": "goroutine 70",
            "records": [
                {
                    "call": "internal/poll.runtime_pollWait(0x7f026465b400, 0x72)",
                    "file": "/usr/lib/go/src/runtime/netpoll.go",
                    "line": 351,
                    "pointer": "+0x85"
                },
                {
                    "call": "internal/poll.(*pollDesc).wait(0xc0002f8100?, 0xc00026a361?, 0x0)",
                    "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                    "line": 84,
                    "pointer": "+0x27"
                },
                {
                    "call": "internal/poll.(*pollDesc).waitRead(...)",
                    "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                    "line": 89,
                    "pointer": ""
                },
                {
                    "call": "internal/poll.(*FD).Read(0xc0002f8100, {0xc00026a361, 0x1, 0x1})",
                    "file": "/usr/lib/go/src/internal/poll/fd_unix.go",
                    "line": 165,
                    "pointer": "+0x279"
                },
                {
                    "call": "net.(*netFD).Read(0xc0002f8100, {0xc00026a361?, 0x1711cf0?, 0xc000524770?})",
                    "file": "/usr/lib/go/src/net/fd_posix.go",
                    "line": 68,
                    "pointer": "+0x25"
                },
                {
                    "call": "net.(*conn).Read(0xc00050e048, {0xc00026a361?, 0xc00005ac08?, 0xc000528000?})",
                    "file": "/usr/lib/go/src/net/net.go",
                    "line": 196,
                    "pointer": "+0x45"
                },
                {
                    "call": "net/http.(*connReader).backgroundRead(0xc00026a340)",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 702,
                    "pointer": "+0x33"
                },
                {
                    "call": "created by net/http.(*connReader).startBackgroundRead in goroutine 69",
                    "file": "/usr/lib/go/src/net/http/server.go",
                    "line": 698,
                    "pointer": "+0xb6"
                }
            ],
            "status": "IO wait"
        },
        {
            "name": "goroutine 60",
            "records": [
                {
                    "call": "github.com/edulinq/autograder/internal/log.logToBackend.gowrap1()",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/log/logging.go",
                    "line": 122,
                    "pointer": ""
                },
                {
                    "call": "runtime.goexit({})",
                    "file": "/usr/lib/go/src/runtime/asm_amd64.s",
                    "line": 1693,
                    "pointer": "+0x1"
                },
                {
                    "call": "created by github.com/edulinq/autograder/internal/log.logToBackend in goroutine 69",
                    "file": "/home/edulinq/code/autograder/autograder-py/testdata/autograder-testdata/autograder-server/internal/log/logging.go",
                    "line": 122,
                    "pointer": "+0x8a"
                }
            ],
            "status": "runnable"
        }
    ]
}
