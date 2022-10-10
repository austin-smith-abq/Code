SELECT DISTINCT
--
-- Case Dates
CrimeCase.OpenDate as OpenDate,
DATEADD(day, TYPE, CrimeCase.OpenDate) as 'TYPE Day',
DATEDIFF(day, CrimeCase.OpenDate, GETDATE()) as 'Time Since Case Opened',
GETDATE() as Timestamp,
--
-- Case Info
CrimeCase.CrimeCase,
CrimeCase.CMSDACase as CMSDACase,
UPPER(CaseStage.CaseStageName) as CaseStage,
--
-- Defendant
UPPER(CONCAT(DefendantAlias.First, ' ', DefendantAlias.Last)) as 'Defendant Full Name',
--
-- Prosecutor
UPPER(CONCAT(ProsecutorAlias.First, ' ', ProsecutorAlias.Last)) as 'Prosecutor Full Name'
--
FROM CrimeCase
--
-- Case Info
LEFT JOIN CaseStage as CaseStage on CrimeCase.CaseStage = CaseStage.CaseStage
--
-- Defendant Info
LEFT JOIN Person as Defendant on CrimeCase.Defendant = Defendant.Person
LEFT JOIN Alias as DefendantAlias on Defendant.Person = DefendantAlias.Person
--
-- Prosecutor Info
LEFT JOIN Person as Prosecutor on CrimeCase.Prosecutor = Prosecutor.Person
LEFT JOIN Alias as ProsecutorAlias on Prosecutor.Person = ProsecutorAlias.Person
--
WHERE CrimeCase.OpenDate >= '2015-01-01'
AND DATEADD(day, TYPE, CrimeCase.OpenDate) < GETDATE()
AND CrimeCase.CMSDACase NOT LIKE '%[A-Z]'
AND CrimeCase.CMSDACase NOT LIKE 'M%'
AND CrimeCase.CMSDACase NOT LIKE 'LR%'
AND CrimeCase.CMSDACase NOT LIKE 'CR%'
AND CrimeCase.CMSDACase NOT LIKE 'T-4-%'
AND CrimeCase.CaseType NOT IN (5,2)
AND CrimeCase.CaseStage NOT IN (5,64)
AND CaseStage.CaseStageCode NOT IN ('CLS','FTA', 'FET', 'OAW', 'OBW', 'PJS','PSN','PIM','PRH')
AND CrimeCase.Prosecutor NOT IN ('4AF53ED5-A3F9-4B6E-9543-2D809A68A293')
-- 60 Day other docket text must be null and detention docket text are null
AND (CrimeCase.OtherDocketText LIKE '%LR%' OR CrimeCase.OtherDocketText LIKE '%PD%')
AND (CrimeCase.DistDocket IS NULL OR CrimeCase.FiledDist IS NULL)
AND CrimeCase.MagDocket IS NOT NULL
AND CrimeCase.MagDocket NOT IN ('T-4-DW%','T-4-DV%')
AND ProsecutorAlias.[primary] = 1
AND DefendantAlias.[primary] = 1
