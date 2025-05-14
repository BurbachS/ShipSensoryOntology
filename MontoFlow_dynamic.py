import duckdb
import os
import pandas as pd



# Path to your Excel file
excel_file = "Property_Matrix/Ontop_Property_Matrix.xlsx"

# Load all sheets into a dictionary
sheets = pd.read_excel(excel_file, sheet_name=None)

# Ensure the output directory exists
output_dir = "data/Ship01/owl"
os.makedirs(output_dir, exist_ok=True)

# Loop through each sheet and export to CSV
for sheet_name, df in sheets.items():
    csv_path = os.path.join(output_dir, f"{sheet_name}.csv")
    df.to_csv(csv_path, index=False, sep=';')
    print(f"Sheet '{sheet_name}' exported to '{csv_path}'")


# Connect to (or create) the DuckDB database
con = duckdb.connect("DuckDB/ontop.duckdb")



# Create subclasses view 
con.execute("""
CREATE OR REPLACE VIEW subclasses AS
SELECT
  "Class"                       AS Class,
  "rdfs:subClassOf"             AS rdfs__subClassOf
FROM read_csv_auto(
  'data/Ship01/owl/Subclass.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("\n✅ subclasses view created.")


# Create observations view with the new timestamp column
con.execute("""
CREATE OR REPLACE VIEW observations AS
SELECT
    split_part(REPLACE(FILENAME, '\\', '/'), '/', -4) AS year,   
    split_part(REPLACE(FILENAME, '\\', '/'), '/', -3) AS month,   
    split_part(REPLACE(FILENAME, '\\', '/'), '/', -2) AS day,     
    REPLACE(split_part(REPLACE(FILENAME, '\\', '/'), '/', -1), '.csv', '') AS sensor, 
    time,    -- Timestamp column from the CSV
    value,   -- Value column from the CSV
    -- Create the timestamp by concatenating year, month, day, and time
    CAST(
        CONCAT(
            split_part(REPLACE(FILENAME, '\\', '/'), '/', -4), '-',   -- Year
            split_part(REPLACE(FILENAME, '\\', '/'), '/', -3), '-',   -- Month
            split_part(REPLACE(FILENAME, '\\', '/'), '/', -2), ' ',   -- Day
            -- time 
            substring(CAST(time AS VARCHAR), 1, 8)                              
        ) AS TIMESTAMP
    ) AS timestamp -- The new combined timestamp column
FROM
    read_csv_auto('data/Ship01/raw/*/*/*/*.csv', AUTO_DETECT=true, FILENAME=true);
""")

print("\n✅ observations view created.")



# Create aggregated_observations view 
con.execute("""
CREATE OR REPLACE VIEW aggregated_observations AS
SELECT
  "Individual"                  AS Individual,
  "rdf:type"                    AS rdf__type,
  "sosa:hasFeatureOfInterest"   AS sosa__hasFeatureOfInterest,
  "sosa:madeBySensor"           AS sosa__madeBySensor,
  "sosa:observedProperty"       AS sosa__observedProperty,
  "qudt:numericValue"           AS qudt__numericValue,
  "qudt:hasUnit"                AS qudt__hasUnit
FROM read_csv_auto(
  'data/Ship01/owl/AggregatedObservation.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ aggregated_observations view created.")


print(df.columns)



# Create anomaly_observations view 
con.execute("""
CREATE OR REPLACE VIEW anomaly_observations AS
SELECT   
  -- normalize backslashes-slashes, then take the folder two levels up
  split_part(
    split_part(replace(filename, '\\', '/'), '/', -2),
    '/', 1
  ) AS anomaly_name,
  -- normalize + take the basename, strip off ".csv"
  regexp_replace(
    split_part(replace(filename, '\\', '/'), '/', -1),
    '\\.csv$', ''
  ) AS sensor,
  timestamp,
  value,
FROM read_csv_auto(
  'data/Ship01/anomaly/*/*.csv',
  DELIM=',',
  HEADER=TRUE,
  AUTO_DETECT=TRUE,
  FILENAME=TRUE
);
""")
print("✅ anomaly_observations view created.")



# Create general_sensors view 
con.execute("""
CREATE OR REPLACE VIEW general_sensors AS
SELECT
  "Individual"               AS Individual,
  "rdf:type"                 AS rdf__type,
  "ship:hasSensorProperty"   AS ship__hasSensorProperty,
  "ssn:detects"              AS ssn__detects,
  "sosa:isHostedBy"          AS sosa__isHostedBy,
  "sosa:madeObservation"     AS sosa__madeObservation,
  "sosa:observes"            AS sosa__observes
FROM read_csv_auto(
  'data/Ship01/owl/GeneralSensor.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ general_sensors view created.")

# Create engine_sensors view 
con.execute("""
CREATE OR REPLACE VIEW engine_sensors AS
SELECT
  "Individual"               AS Individual,
  "rdf:type"                 AS rdf__type,
  "ship:hasSensorProperty"   AS ship__hasSensorProperty,
  "ssn:detects"              AS ssn__detects,
  "sosa:isHostedBy"          AS sosa__isHostedBy,
  "sosa:madeObservation"     AS sosa__madeObservation,
  "sosa:observes"            AS sosa__observes
FROM read_csv_auto(
  'data/Ship01/owl/EngineSensor.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ engine_sensors view created.")


# Create devices view 
con.execute("""
CREATE OR REPLACE VIEW devices AS
SELECT
  "Individual"            AS Individual,
  "rdf:type"              AS rdf__type,
  "sosa:hosts"            AS sosa__hosts,
  "geo:location"          AS geo__location,
FROM read_csv_auto(
  'data/Ship01/owl/Device.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ devices view created.")

# Create engine_comp view 
con.execute("""
CREATE OR REPLACE VIEW engine_comp AS
SELECT
  "Individual"            AS Individual,
  "rdf:type"              AS rdf__type,
  "sosa:hosts"            AS sosa__hosts,
  "geo:location"          AS geo__location,
FROM read_csv_auto(
  'data/Ship01/owl/EngineComp.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ engine_comp view created.")

# Create strustures view 
con.execute("""
CREATE OR REPLACE VIEW structures AS
SELECT
  "Individual"            AS Individual,
  "rdf:type"              AS rdf__type,
  "sosa:hosts"            AS sosa__hosts,
  "geo:location"          AS geo__location,
FROM read_csv_auto(
  'data/Ship01/owl/Structure.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ structures view created.")


# Create alarm_threshold view 
con.execute("""
CREATE OR REPLACE VIEW alarm_threshold AS
SELECT
  "Individual"            AS Individual,
  "rdf:type"              AS rdf__type,
  "qudt:hasUnit"          AS qudt__hasUnit,
  "qudt:lowerBound"       AS qudt__lowerBound,
  "qudt:upperBound"       AS qudt__upperBound,          
FROM read_csv_auto(
  'data/Ship01/owl/AlarmThresholdRange.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ alarm_threshold view created.")


# Create norm_range view 
con.execute("""
CREATE OR REPLACE VIEW norm_range AS
SELECT
  "Individual"            AS Individual,
  "rdf:type"              AS rdf__type,
  "qudt:hasUnit"          AS qudt__hasUnit,
  "qudt:lowerBound"       AS qudt__lowerBound,
  "qudt:upperBound"       AS qudt__upperBound,          
FROM read_csv_auto(
  'data/Ship01/owl/NormValueRange.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ norm_range view created.")


# Create systems view 
con.execute("""
CREATE OR REPLACE VIEW systems AS
SELECT
  raw."Individual"               AS Individual,
  raw."rdf:type"                 AS rdf__type,
  TRIM(s.x)                      AS ssn__hasSubSystem,
  raw."ssn:hasSystemCapability"  AS ssn__hasSystemCapability,         
FROM read_csv_auto(
  'data/Ship01/owl/System.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
) AS raw
CROSS JOIN UNNEST( STRING_SPLIT(raw."ssn:hasSubSystem", ',') ) AS s(x)
WHERE raw."ssn:hasSubSystem" IS NOT NULL
  AND TRIM(s.x) <> '';

""")

print("✅ systems view created.")


# Create sys_capability view 
con.execute("""
CREATE OR REPLACE VIEW sys_capability AS
SELECT
  raw."Individual"               AS Individual,
  raw."rdf:type"                 AS rdf__type,
  TRIM(s.x)                      AS ssn__hasSystemProperty,        
FROM read_csv_auto(
  'data/Ship01/owl/SystemCapability.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
) AS raw
CROSS JOIN UNNEST( STRING_SPLIT(raw."ssn:hasSystemProperty", ',') ) AS s(x)
WHERE raw."ssn:hasSystemProperty" IS NOT NULL
  AND TRIM(s.x) <> '';
            
""")

print("✅ sys_capability view created.")


# Create frequency view 
con.execute("""
CREATE OR REPLACE VIEW frequency AS
SELECT
  "Individual"               AS Individual,
  "rdf:type"                 AS rdf__type,
  "qudt:numericValue"        AS qudt__numericValue,
  "qudt:hasUnit"             AS qudt__hasUnit,       
FROM read_csv_auto(
  'data/Ship01/owl/Frequency.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ frequency view created.")


# Create measurement_range view 
con.execute("""
CREATE OR REPLACE VIEW measurement_range AS
SELECT
  "Individual"            AS Individual,
  "rdf:type"              AS rdf__type,
  "qudt:hasUnit"          AS qudt__hasUnit,
  "qudt:lowerBound"       AS qudt__lowerBound,
  "qudt:upperBound"       AS qudt__upperBound,          
FROM read_csv_auto(
  'data/Ship01/owl/MeasurementRange.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ measurement_range view created.")


# Create stimulus view 
con.execute("""
CREATE OR REPLACE VIEW stimulus AS
SELECT
  "Individual"               AS Individual,
  "rdf:type"                 AS rdf__type,
  "ssn:isProxyFor"           AS ssn__isProxyFor,  
FROM read_csv_auto(
  'data/Ship01/owl/Stimulus.csv',
  DELIM=';',
  HEADER=TRUE,
  AUTO_DETECT=TRUE
)

""")

print("✅ stimulus view created.")



####################################################################################

print("\nTest sample for subclasses view:")
for row in con.execute("SELECT * FROM subclasses LIMIT 10").fetchall():
    print(row)

print("\nTest sample for observations view:")
for row in con.execute("SELECT * FROM observations LIMIT 10").fetchall():
    print(row)

print("\nTest sample for aggregated_observations view:")
for row in con.execute("SELECT * FROM aggregated_observations LIMIT 10").fetchall():
    print(row)

print("\nTest sample for anomaly_observations view:")
for row in con.execute("SELECT * FROM anomaly_observations LIMIT 10").fetchall():
    print(row)

print("\nTest sample for general_sensors view:")
for row in con.execute("SELECT * FROM general_sensors LIMIT 10").fetchall():
    print(row)

print("\nTest sample for engine_sensors view:")
for row in con.execute("SELECT * FROM engine_sensors LIMIT 10").fetchall():
    print(row)

print("\nTest sample for devices view:")
for row in con.execute("SELECT * FROM devices LIMIT 10").fetchall():
    print(row)

print("\nTest sample for engine_comp view:")
for row in con.execute("SELECT * FROM engine_comp LIMIT 10").fetchall():
    print(row)

print("\nTest sample for structures view:")
for row in con.execute("SELECT * FROM structures LIMIT 10").fetchall():
    print(row)

print("\nTest sample for alarm_threshold view:")
for row in con.execute("SELECT * FROM alarm_threshold LIMIT 10").fetchall():
    print(row)

print("\nTest sample for norm_range view:")
for row in con.execute("SELECT * FROM norm_range LIMIT 10").fetchall():
    print(row)

print("\nTest sample for systems view:")
for row in con.execute("SELECT * FROM systems LIMIT 10").fetchall():
    print(row)

print("\nTest sample for sys_capability view:")
for row in con.execute("SELECT * FROM sys_capability LIMIT 10").fetchall():
    print(row)

print("\nTest sample for frequency view:")
for row in con.execute("SELECT * FROM frequency LIMIT 10").fetchall():
    print(row)

print("\nTest sample for measurement_range view:")
for row in con.execute("SELECT * FROM measurement_range LIMIT 10").fetchall():
    print(row)

print("\nTest sample for stimulus view:")
for row in con.execute("SELECT * FROM stimulus LIMIT 10").fetchall():
    print(row)
