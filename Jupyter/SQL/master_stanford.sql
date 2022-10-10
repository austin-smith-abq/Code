WITH case_list AS (
SELECT DISTINCT
CrimeCase.CrimeCase,
CrimeCase.Arraign             AS arraign_date, 
CrimeCase.Arrest              AS arrest_date, 
CrimeCase.ClosedDate          AS closed_date, 
CrimeCase.Complaint           AS complaint_date, 
CrimeCase.Custody             AS custody_date, 
CrimeCase.FiledDist           AS filed_dist_date, 
CrimeCase.JuviDetained        AS juvenile_detained_date, 
CrimeCase.OpenDate            AS open_date, 
DATEDIFF(day, CrimeCase.OpenDate, CrimeCase.FiledDist) AS time_to_file,
DATEDIFF(day, CrimeCase.OpenDate, CrimeCase.ClosedDate) AS time_to_close,
YEAR(CrimeCase.OpenDate)      AS calendar_open_year,
YEAR(CrimeCase.ClosedDate)    AS calendar_closed_year,
FORMAT(CrimeCase.OpenDate,
'MMM')                        AS calendar_open_month,
FORMAT(CrimeCase.ClosedDate,
'MMM')                        AS calendar_closed_month,
CASE
    WHEN
    MONTH(CrimeCase.OpenDate) >= 7 THEN YEAR(CrimeCase.OpenDate) + 1
    ELSE YEAR(CrimeCase.OpenDate)
END                           AS fiscal_open_year,
CASE
    WHEN
    MONTH(CrimeCase.ClosedDate) >= 7 THEN YEAR(CrimeCase.ClosedDate) + 1
    ELSE YEAR(CrimeCase.ClosedDate)
END                           AS fiscal_closed_year,
--
CrimeCase.CustodyLocation     AS custody_type,
CrimeCase.CustodyLocationText AS custody_location, 
CaseClass.ClassName           AS cms_case_class, 
CaseType.TypeDesc             AS cms_case_type,
CASE
    WHEN CrimeDivision.CrimeDivisionDesc LIKE '%General Crimes%' THEN 'General Crimes'
    WHEN CrimeDivision.CrimeDivisionDesc LIKE '%Major Crimes%' THEN 'Major Crimes'
ELSE CrimeDivision.CrimeDivisionDesc END AS crime_division,
CaseStage.CaseStageName       AS cms_case_stage,
CrimeCase.sealCase            AS case_sealed,
CrimeCase.CaseRank            AS case_rank,
--
CrimeCase.Photos              AS photo_evidence,
CrimeCase.Video               AS video_evidence,
CrimeCase.Audio               AS audio_evidence,
CrimeCase.FORF                AS forfeiture_evidence,
CrimeCase.DrugAnalysis        AS drug_tested,
CrimeCase.FingerPalmReport    AS finger_printed,
CrimeCase.DWIBreath           AS dwi_breath_tested,
CrimeCase.DWIBlood            AS dwi_blood_tested,
CrimeCase.DNA                 AS dna_tested,
CrimeCase.OtherReport         AS other_report_type,
--
CrimeCase.CMSDACase           AS cms_case_num, 
CrimeCase.DistDocket          AS dist_docket_num, 
CrimeCase.MagDocket           AS mag_docket_num,
CrimeCase.StateTRK            AS case_state_tracking_num,
CrimeCase.OtherDocketText     AS additional_case_num,
--
Agency.AgencyDesc             AS referring_agency,
CrimeCase.Citation            AS referring_agency_case_num,
CrimeCase.Agent               AS referring_agent_guid, 
UPPER(CONCAT(AgentAlias.First, ' ', AgentAlias.Last)) AS referring_agent_name,
--
CrimeCase.Defendant           AS cms_defendant_guid, 
DefendantAlias.DOB            AS defendant_dob, 
DefendantAlias.Last           AS defendant_last_name,
DefendantAlias.First          AS defendant_first_name,
DefendantAlias.Middle         AS defendant_middle_name,
UPPER(CONCAT(DefendantAlias.First, ' ', DefendantAlias.Last)) AS defendant_name,
DefendantAlias.SSN            AS defendant_ssn, 
ID.StateId                    AS defendant_state_id,
AddressPhone.Zip              AS defendant_last_zip,
DefendantRace.FullRace        AS defendant_race, 
DefendantEthnicity.EthnicityDesc AS defendant_ethnicity,
CASE
    WHEN Defendant.Male = 0 THEN 'F'
    WHEN Defendant.Male = 1 THEN 'M'
    ELSE 'No data'
END                           AS defendant_gender,
-- 
CrimeCase.Prosecutor          AS prosecutor_guid, 
UPPER(CONCAT(ProsecutorAlias.First, ' ', ProsecutorAlias.Last)) AS prosecutor_name,
-- 
CrimeCase.DefenseAtty         AS defense_guid, 
UPPER(CONCAT(DefenseAlias.First, ' ', DefenseAlias.Last)) AS defense_name,
-- 
CrimeCase.VicAdv              AS victim_advocate_guid, 
UPPER(CONCAT(VictimAdvocateAlias.First, ' ', VictimAdvocateAlias.Last)) AS victim_advocate_name,
-- 
CrimeCase.Investigator        AS investigator_guid, 
UPPER(CONCAT(InvestigatorAlias.First, ' ', InvestigatorAlias.Last)) AS investigator_name,
-- 
CrimeCase.Screener            AS screener_guid, 
UPPER(CONCAT(ScreenerAlias.First, ' ', ScreenerAlias.Last)) AS screener_name,
-- 
CrimeCase.DistJudge           AS district_judge_guid, 
UPPER(CONCAT(DistrictJudgeAlias.First, ' ', DistrictJudgeAlias.Last)) AS dist_judge_name,
-- 
CrimeCase.MagJudge            AS magistrate_judge_guid, 
UPPER(CONCAT(MagistrateJudgeAlias.First, ' ', MagistrateJudgeAlias.Last)) AS mag_judge_name,
--
CASE
    WHEN (CaseStatus.CaseStatusDesc = 'Closed') THEN 'Closed'
    WHEN (CaseStatus.CaseStatusDesc = 'Warrant Outstanding') THEN 'Warrant'
    WHEN (CaseStatus.CaseStatusDesc = 'On Appeal') THEN 'On Appeal'
    WHEN (CaseStage.CaseStageName IN ('Forensic Evaluation  Competency Issues')
        ) THEN 'Competency Evaluation'
    WHEN (CaseStage.CaseStageName IN (
                'Participating in Preprosecution Diversion Program',
                'PreTrial Diversion',
                'Pending PrePros Acceptance',
                'Pending Docket Call',
                'Formal Time Waiver Juveniles',
                'Consent Decree without Admission'
            )
        ) THEN 'Diversion Program'
    WHEN (CaseStage.CaseStageName IN (
                'Intake',
                'Intake  further investigation',
                'Pending Further Investigation',
                'Internal or Not Yet Ripe for Prosecution'
            )
        ) THEN 'Active: Intake'
    WHEN (CaseStage.CaseStageName IN (
                'Pending Status Hearing  Post Adjudication',
                'Pending Status Hearing PreAdjudication',
                'Pending Preliminary Hearing',
                'Pending Grand Jury',
                'Pending First Appearance',
                'Pending Detention Hearing'
            )
        ) THEN 'Active: PreLaunch'
    WHEN (CaseStage.CaseStageName IN (
                'Pending Arraignment',
                'Pending Jury Trial',
                'Pending Bench Trial',
                'Pretrial Conference/Pending Trial',
                'Pending Adjudicatory Hearing',
                'Pending Interlocutory Appeal'
            )
        ) THEN 'Active: Launched'
    WHEN (CaseStage.CaseStageName IN (
                'Pending Sentencing',
                'Pending Change of Plea',
                'Pending Judgement and Sentence',
                'Pending Final Disposition',
                'Pending Probation Compliance Review',
                'Pending Motion to Reconsider Sentence'
            )
        ) THEN 'Active: PostDisposition'
    ELSE 'Uncategorized'
END                           AS case_stage,
--
CASE
    WHEN (RIGHT(CrimeCase.CMSDACase, 3) LIKE '%H%'
        OR CaseClass.ClassName = 'Habeas Corpus'
        ) THEN 'Habeas Corpus'
    WHEN (CaseClass.ClassName = 'Civil Mental Commitment') THEN 'Civil Mental Commitment'
    WHEN (CaseClass.ClassName = 'Officer Involved Shootings') THEN 'Officer Involved Shooting'
    WHEN (CaseClass.ClassName = 'Trial De Novo'
        OR CaseStage.CaseStageName = 'Defendant''s Trial De Novo'
        OR CaseStage.CaseStageName = 'State''s Trial De Novo'
         ) THEN 'Trial De Novo'
    WHEN (CaseClass.ClassName = 'Out of State Fugitive') THEN 'Out of State Fugitive'
    WHEN (RIGHT(CrimeCase.CMSDACase,  2) = 'RI'
        OR RIGHT(CrimeCase.CMSDACase, 1) = 'R'
         ) THEN 'Reinitiation'
    WHEN (CaseClass.ClassName = 'Motion After Sentencing'
        OR RIGHT(CrimeCase.CMSDACase, 2) = 'EC'
         ) THEN 'Other'
    WHEN (RIGHT(CrimeCase.CMSDACase, 2) = 'XP'
        OR CaseClass.ClassName = 'Expungement Petitions'
        OR CrimeCase.DistDocket LIKE '%EX%'
         ) THEN 'Expungement'
    WHEN (RIGHT(CrimeCase.CMSDACase, 2) = 'AP'
        OR RIGHT(CrimeCase.CMSDACase, 2) = 'PA'
        OR CaseClass.ClassName = 'Appeal Cases'
        ) THEN 'Appeal'
    WHEN ( CaseClass.ClassName = 'Petition to Revoke Probation'
        OR RIGHT(CrimeCase.CMSDACase, 2) = 'PV'
        OR (RIGHT(CrimeCase.CMSDACase, 1) IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'I')
                AND (RIGHT(CrimeCase.CMSDACase, 2) NOT IN ('WI', 'RI'))
            )
        ) THEN 'Probation Violation'
    ELSE 'Original Crime Case'
