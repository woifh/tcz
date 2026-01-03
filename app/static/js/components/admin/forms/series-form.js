/**
 * Series Form Management
 * Handles recurring block series creation and editing
 */

import { seriesAPI } from '../core/admin-api.js';
import { showToast, formUtils, dateUtils } from '../core/admin-utils.js';

export class SeriesForm {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        const seriesForm = document.getElementById('series-form');
        if (seriesForm) {
            seriesForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // Setup form validation
        this.setupFormValidation();
    }

    setupFormValidation() {
        const form = document.getElementById('series-form');
        if (!form) return;

        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', () => this.validateForm());
            input.addEventListener('input', () => this.validateForm());
        });

        // Initial validation
        this.validateForm();
    }

    validateForm() {
        const form = document.getElementById('series-form');
        if (!form) return false;

        const requiredFields = [
            'series-courts',
            'series-start-date',
            'series-end-date',
            'series-start-time',
            'series-end-time',
            'series-reason',
            'series-frequency'
        ];

        let isValid = true;

        requiredFields.forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"], #${fieldName}`);
            if (field) {
                const value = field.type === 'checkbox' ? field.checked : field.value;
                if (!value || (Array.isArray(value) && value.length === 0)) {
                    isValid = false;
                }
            }
        });

        // Validate date range
        const startDate = form.querySelector('#series-start-date')?.value;
        const endDate = form.querySelector('#series-end-date')?.value;
        
        if (startDate && endDate && new Date(startDate) >= new Date(endDate)) {
            isValid = false;
        }

        // Validate time range
        const startTime = form.querySelector('#series-start-time')?.value;
        const endTime = form.querySelector('#series-end-time')?.value;
        
        if (startTime && endTime && !dateUtils.isValidTimeRange(startTime, endTime)) {
            isValid = false;
        }

        // Update submit button
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
        
        // Handle multiple court selection
        const selectedCourts = Array.isArray(formData['series-courts']) 
            ? formData['series-courts'] 
            : [formData['series-courts']];

        // Handle frequency days
        const frequencyDays = [];
        if (formData['series-frequency'] === 'weekly') {
            const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
            days.forEach(day => {
                if (formData[`series-${day}`]) {
                    frequencyDays.push(day);
                }
            });
        }

        const seriesData = {
            courts: selectedCourts,
            start_date: formData['series-start-date'],
            end_date: formData['series-end-date'],
            start_time: formData['series-start-time'],
            end_time: formData['series-end-time'],
            reason_id: formData['series-reason'],
            sub_reason: formData['series-sub-reason'] || '',
            description: formData['series-description'] || '',
            frequency: formData['series-frequency'],
            frequency_days: frequencyDays,
            skip_conflicts: formData['series-skip-conflicts'] === 'on'
        };

        try {
            const result = await seriesAPI.create(seriesData);

            if (result.success) {
                showToast('Serie erfolgreich erstellt', 'success');
                
                // Reset form
                this.resetForm();
                
                // Reload blocks and series list
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }
                if (window.loadSeriesList) {
                    window.loadSeriesList();
                }
                
                // Close modal if it exists
                const modal = document.getElementById('series-modal');
                if (modal && window.bootstrap) {
                    const bsModal = window.bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                }
            } else {
                showToast(result.error || 'Fehler beim Erstellen der Serie', 'error');
            }
        } catch (error) {
            console.error('Error creating series:', error);
            showToast('Fehler beim Erstellen der Serie', 'error');
        }
    }

    resetForm() {
        const form = document.getElementById('series-form');
        if (form) {
            formUtils.clearForm(form);
            
            // Set default dates
            const today = dateUtils.getTodayString();
            const nextWeek = dateUtils.getDatePlusDays(7);
            
            const startDateInput = form.querySelector('#series-start-date');
            const endDateInput = form.querySelector('#series-end-date');
            
            if (startDateInput) startDateInput.value = today;
            if (endDateInput) endDateInput.value = nextWeek;
            
            this.validateForm();
        }
    }

    initializeForm() {
        const today = dateUtils.getTodayString();
        const nextWeek = dateUtils.getDatePlusDays(7);
        
        const startDateInput = document.getElementById('series-start-date');
        const endDateInput = document.getElementById('series-end-date');
        const startTimeInput = document.getElementById('series-start-time');
        
        if (startDateInput) startDateInput.value = today;
        if (endDateInput) endDateInput.value = nextWeek;
        if (startTimeInput) startTimeInput.value = '08:00';
        
        this.validateForm();
    }
}

