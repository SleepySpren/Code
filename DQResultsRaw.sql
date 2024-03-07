
CREATE TABLE [dbo].[DQResultsRaw](
	[first_name] [varchar](50) NULL,
	[interests] [varchar](200) NULL,
	[username_accounts] [varchar](50) NULL,
	[username_log] [varchar](50) NULL,
	[email] [varchar](50) NULL,
	[last_name] [varchar](50) NULL,
	[city] [varchar](50) NULL,
	[country] [varchar](50) NULL,
	[gender] [varchar](50) NULL,
	[password] [varchar](50) NULL,
	[birth_date2] [varchar](50) NULL,
	[card_number]  [varchar](50) NULL,
	[job_title] [varchar](50) NULL,
	[ip_address] [varchar](250) NULL,
	[birth_date]  [varchar](50) NULL,
	[subscription]  [varchar](50) NULL,
	[account_creation_date]  [varchar](50) NULL,
	[card_type] [varchar](50) NULL,
	[phone_number] [varchar](50) NULL,
	[profile_picture_URL] [varchar](250) NULL,
	[date] [datetime] NULL,
	[login_time]  [varchar](50) NULL,
	[logout_time]  [varchar](50) NULL,
    isFirstNameNoSpecialChar bit, -- Example column for Rule 1
    isPasswordValid bit,
	isFirstNameSameCase bit,
	isValidUsername bit,
	isNameNotNull bit,
	isEmailNotNull bit,
	isUserSingular bit,
	isGenderCorrect bit,
    isPasswordNotNull bit,
    isUserConsistent bit,
    isBirthdateValid bit,
  	isSubscriptionValid bit,
  	isDateCorrect bit,
  	isLoginTimeCorrect bit,
  	isLogoutTimeCorrect bit,
  	isCountryValid bit)


INSERT INTO DQResultsRaw (
      [first_name]
      ,[interests]
      ,[username_accounts]
      ,[username_log]
      ,[email]
      ,[last_name]
      ,[city]
      ,[country]
      ,[gender]
      ,[password]
      ,[birth_date2]
      ,[card_number]
      ,[job_title]
      ,[ip_address]
      ,[birth_date]
      ,[subscription]
      ,[account_creation_date]
      ,[card_type]
      ,[phone_number]
      ,[profile_picture_URL]
      ,[date]
      ,[login_time]
      ,[logout_time]
      ,[isFirstNameNoSpecialChar]
      ,[isPasswordValid]
      ,[isFirstNameSameCase]
      ,[isValidUsername]
      ,[isNameNotNull]
      ,[isEmailNotNull]
      ,[isUserSingular]
      ,[isGenderCorrect]
      ,[isPasswordNotNull]
      ,[isUserConsistent]
      ,[isBirthdateValid]
      ,[isSubscriptionValid]
      ,[isDateCorrect]
      ,[isLoginTimeCorrect]
      ,[isLogoutTimeCorrect]
      ,[isCountryValid])
SELECT
      [first_name]
      ,[interests]
      ,ar.[username]
      , ulr.username
      ,[email]
      ,[last_name]
      ,[city]
      ,[country]
      ,[gender]
      ,[password]
      ,[birth_date2]
      ,[card_number]
      ,[job_title]
      ,[ip_address]
      ,[birth_date]
      ,[subscription]
      ,[account_creation_date]
      ,[card_type]
      ,[phone_number]
      ,[profile_picture_URL]
      , ulr.date
      , login_time
      , logout_time
      -- CASE STATEMENT
      -- Rule 1
       , CASE
            WHEN first_name NOT LIKE '%[^a-zA-Z0-9]%' THEN 1
            ELSE 0
         END AS 'isFirstNameNoSpecialChar'
         --rule 2
        , CASE
        WHEN LEN(password) >= 8
        AND password LIKE '%[A-Z]%'
        AND password LIKE '%[a-z]%'
        AND password LIKE '%[0-9]%' THEN 1
        ELSE 0
    END AS 'isPasswordValid'
        --rule 3
        , CASE
        WHEN LEFT(first_name, 1) = UPPER(LEFT(first_name, 1)) Collate SQL_Latin1_General_CP1_CS_AS
        AND SUBSTRING(first_name, 2, LEN(first_name)) = LOWER(SUBSTRING(first_name, 2, LEN(first_name))) Collate SQL_Latin1_General_CP1_CS_AS THEN 1
        ELSE 0
      END AS isFirstNameSameCase
        --rule 4
        , CASE
        WHEN SUBSTRING(Email, 1, CHARINDEX('@', Email)-1)  = AR.username THEN 1
        ELSE 0
         END AS isValidUsername            
        -- rule 5
        , CASE
        WHEN first_name IS NOT NULL
        AND last_name IS NOT NULL THEN 1
        ELSE 0
    END AS isNameNotNull
        -- 6
        , CASE
        WHEN email IS NULL OR email = '' THEN 0
        ELSE 1
         END AS isEmailNotNull
        --7
        , CASE
        WHEN COUNT(*) OVER (PARTITION BY ar.username) > 1 THEN 0
        ELSE 1
    END AS isUserSingular
        -- 8
        , CASE
        WHEN gender IN ('Male', 'Female', 'Non-Binary', 'Gender-fluid','Prefer not to say') THEN 1
        ELSE 0
    END AS isGenderCorrect
        -- 9
        , CASE
            WHEN password IS NULL OR password = '' THEN 0
            ELSE 1
        END AS isPasswordNotNull
        --10 weird behaviur only one matching username?
        , CASE
            WHEN ulr.record = ar.record and  ulr.username IN (SELECT ar.username FROM [accountsCleaned]) THEN 1
            ELSE 0
        END AS isUserConsistent
        --11
         , CASE
            WHEN TRY_CONVERT(DATE, birth_date, 23) IS NOT NULL THEN 1
            ELSE 0
        END  AS IsBirthdateValid
        --12
        ,CASE
            WHEN subscription = '1' OR subscription = '0'  THEN 1
            ELSE 0
        END AS IsSubscriptionValid
         --13
        , CASE
            WHEN ISDATE(date) = 1 THEN 1
            ELSE 0
        END AS 'isDateCorrect'
        --14
        ,     CASE
                WHEN TRY_CONVERT(time, [login_time]) IS NOT NULL THEN 1
                ELSE 0
            END AS 'isLoginTimeCorrect'
        ,CASE
            WHEN TRY_CONVERT(time, [logout_time]) IS NOT NULL THEN 1
            ELSE 0
        END AS 'isLoginTimeCorrect'
        -- 15
        , CASE
            WHEN COUNTRY IS NULL THEN 0
            ELSE 1
        END AS 'isCountryValid'
  FROM [DM_E2E_Project_Team2].[dbo].[accountsRaw] as AR
  JOIN [dbo].[userLogsRaw] as ULR
  ON ar.record = ulr.record
