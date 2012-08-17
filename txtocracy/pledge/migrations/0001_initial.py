# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Election'
        db.create_table('pledge_election', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('pledge', ['Election'])

        # Adding model 'Pledge'
        db.create_table('pledge_pledge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pledge.Election'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('areacode', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('voted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('pledge', ['Pledge'])


    def backwards(self, orm):
        
        # Deleting model 'Election'
        db.delete_table('pledge_election')

        # Deleting model 'Pledge'
        db.delete_table('pledge_pledge')


    models = {
        'pledge.election': {
            'Meta': {'object_name': 'Election'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'pledge.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'areacode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pledge.Election']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'voted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['pledge']
