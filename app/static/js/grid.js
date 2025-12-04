/**
 * Grid rendering and availability management
 */

import { generateTimeSlots, showError } from './utils.js';

/**
 * Load court availability for the selected date
 */
export async function loadAvailability(currentDate) {
    console.log('Loading availability for date:', currentDate);
    try {
        const response = await fetch(`/courts/availability?date=${currentDate}`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            console.error('Response not OK:', response.status, response.statusText);
            showError(`Fehler beim Laden: ${response.status}`);
            return;
        }
        
        const data = await response.json();
        console.log('Received data:', data);
        
        if (data.grid) {
            renderGrid(data.grid);
        } else {
            showError(data.error || 'Fehler beim Laden der Verfügbarkeit');
        }
    } catch (error) {
        console.error('Error loading availability:', error);
        showError('Fehler beim Laden der Verfügbarkeit: ' + error.message);
    }
}

/**
 * Render the availability grid
 */
export function renderGrid(grid) {
    const gridBody = document.getElementById('grid-body');
    if (!gridBody) return;
    
    // Get current user ID from the booking dropdown
    const bookingForSelect = document.getElementById('booking-for');
    const currentUserId = bookingForSelect ? parseInt(bookingForSelect.querySelector('option')?.value) : null;
    
    const timeSlots = generateTimeSlots();
    let html = '';
    
    timeSlots.forEach((time, timeIndex) => {
        html += '<tr>';
        html += `<td class="border border-gray-300 px-4 py-2 font-semibold">${time}</td>`;
        
        // For each court
        for (let courtIndex = 0; courtIndex < 6; courtIndex++) {
            const court = grid[courtIndex];
            const slot = court.slots[timeIndex];
            
            let cellClass = 'border border-gray-300 px-2 py-4 text-center cursor-pointer hover:opacity-80';
            let cellContent = '';
            let clickHandler = '';
            
            if (slot.status === 'available') {
                cellClass += ' bg-green-500 text-white';
                cellContent = 'Frei';
                clickHandler = `onclick="window.openBookingModal(${court.court_number}, '${time}')"`;
            } else if (slot.status === 'reserved') {
                cellClass += ' bg-red-500 text-white text-xs';
                cellContent = `Gebucht für ${slot.details.booked_for}<br>von ${slot.details.booked_by}`;
                
                // Check if current user can cancel this reservation
                const canCancel = currentUserId && (
                    slot.details.booked_for_id === currentUserId || 
                    slot.details.booked_by_id === currentUserId
                );
                
                if (canCancel) {
                    clickHandler = `onclick="window.handleReservationClick(${slot.details.reservation_id}, '${slot.details.booked_for}', '${time}')"`;
                }
            } else if (slot.status === 'blocked') {
                cellClass += ' bg-gray-400 text-white';
                cellContent = 'Gesperrt';
                clickHandler = '';
            }
            
            html += `<td class="${cellClass}" ${clickHandler}>${cellContent}</td>`;
        }
        
        html += '</tr>';
    });
    
    gridBody.innerHTML = html;
}
