# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Resource.refine_rules'
        db.add_column(u'spider_resource', 'refine_rules',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Resource.refine_rules'
        db.delete_column(u'spider_resource', 'refine_rules')


    models = {
        u'spider.localcontent': {
            'Meta': {'object_name': 'LocalContent'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content'", 'to': u"orm['spider.Resource']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.resource': {
            'Meta': {'object_name': 'Resource'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'crawl_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'expand_rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_xpath': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'refine_rules': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['spider']