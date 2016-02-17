from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal

from coursewarehistoryextended.fields import UnsignedBigIntAutoField
from courseware.models import StudentModule, ChunkingManager

class StudentModuleHistoryExtended(models.Model):
    """Keeps a complete history of state changes for a given XModule for a given
    Student. Right now, we restrict this to problems so that the table doesn't
    explode in size.

    This new extended CSMH has a larger primary key that won't run out of space
    so quickly."""
    objects = ChunkingManager()
    HISTORY_SAVING_TYPES = {'problem'}

    class Meta(object):
        get_latest_by = "created"

    id = UnsignedBigIntAutoField(primary_key=True)  # pylint: disable=invalid-name

    student_module = models.ForeignKey(StudentModule, db_index=True, db_constraint=False, on_delete=models.DO_NOTHING)
    version = models.CharField(max_length=255, null=True, blank=True, db_index=True)

    # This should be populated from the modified field in StudentModule
    created = models.DateTimeField(db_index=True)
    state = models.TextField(null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)
    max_grade = models.FloatField(null=True, blank=True)

    @receiver(post_save, sender=StudentModule)
    def save_history(sender, instance, **kwargs):  # pylint: disable=no-self-argument, unused-argument
        """
        Checks the instance's module_type, and creates & saves a
        StudentModuleHistoryExtended entry if the module_type is one that
        we save.
        """
        if instance.module_type in StudentModuleHistoryExtended.HISTORY_SAVING_TYPES:
            history_entry = StudentModuleHistoryExtended(student_module=instance,
                                                         version=None,
                                                         created=instance.modified,
                                                         state=instance.state,
                                                         grade=instance.grade,
                                                         max_grade=instance.max_grade)
            history_entry.save()

    @receiver(post_delete, sender=StudentModule)
    def delete_history(sender, instance, **kwargs):  # pylint: disable=no-self-argument, unused-argument
        """
        Django can't cascade delete across databases, so we tell it at the model level to
        on_delete=DO_NOTHING and then listen for post_delete so we can clean up the CSMHE rows.
        """
        StudentModuleHistoryExtended.objects.filter(student_module=instance).all().delete()

    def __unicode__(self):
        return unicode(repr(self))

    @property
    def csm(self):
        """
        Finds the StudentModule object for this history record, even if our data is split
        across multiple data stores.  Django does not handle this correctly with the built-in
        student_module property.
        """
        return StudentModule.objects.filter(pk=self.student_module_id).first()


