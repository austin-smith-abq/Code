WITH case_list AS (
SELECT DISTINCT
CrimeCase.CrimeCase,
CrimeCase.Arraign as arraign_date, 
CrimeCase.Arrest as arrest_date, 
CrimeCase.ClosedDate as closed_date, 
CrimeCase.Complaint as complaint_date, 
CrimeCase.Custody as custody_date, 
CrimeCase.FiledDist as filed_dist_date, 
CrimeCase.JuviDetained as juvenile_detained_date, 
CrimeCase.OpenDate as open_date, 
DATEDIFF(day, CrimeCase.OpenDate, CrimeCase.FiledDist) as time_to_file,
DATEDIFF(day, CrimeCase.OpenDate, CrimeCase.ClosedDate) as time_to_close,
YEAR(CrimeCase.OpenDate) as calendar_open_year,
YEAR(CrimeCase.ClosedDate) as calendar_closed_year,
FORMAT(CrimeCase.OpenDate,
'MMM') as calendar_open_month,
FORMAT(CrimeCase.ClosedDate,
'MMM') as calendar_closed_month,
CASE
    WHEN
    MONTH(CrimeCase.OpenDate) >= 7 THEN YEAR(CrimeCase.OpenDate) + 1
    ELSE YEAR(CrimeCase.OpenDate)
END as fiscal_open_year,
CASE
    WHEN
    MONTH(CrimeCase.ClosedDate) >= 7 THEN YEAR(CrimeCase.ClosedDate) + 1
    ELSE YEAR(CrimeCase.ClosedDate)
END as fiscal_closed_year,
--
CrimeCase.CustodyLocation as custody_type,
CrimeCase.CustodyLocationText as custody_location, 
CaseClass.ClassName as cms_case_class, 
CaseType.TypeDesc as cms_case_type,
CASE
    WHEN CrimeDivision.CrimeDivisionDesc LIKE '%General Crimes%' THEN 'General Crimes'
    WHEN CrimeDivision.CrimeDivisionDesc LIKE '%Major Crimes%' THEN 'Major Crimes'
ELSE CrimeDivision.CrimeDivisionDesc END AS crime_division,
CaseStage.CaseStageName as cms_case_stage,
CrimeCase.CaseRank as case_rank,
--
CrimeCase.Photos as photo_evidence,
CrimeCase.Video as video_evidence,
CrimeCase.Audio as audio_evidence,
CrimeCase.FORF as forfeiture_evidence,
CrimeCase.DrugAnalysis as drug_tested,
CrimeCase.FingerPalmReport as finger_printed,
CrimeCase.DWIBreath as dwi_breath_tested,
CrimeCase.DWIBlood as dwi_blood_tested,
CrimeCase.DNA as dna_tested,
CrimeCase.OtherReport as other_report_type,
--
CrimeCase.CMSDACase as cms_case_num, 
CrimeCase.DistDocket as dist_docket_num, 
CrimeCase.MagDocket as mag_docket_num,
CrimeCase.StateTRK as case_state_tracking_num,
CrimeCase.OtherDocketText as additional_case_num,
--
Agency.AgencyDesc as referring_agency,
CrimeCase.Citation as referring_agency_case_num,
CrimeCase.Agent as referring_agent_guid, 
UPPER(CONCAT(AgentAlias.First, ' ', AgentAlias.Last)) as referring_agent_name,
--
CrimeCase.Defendant as cms_defendant_guid, 
DefendantAlias.DOB as defendant_dob, 
DefendantAlias.Last as defendant_last_name,
DefendantAlias.First as defendant_first_name,
DefendantAlias.Middle as defendant_middle_name,
UPPER(CONCAT(DefendantAlias.First, ' ', DefendantAlias.Last)) as defendant_name,
DefendantAlias.SSN as defendant_ssn, 
DefendantRace.FullRace as defendant_race, 
DefendantEthnicity.EthnicityDesc as defendant_ethnicity,
CASE
    WHEN Defendant.Male = 0 THEN 'F'
    WHEN Defendant.Male = 1 THEN 'M'
    ELSE 'No data'
END as defendant_gender,
-- 
CrimeCase.Prosecutor as prosecutor_guid, 
UPPER(CONCAT(ProsecutorAlias.First, ' ', ProsecutorAlias.Last)) as prosecutor_name,
-- 
CrimeCase.DefenseAtty as defense_guid, 
UPPER(CONCAT(DefenseAlias.First, ' ', DefenseAlias.Last)) as defense_name,
-- 
CrimeCase.VicAdv as victim_advocate_guid, 
UPPER(CONCAT(VictimAdvocateAlias.First, ' ', VictimAdvocateAlias.Last)) as victim_advocate_name,
-- 
CrimeCase.Investigator as investigator_guid, 
UPPER(CONCAT(InvestigatorAlias.First, ' ', InvestigatorAlias.Last)) as investigator_name,
-- 
CrimeCase.Screener as screener_guid, 
UPPER(CONCAT(ScreenerAlias.First, ' ', ScreenerAlias.Last)) as screener_name,
-- 
CrimeCase.DistJudge as district_judge_guid, 
UPPER(CONCAT(DistrictJudgeAlias.First, ' ', DistrictJudgeAlias.Last)) as dist_judge_name,
-- 
CrimeCase.MagJudge as magistrate_judge_guid, 
UPPER(CONCAT(MagistrateJudgeAlias.First, ' ', MagistrateJudgeAlias.Last)) as mag_judge_name,
--
CASE
    WHEN (CaseStatus.CaseStatusDesc = 'Closed') THEN 'Closed'
    WHEN (CaseStatus.CaseStatusDesc = 'Warrant Outstanding') THEN 'Warrant Outstanding'
    WHEN (CaseStatus.CaseStatusDesc = 'On Appeal') THEN 'On Appeal'
    WHEN (CaseStage.CaseStageName IN ('Forensic Evaluation  Competency Issues',
                                      'Forensic Evaluation - Competency Issues',
                                      'Youth Diagnostic and Development Center Evaluation'
                                     )
        ) THEN 'Competency Evaluation'
    WHEN (CaseStage.CaseStageName IN (
                'Participating in Preprosecution Diversion Program',
                'Participating in Pre-prosecution Diversion Program',
                'Pre-Trial Diversion',
                'PreTrial Diversion',
                'Pending PrePros Acceptance',
                'Pending Pre-Pros Acceptance',
                'Pending Docket Call',
                'Formal Time Waiver Juveniles',
                'Consent Decree without Admission'
            )
        ) THEN 'Diversion Program'
    WHEN (CaseStage.CaseStageName IN (
                'Intake',
                'Intake  further investigation',
                'Intake - further investigation',
                'Pending Further Investigation',
                'Internal or Not Yet Ripe for Prosecution'
            )
        ) THEN 'Intake'
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
                'Pre-trial Conference/Pending Trial',
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
END as case_stage,
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
END AS case_category
--
    FROM CrimeCase
LEFT JOIN CaseClass ON CrimeCase.CaseClass = CaseClass.CaseClass
LEFT JOIN CaseStage ON CrimeCase.CaseStage = CaseStage.CaseStage
LEFT JOIN CaseStatus ON CaseStage.CaseStatus = CaseStatus.CaseStatus
LEFT JOIN CaseType as CaseType ON CrimeCase.CaseType = CaseType.CaseType
LEFT JOIN CrimeDivision as CrimeDivision ON CrimeCase.CrimeDivision = CrimeDivision.CrimeDivision
--
LEFT JOIN Person as Defendant on CrimeCase.Defendant = Defendant.Person
LEFT JOIN Race as DefendantRace on Defendant.Race = DefendantRace.Race
LEFT JOIN Ethnicity as DefendantEthnicity on Defendant.Ethnicity = DefendantEthnicity.Ethnicity
LEFT JOIN Alias as DefendantAlias on Defendant.Person = DefendantAlias.Person
-- 
LEFT JOIN Alias as ProsecutorAlias on CrimeCase.Prosecutor = ProsecutorAlias.Person
-- 
LEFT JOIN Alias as DefenseAlias on CrimeCase.DefenseAtty = DefenseAlias.Person
--
LEFT JOIN Alias as AgentAlias on CrimeCase.Agent = AgentAlias.Person
--
LEFT JOIN Alias as ScreenerAlias on CrimeCase.Screener = ScreenerAlias.Person
--
LEFT JOIN Alias as InvestigatorAlias on CrimeCase.Investigator = InvestigatorAlias.Person
--
LEFT JOIN Alias as VictimAdvocateAlias on CrimeCase.VicAdv = VictimAdvocateAlias.Person
-- 
LEFT JOIN Alias as DistrictJudgeAlias on CrimeCase.DistJudge = DistrictJudgeAlias.Person
-- 
LEFT JOIN Alias as MagistrateJudgeAlias on CrimeCase.MagJudge = MagistrateJudgeAlias.Person
--
LEFT JOIN Agency as Agency on CrimeCase.Agency = Agency.Agency
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
    END AS case_has_felony
FROM case_list
LEFT JOIN Charges on Charges.CrimeCase = case_list.CrimeCase
LEFT JOIN ChargeCode on ChargeCode.ChargeCode = Charges.ChargeCode
),
-- BEGIN Launched Query <<
launched_status AS (
SELECT DISTINCT
felony_misdemeanor.*,
CASE
    WHEN (felony_misdemeanor.dist_docket_num IS NOT NULL
        OR case_has_felony = 'False') 
    THEN 'Launched' ELSE 'Not Launched'
END AS status
FROM felony_misdemeanor
),
--
-- BEGIN Charge Label Query <<
charge_labels AS (
SELECT DISTINCT
launched_status.*,
-- Start charge trajectory;disposition
-- REMEMBER: ORDER MATTERS
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
        ) THEN 'Prosecuted;Guilty Plea'
    WHEN (
       Reason.ReasonText IN ('Referred for Federal Prosecution', 
                             'Referred for Prosecution to Another Agency',
                             'Referred for Prosecution to Another Sovereignty')
    ) THEN 'Referred;Referred Federally or to Another Agency'
    WHEN (
        Reason.ReasonText IN ('Mistrial - Other', 'Mistrial - Hung Jury')
    ) THEN 'Prosecuted;Mistrial'
    WHEN (
        Reason.ReasonText IN ('Pled to Other Counts')
    ) THEN 'Prosecuted;Prosecutor Dismissed'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Juvenile Time Waiver - Satisfactory Completion',
                'Pre-Prosecution Diversion - Satisfactory Completion'
            ) OR
           Reason.ReasonText IN ('Restitution Made', 
                                 'Defendant Complied with Pre-trial Conditions', 
                                 'Completed Diversion Program')
        ) THEN 'Diversion;Successful Diversion'
    WHEN (
           Reason.ReasonText IN ('Handled informally by JPO', 
                                 'Referred to Diversion Program')
        ) THEN 'Diversion;Diversion'
    WHEN (
            ChargeDispo.ChargeDispoDesc = 'Nolle Pros/Dismissed by Prosecutor'
            AND launched_status.status = 'Not Launched'
        ) THEN 'Prosecution Declined;Prosecution Declined'
    WHEN (
        ChargeDispo.ChargeDispoDesc = 'Prosecution Declined'
        ) THEN 'Prosecution Declined;Prosecution Declined'
    WHEN (
            ChargeDispo.ChargeDispoDesc = 'Nolle Pros/Dismissed by Prosecutor'
            AND launched_status.status = 'Launched'
        ) THEN 'Prosecuted;Prosecutor Dismissed'
    WHEN (ChargeDispo.ChargeDispoDesc = 'Court Dismissed'
        ) THEN 'Prosecuted;Court Dismissed'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Pre-Prosecution Diversion - Unsatisfactory Completion',
                'Juvenile Time Waiver - Unsatisfactory Completion'
            )
        ) THEN 'Diversion;Unsuccessful Diversion'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Not Guilty by Jury',
                'Found Not Guilty by Court',
                'Directed Verdict',
                'Ruling Overturned',
                'Default Judgement Entered'
            )
        ) THEN 'Prosecuted;Acquitted'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN (
                'Ruling Affirmed',
                'Guilty at Trial as Charged',
                'Guilty at Trial Before Judge as Charged',
                'Guilty at Jury Trial Lesser Charge',
                'Guilty at Trial Before Judge Lesser Charge',
                'Guilty at Jury Trial Alternate Charge',
                'Guilty at Trial before Judge Alternate Charge',
                'Motion Granted - Resentenced'
            )
        ) THEN 'Prosecuted;Guilty'
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
            ChargeDispo.ChargeDispoDesc IN ('No Bill/No Bind Over') AND (launched_status.case_stage = 'Closed')
        ) THEN 'Prosecuted;No Bill/No Bind Over'
    WHEN (
            ChargeDispo.ChargeDispoDesc IN ('No Bill/No Bind Over') AND (launched_status.case_stage != 'Closed')
        ) THEN 'Prosecuted;Pending'
    WHEN (
        ChargeDispo.ChargeDispoDesc IS NULL AND (launched_status.status = 'Launched' OR  launched_status.case_stage = 'Active: Launched')
        ) THEN 'Prosecuted;Pending'
    WHEN (
        ChargeDispo.ChargeDispoDesc IS NULL AND launched_status.case_stage != 'Intake'
        ) THEN 'Prosecuted;Pending'  
    ELSE 'Pending Decision;Pending'
