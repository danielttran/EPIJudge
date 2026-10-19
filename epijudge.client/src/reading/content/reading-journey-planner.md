Turn an ambiguous travel request into an explicit search contract.

## Core idea

Model locations as vertices and feasible transitions as edges. Define the optimization objective: cheapest cost, earliest arrival, fewest transfers, or a weighted combination. Timetables may require a search state containing both location and time. A result should explain which constraints it satisfies.

## Try the boundaries

A missed connection; an overnight trip; a closed route; incompatible accessibility requirements; stale availability.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

A single cheapest-distance label is insufficient if arrival time affects future choices. Keep multiple non-dominated labels when cost and time matter together. Cache static topology separately from rapidly changing prices and availability, and revalidate before an irreversible booking.

## Your design exercise

Specify inputs, objective, freshness requirements, and one adversarial itinerary.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
