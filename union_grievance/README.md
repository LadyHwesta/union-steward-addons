# Union Steward Suite - Grievances

A grievance model that follows each contract's own grievance procedures,
not a generic ticket/helpdesk framework.

## Procedures are data, per contract

Union > Configuration > Grievance Procedures (also on each contract): one
procedure per route the contract sets out - e.g. contract interpretation,
discipline and discharge, employer grievances - each an ordered list of
steps. Each step has:

- **Days to Act**, counted from the date of the previous step (0 = the
  contract sets no deadline);
- whether those are **calendar or business days** (business days skip
  weekends);
- a short description of who it goes to.

A procedure is marked as filed by the **union** or the **employer**, and
has notes for anything else, such as what missing a deadline means under
that contract.

A contract pack can install all of this; `union_contract_nuhw_srmh` is the
worked example (Article 30 of the NUHW / Santa Rosa Memorial Hospital
contract).

## A grievance

- picks its **contract** from the grievant's unit, then its **procedure**;
- starts at the procedure's first step;
- **Next Step** moves it on, dated today, with the new deadline filled in;
- `response_deadline_date` fills in from the step's days and the date of
  the current step, and stays editable, since real deadlines key off actual
  meeting dates.

## Missed deadlines

Contracts differ. Often a grievance the union lets lapse is dismissed (set
`outcome` to *Dismissed - Missed Deadline*), while the employer missing its
response moves the grievance on (use **Next Step**). The procedure's notes
say what applies.

## Deadline reminders

Whenever `response_deadline_date` is set (on create or a later write), a
native Odoo activity (`mail.mail_activity_data_todo`) gets scheduled on the
handling steward's user - no custom cron. Closing the grievance (`state =
closed`) removes it. If the steward has no linked `res.users` account yet,
it falls back to whichever user made the change.

## Weingarten meetings

`union_weingarten` stays fully standalone - this module adds the
`grievance_id` field onto `union.weingarten_meeting` itself, so a meeting
can optionally point at the grievance it led to without that module ever
needing to know grievances exist.