END AS charge_trajectory_disposition,
--Start charge dismissal/decline reason
CASE
    WHEN (
        Reason.ReasonText IN (        
        'Essential Evidence Suppressed',
        'Essential Witness Excluded',
        'Evidence Suppressed by Court',
        'Judge dismissed because . . .',
        'Defendant Not Transported',
        'Time Limit Expired/LR2-400 Discovery',
        'Time Limit Expired/LR2-400 Track 1',
        'Time Limit Expired/LR2-400 Track 2',
        'Time Limit Expired/LR2-400 Track 3',
        'Time Limits Expired/State Did Not Timely File Extn',
        'Time Limit Expired/Court Denied Timely Filed Extn',
        'Time Limits Expired/Court Did Not Set for Trial'
        )
    ) THEN 'CMO or Procedural Issues'
    WHEN (
        Reason.ReasonText IN (        
        'Convicted in Another Case'
        )
    ) THEN 'Defendant Convicted in Another Case'
    WHEN (
        Reason.ReasonText IN (        
        'Accused Mentally Incompetent',
        'State Will Not Extradite',
        'Defendant Deceased',
        'Defendant Deported',
        'Defendant Terminally ill'
        )
    ) THEN 'Defendant Deceased, Incompetent, or Unavailable'
    WHEN (
        Reason.ReasonText IN (        
        'Insufficient Evidence',
        'Insufficient Evidence - ID of Defendant',
        'Insufficient Proof of Value',
        'Essential Evidence Lost'
        )
    ) THEN 'Insufficient Evidence'
    WHEN (
        Reason.ReasonText IN (        
        'Officer Failed to Appear',
        'Law Enforcement agency uncooperative'        
        )
    ) THEN 'Law Enforcement Failed to Appear or Uncooperative' 
    WHEN (
        Reason.ReasonText IN (        
        'Prosecutor dismissed/declined because . . .',
        'Unlawful Search and Seizure',
        'Lack of Jurisdiction/Venue',
        'Juvenile Under 12 years of age',
        'Double Jeopardy',
        'Juvenile turned 18 years of age.',
        'Speedy Trial Violation',
        'Probation Expired',
        'Immunity to Be Provided'
        )
    ) THEN 'Other Legal Issues' 
    WHEN (
        Reason.ReasonText IN (        
        'Recommended by Probation Officer',
        'Request of Law Enforcement'
        )
    ) THEN 'At Request of Law Enforcement or Probation Officer'
    WHEN (
        Reason.ReasonText IN (        
            'Conduct Not Criminal',
            'Accused Acted in Self-Defense',
            'No Criminal Intent',
            'Mutual Combat'
        )
    ) THEN 'Self-Defense or Not Criminal'
    WHEN (
        Reason.ReasonText IN (        
            'Age of Case',
            'Statute of Limitations Expired'
        )
    ) THEN 'Statute of Limitations or Age of Case'
    WHEN (
        Reason.ReasonText IN (        
            'Victim/Witness Uncooperative',
            'Witness Failed to Appear on Subpoena'
        )
    ) THEN 'Victim or Witness Uncooperative'
    WHEN (
        Reason.ReasonText IN (        
            'Essential Witness Unavailable',
            'Victim Deceased'
        )
    ) THEN 'Victim or Witness Unavailable'
    ELSE 'None'
