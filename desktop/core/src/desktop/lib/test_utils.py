#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from lxml import objectify, etree

from django.contrib.auth.models import Group, User
from useradmin.models import HuePermission, GroupPermission, get_default_user_group


def grant_access(username, groupname, appname):
    add_permission(username, groupname, 'access', appname)


def add_permission(username, groupname, permname, appname):
    user = User.objects.get(username=username)

    group, created = Group.objects.get_or_create(name=groupname)
    perm, created = HuePermission.objects.get_or_create(app=appname, action=permname)
    GroupPermission.objects.get_or_create(group=group, hue_permission=perm)

    if not user.groups.filter(name=group.name).exists():
        user.groups.add(group)
        user.save()


def add_to_group(username, groupname=get_default_user_group().name):
    user = User.objects.get(username=username)
    group, created = Group.objects.get_or_create(name=groupname)

    if not user.groups.filter(name=group.name).exists():
        user.groups.add(group)
        user.save()


def reformat_json(json_obj):
    if isinstance(json_obj, basestring):
        return json.dumps(json.loads(json_obj))
    else:
        return json.dumps(json_obj)


def reformat_xml(xml_obj):
    if isinstance(xml_obj, basestring):
        return etree.tostring(objectify.fromstring(xml_obj))
    else:
        return etree.tostring(xml_obj)
