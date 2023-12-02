SELECT 
    role, 
    ROUND(AVG(CASE WHEN preference = 'Male' OR preference = 'Both' THEN max_salary END),1) AS male_salary,
    ROUND(AVG(CASE WHEN preference = 'Male' OR preference = 'Both' THEN max_experience_years END),1) AS male_experience,
    ROUND(AVG(CASE WHEN preference = 'Female' OR preference = 'Both' THEN max_salary END),1) AS female_salary,
    ROUND(AVG(CASE WHEN preference = 'Female' OR preference = 'Both' THEN max_experience_years END),1) AS female_experience
FROM Offer
WHERE role = ':user_role'
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