END                           AS case_category,
CASE
    WHEN (CrimeCase.WeaponTypeId IS NOT NULL AND CrimeCase.WeaponTypeId NOT IN (5, 6))
    THEN 'Yes'
    ELSE NULL
END                           as weapon_used_flag,
WeaponType.WeaponTypeDesc     as weapon_type,
PPD.ReferredDate              as diversion_referral_date,
PPD.ApplyDate                 as diversion_apply_date,
PPD.AcceptDate                as diversion_accept_date,
PPD.RejectDate                as diversion_reject_date,
PPD.TermBeginDate             as diversion_begin_date,
PPD.TermEndDate               as diversion_end_date,
PPD.CompletedDate             as diversion_completed_date,
CASE 
    WHEN PPD.ApplyDate < CrimeCase.OpenDate THEN 'True'
    WHEN PPD.ApplyDate > CrimeCase.OpenDate THEN 'False'
    ELSE NULL
END                           as pretrial_diversion_flag,
CASE
    WHEN PPD.AcceptDate IS NOT NULL THEN 'Yes'
    ELSE NULL
END                           as diversion_acceptance_flag,
CASE
    WHEN PPD.CompletedDate = PPD.TermEndDate THEN 'Yes'
    ELSE NULL
END                           as diversion_completion_flag,
CrimeCaseWarrant.IssuedDate   as warrant_issue_date
--
    FROM CrimeCase
