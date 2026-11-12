# Union Steward Suite

Odoo 19 **Community** modules for any union local: members, stewards,
contracts and bargaining units, Weingarten meetings, grievances, direct
actions, and a hardship fund. First built with NUHW for its Santa Rosa
Memorial Hospital contract, then made general: a contract's own terms
(units, shift differentials, grievance procedures and deadlines, steward
notice) are data you set up per contract, or install as a contract pack.

## Modules

- [`union_base/`](union_base/) - **contracts** (employer, dates, bargaining
  units, shift and differential terms), members (via vendored OCA
  `membership`'s own "Members" menu, distinct from core Customers - see
  `VENDORED.md`), bargaining units, shifts, and stewards (a flag, which
  unit(s) they represent, when the employer was told).
- [`union_weingarten/`](union_weingarten/) - investigatory-interview /
  Weingarten-rights meetings: who's being interviewed, which steward(s)
  represent them, and a flag when the steward's release was requested
  later than the contract's required notice. Installable standalone.
- [`union_grievance/`](union_grievance/) - grievances that follow each
  contract's own procedures: ordered steps with deadlines in calendar or
  business days, Next Step to move on, employer-filed grievances, and an
  Odoo activity reminder on the handling steward for every deadline.
  Optionally links back to Weingarten meetings.
- [`union_direct_action/`](union_direct_action/) - lightweight tracking for
  informational pickets, rallies, petitions, button days, and similar
  organizing activity.
- [`union_hardship_fund/`](union_hardship_fund/) - member hardship-fund
  requests with a real, GL-backed running balance.

### Contract packs

- [`union_contract_nuhw_srmh/`](union_contract_nuhw_srmh/) - NUHW and Santa
  Rosa Memorial Hospital: the two units, shift differentials (Article
  12.5), 48-hour steward release notice (7.3), and the three grievance
  procedures of Article 30. Data only; a model for other contracts.

## Testing

See [`testing/`](testing/) for a self-contained local Odoo 19 + Postgres
instance to try these modules against.

## Vendored code

See [`VENDORED.md`](VENDORED.md).
