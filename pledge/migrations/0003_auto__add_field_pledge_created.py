# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Pledge.created'
        db.add_column('pledge_pledge', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 8, 24, 20, 46, 17, 481115), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Pledge.created'
        db.delete_column('pledge_pledge', 'created')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'voted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['pledge']
