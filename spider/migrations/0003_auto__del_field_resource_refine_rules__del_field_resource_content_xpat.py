# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Resource.refine_rules'
        db.delete_column(u'spider_resource', 'refine_rules')

        # Deleting field 'Resource.content_xpath'
        db.delete_column(u'spider_resource', 'content_xpath')

        # Deleting field 'Resource.black_words'
        db.delete_column(u'spider_resource', 'black_words_id')

        # Deleting field 'Resource.meta_xpath'
        db.delete_column(u'spider_resource', 'meta_xpath')

        # Deleting field 'Resource.link_xpath'
        db.delete_column(u'spider_resource', 'link_xpath')


    def backwards(self, orm):
        # Adding field 'Resource.refine_rules'
        db.add_column(u'spider_resource', 'refine_rules',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Resource.content_xpath'
        raise RuntimeError("Cannot reverse this migration. 'Resource.content_xpath' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Resource.content_xpath'
        db.add_column(u'spider_resource', 'content_xpath',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Adding field 'Resource.black_words'
        db.add_column(u'spider_resource', 'black_words',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.WordSet'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Resource.meta_xpath'
        db.add_column(u'spider_resource', 'meta_xpath',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Resource.link_xpath'
        raise RuntimeError("Cannot reverse this migration. 'Resource.link_xpath' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Resource.link_xpath'
        db.add_column(u'spider_resource', 'link_xpath',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


    models = {
        u'spider.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'spider.item': {
            'Meta': {'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'black_words': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.WordSet']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.ContentType']", 'null': 'True', 'blank': 'True'}),
            'content_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'extra_xpath': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_xpath': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'refine_rules': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['spider.Resource']"})
        },
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
            'crawl_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'expand_rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
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