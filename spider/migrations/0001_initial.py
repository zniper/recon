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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'spider', ['Resource'])

        # Adding model 'ItemRule'
        db.create_table(u'spider_itemrule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rules', to=orm['spider.Resource'])),
            ('xpath', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rules', null=True, to=orm['spider.ItemRule'])),
        ))
        db.send_create_signal(u'spider', ['ItemRule'])

        # Adding model 'Item'
        db.create_table(u'spider_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['spider.Resource'])),
            ('hashed_value', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('item_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.ItemType'], blank=True)),
            ('local', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.LocalItem'], blank=True)),
        ))
        db.send_create_signal(u'spider', ['Item'])

        # Adding M2M table for field children on 'Item'
        m2m_table_name = db.shorten_name(u'spider_item_children')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_item', models.ForeignKey(orm[u'spider.item'], null=False)),
            ('to_item', models.ForeignKey(orm[u'spider.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_item_id', 'to_item_id'])

        # Adding model 'ItemType'
        db.create_table(u'spider_itemtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'spider', ['ItemType'])

        # Adding model 'LocalItem'
        db.create_table(u'spider_localitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('item_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'spider', ['LocalItem'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'spider_resource')

        # Deleting model 'ItemRule'
        db.delete_table(u'spider_itemrule')

        # Deleting model 'Item'
        db.delete_table(u'spider_item')

        # Removing M2M table for field children on 'Item'
        db.delete_table(db.shorten_name(u'spider_item_children'))

        # Deleting model 'ItemType'
        db.delete_table(u'spider_itemtype')

        # Deleting model 'LocalItem'
        db.delete_table(u'spider_localitem')


    models = {
        u'spider.item': {
            'Meta': {'object_name': 'Item'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['spider.Item']", 'null': 'True', 'blank': 'True'}),
            'hashed_value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.ItemType']", 'blank': 'True'}),
            'local': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.LocalItem']", 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['spider.Resource']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.itemrule': {
            'Meta': {'object_name': 'ItemRule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rules'", 'null': 'True', 'to': u"orm['spider.ItemRule']"}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': u"orm['spider.Resource']"}),
            'xpath': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.itemtype': {
            'Meta': {'object_name': 'ItemType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'spider.localitem': {
            'Meta': {'object_name': 'LocalItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'spider.resource': {
            'Meta': {'object_name': 'Resource'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['spider']