# Union Steward Suite - Weingarten Meetings

Tracks investigatory interviews where an employee has invoked their right to
union representation. Installable standalone - a Weingarten meeting doesn't
require a grievance to exist, and most won't ever become one. Once
`union_grievance` is installed, a meeting can optionally be linked to a
grievance it led to (the link field lives in that module, so this one stays
usable alone).

## Fields worth knowing

- **Steward Release Notice (hours)** on the contract: how far ahead a
  steward must ask to be released for a meeting (often the same notice the
  employer owes for an investigatory interview). 0 means no rule.
- `release_requested_late` - computed, stored. True when the gap between
  `request_date` and `scheduled_date` is shorter than the employee's
  contract requires. Shown as a warning banner on the form and a red row in
  the list.
- `management_rep` is a plain Char, not a partner - management reps aren't
  union members and have no reason to be in this database.
- `notes` is a dedicated Text field in addition to the chatter log, for a
  longer write-up of what was actually said/decided.

## Security

Everything here is gated to `union_base`'s `group_union_steward` - this
data can touch discipline investigations, so no other internal user (let
alone a portal user) gets any access by default.
