#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from nmadb_contacts.models import Human
from nmadb_academics.models import Academic
from nmadb_session.models import Session


class Teacher(models.Model):
    """ Information about distance learning teacher.
    """

    human = models.ForeignKey(
            Human,
            verbose_name = _(u'human'),
            )

    comment = models.TextField(
            blank=True,
            null=True,
            verbose_name = _(u'comment'),
            )

    students = models.ManyToManyField(
            Academic,
            through='Teaching',
            verbose_name = _(u'students'),
            help_text=_(u'Academics taught by this teacher.'),
            )

    def __unicode__(self):
        return _(u'{0.human} (teacher)').format(self)

    class Meta:
        verbose_name = _(u'teacher')
        verbose_name_plural = _(u'teachers')


class Teaching(models.Model):
    """ Mark that academic belongs to this teacher group.

    .. todo::
        It is better to create virtual group of students or assign to
        human?
    """

    teacher = models.ForeignKey(
            Teacher,
            verbose_name = _(u'teacher'),
            )

    academic = models.ForeignKey(
            Academic,
            verbose_name = _(u'academic'),
            )

    join_date = models.DateField(
            help_text=_(u'When academic joined this group.'),
            verbose_name = _(u'join date'),
            )

    leave_date = models.DateField(
            blank=True,
            null=True,
            verbose_name = _(u'leave date'),
            help_text=_(u'When academic left this group.'),
            )

    class Meta:
        verbose_name = _(u'teaching')
        verbose_name_plural = _(u'teachings')


class Task(models.Model):
    """ Information about distance learning task.
    """

    title = models.CharField(
            max_length=200,
            unique=True,
            verbose_name = _(u'title'),
            )

    creation_date = models.DateField(
            blank=True,
            null=True,
            verbose_name = _(u'creation date'),
            )

    authors = models.ManyToManyField(
            Teacher,
            verbose_name = _(u'authors'),
            )

    comment = models.TextField(
            blank=True,
            null=True,
            verbose_name = _(u'comment'),
            )

    tags = TaggableManager(
            verbose_name = _(u'tags'),
            )

    def __unicode__(self):
        return u'{0.title}'.format(self)

    class Meta:
        verbose_name = _(u'task')
        verbose_name_plural = _(u'tasks')


class Solution(models.Model):
    """ Information about task solution, which was provided (or not)
    by student.

    :py:attr:`give_date`, :py:attr:`sessions` and :py:attr:`number`
    are mainly for indicating the time, when the task was given
    to student.
    """

    give_date = models.DateField(
            verbose_name = _(u'give date'),
            help_text=_(u'Date, when the task was given to student.'),
            )

    receive_date = models.DateField(
            blank=True,
            null=True,
            verbose_name = _(u'receive date'),
            help_text=_(
                u'Date, when the solution was received from student.'),
            )

    sessions = models.ManyToManyField(
            Session,
            verbose_name = _(u'sessions'),
            help_text=_(
                u'Sessions, for which student solved this task. '
                u'(Evaluation of this solution is used in calculating '
                u'payment size for that sessions.)'),
            )

    number = models.IntegerField(
            verbose_name = _(u'number'),
            help_text=_(
                u'Batch number. '
                u'The number of task, when it was given to student. '
                u'It depends on session.'),
            )
    u"""
    .. todo::
        Ensure functional dependency:
        ``\\forall session \\in Solution.sessions
        {session, Solution.number} → {Task.id}``
    """

    academic = models.ForeignKey(
            Academic,
            verbose_name = _(u'academic'),
            )

    task = models.ForeignKey(
            Task,
            verbose_name = _(u'task'),
            )

    mark = models.DecimalField(
            max_digits=3,
            decimal_places=1,
            null=True,
            blank=True,
            verbose_name = _(u'mark'),
            help_text=_(
                u'NULL means that the task was given, but no solution '
                u'was received.'
                )
            )

    assessor = models.ForeignKey(
            Teacher,
            null=True,
            blank=True,
            verbose_name = _(u'assessor'),
            help_text=_(
                u'Teacher, who evaluated the solution.'),
            )

    class Meta:
        unique_together = (
                ('task', 'academic',))
        verbose_name = _(u'solution')
        verbose_name_plural = _(u'solutions')

    def __unicode__(self):
        if self.mark is None:
            return u'-'
        else:
            return unicode(self.mark)
