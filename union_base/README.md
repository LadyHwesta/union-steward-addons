# Union Steward Suite - Base

Members, stewards, contracts, bargaining units, and shift on top of
`res.partner`. Everything else in this suite depends on this module.
Nothing here is specific to one union: a contract pack (such as
`union_contract_nuhw_srmh`) adds a real contract's details as data.

## Contracts

`union.contract` - one per collective bargaining agreement (Union >
Configuration > Contracts): the employer, effective and expiry dates, its
bargaining units, and its shift and differential terms. Other modules add
to it: `union_grievance` its grievance procedures, `union_weingarten` the
steward release notice.

## Members

Depends on OCA's `membership` module (vendored - see this repo's own
`VENDORED.md`) for its "Members" menu, a real action distinct from core
Customers rather than a rename of it (same pattern as this ecosystem's
amateur radio club suite).

**Union dues usually come by payroll check-off, never invoiced through
Odoo** - so `membership`'s own invoice-driven renewal workflow doesn't
apply. Use the **Mark Dues Current** button on a member's form instead: it
creates (or refreshes) one year of a `paid` membership line directly, with
no invoice attached. `membership_state` still reflects it correctly
(`paid`) since `membership`'s own compute preserves an explicitly-set state
when there's no invoice to derive it from.

## Bargaining units

`union.unit` - each belongs to a contract (Union > Configuration >
Bargaining Units, or on the contract). A member's unit shows their
contract on their form.

## Shift

A plain `day`/`evening`/`night` field on every partner; when the member's
contract has shift and differential terms, they show right below it.

## Stewards

A boolean flag, which unit(s) they're designated to represent
(`steward_unit_ids`), and when the employer was told in writing
(`steward_designated_date`) - most contracts require that notice. A
dedicated **Stewards** menu (gated to the `group_union_steward` group)
lists just these partners.

## Security

One group, `group_union_steward`: full read/write on contracts, units and
(once the other modules in this suite are installed) every grievance/
Weingarten/hardship-fund model. Every other internal user gets read-only
access to contracts and units and none at all to the sensitive models -
grant `group_union_steward` only to actual stewards.
