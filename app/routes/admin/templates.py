"""
Admin Templates Module

Contains block template management routes.
"""

from datetime import datetime
from flask import request, jsonify
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required
from app.models import BlockTemplate
from app.services.block_service import BlockService
from . import bp


@bp.route('/block-templates', methods=['GET'])
@login_required
@admin_required
def list_block_templates():
    """List all block templates (admin only)."""
    try:
        templates = BlockService.get_block_templates()
        
        return jsonify({
            'templates': [
                {
                    'id': template.id,
                    'name': template.name,
                    'court_selection': template.court_selection,
                    'start_time': template.start_time.strftime('%H:%M'),
                    'end_time': template.end_time.strftime('%H:%M'),
                    'reason_id': template.reason_id,
                    'reason_name': template.reason_obj.name if template.reason_obj else 'Unknown',
                    'sub_reason': template.sub_reason,
                    'recurrence_pattern': template.recurrence_pattern,
                    'recurrence_days': template.recurrence_days,
                    'created_by': template.created_by.name,
                    'created_at': template.created_at.isoformat()
                }
                for template in templates
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/block-templates', methods=['POST'])
@login_required
@admin_required
def create_block_template():
    """Create block template (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name', '').strip()
        court_selection = data.get('court_selection', [])
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        reason_id = int(data.get('reason_id'))
        sub_reason = data.get('sub_reason', '').strip() or None
        recurrence_pattern = data.get('recurrence_pattern', '').strip() or None
        recurrence_days = data.get('recurrence_days', [])
        
        # Validate required fields
        if not all([name, court_selection, start_time_str, end_time_str, reason_id]):
            return jsonify({'error': 'Alle Pflichtfelder sind erforderlich'}), 400
        
        # Parse times
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        
        # Prepare template data
        template_data = {
            'court_selection': court_selection,
            'start_time': start_time,
            'end_time': end_time,
            'reason_id': reason_id,
            'sub_reason': sub_reason,
            'recurrence_pattern': recurrence_pattern,
            'recurrence_days': recurrence_days
        }
        
        # Create template
        template, error = BlockService.create_block_template(name, template_data, current_user.id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'id': template.id,
            'message': 'Vorlage erfolgreich erstellt',
            'template': {
                'id': template.id,
                'name': template.name,
                'court_selection': template.court_selection,
                'start_time': template.start_time.strftime('%H:%M'),
                'end_time': template.end_time.strftime('%H:%M'),
                'reason_id': template.reason_id,
                'sub_reason': template.sub_reason,
                'recurrence_pattern': template.recurrence_pattern,
                'recurrence_days': template.recurrence_days
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/block-templates/<int:template_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_block_template(template_id):
    """Delete block template (admin only)."""
    try:
        success, error = BlockService.delete_block_template(template_id, current_user.id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Vorlage erfolgreich gelöscht'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/block-templates/<int:template_id>/apply', methods=['POST'])
@login_required
@admin_required
def apply_block_template(template_id):
    """Apply block template with date overrides (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        date_overrides = {}
        if 'start_date' in data:
            date_overrides['start_date'] = data['start_date']
        if 'end_date' in data:
            date_overrides['end_date'] = data['end_date']
        
        form_data = BlockService.apply_block_template(template_id, date_overrides)
        
        if form_data is None:
            return jsonify({'error': 'Vorlage nicht gefunden'}), 404
        
        return jsonify({
            'message': 'Vorlage erfolgreich angewendet',
            'form_data': form_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500