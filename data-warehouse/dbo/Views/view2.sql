CREATE VIEW [dbo].[view2] AS
SELECT
    created_date as 'date',
    MONTH(created_date) as 'month'
FROM 
    fact_facebook;