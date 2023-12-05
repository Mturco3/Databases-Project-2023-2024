SELECT 
    role, 
    ROUND(AVG(CASE WHEN preference = 'Male' OR preference = 'Both' THEN max_salary END),1) AS male_salary,
    ROUND(AVG(CASE WHEN preference = 'Male' OR preference = 'Both' THEN max_experience_years END),1) AS male_experience,
    ROUND(AVG(CASE WHEN preference = 'Female' OR preference = 'Both' THEN max_salary END),1) AS female_salary,
    ROUND(AVG(CASE WHEN preference = 'Female' OR preference = 'Both' THEN max_experience_years END),1) AS female_experience
FROM Offer
WHERE role = ':user_role' -- Specify a desired role
GROUP BY role;
    
SELECT 
    Offer.job_id,
    Offer.job_posting_date,
    Role.job_title,
    Company.company
FROM 
    Offer
JOIN 
    Location ON Offer.latitude = Location.latitude AND Offer.longitude = Location.longitude
JOIN 
    Role ON Offer.role = Role.role
JOIN 
    Company ON Offer.company = Company.company
WHERE 
    Location.country = ':user_country' -- Specify a desired city
ORDER BY 
    Offer.job_posting_date DESC;

SELECT
    C.company AS company_name,
    O.job_portal,
    COUNT(O.job_portal) AS job_offer_count
FROM Company C
JOIN Offer O ON C.company = O.company
WHERE C.company = ':user_company'  -- Replace 'YourCompany' with the specific company name you're searching for
GROUP BY C.company, O.job_portal;

SELECT
    O.qualifications,
    O.role,
    ROUND(MAX(O.max_salary),1) AS max_salary,
    ROUND(MIN(O.min_salary),1) AS min_salary,
    ROUND(MAX(O.max_experience_years),1) AS max_experience,
    ROUND(MIN(O.min_experience_years),1) AS min_experience
FROM Offer O
WHERE O.qualifications = ':user_input'-- Replace 'YourJob' with the specific job title you're searching for
GROUP BY O.qualifications, O.role;

SELECT O.role, O.job_id, O.company
FROM Offer O
WHERE work_type = ':user_work_type' 
  AND O.company IN (
    SELECT C.company
    FROM Company C
    WHERE C.industry = ':user_industry'  -- Replace 'YourIndustry' with the specific industry you're interested in
);


SELECT job_id, role, company, job_posting_date
FROM Offer
WHERE company IN (
    SELECT company 
    FROM Company 
    WHERE sector = ':user_sector')
AND job_posting_date > '2023-01-01';

    



