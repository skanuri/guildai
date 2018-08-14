# Copyright 2017-2018 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

from guild import cli
from guild import remote as remotelib

from . import remote_support

def list_runs(args):
    assert args.remote
    if args.archive:
        cli.error("--archive and --remote cannot both be used")
    remote = remote_support.remote_for_args(args)
    try:
        remote.list_runs(_remote_list_filters(args), args.verbose)
    except remotelib.RemoteProcessError as e:
        cli.error(exit_status=e.exit_status)

def _remote_list_filters(args):
    kw = args.as_kw()
    filter_names = [
        "all",
        "completed",
        "deleted",
        "error",
        "labels",
        "more",
        "ops",
        "running",
        "terminated",
        "unlabeled",
    ]
    filters = {name: kw[name] for name in filter_names}
    ignore_names = [
        "archive",
        "remote",
        "verbose",
    ]
    for name in filter_names + ignore_names:
        del kw[name]
    assert not kw, kw
    return filters