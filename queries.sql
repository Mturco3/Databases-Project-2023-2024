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
    R.role,
    R.job_title,
    O.job_description,
    R.responsibilities,
    O.benefits
FROM Offer O, Role R
WHERE O.job_description LIKE '%:user_input%',  -- Replace 'user_input' with the user's input
    AND O.role = R.role;
 
    



