"""
Admin Reasons Module

Contains block reason and sub-reason management routes.
"""

from flask import request, jsonify
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required
from app.models import BlockReason, SubReasonTemplate
from app.services.block_reason_service import BlockReasonService
from . import bp


@bp.route('/block-reasons', methods=['GET'])
@login_required
@admin_required
def list_block_reasons():
    """List all block reasons (admin only)."""
    try:
        reasons = BlockReasonService.get_all_block_reasons()
        
        reasons_data = []
        for reason in reasons:
            reason_data = {
                'id': reason.id,
                'name': reason.name,
                'description': reason.description if hasattr(reason, 'description') else None,
                'color': reason.color if hasattr(reason, 'color') else '#007bff',
                'is_active': reason.is_active,
                'usage_count': BlockReasonService.get_reason_usage_count(reason.id),
                'created_by': reason.created_by.name,
                'created_at': reason.created_at.isoformat()
            }
            reasons_data.append(reason_data)
        
        return jsonify({'reasons': reasons_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/block-reasons', methods=['POST'])
@login_required
@admin_required
def create_block_reason():
    """Create block reason (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        color = data.get('color', '#007bff')
        is_active = data.get('is_active', True)
        
        if not name:
            return jsonify({'error': 'Name ist erforderlich'}), 400
        
        # Check if reason with same name exists
        existing = BlockReason.query.filter_by(name=name).first()
        if existing:
            return jsonify({'error': 'Ein Grund mit diesem Namen existiert bereits'}), 400
        
        reason, error = BlockReasonService.create_block_reason(
            name=name,
            admin_id=current_user.id,
            description=description,
            color=color,
            is_active=is_active
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'id': reason.id,
            'message': 'Sperrungsgrund erfolgreich erstellt',
            'reason': {
                'id': reason.id,
                'name': reason.name,
                'is_active': reason.is_active
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/block-reasons/<int:reason_id>', methods=['PUT'])
@login_required
@admin_required
def update_block_reason(reason_id):
    """Update block reason (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'error': 'Name ist erforderlich'}), 400
        
        success, error = BlockReasonService.update_block_reason(reason_id, name, current_user.id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Sperrungsgrund erfolgreich aktualisiert'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/block-reasons/<int:reason_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_block_reason(reason_id):
    """Delete block reason with usage check (admin only)."""
    try:
        success, error_or_message = BlockReasonService.delete_block_reason(reason_id, current_user.id)
        
        if not success:
            return jsonify({'error': error_or_message}), 400
        
        # If there's a message, it means the reason was deactivated instead of deleted
        if error_or_message:
            return jsonify({'message': error_or_message, 'deactivated': True}), 200
        else:
            return jsonify({'message': 'Sperrungsgrund erfolgreich gelöscht', 'deleted': True}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/block-reasons/<int:reason_id>/usage', methods=['GET'])
@login_required
@admin_required
def get_reason_usage(reason_id):
    """Get usage count for a block reason (admin only)."""
    try:
        usage_count = BlockReasonService.get_reason_usage_count(reason_id)
        
        return jsonify({
            'reason_id': reason_id,
            'usage_count': usage_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/block-reasons/<int:reason_id>/sub-reason-templates', methods=['GET'])
@login_required
@admin_required
def list_sub_reason_templates(reason_id):
    """List sub-reason templates for a block reason (admin only)."""
    try:
        templates = BlockReasonService.get_sub_reason_templates(reason_id)
        
        return jsonify({
            'reason_id': reason_id,
            'templates': [
                {
                    'id': template.id,
                    'template_name': template.template_name,
                    'created_by': template.created_by.name,
                    'created_at': template.created_at.isoformat()
                }
                for template in templates
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/block-reasons/<int:reason_id>/sub-reason-templates', methods=['POST'])
@login_required
@admin_required
def create_sub_reason_template(reason_id):
    """Create sub-reason template (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        template_name = data.get('template_name', '').strip()
        
        if not template_name:
            return jsonify({'error': 'Vorlagenname ist erforderlich'}), 400
        
        template, error = BlockReasonService.create_sub_reason_template(reason_id, template_name, current_user.id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'id': template.id,
            'message': 'Untergrund-Vorlage erfolgreich erstellt',
            'template': {
                'id': template.id,
                'template_name': template.template_name,
                'reason_id': template.reason_id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/sub-reason-templates/<int:template_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_sub_reason_template(template_id):
    """Delete sub-reason template (admin only)."""
    try:
        success, error = BlockReasonService.delete_sub_reason_template(template_id, current_user.id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Untergrund-Vorlage erfolgreich gelöscht'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500