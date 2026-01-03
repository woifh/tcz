"""
Admin Audit Module

Contains audit log functionality for admin operations.
"""

from datetime import datetime
from flask import request, jsonify
from flask_login import login_required, current_user

from app.decorators import admin_required
from app.services.block_service import BlockService
from . import bp


@bp.route('/blocks/audit-log', methods=['GET'])
@login_required
@admin_required
def get_audit_log():
    """Get block operation audit log (admin only)."""
    try:
        filters = {}
        
        # Optional filters
        if request.args.get('admin_id'):
            filters['admin_id'] = int(request.args.get('admin_id'))
        
        if request.args.get('operation'):
            filters['operation'] = request.args.get('operation')
        
        if request.args.get('date_range_start') and request.args.get('date_range_end'):
            start_date = datetime.strptime(request.args.get('date_range_start'), '%Y-%m-%d')
            end_date = datetime.strptime(request.args.get('date_range_end'), '%Y-%m-%d')
            filters['date_range'] = (start_date, end_date)
        
        audit_logs = BlockService.get_audit_log(filters if filters else None)
        
        return jsonify({
            'audit_logs': [
                {
                    'id': log.id,
                    'operation': log.operation,
                    'block_id': log.block_id,
                    'series_id': log.series_id,
                    'operation_data': log.operation_data,
                    'admin_name': log.admin.name,
                    'timestamp': log.timestamp.isoformat()
                }
                for log in audit_logs
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500