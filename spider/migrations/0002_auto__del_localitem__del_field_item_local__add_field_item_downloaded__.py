# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LocalItem'
        db.delete_table(u'spider_localitem')

        # Deleting field 'Item.local'
        db.delete_column(u'spider_item', 'local_id')

        # Adding field 'Item.downloaded'
        db.add_column(u'spider_item', 'downloaded',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding unique constraint on 'Item', fields ['hashed_value']
        db.create_unique(u'spider_item', ['hashed_value'])


        # Changing field 'ItemRule.data_type'
        db.alter_column(u'spider_itemrule', 'data_type_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['spider.DataType']))

    def backwards(self, orm):
        # Removing unique constraint on 'Item', fields ['hashed_value']
        db.delete_unique(u'spider_item', ['hashed_value'])

        # Adding model 'LocalItem'
        db.create_table(u'spider_localitem', (
            ('item_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'spider', ['LocalItem'])

        # Adding field 'Item.local'
        db.add_column(u'spider_item', 'local',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.LocalItem'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Item.downloaded'
        db.delete_column(u'spider_item', 'downloaded')


        # Changing field 'ItemRule.data_type'
        db.alter_column(u'spider_itemrule', 'data_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.DataType'], null=True))

    models = {
        u'spider.datatype': {
            'Meta': {'object_name': 'DataType'},
            'fields': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_body': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'spider.item': {
            'Meta': {'object_name': 'Item'},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['spider.Item']", 'null': 'True', 'blank': 'True'}),
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashed_value': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['spider.ItemRule']"})
        },
        u'spider.itemattribute': {
            'Meta': {'object_name': 'ItemAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': u"orm['spider.Item']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'spider.itemrule': {
            'Meta': {'object_name': 'ItemRule'},
            'data_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.DataType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rules'", 'null': 'True', 'to': u"orm['spider.ItemRule']"}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': u"orm['spider.Resource']"}),
            'xpath': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.resource': {
            'Meta': {'object_name': 'Resource'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['spider']