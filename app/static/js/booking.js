/**
 * Booking form and reservation management
 */

import { getEndTime, showSuccess, showError } from './utils.js';
import { loadAvailability } from './grid.js';
import { loadUserReservations } from './reservations.js';

let selectedSlot = null;
let currentDate = null;

/**
 * Initialize booking module
 */
export function initBooking(date) {
    currentDate = date;
    
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBookingSubmit);
    }
    
    // Load favourites for booking dropdown
    loadFavourites();
}

/**
 * Update current date
 */
export function setCurrentDate(date) {
    currentDate = date;
}

/**
 * Open booking modal with pre-filled data
 */
export function openBookingModal(courtNumber, time) {
    selectedSlot = { courtNumber, time };
    
    document.getElementById('booking-date').value = currentDate;
    document.getElementById('booking-court').value = `Platz ${courtNumber}`;
    document.getElementById('booking-time').value = `${time} - ${getEndTime(time)}`;
    
    document.getElementById('booking-modal').classList.remove('hidden');
}

/**
 * Close booking modal
 */
export function closeBookingModal() {
    document.getElementById('booking-modal').classList.add('hidden');
    selectedSlot = null;
}

/**
 * Handle booking form submission
 */
async function handleBookingSubmit(event) {
    event.preventDefault();
    
    if (!selectedSlot) return;
    
    const bookedForId = document.getElementById('booking-for').value;
    const courtId = selectedSlot.courtNumber;
    
    const bookingData = {
        court_id: courtId,
        date: currentDate,
        start_time: selectedSlot.time,
        booked_for_id: parseInt(bookedForId)
    };
    
    try {
        const response = await fetch('/reservations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookingData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess('Buchung erfolgreich erstellt!');
            closeBookingModal();
            loadAvailability(currentDate);
            loadUserReservations();
        } else {
            showError(data.error || 'Fehler beim Erstellen der Buchung');
        }
    } catch (error) {
        console.error('Error creating booking:', error);
        showError('Fehler beim Erstellen der Buchung');
    }
}

/**
 * Load user's favourites for the booking dropdown
 */
async function loadFavourites() {
    const bookingForSelect = document.getElementById('booking-for');
    if (!bookingForSelect) return;
    
    try {
        const currentUserOption = bookingForSelect.querySelector('option');
        const currentUserId = currentUserOption ? currentUserOption.value : null;
        
        if (!currentUserId) return;
        
        const response = await fetch(`/members/${currentUserId}/favourites`);
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.favourites && data.favourites.length > 0) {
                data.favourites.forEach(fav => {
                    const option = document.createElement('option');
                    option.value = fav.id;
                    option.textContent = fav.name;
                    bookingForSelect.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading favourites:', error);
    }
}

/**
 * Handle click on a reserved slot
 */
export async function handleReservationClick(reservationId, bookedFor, time) {
    const confirmed = confirm(`Möchten Sie die Buchung für ${bookedFor} um ${time} Uhr stornieren?`);
    
    if (!confirmed) {
        return;
    }
    
    try {
        const response = await fetch(`/reservations/${reservationId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess('Buchung erfolgreich storniert');
            loadAvailability(currentDate);
            loadUserReservations();
        } else {
            showError(data.error || 'Fehler beim Stornieren der Buchung');
        }
    } catch (error) {
        console.error('Error cancelling reservation:', error);
        showError('Fehler beim Stornieren der Buchung');
    }
}
