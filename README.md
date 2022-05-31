# Payroll-Reconciliation

Automation tool to perform analysis across 3 data sets:
1. Employer submitted payroll files via automated integration process
2. Funds being placed into participant accounts via processing of payroll files
3. Financial backend of funds received from client, and potential refunds to clients/participants

Queries for data sets are via:
1. Employer Submission.sql
2. Transactional Recordkeeping.sql
3. Financial Backend.sql

This program provides cost saving upwards of $225,000 per annum and reduces the ETA for the analysis process from 2 weeks to 2 days.
The process moving to automation also reduces points of failure with end users, which creates redistributable results without worry of error.
In summary: client relations improved greatly, reduces labor overhead, improves turn around time, and saves hundreds of thousands of dollars yearly.

Distribution with end users is via PyInstaller and providing Zip file to user directly, as this is considered an ad-hoc end-user tool due to being developed by a
non-developer role.

To-do:
- Design summary sheet in workbook to provide dollar amounts across 3 datasets by pairing contract and various system dates.
- Stakeholder meeting pending 06/02 to discuss UI design, brand voice, and functionality.

Wishlist:
- Create ODBC API connection directly to database to allow for querying without running standalone queries.
