/**
 * Date utility functions
 * Handles date formatting and calculations
 *
 * IMPORTANT: All date functions use Europe/Berlin timezone to ensure
 * consistency with the backend and correct behavior around midnight.
 */

const BERLIN_TIMEZONE = 'Europe/Berlin';

/**
 * Get current date/time in Berlin timezone as a Date-like object with ISO string
 * @returns {string} ISO date string (YYYY-MM-DD) in Berlin timezone
 */
export function getBerlinDateString() {
    return new Date().toLocaleDateString('sv-SE', { timeZone: BERLIN_TIMEZONE });
}

/**
 * Convert a Date object to ISO date string (YYYY-MM-DD) in Berlin timezone
 * @param {Date} date - Date object
 * @returns {string} ISO date string (YYYY-MM-DD)
 */
export function toBerlinDateString(date) {
    return date.toLocaleDateString('sv-SE', { timeZone: BERLIN_TIMEZONE });
}

/**
 * Format ISO date to German format (DD.MM.YYYY)
 * @param {string} isoDate - ISO date string (YYYY-MM-DD)
 * @returns {string} German formatted date
 */
export function formatDate(isoDate) {
    if (!isoDate) return '';
    
    const [year, month, day] = isoDate.split('-');
    return `${day}.${month}.${year}`;
}

/**
 * Format time string (HH:MM)
 * @param {string} time - Time string
 * @returns {string} Formatted time
 */
export function formatTime(time) {
    if (!time) return '';
    return time;
}

/**
 * Get end time from start time (adds 1 hour)
 * @param {string} startTime - Start time (HH:MM)
 * @returns {string} End time (HH:MM)
 */
export function getEndTime(startTime) {
    if (!startTime) return '';
    
    const [hour, minute] = startTime.split(':').map(Number);
    const endHour = hour + 1;
    return `${endHour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
}

/**
 * Get time range string
 * @param {string} startTime - Start time (HH:MM)
 * @returns {string} Time range (HH:MM - HH:MM)
 */
export function getTimeRange(startTime) {
    if (!startTime) return '';
    return `${startTime} - ${getEndTime(startTime)}`;
}

/**
 * Add days to a date
 * @param {string} isoDate - ISO date string (YYYY-MM-DD)
 * @param {number} days - Number of days to add
 * @returns {string} New ISO date string
 */
export function addDays(isoDate, days) {
    const date = new Date(isoDate + 'T12:00:00'); // Use noon to avoid DST edge cases
    date.setDate(date.getDate() + days);
    return toBerlinDateString(date);
}

/**
 * Get today's date in ISO format (Berlin timezone)
 * @returns {string} Today's date (YYYY-MM-DD)
 */
export function getToday() {
    return getBerlinDateString();
}

/**
 * Check if date is in the past
 * @param {string} isoDate - ISO date string (YYYY-MM-DD)
 * @returns {boolean} True if date is in the past
 */
export function isPast(isoDate) {
    const date = new Date(isoDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date < today;
}

/**
 * Check if date is today
 * @param {string} isoDate - ISO date string (YYYY-MM-DD)
 * @returns {boolean} True if date is today
 */
export function isToday(isoDate) {
    return isoDate === getToday();
}