LEFT JOIN CaseClass ON CrimeCase.CaseClass = CaseClass.CaseClass
LEFT JOIN CaseStage ON CrimeCase.CaseStage = CaseStage.CaseStage
LEFT JOIN CaseStatus ON CaseStage.CaseStatus = CaseStatus.CaseStatus
LEFT JOIN CaseType AS CaseType ON CrimeCase.CaseType = CaseType.CaseType
LEFT JOIN CrimeDivision AS CrimeDivision ON CrimeCase.CrimeDivision = CrimeDivision.CrimeDivision
--
LEFT JOIN Defendant as ID on CrimeCase.Defendant = ID.Person
LEFT JOIN Person AS Defendant ON CrimeCase.Defendant = Defendant.Person
LEFT JOIN Race AS DefendantRace ON Defendant.Race = DefendantRace.Race
LEFT JOIN Ethnicity AS DefendantEthnicity ON Defendant.Ethnicity = DefendantEthnicity.Ethnicity
LEFT JOIN Alias AS DefendantAlias ON Defendant.Person = DefendantAlias.Person
-- 
LEFT JOIN Alias AS ProsecutorAlias ON CrimeCase.Prosecutor = ProsecutorAlias.Person
-- 
LEFT JOIN Alias AS DefenseAlias ON CrimeCase.DefenseAtty = DefenseAlias.Person
--
LEFT JOIN Alias AS AgentAlias ON CrimeCase.Agent = AgentAlias.Person
--
LEFT JOIN Alias AS ScreenerAlias ON CrimeCase.Screener = ScreenerAlias.Person
--
LEFT JOIN Alias AS InvestigatorAlias ON CrimeCase.Investigator = InvestigatorAlias.Person
--
LEFT JOIN Alias AS VictimAdvocateAlias ON CrimeCase.VicAdv = VictimAdvocateAlias.Person
-- 
LEFT JOIN Alias AS DistrictJudgeAlias ON CrimeCase.DistJudge = DistrictJudgeAlias.Person
-- 
LEFT JOIN Alias AS MagistrateJudgeAlias ON CrimeCase.MagJudge = MagistrateJudgeAlias.Person
--
LEFT JOIN Agency AS Agency ON CrimeCase.Agency = Agency.Agency
LEFT JOIN PPD ON CrimeCase.CrimeCase = PPD.CrimeCase
LEFT JOIN WeaponType ON CrimeCase.WeaponTypeId = WeaponType.WeaponTypeId
LEFT JOIN CrimeCaseWarrant ON CrimeCase.CrimeCase = CrimeCaseWarrant.CrimeCase AND CrimeCaseWarrant.WarrantSeq = 1
LEFT JOIN AddressPhone ON Defendant.Person = AddressPhone.Person AND AddressPhone.AddressSeq = 1 
    
