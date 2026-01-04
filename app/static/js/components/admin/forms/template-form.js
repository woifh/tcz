/**
 * Template Form Management
 * Handles block template creation and management
 */

import { blockTemplatesAPI } from '../core/admin-api.js';
import { showToast, formUtils, dateUtils } from '../core/admin-utils.js';
import { stateManager } from '../core/admin-state.js';

export class TemplateForm {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        const templateForm = document.getElementById('template-form');
        if (templateForm) {
            templateForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // Setup form validation
        this.setupFormValidation();
    }

    setupFormValidation() {
        const form = document.getElementById('template-form');
        if (!form) return;

        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('change', () => this.validateForm());
            input.addEventListener('input', () => this.validateForm());
        });

        // Initial validation
        this.validateForm();
    }

    validateForm() {
        const form = document.getElementById('template-form');
        if (!form) return false;

        const templateName = form.querySelector('#template-name')?.value;
        const templateCourts = form.querySelectorAll('input[name="template-courts"]:checked');
        const startTime = form.querySelector('#template-start-time')?.value;
        const endTime = form.querySelector('#template-end-time')?.value;
        const reason = form.querySelector('#template-reason')?.value;

        const isValid = templateName && 
                       templateCourts.length > 0 && 
                       startTime && 
                       endTime && 
                       reason &&
                       dateUtils.isValidTimeRange(startTime, endTime);

        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = !isValid;
        }

        return isValid;
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        if (!this.validateForm()) {
            showToast('Bitte füllen Sie alle erforderlichen Felder aus', 'error');
            return;
        }

        const formData = formUtils.getFormData(event.target);
        
        const selectedCourts = Array.isArray(formData['template-courts']) 
            ? formData['template-courts'] 
            : [formData['template-courts']];

        const templateData = {
            name: formData['template-name'],
            courts: selectedCourts,
            start_time: formData['template-start-time'],
            end_time: formData['template-end-time'],
            reason_id: formData['template-reason'],
            details: formData['template-details'] || '',
            description: formData['template-description'] || ''
        };

        try {
            const result = await blockTemplatesAPI.create(templateData);

            if (result.success) {
                showToast('Vorlage erfolgreich erstellt', 'success');
                
                // Reset form and reload templates
                this.resetForm();
                await this.loadTemplates();
                
                // Close modal if it exists
                const modal = document.getElementById('template-modal');
                if (modal && window.bootstrap) {
                    const bsModal = window.bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                }
            } else {
                showToast(result.error || 'Fehler beim Erstellen der Vorlage', 'error');
            }
        } catch (error) {
            console.error('Error creating template:', error);
            showToast('Fehler beim Erstellen der Vorlage', 'error');
        }
    }

    resetForm() {
        const form = document.getElementById('template-form');
        if (form) {
            formUtils.clearForm(form);
            this.validateForm();
        }
    }

    async loadTemplates() {
        try {
            const result = await blockTemplatesAPI.load();
            
            if (result.success) {
                stateManager.setBlockTemplates(result.templates);
                this.renderTemplateList();
            } else {
                showToast(result.error || 'Fehler beim Laden der Vorlagen', 'error');
            }
        } catch (error) {
            console.error('Error loading templates:', error);
            showToast('Fehler beim Laden der Vorlagen', 'error');
        }
    }

    renderTemplateList() {
        const container = document.getElementById('template-list');
        if (!container) return;

        const templates = stateManager.getBlockTemplates();

        if (templates.length === 0) {
            container.innerHTML = '<p class="text-muted">Keine Vorlagen gefunden.</p>';
            return;
        }

        const html = templates.map(template => `
            <div class="card mb-3">
                <div class="card-body">
                    <h6 class="card-title">${template.name}</h6>
                    <p class="card-text">
                        <small class="text-muted">
                            ${dateUtils.formatTime(template.start_time)} - ${dateUtils.formatTime(template.end_time)}<br>
                            Plätze: ${template.courts.join(', ')}<br>
                            Grund: ${template.reason_name}
                            ${template.details ? `<br>Details: ${template.details}` : ''}
                            ${template.description ? `<br>Beschreibung: ${template.description}` : ''}
                        </small>
                    </p>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="applyTemplate(${template.id})">
                            Anwenden
                        </button>
                        <button class="btn btn-outline-danger" onclick="deleteTemplate(${template.id})">
                            Löschen
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    async applyTemplate(templateId, applyData) {
        try {
            const result = await blockTemplatesAPI.apply(templateId, applyData);
            
            if (result.success) {
                showToast('Vorlage erfolgreich angewendet', 'success');
                
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }
            } else {
                showToast(result.error || 'Fehler beim Anwenden der Vorlage', 'error');
            }
        } catch (error) {
            console.error('Error applying template:', error);
            showToast('Fehler beim Anwenden der Vorlage', 'error');
        }
    }

    async deleteTemplate(templateId) {
        if (!confirm('Sind Sie sicher, dass Sie diese Vorlage löschen möchten?')) {
            return;
        }

        try {
            const result = await blockTemplatesAPI.delete(templateId);
            
            if (result.success) {
                showToast('Vorlage erfolgreich gelöscht', 'success');
                await this.loadTemplates();
            } else {
                showToast(result.error || 'Fehler beim Löschen der Vorlage', 'error');
            }
        } catch (error) {
            console.error('Error deleting template:', error);
            showToast('Fehler beim Löschen der Vorlage', 'error');
        }
    }
}

// Template application modal
export class TemplateApplicationModal {
    constructor() {
        this.currentTemplate = null;
    }

    show(template) {
        this.currentTemplate = template;
        
        // Create modal HTML if it doesn't exist
        this.createModal();
        
        // Populate form with template data
        this.populateForm();
        
        // Show modal
        const modal = document.getElementById('apply-template-modal');
        if (modal && window.bootstrap) {
            const bsModal = new window.bootstrap.Modal(modal);
            bsModal.show();
        }
    }

    createModal() {
        const existingModal = document.getElementById('apply-template-modal');
        if (existingModal) return;

        const modalHtml = `
            <div class="modal fade" id="apply-template-modal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Vorlage anwenden</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="apply-template-form">
                                <div class="mb-3">
                                    <label for="apply-date" class="form-label">Datum</label>
                                    <input type="date" class="form-control" id="apply-date" name="date" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Plätze (aus Vorlage übernommen)</label>
                                    <div id="apply-courts-display" class="form-text"></div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Zeit (aus Vorlage übernommen)</label>
                                    <div id="apply-time-display" class="form-text"></div>
                                </div>
                                <div class="mb-3">
                                    <label for="apply-details" class="form-label">Details (optional)</label>
                                    <input type="text" class="form-control" id="apply-details" name="details">
                                </div>
                                <div class="mb-3">
                                    <label for="apply-description" class="form-label">Beschreibung (optional)</label>
                                    <textarea class="form-control" id="apply-description" name="description" rows="3"></textarea>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Abbrechen</button>
                            <button type="button" class="btn btn-primary" onclick="templateApplicationModal.handleApply()">Anwenden</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }

    populateForm() {
        if (!this.currentTemplate) return;

        // Set default date to today
        const dateInput = document.getElementById('apply-date');
        if (dateInput) {
            dateInput.value = dateUtils.getTodayString();
        }

        // Display template info
        const courtsDisplay = document.getElementById('apply-courts-display');
        const timeDisplay = document.getElementById('apply-time-display');
        
        if (courtsDisplay) {
            courtsDisplay.textContent = `Plätze: ${this.currentTemplate.courts.join(', ')}`;
        }
        
        if (timeDisplay) {
            timeDisplay.textContent = `${dateUtils.formatTime(this.currentTemplate.start_time)} - ${dateUtils.formatTime(this.currentTemplate.end_time)}`;
        }

        // Pre-fill details and description if available
        const detailsInput = document.getElementById('apply-details');
        const descriptionInput = document.getElementById('apply-description');
        
        if (detailsInput) {
            detailsInput.value = this.currentTemplate.details || '';
        }
        
        if (descriptionInput) {
            descriptionInput.value = this.currentTemplate.description || '';
        }
    }

    async handleApply() {
        const form = document.getElementById('apply-template-form');
        if (!form || !this.currentTemplate) return;

        const formData = formUtils.getFormData(form);
        
        const applyData = {
            date: formData.date,
            details: formData.details || '',
            description: formData.description || ''
        };

        try {
            const result = await blockTemplatesAPI.apply(this.currentTemplate.id, applyData);
            
            if (result.success) {
                showToast('Vorlage erfolgreich angewendet', 'success');
                
                // Close modal
                const modal = document.getElementById('apply-template-modal');
                if (modal && window.bootstrap) {
                    const bsModal = window.bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                }
                
                // Reload blocks
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }
            } else {
                showToast(result.error || 'Fehler beim Anwenden der Vorlage', 'error');
            }
        } catch (error) {
            console.error('Error applying template:', error);
            showToast('Fehler beim Anwenden der Vorlage', 'error');
        }
    }
}

// Export instances
export const templateForm = new TemplateForm();
export const templateApplicationModal = new TemplateApplicationModal();