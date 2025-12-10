/**
 * Alpine.js Application Entry Point
 * Imports and registers all Alpine components and stores
 */

import { dashboard } from './components/dashboard.js';
import { bookingModal } from './components/booking-modal.js';
import './components/favourites-store.js';

// Make components globally available for Alpine immediately
window.dashboard = dashboard;
window.bookingModal = bookingModal;

// Also register with Alpine's data store
document.addEventListener('alpine:init', () => {
    console.log('Alpine.js Tennis Club App initialized');
});

console.log('Alpine components loaded:', { dashboard, bookingModal });
