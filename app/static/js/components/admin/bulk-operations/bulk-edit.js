/**
 * Bulk Edit Operations
 * Handles bulk editing of blocks
 */

import { blocksAPI } from '../core/admin-api.js';
import { showToast, formUtils } from '../core/admin-utils.js';
import { stateManager } from '../core/admin-state.js';

export class BulkEditManager {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Bulk edit button
        const bulkEditBtn = document.getElementById('bulk-edit-btn');
        if (bulkEditBtn) {
            bulkEditBtn.addEventListener('click', () => this.showBulkEditModal());
        }
    }

    showBulkEditModal() {
        const selectedBlocks = stateManager.getSelectedBlocks();
        
        if (selectedBlocks.length === 0) {
            showToast('Bitte wählen Sie mindestens eine Sperrung aus', 'warning');
            return;
        }

        // Create modal if it doesn't exist
        this.createBulkEditModal();
        
        // Update modal content
        this.updateBulkEditModal(selectedBlocks);
        
        // Show modal
        const modal = document.getElementById('bulk-edit-modal');
        if (modal && window.bootstrap) {
            const bsModal = new window.bootstrap.Modal(modal);
            bsModal.show();
        }
    }

    createBulkEditModal() {
        const existingModal = document.getElementById('bulk-edit-modal');
        if (existingModal) return;

        const modalHtml = `
            <div class="modal fade" id="bulk-edit-modal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Sperrungen bearbeiten</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-info">
                                <i class="fas fa-info-circle me-2"></i>
                                Nur die Felder, die Sie ändern möchten, werden aktualisiert. Leere Felder bleiben unverändert.
                            </div>
                            
                            <div id="bulk-edit-selection" class="mb-4"></div>
                            
                            <form id="bulk-edit-form">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="bulk-edit-reason" class="form-label">Grund ändern</label>
                                            <select class="form-select" id="bulk-edit-reason" name="reason_id">
                                                <option value="">-- Nicht ändern --</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="bulk-edit-sub-reason" class="form-label">Untergrund ändern</label>
                                            <input type="text" class="form-control" id="bulk-edit-sub-reason" name="sub_reason" 
                                                   placeholder="Leer lassen für keine Änderung">
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="bulk-edit-start-time" class="form-label">Startzeit ändern</label>
                                            <input type="time" class="form-control" id="bulk-edit-start-time" name="start_time">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="bulk-edit-end-time" class="form-label">Endzeit ändern</label>
                                            <input type="time" class="form-control" id="bulk-edit-end-time" name="end_time">
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <label for="bulk-edit-description" class="form-label">Beschreibung ändern</label>
                                    <textarea class="form-control" id="bulk-edit-description" name="description" rows="3"
                                              placeholder="Leer lassen für keine Änderung"></textarea>
                                </div>
                                
                                <div class="mb-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" id="bulk-edit-clear-sub-reason" name="clear_sub_reason">
                                        <label class="form-check-label" for="bulk-edit-clear-sub-reason">
                                            Untergrund bei allen ausgewählten Sperrungen löschen
                                        </label>
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" id="bulk-edit-clear-description" name="clear_description">
                                        <label class="form-check-label" for="bulk-edit-clear-description">
                                            Beschreibung bei allen ausgewählten Sperrungen löschen
                                        </label>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Abbrechen</button>
                            <button type="button" class="btn btn-primary" onclick="bulkEditManager.executeBulkEdit()">
                                Änderungen anwenden
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Setup time validation
        const startTimeInput = document.getElementById('bulk-edit-start-time');
        const endTimeInput = document.getElementById('bulk-edit-end-time');
        
        if (startTimeInput && endTimeInput) {
            const validateTimes = () => {
                const startTime = startTimeInput.value;
                const endTime = endTimeInput.value;
                
                if (startTime && endTime) {
                    const start = new Date(`2000-01-01T${startTime}`);
                    const end = new Date(`2000-01-01T${endTime}`);
                    
                    if (start >= end) {
                        endTimeInput.setCustomValidity('Endzeit muss nach Startzeit liegen');
                    } else {
                        endTimeInput.setCustomValidity('');
                    }
                }
            };
            
            startTimeInput.addEventListener('change', validateTimes);
            endTimeInput.addEventListener('change', validateTimes);
        }

        // Setup clear checkboxes
        const clearSubReasonCheckbox = document.getElementById('bulk-edit-clear-sub-reason');
        const clearDescriptionCheckbox = document.getElementById('bulk-edit-clear-description');
        const subReasonInput = document.getElementById('bulk-edit-sub-reason');
        const descriptionInput = document.getElementById('bulk-edit-description');
        
        if (clearSubReasonCheckbox && subReasonInput) {
            clearSubReasonCheckbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    subReasonInput.disabled = true;
                    subReasonInput.value = '';
                } else {
                    subReasonInput.disabled = false;
                }
            });
        }
        
        if (clearDescriptionCheckbox && descriptionInput) {
            clearDescriptionCheckbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    descriptionInput.disabled = true;
                    descriptionInput.value = '';
                } else {
                    descriptionInput.disabled = false;
                }
            });
        }
    }

    updateBulkEditModal(selectedBlocks) {
        // Update selection display
        const selectionContainer = document.getElementById('bulk-edit-selection');
        if (selectionContainer) {
            const batchCount = new Set(selectedBlocks.map(block => block.batch_id)).size;
            selectionContainer.innerHTML = `
                <div class="card">
                    <div class="card-body py-2">
                        <strong>${selectedBlocks.length} Sperrung(en) ausgewählt</strong>
                        <small class="text-muted">(${batchCount} Batch(es))</small>
                    </div>
                </div>
            `;
        }

        // Populate reason dropdown
        this.populateReasonDropdown();
        
        // Reset form
        const form = document.getElementById('bulk-edit-form');
        if (form) {
            form.reset();
            
            // Re-enable inputs that might have been disabled
            const subReasonInput = document.getElementById('bulk-edit-sub-reason');
            const descriptionInput = document.getElementById('bulk-edit-description');
            
            if (subReasonInput) subReasonInput.disabled = false;
            if (descriptionInput) descriptionInput.disabled = false;
        }
    }

    populateReasonDropdown() {
        const reasonSelect = document.getElementById('bulk-edit-reason');
        if (!reasonSelect) return;

        const reasons = stateManager.getBlockReasons().filter(r => r.is_active);
        
        // Clear existing options except the first one
        reasonSelect.innerHTML = '<option value="">-- Nicht ändern --</option>';
        
        // Add reason options
        reasons.forEach(reason => {
            const option = document.createElement('option');
            option.value = reason.id;
            option.textContent = reason.name;
            reasonSelect.appendChild(option);
        });
    }

    async executeBulkEdit() {
        const selectedBlocks = stateManager.getSelectedBlocks();
        
        if (selectedBlocks.length === 0) {
            showToast('Keine Sperrungen ausgewählt', 'error');
            return;
        }

        const form = document.getElementById('bulk-edit-form');
        if (!form) return;

        const formData = formUtils.getFormData(form);
        
        // Build edit data object with only non-empty values
        const editData = {};
        
        if (formData.reason_id) {
            editData.reason_id = parseInt(formData.reason_id);
        }
        
        if (formData.start_time) {
            editData.start_time = formData.start_time;
        }
        
        if (formData.end_time) {
            editData.end_time = formData.end_time;
        }
        
        // Handle sub_reason
        if (formData.clear_sub_reason) {
            editData.sub_reason = '';
        } else if (formData.sub_reason) {
            editData.sub_reason = formData.sub_reason;
        }
        
        // Handle description
        if (formData.clear_description) {
            editData.description = '';
        } else if (formData.description) {
            editData.description = formData.description;
        }

        // Check if any changes were made
        if (Object.keys(editData).length === 0) {
            showToast('Keine Änderungen vorgenommen', 'warning');
            return;
        }

        try {
            const blockIds = selectedBlocks.map(block => block.id);
            const result = await blocksAPI.bulkEdit(blockIds, editData);

            if (result.success) {
                showToast(`${selectedBlocks.length} Sperrung(en) erfolgreich aktualisiert`, 'success');
                
                // Close modal
                const modal = document.getElementById('bulk-edit-modal');
                if (modal && window.bootstrap) {
                    const bsModal = window.bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                }

                // Clear selection and reload
                stateManager.clearSelectedBlocks();
                
                if (window.bulkDeleteManager) {
                    window.bulkDeleteManager.updateBulkActionButtons();
                }
                
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }

            } else {
                showToast(result.error || 'Fehler beim Bearbeiten der Sperrungen', 'error');
            }

        } catch (error) {
            console.error('Error during bulk edit:', error);
            showToast('Fehler beim Bearbeiten der Sperrungen', 'error');
        }
    }
}

// Export singleton instance
export const bulkEditManager = new BulkEditManager();