END as charge_reason,
--Start Murder
CASE
    WHEN(ChargeCode.ChargeCode IN (@MURDER_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END as charge_is_murder,
--
--Start Aggravated_Assault
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@AGGRAVATED_ASSAULT_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END as charge_is_aggravated_assault,
--
--Start Armed_Robbery
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@ARMED_ROBBERY_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END as charge_is_armed_robbery,
--
--Start Rape
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@RAPE_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END AS charge_is_rape,
CASE
    WHEN ((ChargeCode.FelonyMis = 'F') OR (ChargeCode.ChargeCode IN (@FELONY_CHARGE_CODES@))) 
    THEN 'True' ELSE 'False'
END AS charge_is_felony,
CASE
    WHEN(
    ChargeCode.ChargeCode IN (@PRESUMPTION_CHARGE_CODES@))
    THEN 'True' ELSE 'False'
END AS charge_has_rebuttable_presumption,
--
Reason.ReasonText             as charge_cms_reason,
ChargeDispo.ChargeDispoDesc   as charge_cms_disposition,
-- ChargeDispo.EnteredDate   as charge_disposition_date,
ChargeMethod.ChargeMethodText as charge_method,
Charges.ChargeSeq             as charge_sequence, 
UPPER(ChargeCode.Description) as charge_description,
ChargeCode.MasterStatute      as charge_master_statute, 
ChargeCode.ChargeCode         as charge_code,
CASE
    WHEN ChargeCode.[Active] = 1 THEN 'True'
    ELSE 'False'
END                           as charge_code_is_active,         
Degree.DegreeCodeCode         as charge_degree,
UPPER(Charges.Location)       as charge_location,
Charges.StartDate             as charge_start_date,
Charges.EndDate               as charge_end_date,    
Charges.[Primary]             as charge_primary
--
FROM launched_status
--
LEFT JOIN Charges on launched_status.CrimeCase = Charges.CrimeCase
LEFT JOIN ChargeCode on ChargeCode.ChargeCode = Charges.ChargeCode
LEFT JOIN ChargeDispo on Charges.PleaDispo = ChargeDispo.ChargeDispo
LEFT JOIN Reason on Charges.Reason = Reason.Reason
LEFT JOIN ChargeMethod as ChargeMethod on Charges.ChargeMethod = ChargeMethod.ChargeMethod
LEFT JOIN Degree on ChargeCode.Degree = Degree.DegreeCode
WHERE 2 = 2
AND Charges.ChargeSeq != 0
),
charge_level_summary AS (
    SELECT DISTINCT
    charge_labels.*,
    PARSENAME(REPLACE(charge_labels.charge_trajectory_disposition,';','.'),2) as charge_trajectory,
    PARSENAME(REPLACE(charge_labels.charge_trajectory_disposition,';','.'),1) as charge_disposition
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
END as case_is_murder,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_aggravated_assault = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END as case_is_aggravated_assault,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_armed_robbery = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END as case_is_armed_robbery,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_is_rape = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END as case_is_rape,
--
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_has_rebuttable_presumption = 'True' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'True' ELSE 'False'
END as case_has_rebuttable_presumption,
--
--BEGIN CASE TRAJECTORY
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Prosecuted' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Prosecuted'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Referred' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Referred'
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
        charge_level_summary.charge_trajectory = 'Pending Decision' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Pending Decision'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Prosecution Declined' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Prosecution Declined'    
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_trajectory = 'Uncategorized' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Uncategorized' 
    ELSE 'Unknown'
END AS case_trajectory,
--
-- BEGIN CASE DISPOSITION <<
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Guilty' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Guilty'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Guilty Plea' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Guilty Plea' 
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Referred Federally or to Another Agency' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Referred Federally or to Another Agency' 
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Successful Diversion' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Successful Diversion'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Diversion' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Diversion'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Unsuccessful Diversion' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
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
        charge_level_summary.charge_disposition = 'No Bill/No Bind Over' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'No Bill/No Bind Over' 
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
        charge_level_summary.charge_disposition = 'Prosecution Declined' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Prosecution Declined'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_disposition = 'Uncategorized' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Uncategorized' 
    ELSE 'Unknown' 
END AS case_disposition,
-- >> END CASE DISPOSITION   
-- BEGIN CASE REASON <<   
CASE WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Victim or Witness Uncooperative' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Victim or Witness Uncooperative'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Victim or Witness Unavailable' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Victim or Witness Unavailable'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Law Enforcement Failed to Appear or Uncooperative' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Law Enforcement Failed to Appear or Uncooperative'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'CMO or Procedural Issues' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'CMO or Procedural Issues'  
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Statute of Limitations or Age of Case' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Statute of Limitations or Age of Case'
 WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Other Legal Issues' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Other Legal Issues'
  WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Self-Defense or Not Criminal' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Self-Defense or Not Criminal'
  WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'At Request of Law Enforcement or Probation Officer' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'At Request of Law Enforcement or Probation Officer'
  WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Insufficient Evidence' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Insufficient Evidence' 
  WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Defendant Convicted in Another Case' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Defendant Convicted in Another Case'
  WHEN(
    SUM(CASE
        WHEN
        charge_level_summary.charge_reason = 'Defendant Deceased, Incompetent, or Unavailable' THEN 1 ELSE 0 END) OVER (PARTITION BY charge_level_summary.CrimeCase) > 0)
    THEN 'Defendant Deceased, Incompetent, or Unavailable' 
  ELSE 'None'   
END AS case_reason,
-- >> END CASE REASON  
--
CASE
    WHEN (RIGHT(charge_level_summary.cms_case_num, 1) = 'J'
        OR charge_level_summary.crime_division = 'Juvenile Crimes Division'
        OR charge_level_summary.cms_case_type = 'Children''s Court'
        ) THEN 'True'
    ELSE 'False'
END as case_is_juvenile,  
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
'FDV',
'Felony Domestic Violence',
'Misdemeanor Domestic Violence',
'Sex Cases - Adult Victim',
'Sex Cases - Child Victim') THEN 'True' ELSE 'False' END AS case_is_difficult_victim
    
FROM charge_level_summary
)
-- BEGIN Case Level Query  <<
SELECT DISTINCT
*
--
FROM case_level_summary
--
-- END Case Level Query  >>