# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SMS'
        db.create_table('pledge_sms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sms_message_sid', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('pledge', ['SMS'])


    def backwards(self, orm):
        
        # Deleting model 'SMS'
        db.delete_table('pledge_sms')


    models = {
        'pledge.election': {
            'Meta': {'object_name': 'Election'},
            'confirm_txt': ('django.db.models.fields.CharField', [], {'default': "'Thanks for pledging to vote.'", 'max_length': '160'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'pledge.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'areacode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pledge.Election']"}),
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'voted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'pledge.sms': {
            'Meta': {'object_name': 'SMS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sms_message_sid': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['pledge']
