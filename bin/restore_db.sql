DECLARE @FILELISTONLY nvarchar(100),
	@QRESTORE nvarchar(300),
	@DBName nvarchar(100)
SET @DBName = '$(newDB)'
CREATE TABLE #tFILELISTONLY(
	LogicalName nvarchar(128), 
	PhysicalName nvarchar(260), 
	Type char(1), 
	FileGroupName nvarchar(128), 
	[Size] numeric(20,0), 
	[MaxSize] numeric(20,0),
	FileID bigint,
	CreateLSN numeric(25,0),
	DropLSN numeric(25,0),
	UniqueID uniqueidentifier,
	ReadOnlyLSN numeric(25,0),
	ReadWriteLSN numeric(25,0),
	BackupSizeInBytes bigint,
	SourceBlockSize int,
	FileGroupID int,
	LogGroupGUID uniqueidentifier,
	DifferentialBaseLSN numeric(25,0),
	DifferentialBaseGUID uniqueidentifier,
	IsReadOnly bit,
	IsPresent bit,
	TDEThumbprint varbinary(32),
	SnapshotURL nvarchar(360)
)
SET @FILELISTONLY = N'RESTORE FILELISTONLY from DISK = N''$(dfile)'''
INSERT #tFILELISTONLY EXEC(@FILELISTONLY)
SELECT @QRESTORE = 'RESTORE DATABASE [' + @DBName + ']
FROM DISK = ''$(dfile)'' 
WITH 
	MOVE ''' + t1.LogicalName + ''' TO ''D:\MSSQL\' + @DBName + '.mdf'',
	MOVE ''' + t2.LogicalName + ''' TO ''E:\LOGS\' + @DBName + '.ldf'',
	RECOVERY, REPLACE, STATS = 10;
'
FROM #tFILELISTONLY t1
	JOIN #tFILELISTONLY t2
		ON t2.Type = 'L'
WHERE t1.Type = 'D'
EXECUTE(@QRESTORE)
DROP TABLE #tFILELISTONLY
GO