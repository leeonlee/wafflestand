# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Movie.release'
        db.add_column(u'bluray_movie', 'release',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 7, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Movie.release'
        db.delete_column(u'bluray_movie', 'release')


    models = {
        u'bluray.movie': {
            'Meta': {'object_name': 'Movie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'release': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['bluray']