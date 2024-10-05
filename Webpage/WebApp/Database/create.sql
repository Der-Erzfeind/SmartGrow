
CREATE TABLE "Box" (
	"boxID"	TEXT,
	"Username"	TEXT,
	"SensorMAC"	TEXT UNIQUE,
	"PotNum"	INTEGER,
	PRIMARY KEY("boxID","SensorMAC"),
	FOREIGN KEY("Username") REFERENCES "Users"("Username")
)

CREATE TABLE "HerbsDb_Plants_Compare_Value" (
	"pid"	TEXT,
	"max_light_mmol"	INTEGER,
	"min_light_mmol"	INTEGER,
	"max_light_lux"	INTEGER,
	"min_light_lux"	INTEGER,
	"max_temp"	REAL,
	"min_temp"	REAL,
	"max_env_humid"	INTEGER,
	"min_env_humid"	INTEGER,
	"max_soil_moist"	INTEGER,
	"min_soil_moist"	INTEGER,
	"max_soil_ec"	INTEGER,
	"min_soil_ec"	INTEGER,
	"max_pH"	REAL,
	"min_pH"	REAL,
	PRIMARY KEY("pid"),
	FOREIGN KEY("pid") REFERENCES "HerbsDb_Plants_Information"
)

CREATE TABLE "HerbsDb_Plants_Information" (
	"pid"	TEXT,
	"origin"	TEXT,
	"blooming"	TEXT,
	"color"	TEXT,
	"size"	TEXT,
	"soil"	TEXT,
	"sunlight"	TEXT,
	"watering"	TEXT,
	"fertilization"	TEXT,
	"pruning"	TEXT,
	PRIMARY KEY("pid")
)

CREATE TABLE "Liquid_Tanks" (
	"boxID"	TEXT,
	"volume_mix"	INTEGER NOT NULL,
	"volume_water"	INTEGER NOT NULL,
	"volume_fertilizer"	INTEGER NOT NULL,
	"volume_acid"	INTEGER NOT NULL,
	"time"	TEXT,
	PRIMARY KEY("time","boxID"),
	FOREIGN KEY("boxID") REFERENCES "Box"("boxID")
)

CREATE TABLE "Measurements" (
	"SensorMAC"	TEXT,
	"light_lux"	INTEGER NOT NULL,
	"temp"	REAL NOT NULL,
	"soil_moist"	INTEGER NOT NULL,
	"soil_ec"	INTEGER NOT NULL,
	"time"	TEXT,
	"battery"	INTEGER,
	"water_pH"	REAL,
	PRIMARY KEY("time","SensorMAC"),
	FOREIGN KEY("SensorMAC") REFERENCES "Box"("SensorMAC")
)

CREATE TABLE "Plants" (
	"Plantname"	TEXT NOT NULL,
	"SensorMAC"	TEXT,
	"Username"	TEXT NOT NULL,
	"pid"	TEXT,
	FOREIGN KEY("SensorMAC") REFERENCES "Box"("SensorMAC"),
	FOREIGN KEY("Username") REFERENCES "Users"("Username"),
	FOREIGN KEY("pid") REFERENCES "HerbsDb_Plants_Information"("pid")
)

CREATE TABLE "Users" (
	"Username"	TEXT NOT NULL,
	"Password"	TEXT NOT NULL,
	PRIMARY KEY("Username")
)

-- // Use DBML to define your database structure
-- // Docs: https://dbml.dbdiagram.io/docs

-- Table "Users" {
--   "Username" TEXT [pk, not null]
--   "Password" TEXT [not null]
-- }

-- Table "Box" {
--   "boxID" TEXT
--   "Username" TEXT
--   "SensorMAC" TEXT [unique]
--   "PotNum" INT

--   Indexes {
--     (boxID, SensorMAC) [pk]
--   }
-- }

-- Table "HerbsDb_Plants_Compare_Value" {
--   "pid" TEXT [pk]
--   "max_light_mmol" INT
--   "min_light_mmol" INT
--   "max_light_lux" INT
--   "min_light_lux" INT
--   "max_temp" REAL
--   "min_temp" REAL
--   "max_env_humid" INT
--   "min_env_humid" INT
--   "max_soil_moist" INT
--   "min_soil_moist" INT
--   "max_soil_ec" INT
--   "min_soil_ec" INT
--   "max_pH" REAL
--   "min_pH" REAL
-- }

-- Table "HerbsDb_Plants_Information" {
--   "pid" TEXT [pk]
--   "origin" TEXT
--   "blooming" TEXT
--   "color" TEXT
--   "size" TEXT
--   "soil" TEXT
--   "sunlight" TEXT
--   "watering" TEXT
--   "fertilization" TEXT
--   "pruning" TEXT
-- }

-- Table "Liquid_Tanks" {
--   "boxID" TEXT
--   "volume_mix" INT [not null]
--   "volume_water" INT [not null]
--   "volume_fertilizer" INT [not null]
--   "volume_acid" INT [not null]
--   "time" TEXT

--   Indexes {
--     (time, boxID) [pk]
--   }
-- }

-- Table "Measurements" {
--   "SensorMAC" TEXT(255)
--   "light_lux" INT [not null]
--   "temp" FLOAT [not null]
--   "soil_moist" INT [not null]
--   "soil_ec" INT [not null]
--   "time" TEXT
--   "battery" INT
--   "water_pH" REAL

--   Indexes {
--     (time, SensorMAC) [pk]
--   }
-- }

-- Table "Plants" {
--   "Plantname" TEXT [not null]
--   "SensorMAC" TEXT
--   "Username" TEXT [not null]
--   "pid" TEXT
-- }

-- Ref:"Users"."Username" < "Box"."Username"

-- Ref:"HerbsDb_Plants_Information"."pid" < "HerbsDb_Plants_Compare_Value"."pid"

-- Ref:"Box"."boxID" < "Liquid_Tanks"."boxID"

-- Ref:"Box"."SensorMAC" < "Measurements"."SensorMAC"

-- Ref:"Box"."SensorMAC" < "Plants"."SensorMAC"

-- Ref:"Users"."Username" < "Plants"."Username"

-- Ref:"HerbsDb_Plants_Information"."pid" < "Plants"."pid"
