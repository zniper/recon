# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table(u'spider_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('link_xpath', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_xpath', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('expand_rules', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('crawl_depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'spider', ['Resource'])

        # Adding model 'LocalContent'
        db.create_table(u'spider_localcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content', to=orm['spider.Resource'])),
            ('local_path', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
        ))
        db.send_create_signal(u'spider', ['LocalContent'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'spider_resource')

        # Deleting model 'LocalContent'
        db.delete_table(u'spider_localcontent')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['spider']