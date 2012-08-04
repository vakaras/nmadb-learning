from django.contrib import admin
from django.utils.translation import ugettext as _

from nmadb_learning import models
from nmadb_utils import admin as utils


class TeacherAdmin(utils.ModelAdmin):
    """ Administration for teachers.
    """

    list_display = (
            'id',
            'human',
            )

    search_fields = (
            'id',
            'human__first_name',
            'human__last_name',
            'human__old_last_name',
            )


class TeachingAdmin(utils.ModelAdmin):
    """ Administration for teaching.
    """

    list_display = (
            'id',
            'teacher',
            'academic',
            'join_date',
            'leave_date',
            )

    list_filter = (
            'teacher',
            )

    search_fields = (
            'id',
            'teacher__first_name',
            'teacher__last_name',
            'teacher__old_last_name',
            'academic__first_name',
            'academic__last_name',
            'academic__old_last_name',
            'join_date',
            'leave_date',
            )

    raw_id_fields = (
            'teacher',
            'academic',
            )


class TaskAdmin(utils.ModelAdmin):
    """ Administration for task.
    """

    list_display = (
            'id',
            'title',
            'creation_date',
            )

    search_fields = (
            'id',
            'title',
            )

    filter_horizontal = ('authors',)


class SolutionAdmin(utils.ModelAdmin):
    """ Administration for solution.
    """

    list_display = (
            'id',
            'task',
            'give_date',
            'receive_date',
            'number',
            'academic',
            'task',
            'mark',
            'assessor',
            )

    search_fields = (
            'id',
            'task__title',
            'assessor__first_name',
            'assessor__last_name',
            'assessor__old_last_name',
            'academic__first_name',
            'academic__last_name',
            'academic__old_last_name',
            )

    filter_horizontal = ('sessions',)

    raw_id_fields = ('academic',)


admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Teaching, TeachingAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Solution, SolutionAdmin)
