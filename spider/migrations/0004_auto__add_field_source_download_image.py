# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Source.download_image'
        db.add_column(u'spider_source', 'download_image',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Source.download_image'
        db.delete_column(u'spider_source', 'download_image')


    models = {
        u'spider.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'spider.localcontent': {
            'Meta': {'object_name': 'LocalContent'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'content'", 'null': 'True', 'to': u"orm['spider.Source']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.source': {
            'Meta': {'object_name': 'Source'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'black_words': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.WordSet']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.ContentType']", 'null': 'True', 'blank': 'True'}),
            'content_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'crawl_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'download_image': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expand_rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_xpath': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_xpath': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'refine_rules': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.wordset': {
            'Meta': {'object_name': 'WordSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'words': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['spider']