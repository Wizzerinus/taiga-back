# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL
from django.db.models import Q

from taiga.permissions.services import user_has_perm
from taiga.projects.attachments.utils import attach_basic_attachments
from taiga.projects.notifications.utils import attach_watchers_to_queryset
from taiga.projects.notifications.utils import attach_total_watchers_to_queryset
from taiga.projects.notifications.utils import attach_is_watcher_to_queryset
from taiga.projects.votes.utils import attach_total_voters_to_queryset
from taiga.projects.votes.utils import attach_is_voter_to_queryset


def attach_generated_user_stories(queryset, as_field="generated_user_stories_attr"):
    """Attach generated user stories json column to each object of the queryset.

    :param queryset: A Django issues queryset object.
    :param as_field: Attach the generated user stories as an attribute with this name.

    :return: Queryset object with the additional `as_field` field.
    """
    model = queryset.model
    sql = """SELECT json_agg(row_to_json(t))
                FROM(
                    SELECT
                        userstories_userstory.id,
                        userstories_userstory.ref,
                        userstories_userstory.subject
                FROM userstories_userstory
                WHERE generated_from_issue_id = {tbl}.id) t"""

    sql = sql.format(tbl=model._meta.db_table)
    queryset = queryset.extra(select={as_field: sql})
    return queryset


def attach_extra_info(queryset, user=None, include_attachments=False):
    if include_attachments:
        queryset = attach_basic_attachments(queryset)
        queryset = queryset.extra(select={"include_attachments": "True"})

    queryset = attach_generated_user_stories(queryset)
    queryset = attach_total_voters_to_queryset(queryset)
    queryset = attach_watchers_to_queryset(queryset)
    queryset = attach_total_watchers_to_queryset(queryset)
    queryset = attach_is_voter_to_queryset(queryset, user)
    queryset = attach_is_watcher_to_queryset(queryset, user)
    return queryset


def get_allowed_scopes(user, project, target="view") -> list[str]:
    allow_normal = True
    allow_testing = user_has_perm(user, f"{target}_issues_testing", project)
    allow_security = user_has_perm(user, f"{target}_issues_security", project)
    allowed_scopes = []
    for perm, name in [(allow_normal, "normal"), (allow_testing, "testing"), (allow_security, "security")]:
        if perm:
            allowed_scopes.append(name)
    return allowed_scopes


def get_issue_scope_query(user, project):
    return Q(scope__in=get_allowed_scopes(user, project)) | Q(owner=user)
