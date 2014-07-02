# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'spider_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['spider.Resource'])),
            ('link_xpath', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_xpath', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_xpath', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('extra_xpath', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('refine_rules', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.ContentType'], null=True, blank=True)),
            ('black_words', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.WordSet'], null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'spider', ['Item'])

        # Adding model 'ContentType'
        db.create_table(u'spider_contenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'spider', ['ContentType'])

        # Migrate data to new content
        if not db.dry_run:
            for res in orm.Resource.objects.all():
                item = orm.Item()
                item.name = 'Content'
                item.resource = res
                item.link_xpath = res.link_xpath
                item.content_xpath = res.content_xpath
                item.meta_xpath = res.meta_xpath
                item.refine_rules = res.refine_rules
                item.black_words = res.black_words
                item.active = True
                item.save()


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'spider_item')

        # Deleting model 'ContentType'
        db.delete_table(u'spider_contenttype')


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
            'black_words': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.WordSet']", 'null': 'True', 'blank': 'True'}),
            'content_xpath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'crawl_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'expand_rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