// Series management functions
export class SeriesManager {
    constructor() {
        this.currentSeries = [];
    }

    async loadSeriesList() {
        try {
            const result = await seriesAPI.load();
            
            if (result.success) {
                this.currentSeries = result.series;
                this.renderSeriesList();
            } else {
                showToast(result.error || 'Fehler beim Laden der Serien', 'error');
            }
        } catch (error) {
            console.error('Error loading series:', error);
            showToast('Fehler beim Laden der Serien', 'error');
        }
    }

    renderSeriesList() {
        const container = document.getElementById('series-list');
        if (!container) return;

        if (this.currentSeries.length === 0) {
            container.innerHTML = '<p class="text-muted">Keine wiederkehrenden Serien gefunden.</p>';
            return;
        }

        const html = this.currentSeries.map(series => `
            <div class="card mb-3">
                <div class="card-body">
                    <h6 class="card-title">${series.reason_name}</h6>
                    <p class="card-text">
                        <small class="text-muted">
                            ${dateUtils.formatDate(series.start_date)} - ${dateUtils.formatDate(series.end_date)}<br>
                            ${dateUtils.formatTime(series.start_time)} - ${dateUtils.formatTime(series.end_time)}<br>
                            Plätze: ${series.courts.join(', ')}<br>
                            Häufigkeit: ${this.getFrequencyText(series.frequency, series.frequency_days)}
                        </small>
                    </p>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editSeries(${series.id})">
                            Bearbeiten
                        </button>
                        <button class="btn btn-outline-danger" onclick="deleteSeries(${series.id})">
                            Löschen
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    getFrequencyText(frequency, frequencyDays) {
        if (frequency === 'daily') {
            return 'Täglich';
        } else if (frequency === 'weekly') {
            const dayNames = {
                monday: 'Mo',
                tuesday: 'Di',
                wednesday: 'Mi',
                thursday: 'Do',
                friday: 'Fr',
                saturday: 'Sa',
                sunday: 'So'
            };
            
            const days = frequencyDays.map(day => dayNames[day]).join(', ');
            return `Wöchentlich (${days})`;
        }
        return frequency;
    }

    async editSeries(seriesId, editData) {
        try {
            const result = await seriesAPI.update(seriesId, editData);
            
            if (result.success) {
                showToast('Serie erfolgreich aktualisiert', 'success');
                this.loadSeriesList();
                
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }
            } else {
                showToast(result.error || 'Fehler beim Aktualisieren der Serie', 'error');
            }
        } catch (error) {
            console.error('Error updating series:', error);
            showToast('Fehler beim Aktualisieren der Serie', 'error');
        }
    }

    async deleteSeries(seriesId, deleteData) {
        try {
            const result = await seriesAPI.delete(seriesId, deleteData);
            
            if (result.success) {
                showToast('Serie erfolgreich gelöscht', 'success');
                this.loadSeriesList();
                
                if (window.loadUpcomingBlocks) {
                    window.loadUpcomingBlocks();
                }
            } else {
                showToast(result.error || 'Fehler beim Löschen der Serie', 'error');
            }
        } catch (error) {
            console.error('Error deleting series:', error);
            showToast('Fehler beim Löschen der Serie', 'error');
        }
    }
}

// Export instances
export const seriesForm = new SeriesForm();
export const seriesManager = new SeriesManager();