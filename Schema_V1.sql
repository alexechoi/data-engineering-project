CREATE TABLE "weather_location" (
  "id" int PRIMARY KEY,
  "lat" float,
  "long" float,
  "main_id" int,
  "condition_id" int,
  "dt" datetime
);

CREATE TABLE "weather_main" (
  "id" int PRIMARY KEY,
  "main" varhar,
  "desc" varchar
);

CREATE TABLE "weather_conditions" (
  "id" int PRIMARY KEY,
  "temperature" float,
  "feels_like" float,
  "clouds" int
);

CREATE TABLE "events" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "date" date,
  "time" time
);

CREATE TABLE "venue" (
  "id" int PRIMARY KEY,
  "event_id" int,
  "name" varchar,
  "address" varchar
);

CREATE TABLE "venue_location" (
  "id" int PRIMARY KEY,
  "venue_id" int,
  "lat" float,
  "long" float
);

CREATE TABLE "uber_type" (
  "id" int PRIMARY KEY,
  "ride_type_name" varchar
);

CREATE TABLE "uber_journey" (
  "id" int PRIMARY KEY,
  "start_loc_id" int,
  "end_loc_id" int,
  "type_id" int,
  "time_stamp" datetime,
  "price" float
);

CREATE TABLE "hotel_location" (
  "id" int PRIMARY KEY,
  "hotel_id" int,
  "lat" float,
  "long" float
);

CREATE TABLE "hotel_address" (
  "id" int PRIMARY KEY,
  "fields_later" int
);

ALTER TABLE "events" ADD FOREIGN KEY ("id") REFERENCES "venue" ("event_id");

ALTER TABLE "uber_type" ADD FOREIGN KEY ("id") REFERENCES "uber_journey" ("type_id");

ALTER TABLE "venue_location" ADD FOREIGN KEY ("id") REFERENCES "uber_journey" ("start_loc_id");

ALTER TABLE "venue_location" ADD FOREIGN KEY ("id") REFERENCES "uber_journey" ("end_loc_id");

ALTER TABLE "hotel_location" ADD FOREIGN KEY ("id") REFERENCES "uber_journey" ("start_loc_id");

ALTER TABLE "hotel_location" ADD FOREIGN KEY ("id") REFERENCES "uber_journey" ("end_loc_id");

ALTER TABLE "venue" ADD FOREIGN KEY ("id") REFERENCES "venue_location" ("venue_id");

ALTER TABLE "hotel_address" ADD FOREIGN KEY ("id") REFERENCES "hotel_location" ("hotel_id");

ALTER TABLE "weather_conditions" ADD FOREIGN KEY ("id") REFERENCES "weather_location" ("condition_id");

ALTER TABLE "weather_main" ADD FOREIGN KEY ("id") REFERENCES "weather_location" ("main_id");
