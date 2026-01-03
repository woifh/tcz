/**
 * Bulk Delete Operations
 * Handles bulk deletion of blocks and batches
 */

import { blocksAPI } from '../core/admin-api.js';
import { showToast } from '../core/admin-utils.js';
import { stateManager } from '../core/admin-state.js';

export class BulkDeleteManager {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Bulk delete button
        const bulkDeleteBtn = document.getElementById('bulk-delete-btn');
        if (bulkDeleteBtn) {
            bulkDeleteBtn.addEventListener('click', () => this.showBulkDeleteModal());
        }

        // Select all checkbox
        const selectAllCheckbox = document.getElementById('select-all-blocks');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => this.handleSelectAll(e));
        }
    }

    handleSelectAll(event) {
        const isChecked = event.target.checked;
        const blockCheckboxes = document.querySelectorAll('input[name="selected-blocks"]');
        
        blockCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });
        
        this.updateSelectedBlocks();
        this.updateBulkActionButtons();
    }

    updateSelectedBlocks() {
        const selectedCheckboxes = document.querySelectorAll('input[name="selected-blocks"]:checked');
        const selectedBlocks = Array.from(selectedCheckboxes).map(cb => ({
            id: parseInt(cb.value),
            batch_id: cb.dataset.batchId
        }));
        
        stateManager.setSelectedBlocks(selectedBlocks);
    }

    updateBulkActionButtons() {
        const selectedBlocks = stateManager.getSelectedBlocks();
        const bulkDeleteBtn = document.getElementById('bulk-delete-btn');
        const bulkEditBtn = document.getElementById('bulk-edit-btn');
        
        const hasSelection = selectedBlocks.length > 0;
        
        if (bulkDeleteBtn) {
            bulkDeleteBtn.disabled = !hasSelection;
            bulkDeleteBtn.textContent = hasSelection 
                ? `${selectedBlocks.length} Sperrung(en) löschen`
                : 'Löschen';
        }
        
        if (bulkEditBtn) {
            bulkEditBtn.disabled = !hasSelection;
            bulkEditBtn.textContent = hasSelection 
                ? `${selectedBlocks.length} Sperrung(en) bearbeiten`
                : 'Bearbeiten';
        }
    }

    showBulkDeleteModal() {
        const selectedBlocks = stateManager.getSelectedBlocks();
        
        if (selectedBlocks.length === 0) {
            showToast('Bitte wählen Sie mindestens eine Sperrung aus', 'warning');
            return;
        }

        // Create modal if it doesn't exist
        this.createBulkDeleteModal();
        
        // Update modal content
        this.updateBulkDeleteModal(selectedBlocks);
        
        // Show modal
        const modal = document.getElementById('bulk-delete-modal');
        if (modal && window.bootstrap) {
            const bsModal = new window.bootstrap.Modal(modal);
            bsModal.show();
        }
    }

    createBulkDeleteModal() {
        const existingModal = document.getElementById('bulk-delete-modal');
        if (existingModal) return;

        const modalHtml = `
            <div class="modal fade" id="bulk-delete-modal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Sperrungen löschen</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-warning">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                Diese Aktion kann nicht rückgängig gemacht werden!
                            </div>
                            <p>Sie sind dabei, die folgenden Sperrungen zu löschen:</p>
                            <div id="bulk-delete-list" class="mb-3"></div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="confirm-bulk-delete">
                                <label class="form-check-label" for="confirm-bulk-delete">
                                    Ich bestätige, dass ich diese Sperrungen löschen möchte
                                </label>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Abbrechen</button>
                            <button type="button" class="btn btn-danger" id="confirm-bulk-delete-btn" disabled 
                                    onclick="bulkDeleteManager.executeBulkDelete()">
                                Löschen
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Setup confirmation checkbox
        const confirmCheckbox = document.getElementById('confirm-bulk-delete');
        const confirmBtn = document.getElementById('confirm-bulk-delete-btn');
        
        if (confirmCheckbox && confirmBtn) {
            confirmCheckbox.addEventListener('change', (e) => {
                confirmBtn.disabled = !e.target.checked;
            });
        }
    }

    updateBulkDeleteModal(selectedBlocks) {
        const listContainer = document.getElementById('bulk-delete-list');
        if (!listContainer) return;

        // Group blocks by batch_id for better display
        const batches = {};
        selectedBlocks.forEach(block => {
            if (!batches[block.batch_id]) {
                batches[block.batch_id] = [];
            }
            batches[block.batch_id].push(block);
        });

        const html = Object.keys(batches).map(batchId => {
            const blocks = batches[batchId];
            const blockCount = blocks.length;
            
            return `
                <div class="card mb-2">
                    <div class="card-body py-2">
                        <small class="text-muted">Batch ${batchId}</small><br>
                        <strong>${blockCount} Sperrung(en)</strong>
                    </div>
                </div>
            `;
        }).join('');

        listContainer.innerHTML = html;

        // Reset confirmation
        const confirmCheckbox = document.getElementById('confirm-bulk-delete');
        const confirmBtn = document.getElementById('confirm-bulk-delete-btn');
        
        if (confirmCheckbox) confirmCheckbox.checked = false;
        if (confirmBtn) confirmBtn.disabled = true;
    }

    async executeBulkDelete() {
        const selectedBlocks = stateManager.getSelectedBlocks();
        
        if (selectedBlocks.length === 0) {
            showToast('Keine Sperrungen ausgewählt', 'error');
            return;
        }

        try {
            // Group by batch_id and delete batches
            const batchIds = [...new Set(selectedBlocks.map(block => block.batch_id))];
            
            const deletePromises = batchIds.map(batchId => 
                blocksAPI.deleteBatch(batchId)
            );

            const results = await Promise.all(deletePromises);
            
            const successCount = results.filter(r => r.success).length;
            const failCount = results.length - successCount;

            if (successCount > 0) {
                showToast(`${successCount} Batch(es) erfolgreich gelöscht`, 'success');
            }
            
            if (failCount > 0) {
                showToast(`${failCount} Batch(es) konnten nicht gelöscht werden`, 'error');
            }

            // Close modal
            const modal = document.getElementById('bulk-delete-modal');
            if (modal && window.bootstrap) {
                const bsModal = window.bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
            }

            // Clear selection and reload
            stateManager.clearSelectedBlocks();
            this.updateBulkActionButtons();
            
            if (window.loadUpcomingBlocks) {
                window.loadUpcomingBlocks();
            }

        } catch (error) {
            console.error('Error during bulk delete:', error);
            showToast('Fehler beim Löschen der Sperrungen', 'error');
        }
    }

    // Single batch delete function
    async deleteBatch(batchId) {
        try {
            // First, get batch details to show proper confirmation message
            const blocksResult = await blocksAPI.load({
                date_range_start: new Date().toISOString().split('T')[0],
                date_range_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            });

            if (!blocksResult.success) {
                showToast('Fehler beim Laden der Batch-Details', 'error');
                return;
            }

            const batchBlocks = blocksResult.blocks.filter(block => block.batch_id === batchId);
            
            if (batchBlocks.length === 0) {
                showToast('Batch nicht gefunden', 'error');
                return;
            }

            // Show confirmation dialog
            const firstBlock = batchBlocks[0];
            const courtNames = [...new Set(batchBlocks.map(block => block.court_name))].join(', ');
            const blockCount = batchBlocks.length;
            
            const confirmMessage = blockCount === 1 
                ? `Möchten Sie die Sperrung für ${courtNames} am ${firstBlock.date} von ${firstBlock.start_time} bis ${firstBlock.end_time} wirklich löschen?`
                : `Möchten Sie die ${blockCount} Sperrungen für ${courtNames} am ${firstBlock.date} von ${firstBlock.start_time} bis ${firstBlock.end_time} wirklich löschen?`;

            if (!confirm(confirmMessage)) {
                return;
            }

            // Delete the batch
            const result = await blocksAPI.deleteBatch(batchId);

            if (result.success) {
                const successMessage = blockCount === 1 
                    ? 'Sperrung erfolgreich gelöscht'
                    : `${blockCount} Sperrungen erfolgreich gelöscht`;
                showToast(successMessage, 'success');
                
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }
            } else {
                showToast(result.error || 'Fehler beim Löschen der Sperrung', 'error');
            }

        } catch (error) {
            console.error('Error deleting batch:', error);
            showToast('Fehler beim Löschen der Sperrung', 'error');
        }
    }
}

// Export singleton instance
export const bulkDeleteManager = new BulkDeleteManager();