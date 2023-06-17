# Generated by Django 3.2.18 on 2023-05-24 12:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0068_alter_project_public_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_employee_log_activated',
            field=models.BooleanField(blank=True, default=True, verbose_name='active employee log panel'),
        ),
        migrations.AddField(
            model_name='projecttemplate',
            name='is_employee_log_activated',
            field=models.BooleanField(blank=True, default=True, verbose_name='active employee log panel'),
        ),
        migrations.AlterField(
            model_name='project',
            name='public_permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('add_milestone', 'Add milestone'), ('modify_milestone', 'Modify milestone'), ('delete_milestone', 'Delete milestone'), ('view_epics', 'View epic'), ('add_epic', 'Add epic'), ('modify_epic', 'Modify epic'), ('comment_epic', 'Comment epic'), ('delete_epic', 'Delete epic'), ('view_us', 'View user story'), ('add_us', 'Add user story'), ('modify_us', 'Modify user story'), ('comment_us', 'Comment user story'), ('delete_us', 'Delete user story'), ('view_tasks', 'View tasks'), ('add_task', 'Add task'), ('modify_task', 'Modify task'), ('comment_task', 'Comment task'), ('delete_task', 'Delete task'), ('view_issues', 'View issues'), ('add_issue', 'Add issue'), ('modify_issue', 'Modify issue'), ('comment_issue', 'Comment issue'), ('delete_issue', 'Delete issue'), ('view_issues_testing', 'View issues (Testing)'), ('edit_issues_testing', 'Edit issues (Testing)'), ('view_issues_security', 'View issues (Security)'), ('edit_issues_security', 'Edit issues (Security)'), ('view_wiki_pages', 'View wiki pages'), ('add_wiki_page', 'Add wiki page'), ('modify_wiki_page', 'Modify wiki page'), ('comment_wiki_page', 'Comment wiki page'), ('delete_wiki_page', 'Delete wiki page'), ('view_wiki_links', 'View wiki links'), ('add_wiki_link', 'Add wiki link'), ('modify_wiki_link', 'Modify wiki link'), ('delete_wiki_link', 'Delete wiki link'), ('is_employee', 'Listed on the Employee page'), ('is_management', "Can access other employees' logs")]), blank=True, default=list, null=True, size=None, verbose_name='user permissions'),
        ),
    ]
