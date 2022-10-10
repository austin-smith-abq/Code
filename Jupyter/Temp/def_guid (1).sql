SELECT DISTINCT
CrimeCase.CMSDACase as def_cms_case_num,
CrimeCase.Defendant as def_defendant_guid,
CrimeCase.ClosedDate as def_closed_date
FROM CrimeCase
LEFT JOIN Person on Person.Person = CrimeCase.Defendant
WHERE 1 = 1
AND CaseType != 5
AND Person.Active = 1