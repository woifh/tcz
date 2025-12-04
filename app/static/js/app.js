/**
 * Main application entry point for Tennis Club Reservation System
 * Coordinates all modules and manages global state
 */

import { loadAvailability } from './grid.js';
import { initBooking, openBookingModal, closeBookingModal, handleReservationClick, setCurrentDate } from './booking.js';
import { loadUserReservations, cancelReservationFromDashboard, cancelReservation } from './reservations.js';

// Global state
let currentDate = new Date().toISOString().split('T')[0];

// Expose functions to global scope for inline event handlers
window.openBookingModal = openBookingModal;
window.closeBookingModal = closeBookingModal;
window.handleReservationClick = handleReservationClick;
window.cancelReservationFromDashboard = cancelReservationFromDashboard;
window.cancelReservation = cancelReservation;
window.changeDate = changeDate;
window.goToToday = goToToday;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tennis Club Reservation System loaded - ES6 modules version');
    console.log('Current date:', currentDate);
    
    // Set today's date as default
    const dateSelector = document.getElementById('date-selector');
    console.log('Date selector found:', !!dateSelector);
    
    if (dateSelector) {
        dateSelector.value = currentDate;
        dateSelector.addEventListener('change', function() {
            currentDate = this.value;
            setCurrentDate(currentDate);
            loadAvailability(currentDate);
        });
        
        // Load initial availability
        console.log('Loading initial availability...');
        loadAvailability(currentDate);
    } else {
        console.error('Date selector not found!');
    }
    
    // Initialize booking module
    console.log('Initializing booking module...');
    initBooking(currentDate);
    
    // Load user's upcoming reservations
    console.log('Loading user reservations...');
    loadUserReservations();
});

/**
 * Change date by offset (days)
 */
function changeDate(offset) {
    const date = new Date(currentDate);
    date.setDate(date.getDate() + offset);
    currentDate = date.toISOString().split('T')[0];
    
    const dateSelector = document.getElementById('date-selector');
    if (dateSelector) {
        dateSelector.value = currentDate;
    }
    
    setCurrentDate(currentDate);
    loadAvailability(currentDate);
}

/**
 * Go to today's date
 */
function goToToday() {
    currentDate = new Date().toISOString().split('T')[0];
    
    const dateSelector = document.getElementById('date-selector');
    if (dateSelector) {
        dateSelector.value = currentDate;
    }
    
    setCurrentDate(currentDate);
    loadAvailability(currentDate);
}