WHERE 1 = 1 
AND    (DefendantAlias.[Primary] IS NULL OR DefendantAlias.[Primary] = 1)
AND    (ProsecutorAlias.[Primary] IS NULL OR ProsecutorAlias.[Primary] = 1)
AND    (DefenseAlias.[Primary] IS NULL OR DefenseAlias.[Primary] = 1)
AND    (AgentAlias.[Primary] IS NULL OR AgentAlias.[Primary] = 1)
AND    (ScreenerAlias.[Primary] IS NULL OR ScreenerAlias.[Primary] = 1)
AND    (InvestigatorAlias.[Primary] IS NULL OR InvestigatorAlias.[Primary] = 1)
AND    (VictimAdvocateAlias.[Primary] IS NULL OR VictimAdvocateAlias.[Primary] = 1)
AND    (MagistrateJudgeAlias.[Primary] IS NULL OR MagistrateJudgeAlias.[Primary] = 1)
AND    (DistrictJudgeAlias.[Primary] IS NULL OR DistrictJudgeAlias.[Primary] = 1)
AND    CrimeCase.CaseType != 5
),
-- BEGIN Felony/Mis Query <<
felony_misdemeanor AS (
SELECT DISTINCT
case_list.*,
CASE
    WHEN(SUM(CASE WHEN (ChargeCode.FelonyMis = 'F' OR ChargeCode.ChargeCode IN (@FELONY_CHARGE_CODES@)) THEN 1 ELSE 0 END) OVER (PARTITION BY case_list.CrimeCase) > 0) 
    THEN 'True' ELSE 'False'
    END                       AS case_has_felony
FROM case_list
LEFT JOIN Charges ON Charges.CrimeCase = case_list.CrimeCase
LEFT JOIN ChargeCode ON ChargeCode.ChargeCode = Charges.ChargeCode
),
-- BEGIN Launched Query <<
launched_status AS (
SELECT DISTINCT
felony_misdemeanor.*,
CASE
    WHEN (felony_misdemeanor.dist_docket_num IS NOT NULL
        OR case_has_felony = 'False') 
    THEN 'Launched' ELSE 'Not Launched'
END                           AS status
FROM felony_misdemeanor
),
--
-- BEGIN Charge Label Query <<
charge_labels AS (
SELECT DISTINCT
launched_status.*,
-- Moved Guilty to top, was between dismissal and diversion  
CASE
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Guilty Plea',
                'Dismissed per Plea Agreement',
                'Pled Guilty to Lesser Charge',
                'No Contest',
                'No Contest Lesser Charge',
                'Alford Plea',
                'Alford Plea to a Lesser Charge',
                'Pled Guilty but Mentally Ill',
                'Without Admission',
                'Guilty Plea Alternate Charge',
                'No Contest Alternate Charge'
            )
        ) THEN 'Plea;Guilty'
    WHEN (
            ChargeDispo.ChargeDispoDesc = 'Prosecution Declined'
        ) THEN 'Declination;Prosecution Declined'
    WHEN (
        Reason.ReasonText IN ('Mistrial - Other', 'Mistrial - Hung Jury')
    ) THEN 'Trial;Mistrial'
    WHEN (
            ChargeDispo.ChargeDispoDesc = 'Nolle Pros/Dismissed by Prosecutor'
            AND launched_status.status = 'Not Launched'
        ) THEN 'Declination;Nolle Pros'
    WHEN (
            ChargeDispo.ChargeDispoDesc = 'Nolle Pros/Dismissed by Prosecutor'
            AND launched_status.status = 'Launched'
        ) THEN 'Dismissal;Prosecutor Dismissed'
    WHEN (ChargeDispo.ChargeDispoDesc = 'Court Dismissed') THEN 'Dismissal;Court Dismissed'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Juvenile Time Waiver - Satisfactory Completion',
                'Pre-Prosecution Diversion - Satisfactory Completion'
            )
        ) THEN 'Diversion;Successful'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Pre-Prosecution Diversion - Unsatisfactory Completion',
                'Juvenile Time Waiver - Unsatisfactory Completion'
            )
        ) THEN 'Diversion;Unsuccessful'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Not Guilty by Jury',
                'Found Not Guilty by Court',
                'Directed Verdict',
                'Ruling Overturned',
                'Default Judgement Entered'
            )
        ) THEN 'Trial;Acquitted'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Ruling Affirmed',
                'Guilty at Trial AS Charged',
                'Guilty at Trial Before Judge AS Charged',
                'Guilty at Jury Trial Lesser Charge',
                'Guilty at Trial Before Judge Lesser Charge',
                'Guilty at Jury Trial Alternate Charge',
                'Guilty at Trial before Judge Alternate Charge',
                'Motion Granted - Resentenced'
            )
        ) THEN 'Trial;Guilty'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Not Committed',
                'Treatment Guardian Appointed',
                'Treatment Guardian Not Appointed',
                'Involuntary Mental Commitment',
                'Voluntary Commitment'
            )
        ) THEN 'Mental Commitment;Mental Commitment'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Writ Withdrawn',
                'Writ of Habeus Corpus - Relief Granted',
                'Writ of Habeas Corpus - Relief Denied'
            )
        ) THEN 'Habeas Corpus;Habeas Corpus'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Accused Competent',
                'Motion Granted - No Resentencing',
                'Withdrawn Appeal'
            )
        ) THEN 'Uncategorized;Uncategorized'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Extradition Ordered by Court',
                'Extradition Waived'
            )
        ) THEN 'Out of State Fugitive;Out of State Fugitive'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN ('No Bill/No Bind Over')
        ) THEN 'Failed Launch;Failed Launch'
    ELSE 'Pending;Pending'
    -- Updated to Pending ON 8/23/22 per Adolfo Mendez
    --ELSE 'None;None'
