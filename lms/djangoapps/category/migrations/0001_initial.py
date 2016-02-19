# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseCategory'
        db.create_table('category_coursecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_id', self.gf('django.db.models.fields.IntegerField')()),
            ('course_id', self.gf('xmodule_django.models.CourseKeyField')(max_length=255)),
        ))
        db.send_create_signal('category', ['CourseCategory'])

        # Adding unique constraint on 'CourseCategory', fields ['category_id', 'course_id']
        db.create_unique('category_coursecategory', ['category_id', 'course_id'])

        # Adding model 'CourseCategoryClass'
        db.create_table('category_coursecategoryclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dimension_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('category', ['CourseCategoryClass'])

        # Adding model 'CourseCategoryClassDimension'
        db.create_table('category_coursecategoryclassdimension', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dimension_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('category', ['CourseCategoryClassDimension'])


    def backwards(self, orm):
        # Removing unique constraint on 'CourseCategory', fields ['category_id', 'course_id']
        db.delete_unique('category_coursecategory', ['category_id', 'course_id'])

        # Deleting model 'CourseCategory'
        db.delete_table('category_coursecategory')

        # Deleting model 'CourseCategoryClass'
        db.delete_table('category_coursecategoryclass')

        # Deleting model 'CourseCategoryClassDimension'
        db.delete_table('category_coursecategoryclassdimension')


    models = {
        'category.coursecategory': {
            'Meta': {'unique_together': "(('category_id', 'course_id'),)", 'object_name': 'CourseCategory'},
            'category_id': ('django.db.models.fields.IntegerField', [], {}),
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'category.coursecategoryclass': {
            'Meta': {'object_name': 'CourseCategoryClass'},
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'dimension_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'category.coursecategoryclassdimension': {
            'Meta': {'object_name': 'CourseCategoryClassDimension'},
            'dimension_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['category']