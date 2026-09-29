# Lab 3 - Component Modelling & Architectural Pattern Selection

**System:** Smart Lab Equipment & Slot Reservation Portal  
**Name:** Himesh Raghav  
**SRN:** PES1UG24CS188

## Architecture selected
Layered Architecture (Presentation, Business, Data)

## Components
1. Student / Technician UI
2. Authentication & Authorization
3. Reservation Manager
4. Equipment & Calibration Manager
5. Return & Late-Return Manager
6. Lab Reservation Database

## Interfaces shown
- IAuthAPI - authentication and role checks
- IReservationAPI - availability, reserve, cancel, reservation state
- IEquipmentAPI - equipment availability and calibration
- IReturnAPI - return and overdue handling
- IRepository - transactional persistence

## Requirements reflected
- Maximum 2-hour reservations and 7-day booking window
- Only calibrated equipment can be reserved
- Double-booking prevention using transactional locking
- Equipment return and late-return identification
- Reservation cancellation before scheduled start
- Authentication and authorization for restricted operations
- Concurrent reservation target of 200 ms

## Note on the Lab 3 handout
The handout's sample coffee-kiosk scenario names generic components such as `Order Manager` and `Payment Service`. Labs 1 and 2 establish a different assigned scenario: the Smart Lab Equipment & Slot Reservation Portal. The Lab 3 component model therefore uses domain-equivalent components for the assigned system rather than introducing an unrelated payment component.
