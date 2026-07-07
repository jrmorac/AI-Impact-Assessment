# SQL Test Data Generation Conversation Summary

## CustomerActivityLogs

Table structure:
- CustomerActivityLogsId
- ActionTimestamp
- ActionName
- Status
- UserName
- CustomerId
- ProjectId

Valid Action values:
- Upload structured data
- Upload unstructured data
- Upload Database Backup
- Upload documents

Valid Status values:
- Success
- Partial Success
- Failure

Fixed values:
- UserName: jcasal@mediquant.com
- CustomerId: 647
- ProjectId: 55

### Final CustomerActivityLogs Script

```sql
SET NOCOUNT ON;

DECLARE @Seed INT = 12345;
DECLARE @MonthOffset INT = 0;
DECLARE @RecordInMonth INT;
DECLARE @StartOfMonth DATE;
DECLARE @DaysInMonth INT;

WHILE @MonthOffset < 6
BEGIN
    SET @StartOfMonth =
        DATEADD(
            MONTH,
            -@MonthOffset,
            DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
        );

    SET @DaysInMonth = DAY(EOMONTH(@StartOfMonth));
    SET @RecordInMonth = 1;

    WHILE @RecordInMonth <= 5
    BEGIN
        DECLARE @Rand INT =
            ABS(CHECKSUM(@Seed, @MonthOffset, @RecordInMonth));

        DECLARE @ActionTimestamp DATETIME2 =
            DATEADD(
                MINUTE,
                8 * 60 + (@Rand % (10 * 60)),
                CAST(
                    DATEADD(
                        DAY,
                        @Rand % @DaysInMonth,
                        @StartOfMonth
                    ) AS DATETIME2
                )
            );

        INSERT INTO dbo.CustomerActivityLogs
        (
            ActionTimestamp,
            ActionName,
            Status,
            UserName,
            CustomerId,
            ProjectId
        )
        VALUES
        (
            @ActionTimestamp,
            CASE @Rand % 4
                WHEN 0 THEN 'Upload structured data'
                WHEN 1 THEN 'Upload unstructured data'
                WHEN 2 THEN 'Upload Database Backup'
                ELSE 'Upload documents'
            END,
            CASE
                WHEN @Rand % 10 < 7 THEN 'Success'
                WHEN @Rand % 10 < 9 THEN 'Partial Success'
                ELSE 'Failure'
            END,
            'jcasal@mediquant.com',
            647,
            55
        );

        SET @RecordInMonth += 1;
    END;

    SET @MonthOffset += 1;
END;
```

---

## CustomerExceptionLogs

Table structure:
- CustomerExceptionLogsId
- ActionTimestamp
- ActionName
- LogMessage
- UserName
- CustomerId
- ProjectId

### Final CustomerExceptionLogs Script

```sql
SET NOCOUNT ON;

DECLARE @Seed INT = 54321;
DECLARE @MonthOffset INT = 0;
DECLARE @RecordInMonth INT;
DECLARE @StartOfMonth DATE;
DECLARE @DaysInMonth INT;

WHILE @MonthOffset < 6
BEGIN
    SET @StartOfMonth =
        DATEADD(
            MONTH,
            -@MonthOffset,
            DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
        );

    SET @DaysInMonth = DAY(EOMONTH(@StartOfMonth));
    SET @RecordInMonth = 1;

    WHILE @RecordInMonth <= 5
    BEGIN
        DECLARE @Rand INT =
            ABS(CHECKSUM(@Seed, @MonthOffset, @RecordInMonth));

        DECLARE @ActionTimestamp DATETIME2 =
            DATEADD(
                MINUTE,
                8 * 60 + (@Rand % (10 * 60)),
                CAST(
                    DATEADD(
                        DAY,
                        @Rand % @DaysInMonth,
                        @StartOfMonth
                    ) AS DATETIME2
                )
            );

        INSERT INTO dbo.CustomerExceptionLogs
        (
            ActionTimestamp,
            ActionName,
            LogMessage,
            UserName,
            CustomerId,
            ProjectId
        )
        VALUES
        (
            @ActionTimestamp,
            CASE @Rand % 4
                WHEN 0 THEN 'Upload structured data'
                WHEN 1 THEN 'Upload unstructured data'
                WHEN 2 THEN 'Upload Database Backup'
                ELSE 'Upload documents'
            END,
            CASE @Rand % 5
                WHEN 0 THEN 'File validation failed: missing required fields.'
                WHEN 1 THEN 'Schema mismatch detected during ingestion.'
                WHEN 2 THEN 'Connection timeout while processing data.'
                WHEN 3 THEN 'Unsupported file format encountered.'
                ELSE 'Unexpected error during data processing.'
            END,
            'jcasal@mediquant.com',
            647,
            55
        );

        SET @RecordInMonth += 1;
    END;

    SET @MonthOffset += 1;
END;
```
