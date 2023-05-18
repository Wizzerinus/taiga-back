# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL
from django.apps import apps
from django.conf import settings
from django.db.models import Q

from taiga.base.filters import FilterBackend, PermissionBasedFilterBackend
from taiga.base.utils.db import to_tsquery

from . import services


class HideUsersFilterBackend(FilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if not settings.HIDDEN_USERS_ENABLED or user.is_superuser:
            return queryset

        user_model = apps.get_model("users", "User")
        if not user.is_authenticated:
            return user_model.objects.none()
        project_ids = services.get_visible_project_ids(user, user)
        return queryset.filter(Q(is_active=True, memberships__project_id__in=project_ids) | Q(pk=user.pk))


class ContactsFilterBackend(PermissionBasedFilterBackend):
    def filter_queryset(self, user, request, queryset, view):
        qs = user.contacts_visible_by_user(request.user)

        exclude_project = request.QUERY_PARAMS.get('exclude_project', None)
        if exclude_project:
            qs = qs.exclude(projects__id=exclude_project)

        q = request.QUERY_PARAMS.get('q', None)
        if q:
            table = qs.model._meta.db_table
            where_clause = ("""
                to_tsvector('simple',
                            coalesce({table}.username, '') || ' ' ||
                            coalesce({table}.full_name) || ' ' ||
                            coalesce({table}.email, '')) @@ to_tsquery('simple', %s)
            """.format(table=table))

            qs = qs.extra(where=[where_clause], params=[to_tsquery(q)])

        return qs.distinct()