END                           AS charge_trajectory_disposition,
--
CASE
    WHEN(ChargeCode.ChargeCode IN (@MURDER_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END                           AS charge_is_murder,
--
--Start Aggravated_Assault
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@AGGRAVATED_ASSAULT_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END                           AS charge_is_aggravated_assault,
    --
--Start Armed_Robbery
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@ARMED_ROBBERY_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END                           AS charge_is_armed_robbery,
    --
--Start Rape
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@RAPE_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END                           AS charge_is_rape,
CASE
    WHEN ((ChargeCode.FelonyMis = 'F') OR (ChargeCode.ChargeCode IN (@FELONY_CHARGE_CODES@))) 
    THEN 'True' ELSE 'False'
END                           AS charge_is_felony,
--
CASE
    WHEN Charges.DomesticViolence = 1 THEN 'True'
    WHEN Charges.DomesticViolence = 0 THEN 'False'
    ELSE NULL
END                           AS charge_is_domestic_violence,
Reason.ReasonText             AS charge_reason,
ChargeDispo.ChargeDispoDesc   AS charge_cms_disposition,
ChargeMethod.ChargeMethodText AS charge_method,
Charges.ChargeSeq             AS charge_sequence, 
UPPER(ChargeCode.Description) AS charge_description,
ChargeCode.MasterStatute      AS charge_master_statute, 
ChargeCode.ChargeCode         AS charge_code,
CASE
    WHEN ChargeCode.[Active] = 1 THEN 'True'
    ELSE 'False'
END                           AS charge_code_is_active,         
Degree.DegreeCodeCode         AS charge_degree,
--Degree.DegreeDesc             AS charge_degree_description
UPPER(Charges.Location)       AS charge_location,
Charges.StartDate             AS charge_start_date,
Charges.EndDate               AS charge_end_date,    
Charges.[Primary]             AS charge_primary,
Enhancements.EnhancementName   AS charge_enhancement,
DrugTypes.DrugTypeDesc        AS drug_type,
PleaOffer.ChargeDispoDesc     AS plea_offered,
Charges.PleaDate              AS plea_date,
Charges.SentenceDate          AS sentence_date,
Charges.SentenceDays          AS sentence_days,
SentenceSeverity.SentenceSeverityDesc AS sentence_severity,
CASE 
    WHEN SentenceSeverity.ProbationViolation = 1 THEN 'True' 
    WHEN SentenceSeverity.ProbationViolation = 0 THEN 'False' 
    ELSE NULL
END                           AS charge_is_probation_violation,
CASE
    WHEN Charges.Concurrent = 1 THEN 'True'
    WHEN Charges.Concurrent = 0 THEN 'False'
    ELSE NULL
END                           AS sentence_is_concurrent,
CASE
    WHEN Charges.Consecutive = 1 THEN 'True'
    WHEN Charges.Consecutive = 0 THEN 'False'
    ELSE NULL
END                           AS sentence_is_consecutive,
CASE
    WHEN Charges.Death = 1 THEN 'True'
    WHEN Charges.Death = 0 THEN 'False'
    ELSE NULL
END                           AS sentence_is_death,
CONCAT(Charges.SentenceYears, ' years, ', 
       Charges.SentenceMonths, ' months, and ', 
       Charges.SentenceDays, 'days') AS sentence_length,
CONCAT(Charges.SuspendedYears, ' years, ', 
       Charges.SuspendedMonths, ' months, and ', 
       Charges.SuspendedDays, ' days') AS suspended_length,
CONCAT(Charges.ProbationYears, ' years, ', 
       Charges.ProbationMonths, ' months, and ', 
       Charges.ProbationDays, ' days') AS probation_length,
Charges.Fine as fines,
Charges.FineSuspended as fines_suspended,
Charges.Restitution as restitution,
CONCAT(VictimAlias.First, ' ', VictimAlias.Last) AS victim_name,
VictimPerson.Race             AS victim_race,
VictimPerson.Ethnicity        AS victim_ethnicity,
CASE
    WHEN VictimPerson.Male = 1 THEN 'Male' 
    WHEN VictimPerson.Male = 0 THEN 'Female'
    ELSE NULL
END                           AS victim_gender,
VictimAlias.DOB               AS victim_dob,
RelationshipType.RelationshipDesc AS victim_relationship

--
FROM launched_status
--
LEFT JOIN Charges ON launched_status.CrimeCase = Charges.CrimeCase
LEFT JOIN ChargeCode ON ChargeCode.ChargeCode = Charges.ChargeCode
LEFT JOIN ChargeDispo ON Charges.PleaDispo = ChargeDispo.ChargeDispo
LEFT JOIN Reason ON Charges.Reason = Reason.Reason
LEFT JOIN ChargeMethod AS ChargeMethod ON Charges.ChargeMethod = ChargeMethod.ChargeMethod
LEFT JOIN Degree ON ChargeCode.Degree = Degree.DegreeCode
LEFT JOIN SentenceType ON Charges.SentenceType = SentenceType.SentenceType
LEFT JOIN SentenceSeverity ON Charges.SentenceSeverity = SentenceSeverity.SentenceSeverity
LEFT JOIN Victim ON Charges.CrimeCase = Victim.Crimecase and Charges.ChargeSeq = Victim.ChargeNum
LEFT JOIN Alias AS VictimAlias ON Victim.Victim = VictimAlias.Person
LEFT JOIN Person AS VictimPerson ON Victim.Victim = VictimPerson.Person
LEFT JOIN RelationshipType ON Victim.RelationshipTypeCode = RelationshipType.RelationshipTypeCode
LEFT JOIN ChargeDispo AS PleaOffer ON Charges.PleaOffered = PleaOffer.ChargeDispo
LEFT JOIN DrugTypes ON Charges.DrugType = DrugTypes.DrugType
LEFT JOIN ChargeEnhancements on Charges.CrimeCase = ChargeEnhancements.CrimeCase AND Charges.ChargeSeq = ChargeEnhancements.ChargeSeq
LEFT JOIN Enhancements on ChargeEnhancements.Enhancement = Enhancements.Enhancement
WHERE 2 = 2
AND Charges.ChargeSeq != 0
AND (VictimAlias.[Primary] IS NULL OR VictimAlias.[Primary] = 1)
),
charge_level_summary AS (
    SELECT DISTINCT
    charge_labels.*,
    PARSENAME(REPLACE(charge_labels.charge_trajectory_disposition,';','.'),2) AS charge_trajectory,
    PARSENAME(REPLACE(charge_labels.charge_trajectory_disposition,';','.'),1) AS charge_disposition
    FROM charge_labels
    ),
case_level_summary AS (
SELECT DISTINCT
charge_level_summary.*,
    CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_murder = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END                           AS case_is_murder,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_aggravated_assault = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END                           AS case_is_aggravated_assault,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_armed_robbery = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END                           AS case_is_armed_robbery,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_rape = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END                           AS case_is_rape,
--
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Trial' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Trial'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Plea' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Plea'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Diversion' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Diversion'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Mental Commitment' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Mental Commitment'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Out of State Fugitive' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Out of State Fugitive'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Habeas Corpus' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Habeas Corpus'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Pending' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Pending'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Failed Launch' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Failed Launch'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Dismissal' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Dismissal'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Declination' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Declination'    
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Uncategorized' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Uncategorized' 
    ELSE 'Unknown'
END                           AS case_trajectory,
--
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Guilty' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Guilty'    
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Successful' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Successful Diversion'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Unsuccessful' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Unsuccessful Diversion'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Mental Commitment' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Mental Commitment'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Out of State Fugitive' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Out of State Fugitive'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Habeas Corpus' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Habeas Corpus'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Mistrial' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Mistrial'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Acquitted' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Acquitted'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Pending' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Pending' 
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Court Dismissed' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Court Dismissed'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Prosecutor Dismissed' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Prosecutor Dismissed'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Nolle Pros' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Nolle Pros'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Prosecution Declined' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Prosecution Declined'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Uncategorized' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Uncategorized' 
    ELSE 'Unknown' 
END                           AS case_disposition,
--
CASE
    WHEN (RIGHT(charge_level_summary.cms_case_num, 1) = 'J'
        OR charge_level_summary.crime_division = 'Juvenile Crimes Division'
        OR charge_level_summary.cms_case_type = 'Children''s Court'
        ) THEN 'True'
    ELSE 'False'
END                           AS case_is_juvenile,  
CASE WHEN charge_level_summary.cms_case_class IN ('Child Abuse Cases',
'Crime Against Children',
'Crimes Against Persons',
'Criminal Sexual Contact',
'CSP/CSC of a Minor',
'Domestic Violence',
'Domestic Violence  Felony',
'Domestic Violence (felony)',
'Domestic Violence - Felony',
'Domestic Violence - Misdemeanor',
'Domestic Violence Misdemeanor',
'Domestic Violence(misdemeanor)',
'FDV',
'Felony Domestic Violence',
'Homicide',
'Misdemeanor Domestic Violence',
'Peace Officer Crimes',
'Sex Cases - Adult Victim',
'Sex Cases - Child Victim',
'Vehicular Homicide',
'Vehicular Homicide Cases') THEN 'True' ELSE 'False' END AS case_is_violent,
CASE WHEN charge_level_summary.cms_case_class IN ('Child Abuse Cases',
                                                  'Crime Against Children',
                                                  'Criminal Sexual Contact',
                                                  'CSP/CSC of a Minor',
                                                  'Domestic Violence',
                                                  'Domestic Violence  Felony',
                                                  'Domestic Violence (felony)',
                                                  'Domestic Violence - Felony',
                                                  'Domestic Violence - Misdemeanor',
                                                  'Domestic Violence Misdemeanor',
                                                  'Domestic Violence(misdemeanor)',
                                                  'FDV','Felony Domestic Violence',
                                                  'Misdemeanor Domestic Violence',
                                                  'Sex Cases - Adult Victim',
                                                  'Sex Cases - Child Victim') 
    THEN 'True' ELSE 'False' END AS case_is_difficult_victim,
CASE WHEN charge_level_summary.cms_case_class IN ('Child Abuse Cases',
                                                  'Crime Against Children',
                                                  'Sex Cases - Child Victim',
                                                  'CSP/CSC of a Minor')
    THEN 'True' ELSE 'False' END AS case_is_minor_victim
FROM charge_level_summary
)
-- BEGIN Case Level Query  <<
SELECT DISTINCT
*
--
FROM case_level_summary
--
-- END Case Level Query  >>