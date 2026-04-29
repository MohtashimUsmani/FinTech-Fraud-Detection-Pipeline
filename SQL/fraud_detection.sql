-- 1. Detecting Recursive Fraudulent Transactions
WITH recursive fraud_chain AS (
SELECT nameorig AS initial_account,
namedest AS next_account,
step,
amount,
newbalancedest
FROM transactions
WHERE isfraud = 1 AND TYPE = 'TRANSFER'
UNION ALL
SELECT fc.initial_account,
t.namedest,
t.step,
t.amount,
t.newbalancedest
FROM fraud_chain AS fc
JOIN transactions AS t
on fc.next_account = t.nameorig AND fc.step < t.step
WHERE t.isfraud = 1 AND t.type = 'TRANSFER'
)
SELECT * FROM fraud_chain

--2. Analyzing Fraudulent Activity over Time
WITH rolling_fraud AS (
SELECT nameorig, step,
SUM(isfraud) OVER (
PARTITION BY nameorig 
ORDER BY step 
ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS fraud_rolling
FROM transactions
)
SELECT * FROM rolling_fraud
WHERE fraud_rolling > 0

-- 3. Complex Fraud Detection Using Multiple CTEs
WITH large_transfers AS (
SELECT nameorig, step, amount 
FROM transactions
WHERE type = 'TRANSFER' AND amount > 500000
), no_balance_change AS (
SELECT nameorig, step, oldbalanceOrg, newbalanceOrig  
FROM transactions
WHERE oldbalanceorg = newbalanceorig
), flagged_transctions AS (
SELECT nameorig, step 
FROM transactions
WHERE isflaggedfraud = 1
)
SELECT lt.nameorig
FROM large_transfers AS lt
join no_balance_change AS nbc
ON lt.nameOrig = nbc.nameOrig AND lt.step = nbc.step
join flagged_transctions AS ft
ON lt.nameOrig = ft.nameOrig AND lt.step = ft.step

-- 4. Write me a query that checks if the computed new_updated_Balance is the same as the actual newbalanceDest in the table. If they are equal, it returns those rows.
with CTE as (
SELECT amount,
nameorig,
oldbalancedest,
newbalanceDest,
(amount+oldbalancedest) as new_updated_Balance 
FROM transactions
)
SELECT * 
FROM CTE 
where new_updated_Balance = newbalanceDest;

-- 5. Detect Transactions with Zero Balance Before or After
SELECT *
FROM transactions
WHERE oldbalanceDest = 0 OR newbalanceDest = 0;











