#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

from nmadb_contacts.models import Human
from nmadb_academics.models import Academic
from nmadb_session.models import Session


class Teacher(models.Model):
    """ Information about distance learning teacher.
    """

    human = models.ForeignKey(
            Human,
            )

    comment = models.TextField(
            blank=True,
            null=True,
            )

    students = models.ManyToManyField(
            Academic,
            through='Teaching',
            help_text=_(u'Academics taught by this teacher.'),
            )

    def __unicode__(self):
        return _(u'{0.human} (teacher)').format(self)


class Teaching(models.Model):
    """ Mark that academic belongs to this teacher group.

    .. todo::
        It is better to create virtual group of students or assign to
        human?
    """

    teacher = models.ForeignKey(
            Teacher,
            )

    academic = models.ForeignKey(
            Academic,
            )

    join_date = models.DateField(
            help_text=_(u'When academic joined this group.'),
            )

    leave_date = models.DateField(
            blank=True,
            null=True,
            help_text=_(u'When academic left this group.'),
            )


class Task(models.Model):
    """ Information about distance learning task.
    """

    title = models.CharField(
            max_length=200,
            unique=True,
            )

    creation_date = models.DateField(
            blank=True,
            null=True,
            )

    authors = models.ManyToManyField(
            Teacher,
            )

    comment = models.TextField(
            blank=True,
            null=True,
            )

    tags = TaggableManager()

    def __unicode__(self):
        return u'{0.title}'.format(self)


class Solution(models.Model):
    """ Information about task solution, which was provided (or not)
    by student.

    :py:attr:`give_date`, :py:attr:`sessions` and :py:attr:`number`
    are mainly for indicating the time, when the task was given
    to student.
    """

    give_date = models.DateField(
            help_text=_(u'Date, when the task was given to student.')
            )

    receive_date = models.DateField(
            help_text=_(
                u'Date, when the solution was received from student.'),
            blank=True,
            null=True,
            )

    sessions = models.ManyToManyField(
            Session,
            help_text=_(
                u'Sessions, for which student solved this task. '
                u'(Evaluation of this solution is used in calculating '
                u'payment size for that sessions.)')
            )

    number = models.IntegerField(
            help_text=_(
                u'Batch number. '
                u'The number of task, when it was given to student. '
                u'It depends on session.')
            )
    u"""
    .. todo::
        Ensure functional dependency:
        ``\\forall session \\in Solution.sessions
        {session, Solution.number} → {Task.id}``
    """

    academic = models.ForeignKey(
            Academic,
            )

    task = models.ForeignKey(
            Task,
            )

    mark = models.DecimalField(
            max_digits=3,
            decimal_places=1,
            null=True,
            blank=True,
            help_text=_(
                u'NULL means that the task was given, but no solution '
                u'was received.'
                )
            )

    assessor = models.ForeignKey(
            Teacher,
            help_text=_(
                u'Teacher, who evaluated the solution.'),
            null=True,
            blank=True,
            )

    class Meta:
        unique_together = (
                ('task', 'academic',))

    def __unicode__(self):
        if self.mark is None:
            return u'-'
        else:
            return unicode(self.mark)
